import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Bot, User, Trash2, ArrowUpRight, CheckCircle2 } from 'lucide-react';

const SUGGESTED_QUERIES = [
  "What were the total sales this month?",
  "Which products are selling the most?",
  "Which customers have overdue payments?",
  "What are the major sales trends?",
  "Summarize the current business situation."
];

export default function CopilotChat({ onRefreshData }) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'copilot',
      text: "👋 **Hello! I am your AI Business Copilot.**\n\nI analyze your live ERP operations data (Sales, Invoices, Customers, and Inventory) to answer strategic business questions.\n\nClick any suggested question below or type your own!",
      suggestions: SUGGESTED_QUERIES,
      timestamp: new Date()
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isSubmitting]);

  const handleSendQuery = async (queryText) => {
    const text = queryText || inputQuery;
    if (!text.trim() || isSubmitting) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: text.trim(),
      timestamp: new Date()
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputQuery('');
    setIsSubmitting(true);

    try {
      const response = await fetch('/api/copilot/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text.trim() })
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();

      const copilotMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'copilot',
        text: data.answer,
        intent: data.intent,
        confidence: data.confidence,
        tableData: data.table_data,
        metrics: data.metrics,
        suggestions: data.suggestions || [],
        inferenceProvider: data.inference_provider,
        timestamp: new Date()
      };

      setMessages((prev) => [...prev, copilotMessage]);
      if (onRefreshData) onRefreshData();
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'copilot',
          text: `⚠️ **Error connecting to Copilot Service**: ${err.message}. Please verify the backend is running.`,
          isError: true,
          suggestions: SUGGESTED_QUERIES.slice(0, 3),
          timestamp: new Date()
        }
      ]);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendQuery();
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 'welcome-cleared',
        sender: 'copilot',
        text: "Conversation cleared. How can I assist with your business data?",
        suggestions: SUGGESTED_QUERIES,
        timestamp: new Date()
      }
    ]);
  };

  // Simple Markdown Parser helper for lists, bolding, headings
  const renderFormattedText = (text) => {
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      // Header 3
      if (line.startsWith('### ')) {
        return <h4 key={idx} className="text-sm font-bold text-white mt-2 mb-1">{line.replace('### ', '')}</h4>;
      }
      // Bold bullet points
      if (line.startsWith('- ')) {
        const content = line.replace('- ', '');
        return (
          <li key={idx} className="ml-4 list-disc text-slate-300 text-xs my-0.5 leading-relaxed">
            {formatBold(content)}
          </li>
        );
      }
      // Empty line
      if (line.trim() === '') {
        return <div key={idx} className="h-1.5" />;
      }
      // Paragraph
      return (
        <p key={idx} className="text-xs text-slate-300 my-0.5 leading-relaxed">
          {formatBold(line)}
        </p>
      );
    });
  };

  const formatBold = (str) => {
    const parts = str.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-semibold text-slate-100">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <div className="flex flex-col h-[580px] rounded-xl bg-[#111726] border border-[#1f2a40] shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-[#1f2a40] bg-[#141c2e] flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-red-600/20 border border-red-500/30 text-red-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white">Ask Copilot (Natural Language ERP Analysis)</h2>
            <p className="text-[11px] text-slate-400">Trained on local business schemas & sales ledgers</p>
          </div>
        </div>

        <button
          onClick={handleClearChat}
          title="Reset conversation"
          className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-[#1f2a40] rounded-lg transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Suggested Chips Bar (Always visible at top for quick testing) */}
      <div className="px-3 py-2 bg-[#0c121e]/80 border-b border-[#1b2538] flex items-center gap-1.5 overflow-x-auto text-xs no-scrollbar">
        <span className="text-[11px] font-medium text-slate-500 whitespace-nowrap px-1">Try asking:</span>
        {SUGGESTED_QUERIES.map((q, i) => (
          <button
            key={i}
            onClick={() => handleSendQuery(q)}
            disabled={isSubmitting}
            className="px-2.5 py-1 rounded-md bg-[#162033] hover:bg-red-950/40 text-slate-300 hover:text-red-200 border border-[#243350] hover:border-red-600/40 whitespace-nowrap text-[11px] font-medium transition-colors"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Message History */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          return (
            <div key={msg.id} className={`flex items-start gap-2.5 ${isUser ? 'flex-row-reverse' : ''}`}>
              {/* Avatar */}
              <div
                className={`flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-xs ${
                  isUser
                    ? 'bg-blue-600 text-white'
                    : 'bg-gradient-to-tr from-red-600 to-rose-400 text-white shadow-sm'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Bubble */}
              <div className={`max-w-[85%] rounded-xl p-3 text-xs leading-relaxed ${
                isUser 
                  ? 'bg-blue-600 text-white shadow'
                  : 'bg-[#162032] border border-[#22314a] text-slate-200 shadow-sm'
              }`}>
                {isUser ? (
                  <p className="font-medium">{msg.text}</p>
                ) : (
                  <div>
                    {renderFormattedText(msg.text)}

                    {/* Render Table Data if returned */}
                    {msg.tableData && msg.tableData.length > 0 && (
                      <div className="mt-3 overflow-x-auto rounded-lg border border-[#23334d]">
                        <table className="w-full text-left border-collapse text-[11px]">
                          <thead>
                            <tr className="bg-[#1c283f] text-slate-300">
                              {Object.keys(msg.tableData[0]).map((col) => (
                                <th key={col} className="px-2.5 py-1.5 font-semibold border-b border-[#23334d]">
                                  {col}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {msg.tableData.map((row, rIdx) => (
                              <tr key={rIdx} className="hover:bg-[#1e2c45] border-b border-[#1b273b] last:border-0">
                                {Object.values(row).map((val, cIdx) => (
                                  <td key={cIdx} className="px-2.5 py-1 text-slate-300 font-mono text-[10.5px]">
                                    {String(val)}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}

                    {/* Suggestions Chips inside message */}
                    {msg.suggestions && msg.suggestions.length > 0 && (
                      <div className="mt-3 pt-2.5 border-t border-[#23334d] flex flex-wrap gap-1.5">
                        <span className="text-[10.5px] text-slate-400 w-full mb-0.5">Follow-up inquiries:</span>
                        {msg.suggestions.map((sug, sIdx) => (
                          <button
                            key={sIdx}
                            onClick={() => handleSendQuery(sug)}
                            className="flex items-center space-x-1 px-2 py-0.5 rounded bg-[#101726] hover:bg-[#1a253a] border border-[#23334d] text-slate-300 text-[10.5px] hover:text-white transition-colors"
                          >
                            <span>{sug}</span>
                            <ArrowUpRight className="w-2.5 h-2.5 text-slate-400" />
                          </button>
                        ))}
                      </div>
                    )}

                    {/* Inference Provider Tag */}
                    {msg.inferenceProvider && (
                      <div className="mt-2 text-[10px] text-slate-500 flex items-center justify-end space-x-1">
                        <span>Engine: {msg.inferenceProvider}</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Bubble */}
        {isSubmitting && (
          <div className="flex items-start gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-red-600/80 flex items-center justify-center text-white">
              <Bot className="w-4 h-4 animate-pulse" />
            </div>
            <div className="p-3 rounded-xl bg-[#162032] border border-[#22314a] text-xs text-slate-400 flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
              <span>Analyzing business ledger and formulating response...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-3 bg-[#141c2e] border-t border-[#1f2a40]">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question (e.g., 'What were total sales this month?')..."
            disabled={isSubmitting}
            className="flex-1 px-3.5 py-2.5 rounded-lg bg-[#0c121e] border border-[#243350] focus:border-red-500 focus:outline-none text-xs text-white placeholder-slate-500 transition-colors"
          />
          <button
            onClick={() => handleSendQuery()}
            disabled={!inputQuery.trim() || isSubmitting}
            className="px-4 py-2.5 rounded-lg bg-gradient-to-r from-red-600 to-rose-500 hover:from-red-500 hover:to-rose-400 text-white font-medium text-xs flex items-center space-x-1.5 shadow-md shadow-red-950/40 disabled:opacity-40 transition-all duration-150"
          >
            <span>Ask</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
