from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseInferenceProvider(ABC):
    """
    Abstract Base Class for Copilot Inference Providers.
    Designed to allow pluggable backends:
      1. LocalAnalyticsProvider (zero-key deterministic NLP & metrics)
      2. CloudLLMProvider (OpenAI / Gemini / Anthropic)
      3. QualcommAIHubAdapter (Phase 2 on-device Snapdragon NPU execution)
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name identifier."""
        pass

    @property
    @abstractmethod
    def is_on_device(self) -> bool:
        """Whether inference executes on-device."""
        pass

    @abstractmethod
    async def process_query(self, query: str, erp_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a natural language business query given ERP context.
        Returns dictionary conforming to QueryResponse schema.
        """
        pass
