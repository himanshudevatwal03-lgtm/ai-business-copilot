import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import KPICards from './components/KPICards';
import SalesCharts from './components/SalesCharts';
import CopilotChat from './components/CopilotChat';
import DataExplorer from './components/DataExplorer';
import SnapdragonModal from './components/SnapdragonModal';

export default function App() {
  const [kpis, setKpis] = useState(null);
  const [trends, setTrends] = useState([]);
  const [topProducts, setTopProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isReseeding, setIsReseeding] = useState(false);
  const [isSnapdragonModalOpen, setIsSnapdragonModalOpen] = useState(false);

  const fetchDashboardData = async () => {
    try {
      const [kpiRes, trendsRes, topProdRes] = await Promise.all([
        fetch('/api/dashboard/kpis'),
        fetch('/api/dashboard/trends?months=6'),
        fetch('/api/dashboard/top-products?limit=5')
      ]);

      if (kpiRes.ok) setKpis(await kpiRes.json());
      if (trendsRes.ok) setTrends(await trendsRes.json());
      if (topProdRes.ok) setTopProducts(await topProdRes.json());
    } catch (err) {
      console.error('Failed to load dashboard metrics:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleReseed = async () => {
    setIsReseeding(true);
    try {
      const res = await fetch('/api/erp/reseed', { method: 'POST' });
      if (res.ok) {
        await fetchDashboardData();
      }
    } catch (e) {
      console.error('Error reseeding:', e);
    } finally {
      setIsReseeding(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100 flex flex-col selection:bg-red-500 selection:text-white">
      {/* Navigation */}
      <Navbar
        onOpenSnapdragonModal={() => setIsSnapdragonModalOpen(true)}
        onReseed={handleReseed}
        isReseeding={isReseeding}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* Executive KPI Cards */}
        <KPICards kpis={kpis} isLoading={isLoading} />

        {/* 2-Column Section: Visual Analytics & Copilot Chat */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column: Visual Trends & Charts (7 cols) */}
          <div className="lg:col-span-6 space-y-6">
            <SalesCharts trends={trends} topProducts={topProducts} isLoading={isLoading} />
            <DataExplorer />
          </div>

          {/* Right Column: AI Copilot Conversational Assistant (6 cols) */}
          <div className="lg:col-span-6">
            <CopilotChat onRefreshData={fetchDashboardData} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-[#1a2336] bg-[#0c121f] py-4 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>AI Business Copilot • Snapdragon AI Lab Build & Present Challenge 2026</span>
          <span className="text-slate-400">Local-First Enterprise Intelligence Architecture</span>
        </div>
      </footer>

      {/* Snapdragon AI Hub Modal */}
      <SnapdragonModal
        isOpen={isSnapdragonModalOpen}
        onClose={() => setIsSnapdragonModalOpen(false)}
      />
    </div>
  );
}
