import React, { useState, useEffect } from 'react';
import { FileText, Users, Boxes, Search, AlertCircle, CheckCircle, Clock } from 'lucide-react';

export default function DataExplorer() {
  const [activeTab, setActiveTab] = useState('invoices');
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  
  const [invoices, setInvoices] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const runFetch = async () => {
      setIsLoading(true);
      try {
        if (activeTab === 'invoices') {
          let url = `/api/erp/invoices?search=${encodeURIComponent(search)}`;
          if (statusFilter) url += `&status=${encodeURIComponent(statusFilter)}`;
          const res = await fetch(url);
          if (res.ok && !cancelled) setInvoices(await res.json());
        } else if (activeTab === 'customers') {
          const res = await fetch(`/api/erp/customers?search=${encodeURIComponent(search)}`);
          if (res.ok && !cancelled) setCustomers(await res.json());
        } else if (activeTab === 'products') {
          const res = await fetch(`/api/erp/products?search=${encodeURIComponent(search)}`);
          if (res.ok && !cancelled) setProducts(await res.json());
        }
      } catch (e) {
        if (!cancelled) console.error(e);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    // Debounce search-driven refetches so we don't fire a request per keystroke.
    const timer = setTimeout(runFetch, 300);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [activeTab, search, statusFilter]);

  return (
    <div className="rounded-xl bg-[#111726] border border-[#1f2a40] overflow-hidden shadow-sm">
      {/* Tab Navigation & Search */}
      <div className="p-4 border-b border-[#1f2a40] bg-[#141c2e] flex flex-col md:flex-row md:items-center justify-between gap-3">
        {/* Tabs */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => { setActiveTab('invoices'); setSearch(''); setStatusFilter(''); }}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'invoices'
                ? 'bg-red-600/20 text-red-400 border border-red-500/40'
                : 'text-slate-400 hover:text-white hover:bg-[#1f2a40]'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Invoices Ledger</span>
          </button>

          <button
            onClick={() => { setActiveTab('customers'); setSearch(''); setStatusFilter(''); }}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'customers'
                ? 'bg-red-600/20 text-red-400 border border-red-500/40'
                : 'text-slate-400 hover:text-white hover:bg-[#1f2a40]'
            }`}
          >
            <Users className="w-3.5 h-3.5" />
            <span>Customers & Accounts</span>
          </button>

          <button
            onClick={() => { setActiveTab('products'); setSearch(''); setStatusFilter(''); }}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'products'
                ? 'bg-red-600/20 text-red-400 border border-red-500/40'
                : 'text-slate-400 hover:text-white hover:bg-[#1f2a40]'
            }`}
          >
            <Boxes className="w-3.5 h-3.5" />
            <span>Catalog & Inventory</span>
          </button>
        </div>

        {/* Filters */}
        <div className="flex items-center space-x-2">
          {activeTab === 'invoices' && (
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-[#0c121e] border border-[#243350] text-xs text-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-red-500"
            >
              <option value="">All Statuses</option>
              <option value="Paid">Paid</option>
              <option value="Pending">Pending</option>
              <option value="Overdue">Overdue</option>
            </select>
          )}

          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
            <input
              type="text"
              placeholder={`Search ${activeTab}...`}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-[#0c121e] border border-[#243350] rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-red-500 w-40 sm:w-56"
            />
          </div>
        </div>
      </div>

      {/* Table Body */}
      <div className="overflow-x-auto max-h-[380px] overflow-y-auto">
        {isLoading ? (
          <div className="p-8 text-center text-slate-400 text-xs">Loading ERP records...</div>
        ) : (
          <table className="w-full text-left border-collapse text-xs">
            {/* INVOICES */}
            {activeTab === 'invoices' && (
              <>
                <thead className="bg-[#161f31] text-slate-400 uppercase text-[10px] tracking-wider sticky top-0">
                  <tr>
                    <th className="px-4 py-2.5">Invoice #</th>
                    <th className="px-4 py-2.5">Customer</th>
                    <th className="px-4 py-2.5">Issue Date</th>
                    <th className="px-4 py-2.5">Due Date</th>
                    <th className="px-4 py-2.5 text-right">Total Amount</th>
                    <th className="px-4 py-2.5 text-right">Balance Due</th>
                    <th className="px-4 py-2.5 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1b263b]">
                  {invoices.map((inv) => (
                    <tr key={inv.id} className="hover:bg-[#172236] transition-colors">
                      <td className="px-4 py-2.5 font-mono text-slate-200">{inv.invoice_number}</td>
                      <td className="px-4 py-2.5 font-medium text-white">{inv.customer_name}</td>
                      <td className="px-4 py-2.5 text-slate-400">{inv.issue_date}</td>
                      <td className="px-4 py-2.5 text-slate-400">{inv.due_date}</td>
                      <td className="px-4 py-2.5 text-right font-mono font-medium text-slate-200">
                        ${inv.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-2.5 text-right font-mono font-medium">
                        {inv.balance_due > 0 ? (
                          <span className="text-amber-400">${inv.balance_due.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
                        ) : (
                          <span className="text-slate-500">$0.00</span>
                        )}
                      </td>
                      <td className="px-4 py-2.5 text-center">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10.5px] font-semibold ${
                          inv.status === 'Paid'
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : inv.status === 'Overdue'
                            ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        }`}>
                          {inv.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {invoices.length === 0 && (
                    <tr>
                      <td colSpan={7} className="text-center py-6 text-slate-500">No invoices match your filter.</td>
                    </tr>
                  )}
                </tbody>
              </>
            )}

            {/* CUSTOMERS */}
            {activeTab === 'customers' && (
              <>
                <thead className="bg-[#161f31] text-slate-400 uppercase text-[10px] tracking-wider sticky top-0">
                  <tr>
                    <th className="px-4 py-2.5">Company Name</th>
                    <th className="px-4 py-2.5">Region</th>
                    <th className="px-4 py-2.5">Segment</th>
                    <th className="px-4 py-2.5">Contact Email</th>
                    <th className="px-4 py-2.5 text-right">Credit Limit</th>
                    <th className="px-4 py-2.5 text-center">Account Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1b263b]">
                  {customers.map((c) => (
                    <tr key={c.id} className="hover:bg-[#172236] transition-colors">
                      <td className="px-4 py-2.5 font-medium text-white">{c.name}</td>
                      <td className="px-4 py-2.5 text-slate-400">{c.region}</td>
                      <td className="px-4 py-2.5 text-slate-300">{c.segment}</td>
                      <td className="px-4 py-2.5 text-slate-400 font-mono text-[11px]">{c.email}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-slate-200">
                        ${c.credit_limit.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-2.5 text-center">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10.5px] font-semibold ${
                          c.status === 'Active'
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : c.status === 'Delinquent'
                            ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        }`}>
                          {c.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {customers.length === 0 && (
                    <tr>
                      <td colSpan={6} className="text-center py-6 text-slate-500">No customers found.</td>
                    </tr>
                  )}
                </tbody>
              </>
            )}

            {/* PRODUCTS */}
            {activeTab === 'products' && (
              <>
                <thead className="bg-[#161f31] text-slate-400 uppercase text-[10px] tracking-wider sticky top-0">
                  <tr>
                    <th className="px-4 py-2.5">SKU</th>
                    <th className="px-4 py-2.5">Product Name</th>
                    <th className="px-4 py-2.5">Category</th>
                    <th className="px-4 py-2.5 text-right">Unit Price</th>
                    <th className="px-4 py-2.5 text-right">Current Stock</th>
                    <th className="px-4 py-2.5 text-center">Inventory Health</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1b263b]">
                  {products.map((p) => (
                    <tr key={p.id} className="hover:bg-[#172236] transition-colors">
                      <td className="px-4 py-2.5 font-mono text-slate-300">{p.sku}</td>
                      <td className="px-4 py-2.5 font-medium text-white">{p.name}</td>
                      <td className="px-4 py-2.5 text-slate-400">{p.category}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-slate-200">
                        ${p.unit_price.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-2.5 text-right font-mono font-medium">
                        {p.stock_quantity} units
                      </td>
                      <td className="px-4 py-2.5 text-center">
                        {p.is_low_stock ? (
                          <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-[10.5px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                            <AlertCircle className="w-3 h-3" />
                            <span>Low Stock (≤{p.reorder_threshold})</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-[10.5px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            <CheckCircle className="w-3 h-3" />
                            <span>Healthy</span>
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                  {products.length === 0 && (
                    <tr>
                      <td colSpan={6} className="text-center py-6 text-slate-500">No products found.</td>
                    </tr>
                  )}
                </tbody>
              </>
            )}
          </table>
        )}
      </div>
    </div>
  );
}
