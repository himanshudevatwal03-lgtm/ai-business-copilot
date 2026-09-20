import React from 'react';
import { Cpu, RefreshCw, Layers, ShieldCheck, Sparkles } from 'lucide-react';

export default function Navbar({ onOpenSnapdragonModal, onReseed, isReseeding }) {
  return (
    <header className="sticky top-0 z-40 border-b border-[#1f293d] bg-[#0c121e]/90 backdrop-blur-md px-4 sm:px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3">
        {/* Brand & Badge */}
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-red-600 to-rose-400 flex items-center justify-center shadow-lg shadow-red-950/40 ring-1 ring-red-500/30">
            <Cpu className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold tracking-tight text-white">AI Business Copilot</h1>
              <span className="text-[11px] font-semibold tracking-wide uppercase px-2 py-0.5 rounded-full bg-red-500/15 text-red-400 border border-red-500/30">
                Snapdragon AI Lab 2026
              </span>
            </div>
            <p className="text-xs text-slate-400">Local-First ERP Operations & Intelligence Assistant</p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center flex-wrap gap-2.5">
          {/* Status badge */}
          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#151d2f] border border-[#222e47] text-xs text-slate-300">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span className="font-mono text-emerald-400 font-medium">Local-Ready</span>
            <span className="text-slate-500">|</span>
            <span className="text-slate-400">Zero Cloud Keys Needed</span>
          </div>

          {/* Architecture Roadmap Button */}
          <button
            onClick={onOpenSnapdragonModal}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-red-950/40 hover:bg-red-900/50 text-red-300 border border-red-700/50 text-xs font-semibold transition-colors duration-150"
          >
            <Layers className="w-3.5 h-3.5 text-red-400" />
            <span>Qualcomm AI Hub Roadmap</span>
          </button>

          {/* Reseed Data */}
          <button
            onClick={onReseed}
            disabled={isReseeding}
            title="Reseed sample ERP dataset"
            className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg bg-[#151d2f] hover:bg-[#1b263d] text-slate-300 hover:text-white border border-[#222e47] text-xs transition-colors duration-150 disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isReseeding ? 'animate-spin text-red-400' : ''}`} />
            <span>{isReseeding ? 'Resetting...' : 'Reset ERP Data'}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
