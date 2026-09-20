import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  AreaChart,
  Area
} from 'recharts';
import { BarChart3, TrendingUp } from 'lucide-react';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-[#111726] p-3 rounded-lg border border-[#243350] shadow-xl text-xs">
        <p className="font-semibold text-slate-200 mb-1">{label}</p>
        {payload.map((entry, index) => (
          <p key={`item-${index}`} style={{ color: entry.color }}>
            {entry.name}: {entry.name.toLowerCase().includes('rev') || entry.name.toLowerCase().includes('sales') 
              ? `$${Number(entry.value).toLocaleString('en-US', { minimumFractionDigits: 2 })}` 
              : entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function SalesCharts({ trends, topProducts, isLoading }) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="h-64 bg-[#111726] animate-pulse rounded-xl border border-[#1f2a40]" />
        <div className="h-64 bg-[#111726] animate-pulse rounded-xl border border-[#1f2a40]" />
      </div>
    );
  }

  // Format top products data for horizontal bar
  const formattedProducts = (topProducts || []).map(p => ({
    name: p.product_name.length > 22 ? p.product_name.slice(0, 20) + '...' : p.product_name,
    fullName: p.product_name,
    revenue: p.total_revenue,
    qty: p.quantity_sold
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {/* Monthly Sales Trajectory */}
      <div className="p-4 rounded-xl bg-[#111726] border border-[#1f2a40] flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-red-500" />
            <h3 className="text-sm font-semibold text-white">Monthly Sales Trend</h3>
          </div>
          <span className="text-xs text-slate-400">Past 6 Months</span>
        </div>
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trends || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="salesGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#E10600" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#E10600" stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1c2638" vertical={false} />
              <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis 
                stroke="#64748b" 
                tick={{ fontSize: 11 }} 
                tickFormatter={(val) => `$${val > 999 ? (val / 1000).toFixed(0) + 'k' : val}`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area 
                type="monotone" 
                dataKey="revenue" 
                name="Revenue" 
                stroke="#E10600" 
                strokeWidth={2.5} 
                fillOpacity={1} 
                fill="url(#salesGrad)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Products by Revenue */}
      <div className="p-4 rounded-xl bg-[#111726] border border-[#1f2a40] flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-semibold text-white">Top 5 Products by Revenue</h3>
          </div>
          <span className="text-xs text-slate-400">Lifetime Leaderboard</span>
        </div>
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart 
              data={formattedProducts} 
              layout="vertical" 
              margin={{ top: 5, right: 15, left: 10, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1c2638" horizontal={false} />
              <XAxis 
                type="number" 
                stroke="#64748b" 
                tick={{ fontSize: 10 }}
                tickFormatter={(val) => `$${val > 999 ? (val / 1000).toFixed(0) + 'k' : val}`}
              />
              <YAxis 
                type="category" 
                dataKey="name" 
                stroke="#94a3b8" 
                tick={{ fontSize: 11 }} 
                width={110} 
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="revenue" name="Revenue" fill="#3b82f6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
