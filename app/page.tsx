"use client";

import { useEffect, useMemo, useState } from "react";
import { Activity, ArrowUpRight, Bell, BriefcaseBusiness, CheckCircle2, CircleHelp, CreditCard, Download, FileSpreadsheet, LayoutDashboard, Loader2, Menu, Search, ShieldAlert, ShoppingBag, UploadCloud, Users, WalletCards, X, AlertTriangle, RefreshCw } from "lucide-react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, BarChart, Bar } from "recharts";

type Customer = {id:string;segment:string;days_since_activity:number|null;churn_risk:string;risk_score:number;engagement_score:number;transactions:number;total_value:number;reason:string;action:string};
type Analysis = {overview:{customers_analysed:number;high_churn_risk:number;high_value_customers:number;cross_sell_leads:number;data_mode:string;transaction_rows?:number;currency_note?:string};segments:{name:string;customers:number}[];customers:Customer[];recommendations:{segment:string;customers?:number;opportunity:string;rationale:string;priority:string}[];profile?:{rows:number;columns:string[];missing_values:Record<string,number>;duplicate_customer_ids:number;detected_fields:Record<string,string|null>}|null;trend:{period:string;transactions:number;customers:number}[];insights:string[];mode_note:string};

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const demo:Analysis = {
 overview:{customers_analysed:16170,high_churn_risk:1960,high_value_customers:2840,cross_sell_leads:3420,data_mode:"synthetic_demo"},
 segments:[{name:"High value",customers:2840},{name:"Growing",customers:4120},{name:"Regular",customers:6380},{name:"At risk",customers:1960},{name:"Dormant",customers:870}],
 customers:[
 {id:"CUS-1048",segment:"High value",days_since_activity:0,churn_risk:"Low",risk_score:8,engagement_score:92,transactions:44,total_value:8200,reason:"Consistent recent activity and high relative value",action:"Relationship review"},
 {id:"CUS-2081",segment:"Growing",days_since_activity:1,churn_risk:"Low",risk_score:19,engagement_score:81,transactions:25,total_value:2300,reason:"Recent activity and increasing engagement",action:"Engagement and product education"},
 {id:"CUS-3194",segment:"At risk",days_since_activity:28,churn_risk:"High",risk_score:87,engagement_score:13,transactions:3,total_value:160,reason:"28 days inactive; low transaction frequency and value",action:"Retention outreach and service check-in"},
 {id:"CUS-4270",segment:"Regular",days_since_activity:4,churn_risk:"Medium",risk_score:52,engagement_score:48,transactions:12,total_value:900,reason:"Moderate activity relative to this sample",action:"Personalised engagement"},
 {id:"CUS-5112",segment:"At risk",days_since_activity:35,churn_risk:"High",risk_score:94,engagement_score:6,transactions:2,total_value:80,reason:"35 days inactive; low transaction frequency and value",action:"Retention outreach and service check-in"}],
 recommendations:[{segment:"At risk",customers:1960,opportunity:"Retention outreach",rationale:"Illustrative demo rule: declining activity and long inactivity gaps.",priority:"High"},{segment:"High value",customers:2840,opportunity:"Relationship review",rationale:"Illustrative demo rule: strong relative transaction value.",priority:"Medium"}],
 profile:null,trend:[{period:"Demo sample",transactions:31200,customers:16170}],insights:["Synthetic demonstration records are loaded.","Upload a CSV to calculate metrics from your own data.","No supervised churn model has been trained."],mode_note:"Synthetic demonstration only. Upload CSV to calculate behavioural analytics."
};

function Metric({label,value,sub,icon:Icon}:{label:string;value:string;sub:string;icon:React.ElementType}) {
 return <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-center justify-between"><p className="text-sm text-slate-500">{label}</p><span className="rounded-xl bg-blue-50 p-2 text-blue-700"><Icon size={18}/></span></div><p className="mt-4 text-3xl font-bold tracking-tight">{value}</p><p className="mt-2 text-xs text-slate-400">{sub}</p></div>;
}
function downloadSampleCsv() {
 const csv = [
  "customer_id,transaction_date,amount,transaction_type,channel",
  "CUST-001,2026-11-08,125.50,POS,Card",
  "CUST-001,2026-10-25,80.00,Transfer,Mobile",
  "CUST-001,2026-09-20,210.00,POS,Card",
  "CUST-002,2026-10-30,45.00,Bill payment,Mobile",
  "CUST-002,2026-09-18,32.00,Transfer,Online",
  "CUST-003,2026-08-01,18.00,POS,Card",
  "CUST-004,2026-11-10,560.00,Transfer,Online",
  "CUST-004,2026-11-02,340.00,POS,Card",
  "CUST-004,2026-10-28,125.00,Bill payment,Mobile",
  "CUST-005,2026-07-15,12.00,POS,Card"
 ].join("\n");
 const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));const a=document.createElement("a");a.href=url;a.download="intellibank-demo-transactions.csv";a.click();URL.revokeObjectURL(url);
}
function downloadCsv(rows:Customer[]) {
 const columns=["id","segment","churn_risk","risk_score","engagement_score","days_since_activity","transactions","total_value","reason","action"];
 const csv=[columns.join(","),...rows.map(r=>columns.map(k=>JSON.stringify((r as any)[k] ?? "")).join(","))].join("\n");
 const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"})); const a=document.createElement("a");a.href=url;a.download="intellibank-customer-analysis.csv";a.click();URL.revokeObjectURL(url);
}

