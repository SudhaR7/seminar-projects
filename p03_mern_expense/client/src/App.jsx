// ===== R: React frontend — talks to the Express API =====
import { useEffect, useMemo, useState } from "react";

const CATS = { Food: "🍔", Travel: "🚌", Shopping: "🛍️", Bills: "💡", Education: "📚", Fun: "🎮" };
const COLORS = { Food: "#ff7a59", Travel: "#00d4ff", Shopping: "#ff4fa3", Bills: "#ffd23f", Education: "#7c5cff", Fun: "#2bd67b" };
const BUDGET = 10000;
const rupee = (n) => "₹" + Number(n).toLocaleString("en-IN");

export default function App() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ title: "", amount: "", category: "Food" });
  const [filter, setFilter] = useState("All");
  const [error, setError] = useState("");

  const load = () =>
    fetch("/api/expenses")
      .then((r) => r.json())
      .then(setItems)
      .catch(() => setError("Server not reachable — is `npm run dev` running in /server?"));

  useEffect(() => { load(); }, []);

  const add = async (e) => {
    e.preventDefault();
    if (!form.title.trim() || +form.amount <= 0) return setError("Enter a title and a positive amount");
    setError("");
    const res = await fetch("/api/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, amount: +form.amount }),
    });
    if (!res.ok) return setError((await res.json()).error);
    setForm({ title: "", amount: "", category: form.category });
    load();
  };

  const remove = async (id) => {
    await fetch(`/api/expenses/${id}`, { method: "DELETE" });
    load();
  };

  const total = items.reduce((s, x) => s + x.amount, 0);
  const byCat = useMemo(() => {
    const m = {};
    items.forEach((x) => (m[x.category] = (m[x.category] || 0) + x.amount));
    return Object.entries(m).sort((a, b) => b[1] - a[1]);
  }, [items]);
  const shown = filter === "All" ? items : items.filter((x) => x.category === filter);
  const pct = Math.min(100, (total / BUDGET) * 100);

  return (
    <div className="wrap">
      <header>
        <h1>Spend<span>Smart</span></h1>
        <p>MongoDB · Express · React · Node.js</p>
      </header>

      <div className="kpis">
        <div className="kpi"><small>Total Spent</small><b>{rupee(total)}</b></div>
        <div className="kpi"><small>Transactions</small><b>{items.length}</b></div>
        <div className="kpi"><small>Budget Left</small><b className={total > BUDGET ? "red" : ""}>{rupee(BUDGET - total)}</b></div>
      </div>

      <div className="budget"><i style={{ width: pct + "%", background: pct > 80 ? "#ff4f6d" : undefined }} /></div>
      {pct > 80 && <p className="warn">⚠️ You have used {pct.toFixed(0)}% of your monthly budget!</p>}

      <div className="cols">
        <form className="panel" onSubmit={add}>
          <h3>➕ Add Expense</h3>
          <input placeholder="What did you spend on?" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          <input type="number" placeholder="Amount (₹)" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} />
          <div className="chips">
            {Object.keys(CATS).map((c) => (
              <button type="button" key={c} className={form.category === c ? "chip on" : "chip"} onClick={() => setForm({ ...form, category: c })}>
                {CATS[c]} {c}
              </button>
            ))}
          </div>
          <button className="primary">Save to MongoDB</button>
          {error && <p className="err">{error}</p>}
        </form>

        <div className="panel">
          <h3>📊 Where is my money going?</h3>
          {byCat.length === 0 && <p className="muted">Add an expense to see the chart</p>}
          {byCat.map(([c, v]) => (
            <div className="row" key={c}>
              <span>{CATS[c]} {c}</span>
              <div className="track"><i style={{ width: (v / byCat[0][1]) * 100 + "%", background: COLORS[c] }} /></div>
              <b>{rupee(v)}</b>
            </div>
          ))}
        </div>
      </div>

      <div className="panel">
        <div className="head">
          <h3>🧾 Transactions</h3>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option>All</option>
            {Object.keys(CATS).map((c) => <option key={c}>{c}</option>)}
          </select>
        </div>
        {shown.map((x) => (
          <div className="tx" key={x._id}>
            <span className="ico" style={{ background: COLORS[x.category] + "33" }}>{CATS[x.category]}</span>
            <div><b>{x.title}</b><small>{new Date(x.date).toLocaleDateString("en-IN")} · {x.category}</small></div>
            <b className="amt">{rupee(x.amount)}</b>
            <button className="del" onClick={() => remove(x._id)}>✕</button>
          </div>
        ))}
        {shown.length === 0 && <p className="muted">No transactions yet</p>}
      </div>
    </div>
  );
}
