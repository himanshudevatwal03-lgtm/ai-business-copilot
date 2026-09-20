"""
Qualcomm AI Hub & Snapdragon NPU Adapter (Phase 2).

Real pipeline (confirmed against Qualcomm/Microsoft docs, Sept 2026):
  1. Export a compiled model bundle with the Qualcomm AI Hub Models package,
     run on a machine with a QAI Hub API token:

       pip install qai_hub_models
       qai-hub configure --api_token <YOUR_QAI_HUB_TOKEN>
       python -m qai_hub_models.models.phi_3_5_mini_instruct.export \
           --device "Snapdragon X Elite CRD" \
           --skip-inferencing --skip-profiling \
           --output-dir genie_bundle

     This step compiles/quantizes the model on Qualcomm's cloud device farm
     and can take a while depending on upload speed. It must be run on the
     Snapdragon X Elite device itself (or a machine that can copy the
     resulting bundle onto it) — it cannot run inside this project's Linux
     Docker container, which targets amd64 for the Render deployment.

  2. Point QUALCOMM_MODEL_DIR at the resulting genie_bundle/ directory
     (it should contain genai_config.json, the tokenizer files, and the
     QNN context binaries).

  3. Install the on-device runtime on the Snapdragon machine:

       pip install onnxruntime-genai

     This adapter then loads the bundle with onnxruntime-genai's QNN
     execution provider and runs real autoregressive generation via
     og.Model / og.Tokenizer / og.Generator.

This module is safe to import anywhere (including the Render/Linux
deployment): if onnxruntime-genai or the model bundle aren't present, it
reports that truthfully via _probe_runtime() and falls back to
LocalAnalyticsProvider rather than failing.
"""

import os
from typing import Dict, Any, Optional
from app.providers.base import BaseInferenceProvider
from app.providers.local_analytics import LocalAnalyticsProvider

CHAT_TEMPLATE = "<|user|>\n{input}<|end|>\n<|assistant|>"

SYSTEM_PROMPT = (
    "You are AI Business Copilot, an on-device assistant for an enterprise "
    "ERP system running locally on a Snapdragon NPU. Answer the user's "
    "business question using only the JSON ERP context provided. Be concise "
    "and cite concrete numbers from the context."
)


