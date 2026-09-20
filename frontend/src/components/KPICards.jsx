import React from 'react';
import { DollarSign, TrendingUp, AlertTriangle, Boxes, Users, ShoppingCart } from 'lucide-react';

export default function KPICards({ kpis, isLoading }) {
  if (isLoading || !kpis) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-28 bg-[#131a29] animate-pulse rounded-xl border border-[#1e293b]" />
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: "Total Sales This Month",
      value: `$${kpis.monthly_revenue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      subtext: `${kpis.revenue_growth_pct >= 0 ? '+' : ''}${kpis.revenue_growth_pct}% vs last month`,
      subtextColor: kpis.revenue_growth_pct >= 0 ? "text-emerald-400" : "text-rose-400",
      icon: DollarSign,
      iconBg: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
    },
    {
      title: "All-Time Revenue",
      value: `$${kpis.total_revenue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      subtext: `${kpis.total_orders_count} lifetime orders processed`,
      subtextColor: "text-slate-400",
      icon: TrendingUp,
      iconBg: "bg-blue-500/10 text-blue-400 border-blue-500/20"
    },
    {
      title: "Overdue Receivables",
      value: `$${kpis.overdue_receivables.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      subtext: `${kpis.overdue_invoices_count} delinquent invoices`,
      subtextColor: kpis.overdue_invoices_count > 0 ? "text-amber-400" : "text-slate-400",
      icon: AlertTriangle,
      iconBg: "bg-amber-500/10 text-amber-400 border-amber-500/20"
    },
    {
      title: "Inventory & Clients",
      value: `${kpis.active_customers_count} Active Clients`,
      subtext: `${kpis.low_stock_products_count} SKUs below reorder point`,
      subtextColor: kpis.low_stock_products_count > 0 ? "text-rose-400" : "text-slate-400",
      icon: Boxes,
      iconBg: "bg-rose-500/10 text-rose-400 border-rose-500/20"
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="p-4 rounded-xl bg-[#111726] border border-[#1f2a40] shadow-sm hover:border-[#2b3a58] transition-all duration-200"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                {card.title}
              </span>
              <div className={`p-2 rounded-lg border ${card.iconBg}`}>
                <Icon className="w-4 h-4" />
              </div>
            </div>
            <div className="text-2xl font-bold tracking-tight text-white mb-1">
              {card.value}
            </div>
            <div className={`text-xs font-medium ${card.subtextColor}`}>
              {card.subtext}
            </div>
          </div>
        );
      })}
    </div>
  );
}
