from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.services.erp_service import ERPService
from app.providers.base import BaseInferenceProvider
from app.providers.local_analytics import LocalAnalyticsProvider
from app.providers.cloud_llm import CloudLLMProvider
from app.providers.qualcomm_adapter import QualcommAIHubAdapter
from app.config import settings

class CopilotService:
    def __init__(self):
        self.provider = self._resolve_provider(settings.INFERENCE_PROVIDER)

    def _resolve_provider(self, provider_type: str) -> BaseInferenceProvider:
        p = provider_type.lower()
        if p == "cloud":
            return CloudLLMProvider()
        elif p == "qualcomm":
            return QualcommAIHubAdapter()
        else:
            return LocalAnalyticsProvider()

    def set_provider(self, provider_type: str):
        self.provider = self._resolve_provider(provider_type)

    def get_provider_info(self) -> Dict[str, Any]:
        return {
            "current_provider": self.provider.name,
            "is_on_device": self.provider.is_on_device,
            "configured_type": settings.INFERENCE_PROVIDER,
            "phase": "Phase 1 Baseline (Snapdragon NPU Ready)"
        }

    async def answer_query(self, query: str, db: Session, client_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # 1. Fetch real-time ERP context from database
        kpis = ERPService.get_dashboard_kpis(db)
        top_products = ERPService.get_top_selling_products(db, limit=5)
        trends = ERPService.get_monthly_sales_trend(db, months=6)
        overdue = ERPService.get_overdue_invoices(db)
        low_stock = ERPService.get_low_stock_products(db)
        customers = ERPService.get_customers(db)

        erp_context = {
            "kpis": kpis,
            "top_products": top_products,
            "trends": trends,
            "overdue": overdue,
            "low_stock": low_stock,
            "customers": customers,
            "client_context": client_context or {}
        }

        # 2. Delegate to configured inference provider
        result = await self.provider.process_query(query, erp_context)
        
        # Ensure standard envelope
        return {
            "query": query,
            "answer": result.get("answer", "No answer generated."),
            "intent": result.get("intent", "general"),
            "confidence": result.get("confidence", 0.90),
            "metrics": result.get("metrics"),
            "table_data": result.get("table_data"),
            "chart_data": result.get("chart_data"),
            "suggestions": result.get("suggestions", []),
            "inference_provider": result.get("inference_provider", self.provider.name)
        }

copilot_service = CopilotService()