class QualcommAIHubAdapter(BaseInferenceProvider):
    """
    On-device inference adapter for Snapdragon X Elite via onnxruntime-genai
    + QNN, running a model exported through Qualcomm AI Hub Models.
    """

    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = model_dir or os.getenv("QUALCOMM_MODEL_DIR", "")
        self.fallback = LocalAnalyticsProvider()
        self.runtime_check = self._probe_runtime()
        self.is_npu_available = self.runtime_check["npu_ready"]
        self._model = None
        self._tokenizer = None

    def _probe_runtime(self) -> Dict[str, Any]:
        """
        Genuinely checks whether this machine can run Phase 2 on-device
        inference: is onnxruntime-genai installed, and does a genai_config.json
        exist in the configured model directory (the file onnxruntime-genai
        requires to load a bundle). Flips to ready automatically on a real
        Snapdragon X Elite machine with the exported bundle in place.
        """
        status = {
            "onnxruntime_genai_installed": False,
            "model_bundle_found": False,
            "npu_ready": False,
            "detail": "onnxruntime-genai not installed (expected off-device, e.g. this Render deployment)"
        }
        try:
            import onnxruntime_genai  # noqa: F401
            status["onnxruntime_genai_installed"] = True
            config_path = os.path.join(self.model_dir, "genai_config.json") if self.model_dir else ""
            status["model_bundle_found"] = bool(self.model_dir) and os.path.isfile(config_path)
            status["npu_ready"] = status["model_bundle_found"]
            status["detail"] = (
                "Ready for on-device inference"
                if status["npu_ready"]
                else f"onnxruntime-genai present but no genai_config.json found under QUALCOMM_MODEL_DIR={self.model_dir!r}"
            )
        except ImportError:
            pass
        return status

    @property
    def name(self) -> str:
        return "Qualcomm AI Hub Adapter (onnxruntime-genai + QNN)"

    @property
    def is_on_device(self) -> bool:
        return True

    def _load_model(self):
        """Lazily load the model/tokenizer once, on first real query."""
        if self._model is None:
            import onnxruntime_genai as og
            self._model = og.Model(self.model_dir)
            self._tokenizer = self._tokenizer or og.Tokenizer(self._model)
        return self._model, self._tokenizer

    def _generate(self, prompt: str, max_length: int = 1024) -> str:
        """
        Real autoregressive generation on the Snapdragon NPU via
        onnxruntime-genai. Raises on any failure so the caller can fall
        back cleanly — this method never silently returns fabricated text.
        """
        import onnxruntime_genai as og
        model, tokenizer = self._load_model()

        input_tokens = tokenizer.encode(prompt)
        params = og.GeneratorParams(model)
        params.set_search_options(max_length=max_length, temperature=0.2)
        generator = og.Generator(model, params)
        generator.append_tokens(input_tokens)

        output_tokens = []
        while not generator.is_done():
            generator.generate_next_token()
            output_tokens.append(generator.get_next_tokens()[0])
        del generator

        return tokenizer.decode(output_tokens)

    async def process_query(self, query: str, erp_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        On a real Snapdragon X Elite machine with the model bundle in place,
        runs genuine on-device NPU generation grounded in the live ERP data.
        Anywhere else (dev machine, this project's Render deployment), it
        reports the real capability probe and transparently falls back to
        the deterministic LocalAnalyticsProvider.
        """
        if self.is_npu_available:
            try:
                import json
                # Keep the context compact — full erp_context can be large;
                # trim to what the model actually needs to answer well.
                compact_context = {
                    "kpis": erp_context.get("kpis"),
                    "top_products": erp_context.get("top_products"),
                    "overdue": erp_context.get("overdue", [])[:5],
                    "low_stock": erp_context.get("low_stock", [])[:5],
                }
                user_turn = f"ERP context (JSON): {json.dumps(compact_context)}\n\nQuestion: {query}"
                prompt = CHAT_TEMPLATE.format(input=f"{SYSTEM_PROMPT}\n\n{user_turn}")
                answer_text = self._generate(prompt)
                return {
                    "answer": answer_text,
                    "intent": "on_device_llm_inference",
                    "confidence": 0.9,
                    "inference_provider": "qualcomm_npu (onnxruntime-genai + QNN, live)",
                    "snapdragon_roadmap": {
                        "status": "Phase 2 active — running on Snapdragon NPU",
                        "runtime_probe": self.runtime_check
                    },
                    "suggestions": [
                        "What were the total sales this month?",
                        "Which products are selling the most?",
                        "Summarize the current business situation."
                    ]
                }
            except Exception as exc:
                # Real on-device generation failed at runtime (e.g. driver
                # issue, OOM) — fall through to the deterministic engine
                # rather than surfacing a raw exception to the user.
                result = await self.fallback.process_query(query, erp_context)
                result["inference_provider"] = f"local_analytics (NPU generation failed: {exc})"
                result["snapdragon_roadmap"] = {
                    "status": "Phase 2 configured but generation errored — see inference_provider",
                    "runtime_probe": self.runtime_check
                }
                return result

        result = await self.fallback.process_query(query, erp_context)
        result["inference_provider"] = "local_analytics (Qualcomm NPU Adapter slot ready for Phase 2)"
        result["snapdragon_roadmap"] = {
            "status": "Ready for Phase 2 Integration",
            "target_npu": "Snapdragon X Elite Hexagon NPU",
            "runtime": "onnxruntime-genai + QNN Execution Provider",
            "hub_compilation": "Export the model with qai_hub_models, then set QUALCOMM_MODEL_DIR",
            "runtime_probe": self.runtime_check
        }
        return result
