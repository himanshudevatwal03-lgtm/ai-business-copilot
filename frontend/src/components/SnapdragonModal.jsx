import React from 'react';
import { X, Cpu, CheckCircle2, ArrowRight, ShieldCheck, Zap, Layers, HardDrive } from 'lucide-react';

export default function SnapdragonModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-2xl rounded-2xl bg-[#0e1524] border border-[#23314d] shadow-2xl p-6 text-slate-200 overflow-hidden">
        {/* Glow decoration */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-red-600/20 rounded-full blur-3xl pointer-events-none" />
        
        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-[#1f2b42]">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-gradient-to-tr from-red-600 to-rose-500 text-white shadow-lg">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">
                Snapdragon AI Lab Architecture & Roadmap
              </h2>
              <p className="text-xs text-slate-400">Qualcomm AI Hub On-Device Integration Plan (2026)</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-[#1c273d] transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="py-4 space-y-4 text-xs max-h-[70vh] overflow-y-auto pr-1">
          {/* Phase 1 Badge & Clarification */}
          <div className="p-3.5 rounded-xl bg-[#131b2c] border border-[#23334d]">
            <div className="flex items-center space-x-2 text-emerald-400 font-semibold mb-1">
              <CheckCircle2 className="w-4 h-4" />
              <span>Phase 1 (Current Working Baseline): Clean Local Architecture</span>
            </div>
            <p className="text-slate-300 leading-relaxed">
              The application runs 100% locally using a robust <strong>Deterministic Business Analytics Engine</strong>. 
              Zero external API keys are required to run, test, and verify. No false claims of active NPU execution are made in this baseline.
            </p>
          </div>

          {/* Phase 2 Qualcomm AI Hub Roadmap */}
          <div className="p-3.5 rounded-xl bg-[#171220] border border-red-900/40">
            <div className="flex items-center space-x-2 text-red-400 font-semibold mb-2">
              <Zap className="w-4 h-4" />
              <span>Phase 2: Qualcomm AI Hub & Snapdragon NPU Acceleration</span>
            </div>
            
            <div className="space-y-2.5 text-slate-300">
              <div className="flex items-start space-x-2">
                <HardDrive className="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-white">Hardware Target:</strong> Snapdragon X Elite / Snapdragon Compute platform with Hexagon NPU (45+ TOPS).
                </div>
              </div>

              <div className="flex items-start space-x-2">
                <Layers className="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-white">Model Compilation:</strong> Quantized models (e.g. <code>Phi-3-mini-4k-instruct INT4</code> or <code>Llama-3-8B-Instruct W4A16</code>) compiled via <strong>Qualcomm AI Hub</strong>.
                </div>
              </div>

              <div className="flex items-start space-x-2">
                <Cpu className="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-white">Runtime Bridge:</strong> ONNX Runtime with <code>QNNExecutionProvider</code> (Qualcomm Neural Processing SDK) plugged into <code>app/providers/qualcomm_adapter.py</code>.
                </div>
              </div>

              <div className="flex items-start space-x-2">
                <ShieldCheck className="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" />
                <div>
                  <strong className="text-white">Privacy & Compliance:</strong> ERP financial ledgers, customer debts, and margins remain 100% confidential on-device, satisfying strict enterprise data isolation regulations.
                </div>
              </div>
            </div>
          </div>

          {/* Modular Adapter Code Architecture */}
          <div className="p-3 rounded-xl bg-[#090d16] border border-[#1d273a] font-mono text-[11px]">
            <p className="text-slate-400 mb-1">// backend/app/providers/qualcomm_adapter.py</p>
            <p className="text-rose-400">class <span className="text-yellow-300">QualcommAIHubAdapter</span>(BaseInferenceProvider):</p>
            <p className="text-slate-300 pl-4">providers = [('<span className="text-emerald-300">QNNExecutionProvider</span>', &#123;'backend_path': 'QnnHtp.dll'&#125;)]</p>
            <p className="text-slate-300 pl-4">session = ort.InferenceSession(model_path, providers=providers)</p>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-[#1f2b42] flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-[#1a253a] hover:bg-[#23324f] text-slate-200 text-xs font-medium transition-colors"
          >
            Close Roadmap
          </button>
        </div>
      </div>
    </div>
  );
}
