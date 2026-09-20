import os
from typing import Dict, Any
from app.providers.base import BaseInferenceProvider
from app.providers.local_analytics import LocalAnalyticsProvider
from app.config import settings

class CloudLLMProvider(BaseInferenceProvider):
    """
    Optional Cloud LLM Provider (e.g. OpenAI / Gemini).
    Falls back gracefully to LocalAnalyticsProvider if no API key is provided
    or if cloud connectivity is unavailable.
    """

    def __init__(self):
        self.fallback = LocalAnalyticsProvider()
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")

    @property
    def name(self) -> str:
        return "Cloud LLM Provider (OpenAI/Gemini)"

    @property
    def is_on_device(self) -> bool:
        return False

    async def process_query(self, query: str, erp_context: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            # Automatic fallback to deterministic local analytics
            result = await self.fallback.process_query(query, erp_context)
            result["inference_provider"] = "local (fallback: no cloud api key set)"
            return result

        try:
            import httpx
            # Call standard OpenAI-compatible completions
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            system_prompt = (
                "You are AI Business Copilot for an enterprise ERP system. "
                "Analyze the provided JSON ERP context and answer user business questions accurately and concisely."
            )
            payload = {
                "model": settings.OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"ERP Context:\n{erp_context}\n\nUser Question: {query}"}
                ],
                "temperature": 0.2
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    answer_text = data["choices"][0]["message"]["content"]
                    return {
                        "answer": answer_text,
                        "intent": "cloud_llm_inference",
                        "confidence": 0.95,
                        "inference_provider": "cloud_llm",
                        "suggestions": [
                            "What were the total sales this month?",
                            "Which products are selling the most?",
                            "Which customers have overdue payments?"
                        ]
                    }
        except Exception:
            pass

        # Fallback if request fails
        result = await self.fallback.process_query(query, erp_context)
        result["inference_provider"] = "local (fallback: cloud request unavailable)"
        return result
