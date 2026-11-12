"use client";

import { useMemo, useState } from "react";
import { Activity, ArrowDownRight, ArrowUpRight, Bell, BriefcaseBusiness, ChevronDown, CircleHelp, CreditCard, Download, LayoutDashboard, Menu, Search, Settings2, ShieldAlert, ShoppingBag, Users, WalletCards, X } from "lucide-react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, BarChart, Bar } from "recharts";

const trend = [
  { month: "May", transactions: 18400, value: 2.1 },
  { month: "Jun", transactions: 21300, value: 2.4 },
  { month: "Jul", transactions: 19800, value: 2.3 },
  { month: "Aug", transactions: 24700, value: 2.8 },
  { month: "Sep", transactions: 23100, value: 2.6 },
  { month: "Oct", transactions: 28600, value: 3.2 },
  { month: "Nov", transactions: 31200, value: 3.6 }
];
const segments = [
  { name: "High value", customers: 2840, fill: "#145dcc" },
  { name: "Growing", customers: 4120, fill: "#3985e8" },
  { name: "Regular", customers: 6380, fill: "#77a9ee" },
  { name: "At risk", customers: 1960, fill: "#e5a23b" },
  { name: "Dormant", customers: 870, fill: "#d96b6b" }
];
const customers = [
  { id: "CUS-1048", name: "Customer 1048", segment: "High value", activity: "Today", risk: "Low", score: "92" },
  { id: "CUS-2081", name: "Customer 2081", segment: "Growing", activity: "Yesterday", risk: "Low", score: "81" },
  { id: "CUS-3194", name: "Customer 3194", segment: "At risk", activity: "28 days ago", risk: "High", score: "34" },
  { id: "CUS-4270", name: "Customer 4270", segment: "Regular", activity: "4 days ago", risk: "Medium", score: "67" },
  { id: "CUS-5112", name: "Customer 5112", segment: "At risk", activity: "35 days ago", risk: "High", score: "21" }
];

function Metric({ label, value, change, up, icon: Icon }: { label: string; value: string; change: string; up?: boolean; icon: React.ElementType }) {
  return <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
    <div className="flex items-center justify-between"><p className="text-sm text-slate-500">{label}</p><span className="rounded-xl bg-blue-50 p-2 text-blue-700"><Icon size={18}/></span></div>
    <div className="mt-4 flex items-end justify-between"><h3 className="text-2xl font-bold tracking-tight">{value}</h3><span className={`flex items-center gap-1 text-xs font-semibold ${up ? "text-emerald-600" : "text-rose-600"}`}>{up ? <ArrowUpRight size={14}/> : <ArrowDownRight size={14}/>} {change}</span></div>
    <p className="mt-2 text-xs text-slate-400">Compared with previous period</p>
  </div>;
}

