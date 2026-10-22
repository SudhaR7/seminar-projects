"""
PROJECT 7 — ShopSense: Festive Sales Analysis 🛒📈  (Python + Data Analysis)
Business question from the boss:
  "Where is our money coming from? Who buys? When? What should we do next Diwali?"

Pipeline:  Raw data → Clean → Analyse (groupby / pivot) → Visualise → Excel report for managers
Run:  python sales_analysis.py
Outputs: orders.csv, sales_dashboard.png, ShopSense_Report.xlsx
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(2025)

# ---------------- 1. RAW DATA (15,000 orders, Jan–Dec 2025) ----------------
N = 15000
days = pd.date_range("2025-01-01", "2025-12-31")
weights = np.ones(len(days))
weights[(days >= "2025-10-10") & (days <= "2025-10-25")] *= 4.5   # Diwali rush
weights[(days >= "2025-01-10") & (days <= "2025-01-16")] *= 2.5   # Pongal
weights[(days >= "2025-08-20") & (days <= "2025-08-31")] *= 1.8   # Onam / Ganesh Chaturthi
weights[days.weekday >= 5] *= 1.3                                  # weekends
dates = rng.choice(days, N, p=weights / weights.sum())

states = {"Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Trichy"], "Karnataka": ["Bengaluru", "Mysuru"],
          "Maharashtra": ["Mumbai", "Pune"], "Kerala": ["Kochi", "Trivandrum"], "Telangana": ["Hyderabad"],
          "Delhi": ["New Delhi"]}
st = rng.choice(list(states), N, p=[.32, .2, .17, .12, .11, .08])
city = [rng.choice(states[s]) for s in st]
cats = {"Electronics": (8000, 3000), "Fashion": (1500, 600), "Home & Kitchen": (2500, 900),
        "Beauty": (900, 300), "Sweets & Gifts": (1200, 500), "Books": (500, 200)}
cat = rng.choice(list(cats), N, p=[.18, .3, .17, .12, .15, .08])
price = np.array([max(149, rng.normal(*cats[c])) for c in cat]).round(0)
qty = rng.choice([1, 1, 1, 2, 2, 3], N)

orders = pd.DataFrame({
    "order_id": [f"ORD{100000 + i}" for i in range(N)],
    "date": dates, "state": st, "city": city,
    "gender": rng.choice(["Female", "Male"], N, p=[.56, .44]),
    "age_group": rng.choice(["18-25", "26-35", "36-45", "46-60", "60+"], N, p=[.27, .35, .2, .13, .05]),
    "category": cat, "unit_price": price, "qty": qty,
    "payment": rng.choice(["UPI", "Card", "COD", "Net Banking", "EMI"], N, p=[.52, .18, .17, .06, .07]),
    "rating": rng.choice([1, 2, 3, 4, 5, np.nan], N, p=[.03, .05, .15, .37, .3, .1]),
})
# messy real-world issues
orders.loc[rng.choice(N, 40, replace=False), "unit_price"] = -1        # bad entries
orders = pd.concat([orders, orders.sample(60, random_state=1)])        # duplicates
orders.to_csv("orders.csv", index=False)
print(f"📥 Loaded {len(orders):,} raw rows")

# ---------------- 2. CLEANING ----------------
before = len(orders)
orders = orders.drop_duplicates("order_id")
orders = orders[orders.unit_price > 0].copy()
orders["revenue"] = orders.unit_price * orders.qty
orders["month"] = orders.date.dt.month_name().str[:3]
orders["weekday"] = orders.date.dt.day_name()
print(f"🧹 Removed {before - len(orders)} duplicate / invalid rows → {len(orders):,} clean orders")

# ---------------- 3. ANALYSIS ----------------
total = orders.revenue.sum()
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthly = orders.groupby("month").revenue.sum().reindex(months)
by_cat = orders.groupby("category").revenue.sum().sort_values()
by_state = orders.groupby("state").revenue.sum().sort_values()
by_pay = orders.payment.value_counts(normalize=True)
pivot = orders.pivot_table(index="age_group", columns="gender", values="revenue", aggfunc="sum")
top_cities = orders.groupby("city").agg(orders=("order_id", "count"), revenue=("revenue", "sum")).sort_values("revenue", ascending=False).head(5)
diwali = orders[(orders.date >= "2025-10-10") & (orders.date <= "2025-10-25")].revenue.sum()
avg_rating = orders.groupby("category").rating.mean().round(2)

L = lambda x: f"₹{x / 1e5:,.1f} L"
print("\n📊 BUSINESS SNAPSHOT")
print(f"   Total revenue      : {L(total)}")
print(f"   Orders             : {len(orders):,}")
print(f"   Avg order value    : ₹{orders.revenue.mean():,.0f}")
print(f"   Best month         : {monthly.idxmax()} ({L(monthly.max())})")
print(f"   Diwali 16 days     : {L(diwali)} = {diwali / total:.0%} of the whole year!")
print(f"   Top category       : {by_cat.idxmax()}")
print(f"   Top state          : {by_state.idxmax()}")
print(f"   UPI share          : {by_pay['UPI']:.0%} of orders")
print(f"\n🏙️ Top 5 cities:\n{top_cities.assign(revenue=top_cities.revenue.map(L)).to_string()}")

# ---------------- 4. DASHBOARD ----------------
plt.style.use("dark_background")
fig, ax = plt.subplots(2, 3, figsize=(18, 10), facecolor="#0b0b16")
fig.suptitle(f"ShopSense 2025 — Revenue {L(total)} | {len(orders):,} orders", fontsize=20, fontweight="bold", color="#ffd23f")

a = ax[0, 0]
a.plot(months, monthly.values / 1e5, marker="o", color="#00d4ff", lw=3)
a.fill_between(months, monthly.values / 1e5, alpha=.2, color="#00d4ff")
a.annotate("Diwali spike", xy=(9, monthly["Oct"] / 1e5), xytext=(4.5, monthly["Oct"] / 1e5 * .95),
           arrowprops=dict(arrowstyle="->", color="#ffd23f"), color="#ffd23f", fontsize=12)
a.set_title("Monthly revenue (₹ Lakhs)")

a = ax[0, 1]
a.barh(by_cat.index, by_cat.values / 1e5, color="#7c5cff")
a.set_title("Revenue by category (₹ L)")

a = ax[0, 2]
a.pie(by_pay.values, labels=by_pay.index, autopct="%1.0f%%", colors=["#2bd67b", "#00d4ff", "#ff4fa3", "#ffd23f", "#7c5cff"],
      wedgeprops=dict(width=.45), textprops={"color": "white"})
a.set_title("Payment mode")

a = ax[1, 0]
a.barh(by_state.index, by_state.values / 1e5, color="#ff4fa3")
a.set_title("Revenue by state (₹ L)")

a = ax[1, 1]
(pivot / 1e5).plot.bar(ax=a, color=["#ff4fa3", "#00d4ff"], rot=0)
a.set_title("Who buys? Age × Gender (₹ L)")

a = ax[1, 2]
wd = orders.groupby("weekday").revenue.sum().reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
a.bar([d[:3] for d in wd.index], wd.values / 1e5, color=["#555"] * 5 + ["#2bd67b"] * 2)
a.set_title("Weekend effect (₹ L)")

plt.tight_layout(rect=[0, 0, 1, .94])
plt.savefig("sales_dashboard.png", dpi=110, facecolor=fig.get_facecolor())

# ---------------- 5. EXCEL REPORT FOR MANAGERS ----------------
with pd.ExcelWriter("ShopSense_Report.xlsx") as xl:
    pd.DataFrame({"Metric": ["Total revenue", "Orders", "Avg order value", "Best month", "Diwali share", "UPI share"],
                  "Value": [round(total), len(orders), round(orders.revenue.mean()), monthly.idxmax(),
                            f"{diwali / total:.0%}", f"{by_pay['UPI']:.0%}"]}).to_excel(xl, sheet_name="Summary", index=False)
    monthly.rename("revenue").to_excel(xl, sheet_name="Monthly")
    by_cat.rename("revenue").sort_values(ascending=False).to_frame().join(avg_rating.rename("avg_rating")).to_excel(xl, sheet_name="Category")
    top_cities.to_excel(xl, sheet_name="Top Cities")
    pivot.round(0).to_excel(xl, sheet_name="Age x Gender")
print("\n💾 Saved: sales_dashboard.png, ShopSense_Report.xlsx")

print("\n💡 RECOMMENDATIONS FOR NEXT DIWALI")
print(f"   1. Stock up {by_cat.idxmax()} — it drives {by_cat.max() / total:.0%} of revenue")
print(f"   2. Run UPI cashback offers — {by_pay['UPI']:.0%} of customers already pay by UPI")
print(f"   3. Focus ads on {by_state.idxmax()} and age group {orders.groupby('age_group').revenue.sum().idxmax()}")
print("   4. Push weekend flash sales — weekends earn more per day")