export default function Dashboard() {
 const [data,setData]=useState<Analysis>(demo);
 const [active,setActive]=useState("Overview");
 const [query,setQuery]=useState("");
 const [file,setFile]=useState<File|null>(null);
 const [busy,setBusy]=useState(false);
 const [error,setError]=useState("");
 const [notice,setNotice]=useState("");
 const [mobileOpen,setMobileOpen]=useState(false);
 useEffect(()=>{fetch(API+"/api/analysis").then(r=>{if(!r.ok)throw new Error("API unavailable");return r.json()}).then((d:Analysis)=>setData(d)).catch(()=>setNotice("Backend is not connected. Showing clearly labelled sample data; start the FastAPI service to enable CSV analysis."));},[]);
 const filtered=useMemo(()=>data.customers.filter(c=>[c.id,c.segment,c.churn_risk].join(" ").toLowerCase().includes(query.toLowerCase())),[data.customers,query]);
 const nav=[{label:"Overview",icon:LayoutDashboard},{label:"Customers",icon:Users},{label:"Churn intelligence",icon:ShieldAlert},{label:"Segments",icon:BriefcaseBusiness},{label:"Cross-sell",icon:ShoppingBag}];
 async function analyse() {
  if(!file)return;setBusy(true);setError("");setNotice("");
  try {if(!file.name.toLowerCase().endsWith(".csv"))throw new Error("Please select a CSV file.");if(file.size>15*1024*1024)throw new Error("File must be smaller than 15 MB.");
   const response=await fetch(API+"/api/analyse",{method:"POST",headers:{"Content-Type":"text/csv"},body:await file.text()});
   const result=await response.json();if(!response.ok)throw new Error(result.detail||"Could not analyse this file.");
   setData(result);setActive("Overview");setNotice("Dataset analysed successfully. Results now reflect your uploaded CSV.");setFile(null);
  } catch(e){setError(e instanceof Error?e.message:"Upload failed. Check that the API is running.");} finally{setBusy(false);}
 }
 const uploaded=data.overview.data_mode==="uploaded_csv";
 return <div className="min-h-screen lg:flex">
  <aside className={`fixed inset-y-0 left-0 z-30 flex w-64 flex-col border-r border-slate-200 bg-white px-5 py-6 transition-transform lg:static lg:translate-x-0 ${mobileOpen?"translate-x-0":"-translate-x-full"}`}>
   <div className="flex items-center justify-between"><div className="flex items-center gap-3"><div className="rounded-xl bg-blue-700 p-2 text-white"><Activity size={21}/></div><div><p className="font-bold">IntelliBank</p><p className="text-[11px] text-slate-400">BancABC customer intelligence</p></div></div><button className="lg:hidden" onClick={()=>setMobileOpen(false)}><X size={19}/></button></div>
   <p className="mb-3 mt-10 px-3 text-[10px] font-bold uppercase tracking-[.16em] text-slate-400">Workspace</p>
   <nav className="space-y-1">{nav.map(item=><button key={item.label} onClick={()=>{setActive(item.label);setMobileOpen(false)}} className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-medium ${active===item.label?"bg-blue-50 text-blue-700":"text-slate-500 hover:bg-slate-50"}`}><item.icon size={18}/>{item.label}</button>)}</nav>
   <div className="mt-auto rounded-2xl bg-slate-900 p-4 text-white"><div className="mb-3 flex items-center gap-2 text-blue-300"><CircleHelp size={17}/><span className="text-xs font-semibold">Decision intelligence</span></div><p className="text-sm font-semibold">Turn transactions into decisions.</p><p className="mt-2 text-xs leading-5 text-slate-400">Find risk, understand customer value and recommend relevant next actions.</p></div>
   <div className="mt-5 flex items-center gap-3 border-t border-slate-100 pt-5"><div className="grid h-9 w-9 place-items-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">UZ</div><div><p className="text-sm font-semibold">Project team</p><p className="text-xs text-slate-400">University of Zimbabwe</p></div></div>
  </aside>
  {mobileOpen&&<button aria-label="Close navigation overlay" className="fixed inset-0 z-20 bg-slate-950/30 lg:hidden" onClick={()=>setMobileOpen(false)}/>}
  <main className="min-w-0 flex-1">
   <header className="sticky top-0 z-10 flex h-[76px] items-center justify-between border-b border-slate-200 bg-white/90 px-5 backdrop-blur md:px-8"><div className="flex items-center gap-3"><button className="lg:hidden" onClick={()=>setMobileOpen(true)}><Menu/></button><div><p className="text-xs text-slate-400">Workspace / {active}</p><h1 className="text-lg font-bold">{active}</h1></div></div><div className="flex items-center gap-2"><span className={`rounded-full px-3 py-1.5 text-[11px] font-semibold ${uploaded?"bg-emerald-50 text-emerald-700":"bg-amber-50 text-amber-700"}`}>{uploaded?"UPLOADED DATA":"DEMO DATA"}</span><button onClick={()=>fetch(API+"/api/analysis").then(r=>r.json()).then(setData)} className="rounded-xl border border-slate-200 p-2 text-slate-500" title="Refresh"><RefreshCw size={17}/></button></div></header>
   <div className="mx-auto max-w-[1440px] space-y-6 p-5 md:p-8">
    <section className="flex flex-col justify-between gap-4 md:flex-row md:items-end"><div><p className="text-sm font-medium text-blue-700">BancABC Universities Hackathon 2026</p><h2 className="mt-1 text-2xl font-bold tracking-tight md:text-3xl">Customer intelligence at a glance</h2><p className="mt-2 text-sm text-slate-500">Identify customer risk, value and actionable growth opportunities.</p></div><button onClick={()=>downloadCsv(data.customers)} className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-800"><Download size={16}/> Export customer report</button></section>
    {(notice||error)&&<div className={`flex items-start gap-2 rounded-xl border px-4 py-3 text-sm ${error?"border-rose-200 bg-rose-50 text-rose-800":"border-emerald-200 bg-emerald-50 text-emerald-800"}`}>{error?<AlertTriangle size={17}/>:<CheckCircle2 size={17}/>}<span>{error||notice}</span></div>}
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div className="flex items-start gap-3"><div className="rounded-xl bg-blue-50 p-3 text-blue-700"><FileSpreadsheet size={22}/></div><div><h3 className="font-bold">Upload transaction dataset</h3><p className="mt-1 max-w-2xl text-xs leading-5 text-slate-500">Upload a UTF-8 CSV containing a customer identifier. Transaction date and amount columns improve recency and value analysis. Files are processed in the running API process and are not saved to the repository.</p></div></div><div className="flex flex-col gap-2 sm:flex-row"><button onClick={downloadSampleCsv} className="rounded-xl border border-slate-300 px-3 py-2.5 text-xs font-semibold text-slate-600 hover:bg-slate-50">Download sample CSV</button><label className="flex cursor-pointer items-center justify-center gap-2 rounded-xl border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"><UploadCloud size={17}/>{file?file.name:"Choose CSV"}<input type="file" accept=".csv,text/csv" className="hidden" onChange={e=>{setFile(e.target.files?.[0]||null);setError("");}}/></label><button disabled={!file||busy} onClick={analyse} className="inline-flex items-center justify-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40">{busy?<Loader2 size={16} className="animate-spin"/>:<Activity size={16}/>}Analyse dataset</button></div></div>
     {data.profile&&<div className="mt-4 grid gap-3 border-t border-slate-100 pt-4 sm:grid-cols-2 lg:grid-cols-4"><div><p className="text-xs text-slate-400">Rows processed</p><p className="font-semibold">{data.profile.rows.toLocaleString()}</p></div><div><p className="text-xs text-slate-400">Columns detected</p><p className="font-semibold">{data.profile.columns.length}</p></div><div><p className="text-xs text-slate-400">Duplicate customer IDs</p><p className="font-semibold">{data.profile.duplicate_customer_ids}</p></div><div><p className="text-xs text-slate-400">Detected fields</p><p className="text-xs font-medium">{Object.entries(data.profile.detected_fields).filter(([,v])=>v).map(([k,v])=>k+": "+v).join(" · ")||"Customer identifier only"}</p></div></div>}
    </section>
    <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-xs leading-5 text-amber-900"><strong>Methodology:</strong> {data.mode_note} Behavioural risk is not a confirmed probability of churn. Supervised prediction requires approved churn labels and a defined prediction window.</div>
    {active==="Overview"&&<><section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><Metric label="Customers analysed" value={data.overview.customers_analysed.toLocaleString()} sub="Unique customer identifiers" icon={Users}/><Metric label="High behavioural risk" value={data.overview.high_churn_risk.toLocaleString()} sub="Relative risk ranking, not probability" icon={ShieldAlert}/><Metric label="High-value customers" value={data.overview.high_value_customers.toLocaleString()} sub="RFM-style behavioural segment" icon={WalletCards}/><Metric label="Growth opportunities" value={data.overview.cross_sell_leads.toLocaleString()} sub="Customers outside the at-risk group" icon={CreditCard}/></section>
    <section className="grid gap-5 xl:grid-cols-[1.3fr_1fr]"><div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><h3 className="font-bold">Customer segment distribution</h3><p className="mt-1 text-xs text-slate-400">Calculated from current dataset</p><div className="mt-5 h-[260px]"><ResponsiveContainer width="100%" height="100%"><BarChart data={data.segments} layout="vertical" margin={{left:8,right:12}}><CartesianGrid stroke="#eef1f6" horizontal={false}/><XAxis type="number" axisLine={false} tickLine={false}/><YAxis type="category" dataKey="name" width={95} axisLine={false} tickLine={false} tick={{fontSize:11}}/><Tooltip/><Bar dataKey="customers" fill="#2469d5" radius={[0,6,6,0]}/></BarChart></ResponsiveContainer></div></div>
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><h3 className="font-bold">Management insights</h3><p className="mt-1 text-xs text-slate-400">Automatically generated from the analysis</p><ul className="mt-4 space-y-3">{data.insights.map((v,i)=><li key={i} className="flex gap-2 text-sm leading-6 text-slate-600"><ArrowUpRight size={16} className="mt-1 shrink-0 text-blue-600"/>{v}</li>)}</ul></div></section></>}
    {(active==="Customers"||active==="Churn intelligence")&&<section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center"><div><h3 className="font-bold">{active==="Customers"?"Customer explorer":"Behavioural risk watchlist"}</h3><p className="mt-1 text-xs text-slate-400">Ranked customer records with evidence and recommended action</p></div><div className="relative"><Search className="absolute left-3 top-2.5 text-slate-400" size={16}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search ID, segment or risk..." className="w-full rounded-xl border border-slate-200 py-2 pl-9 pr-3 text-sm outline-none sm:w-72"/></div></div><div className="mt-5 overflow-x-auto"><table className="w-full min-w-[850px] text-left text-sm"><thead><tr className="border-b text-xs text-slate-400"><th className="pb-3">Customer</th><th className="pb-3">Segment</th><th className="pb-3">Risk score</th><th className="pb-3">Activity</th><th className="pb-3">Evidence</th><th className="pb-3">Next action</th></tr></thead><tbody>{filtered.map(c=><tr key={c.id} className="border-b border-slate-50 align-top"><td className="py-4 font-semibold">{c.id}</td><td className="py-4">{c.segment}</td><td className="py-4"><span className={`rounded-full px-2 py-1 text-xs font-semibold ${c.churn_risk==="High"?"bg-rose-50 text-rose-700":c.churn_risk==="Medium"?"bg-amber-50 text-amber-700":"bg-emerald-50 text-emerald-700"}`}>{c.churn_risk} · {c.risk_score}/100</span></td><td className="py-4">{c.days_since_activity===null?"Date unavailable":c.days_since_activity+" days ago"}<p className="text-xs text-slate-400">{c.transactions} transactions</p></td><td className="max-w-xs py-4 text-xs leading-5 text-slate-500">{c.reason}</td><td className="max-w-xs py-4 text-xs leading-5 font-medium text-blue-800">{c.action}</td></tr>)}</tbody></table>{filtered.length===0&&<p className="py-8 text-center text-sm text-slate-400">No matching customers.</p>}</div></section>}
    {active==="Segments"&&<section className="grid gap-4 md:grid-cols-2">{data.segments.map(s=><div key={s.name} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-sm text-slate-500">{s.name}</p><p className="mt-2 text-3xl font-bold">{s.customers.toLocaleString()}</p><p className="mt-2 text-xs text-slate-400">Customers assigned to this behavioural segment</p></div>)}</section>}
    {active==="Cross-sell"&&<section className="grid gap-4 md:grid-cols-2">{data.recommendations.map((r,i)=><div key={i} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-center justify-between"><span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">{r.segment}</span><span className={`text-xs font-semibold ${r.priority==="High"?"text-rose-600":"text-amber-600"}`}>{r.priority} priority</span></div><h3 className="mt-4 text-lg font-bold">{r.opportunity}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{r.rationale}</p><p className="mt-4 text-xs text-slate-400">{r.customers??"—"} customers in segment</p></div>)}</section>}
    <footer className="flex flex-col justify-between gap-2 pb-4 text-xs text-slate-400 sm:flex-row"><span>IntelliBank · BancABC Universities Hackathon 2026</span><span>{uploaded?"Uploaded CSV analysis · behavioural heuristics":"Synthetic demonstration · not actual bank data"}</span></footer>
   </div>
  </main>
 </div>;
}