export default function Dashboard() {
  const [active, setActive] = useState("Overview");
  const [query, setQuery] = useState("");
  const [mobileOpen, setMobileOpen] = useState(false);
  const filtered = useMemo(() => customers.filter(c => [c.id, c.name, c.segment].join(" ").toLowerCase().includes(query.toLowerCase())), [query]);
  const nav = [
    { label: "Overview", icon: LayoutDashboard },
    { label: "Customers", icon: Users },
    { label: "Churn intelligence", icon: ShieldAlert },
    { label: "Segments", icon: BriefcaseBusiness },
    { label: "Cross-sell", icon: ShoppingBag }
  ];
  return <div className="min-h-screen lg:flex">
    <aside className={`fixed inset-y-0 left-0 z-30 flex w-64 flex-col border-r border-slate-200 bg-white px-5 py-6 transition-transform lg:static lg:translate-x-0 ${mobileOpen ? "translate-x-0" : "-translate-x-full"}`}>
      <div className="flex items-center justify-between"><div className="flex items-center gap-3"><div className="rounded-xl bg-blue-700 p-2 text-white"><Activity size={21}/></div><div><p className="font-bold tracking-tight">IntelliBank</p><p className="text-[11px] text-slate-400">BancABC customer intelligence</p></div></div><button className="lg:hidden" onClick={() => setMobileOpen(false)} aria-label="Close menu"><X size={19}/></button></div>
      <p className="mb-3 mt-10 px-3 text-[10px] font-bold uppercase tracking-[.16em] text-slate-400">Workspace</p>
      <nav className="space-y-1">{nav.map(item => <button key={item.label} onClick={() => { setActive(item.label); setMobileOpen(false); }} className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-medium transition ${active === item.label ? "bg-blue-50 text-blue-700" : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"}`}><item.icon size={18}/>{item.label}</button>)}</nav>
      <div className="mt-auto rounded-2xl bg-slate-900 p-4 text-white"><div className="mb-3 flex items-center gap-2 text-blue-300"><CircleHelp size={17}/><span className="text-xs font-semibold">Hackathon build</span></div><p className="text-sm font-semibold">Turn transactions into decisions.</p><p className="mt-2 text-xs leading-5 text-slate-400">A prototype for customer retention, value discovery and smarter product recommendations.</p></div>
      <div className="mt-5 flex items-center gap-3 border-t border-slate-100 pt-5"><div className="grid h-9 w-9 place-items-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">UZ</div><div><p className="text-sm font-semibold">Project team</p><p className="text-xs text-slate-400">University of Zimbabwe</p></div><ChevronDown className="ml-auto text-slate-400" size={16}/></div>
    </aside>
    {mobileOpen && <button aria-label="Close navigation overlay" className="fixed inset-0 z-20 bg-slate-950/30 lg:hidden" onClick={() => setMobileOpen(false)}/>}
    <main className="min-w-0 flex-1">
      <header className="sticky top-0 z-10 flex h-[76px] items-center justify-between border-b border-slate-200 bg-white/90 px-5 backdrop-blur md:px-8">
        <div className="flex items-center gap-3"><button className="lg:hidden" onClick={() => setMobileOpen(true)} aria-label="Open menu"><Menu/></button><div><p className="text-xs text-slate-400">Workspace / {active}</p><h1 className="text-lg font-bold">{active}</h1></div></div>
        <div className="flex items-center gap-3"><span className="hidden rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-[11px] font-semibold text-amber-700 sm:inline-flex">DEMO DATA</span><button className="rounded-xl border border-slate-200 p-2 text-slate-500 hover:bg-slate-50" aria-label="Notifications"><Bell size={18}/></button><button className="hidden rounded-xl border border-slate-200 p-2 text-slate-500 hover:bg-slate-50 sm:block" aria-label="Settings"><Settings2 size={18}/></button></div>
      </header>
      <div className="mx-auto max-w-[1440px] space-y-6 p-5 md:p-8">
        <section className="flex flex-col justify-between gap-4 md:flex-row md:items-end"><div><p className="text-sm font-medium text-blue-700">Good morning</p><h2 className="mt-1 text-2xl font-bold tracking-tight md:text-3xl">Customer intelligence at a glance</h2><p className="mt-2 text-sm text-slate-500">Monitor customer value, engagement and retention opportunities.</p></div><button className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-800"><Download size={16}/> Export report</button></section>
        <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-xs leading-5 text-amber-800"><strong>Prototype notice:</strong> All figures and customer records shown here are synthetic demonstration data. They are not actual BancABC customer information.</div>
        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <Metric label="Customers analysed" value="16,170" change="+8.4%" up icon={Users}/>
          <Metric label="Customers at high churn risk" value="1,960" change="+2.1%" icon={ShieldAlert}/>
          <Metric label="High-value customers" value="2,840" change="+6.7%" up icon={WalletCards}/>
          <Metric label="Potential cross-sell leads" value="3,420" change="+11.2%" up icon={CreditCard}/>
        </section>
        <section className="grid gap-5 xl:grid-cols-[1.65fr_1fr]">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft"><div className="flex flex-wrap items-start justify-between gap-3"><div><h3 className="font-bold">Transaction activity</h3><p className="mt-1 text-xs text-slate-400">Monthly transaction volume · synthetic sample</p></div><span className="rounded-lg bg-slate-50 px-3 py-1.5 text-xs text-slate-500">Last 7 months</span></div><div className="mt-5 h-[260px] w-full"><ResponsiveContainer width="100%" height="100%"><AreaChart data={trend}><defs><linearGradient id="volumeFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2166d1" stopOpacity={0.2}/><stop offset="95%" stopColor="#2166d1" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#eef1f6" vertical={false}/><XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fontSize:12,fill:"#98a2b3"}}/><YAxis axisLine={false} tickLine={false} tick={{fontSize:11,fill:"#98a2b3"}} tickFormatter={v => `${v/1000}k`}/><Tooltip/><Area type="monotone" dataKey="transactions" stroke="#2166d1" strokeWidth={2.5} fill="url(#volumeFill)"/></AreaChart></ResponsiveContainer></div></div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft"><h3 className="font-bold">Customer segments</h3><p className="mt-1 text-xs text-slate-400">Distribution by behavioural group</p><div className="mt-4 h-[205px]"><ResponsiveContainer width="100%" height="100%"><BarChart data={segments} layout="vertical" margin={{left:8,right:8}}><XAxis type="number" hide/><YAxis type="category" dataKey="name" width={82} axisLine={false} tickLine={false} tick={{fontSize:11,fill:"#667085"}}/><Tooltip/><Bar dataKey="customers" radius={[0,6,6,0]} fill="#2469d5" barSize={17}/></BarChart></ResponsiveContainer></div><div className="mt-2 grid grid-cols-2 gap-2">{segments.slice(0,4).map(s => <div key={s.name} className="flex items-center gap-2 text-xs text-slate-500"><span className="h-2 w-2 rounded-full" style={{background:s.fill}}/>{s.name}<strong className="ml-auto text-slate-800">{s.customers.toLocaleString()}</strong></div>)}</div></div>
        </section>
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft"><div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center"><div><h3 className="font-bold">Customer watchlist</h3><p className="mt-1 text-xs text-slate-400">Sample customers ranked by engagement and churn signals</p></div><div className="relative"><Search className="absolute left-3 top-2.5 text-slate-400" size={16}/><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search customers..." className="w-full rounded-xl border border-slate-200 py-2 pl-9 pr-3 text-sm outline-none focus:border-blue-500 sm:w-64"/></div></div><div className="mt-5 overflow-x-auto"><table className="w-full min-w-[620px] text-left text-sm"><thead><tr className="border-b border-slate-100 text-xs text-slate-400"><th className="pb-3 font-medium">Customer</th><th className="pb-3 font-medium">Segment</th><th className="pb-3 font-medium">Last activity</th><th className="pb-3 font-medium">Churn risk</th><th className="pb-3 text-right font-medium">Engagement</th></tr></thead><tbody>{filtered.map(c => <tr key={c.id} className="border-b border-slate-50 last:border-0"><td className="py-4"><p className="font-semibold text-slate-800">{c.name}</p><p className="text-xs text-slate-400">{c.id}</p></td><td className="py-4 text-slate-600">{c.segment}</td><td className="py-4 text-slate-500">{c.activity}</td><td className="py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${c.risk === "High" ? "bg-rose-50 text-rose-700" : c.risk === "Medium" ? "bg-amber-50 text-amber-700" : "bg-emerald-50 text-emerald-700"}`}>{c.risk}</span></td><td className="py-4 text-right font-semibold">{c.score}<span className="text-slate-400">/100</span></td></tr>)}</tbody></table>{filtered.length === 0 && <p className="py-8 text-center text-sm text-slate-400">No matching customers.</p>}</div></section>
        <footer className="flex flex-col justify-between gap-2 pb-4 text-xs text-slate-400 sm:flex-row"><span>IntelliBank · BancABC Universities Hackathon 2026</span><span>Prototype interface · Synthetic data only</span></footer>
      </div>
    </main>
  </div>;
}
