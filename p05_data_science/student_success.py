"""
PROJECT 5 — Student Success Science 🎓📊  (Advanced Python + Data Science)
Question: "What REALLY decides a student's marks?" — study hours? sleep? Instagram? attendance?

Steps a Data Scientist follows:
  1. Collect data   -> 1,200 students (realistic simulated dataset, saved as CSV)
  2. Clean & explore -> statistics, missing values
  3. Find patterns  -> correlation heatmap
  4. Prove it       -> hypothesis test (t-test)
  5. Discover groups -> K-Means clustering finds student "personas" automatically
  6. Tell the story -> one dashboard image + insights

Run:  python student_success.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)

# ---------------- 1. COLLECT DATA ----------------
N = 1200
study = rng.gamma(3, 1.2, N).clip(0, 10)
sleep = rng.normal(6.8, 1.1, N).clip(3.5, 10)
social = rng.gamma(2.2, 1.3, N).clip(0, 10)
attendance = rng.normal(80, 12, N).clip(35, 100)
exercise = rng.choice([0, 1], N, p=[0.6, 0.4])
part_time = rng.choice([0, 1], N, p=[0.8, 0.2])
marks = (30 + 5.2 * study + 2.5 * (sleep - 4.5) - 2.8 * social + 0.25 * attendance
         + 3 * exercise - 4 * part_time - 0.9 * np.abs(sleep - 7.5) ** 2 + rng.normal(0, 6, N)).clip(0, 100)

df = pd.DataFrame({
    "study_hours": study.round(1), "sleep_hours": sleep.round(1), "social_media_hours": social.round(1),
    "attendance_pct": attendance.round(0), "exercise": exercise, "part_time_job": part_time, "marks": marks.round(0),
})
# add a few missing values like real data
df.loc[rng.choice(N, 25, replace=False), "sleep_hours"] = np.nan
df.to_csv("students.csv", index=False)

# ---------------- 2. CLEAN & EXPLORE ----------------
print("\n🔍 Missing values before cleaning:\n", df.isna().sum()[df.isna().sum() > 0].to_string())
df["sleep_hours"] = df["sleep_hours"].fillna(df["sleep_hours"].median())
print("\n📋 Quick statistics:\n", df.describe().round(1).T[["mean", "min", "max"]].to_string())

# ---------------- 3. PATTERNS ----------------
corr = df.corr()["marks"].drop("marks").sort_values()
print("\n🔗 What affects marks (correlation, -1 to +1):")
for k, v in corr.items():
    bar = ("🟩" if v > 0 else "🟥") * int(abs(v) * 20)
    print(f"   {k:20s} {v:+.2f} {bar}")

# ---------------- 4. HYPOTHESIS TEST ----------------
heavy = df[df.social_media_hours >= 4].marks
light = df[df.social_media_hours < 2].marks
t, p = stats.ttest_ind(light, heavy, equal_var=False)
print(f"\n🧪 Hypothesis test: Do heavy social-media users (4h+) score lower?")
print(f"   Light users avg: {light.mean():.1f} | Heavy users avg: {heavy.mean():.1f} | p-value = {p:.2e}")
print("   ✅ Statistically PROVEN difference (p < 0.05)" if p < 0.05 else "   ❌ No significant difference")

# ---------------- 5. K-MEANS PERSONAS ----------------
features = ["study_hours", "sleep_hours", "social_media_hours", "attendance_pct"]
X = StandardScaler().fit_transform(df[features])
df["cluster"] = KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X)
profile = df.groupby("cluster")[features + ["marks"]].mean()

def name_persona(row):
    if row.marks == profile.marks.max(): return "Focused Toppers"
    if row.social_media_hours == profile.social_media_hours.max(): return "Scroll Addicts"
    if row.attendance_pct == profile.attendance_pct.min(): return "Class Skippers"
    return "Balanced Average"

names = {c: name_persona(r) for c, r in profile.iterrows()}
df["persona"] = df.cluster.map(names)
print("\n🤖 AI found these student personas automatically (K-Means):")
print(df.groupby("persona")[features + ["marks"]].mean().round(1).assign(students=df.persona.value_counts()).to_string())

# ---------------- 6. DASHBOARD ----------------
plt.style.use("dark_background")
fig = plt.figure(figsize=(16, 10), facecolor="#0b0b16")
fig.suptitle("Student Success Science — What decides your marks?", fontsize=20, fontweight="bold", color="#00d4ff")
gs = fig.add_gridspec(2, 3, hspace=.55, wspace=.5)

ax = fig.add_subplot(gs[0, 0])
sns.heatmap(df[features + ["marks"]].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax, cbar=False)
ax.set_title("Correlation Heatmap")

ax = fig.add_subplot(gs[0, 1])
sns.regplot(data=df, x="study_hours", y="marks", ax=ax, scatter_kws={"alpha": .3, "s": 10, "color": "#7c5cff"}, line_kws={"color": "#00d4ff"})
ax.set_title("Study hours ↑  →  Marks ↑")

ax = fig.add_subplot(gs[0, 2])
sns.regplot(data=df, x="social_media_hours", y="marks", ax=ax, scatter_kws={"alpha": .3, "s": 10, "color": "#ff4fa3"}, line_kws={"color": "#ffd23f"})
ax.set_title("Social media ↑  →  Marks ↓")

ax = fig.add_subplot(gs[1, 0])
df["sleep_band"] = pd.cut(df.sleep_hours, [0, 5, 6, 7, 8, 12], labels=["<5", "5-6", "6-7", "7-8", "8+"])
df.groupby("sleep_band", observed=True).marks.mean().plot.bar(ax=ax, color="#2bd67b")
ax.set_title("Sleep sweet spot"); ax.set_xlabel("Sleep hours"); ax.set_ylabel("Avg marks"); ax.tick_params(axis="x", rotation=0)

ax = fig.add_subplot(gs[1, 1])
sns.scatterplot(data=df, x="study_hours", y="social_media_hours", hue="persona", s=14, ax=ax, palette="Set2")
ax.set_title("K-Means Student Personas"); ax.legend(fontsize=8, loc="upper right")

ax = fig.add_subplot(gs[1, 2])
df.groupby("persona").marks.mean().sort_values().plot.barh(ax=ax, color=["#ff4fa3", "#ffd23f", "#00d4ff", "#2bd67b"])
ax.set_title("Average marks by persona"); ax.set_ylabel("")

plt.savefig("student_dashboard.png", dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
print("\n💾 Saved: students.csv, student_dashboard.png")

best = df.groupby("sleep_band", observed=True).marks.mean().idxmax()
print("\n💡 KEY INSIGHTS")
print(f"   • Every extra study hour adds ~{np.polyfit(df.study_hours, df.marks, 1)[0]:.1f} marks")
print(f"   • Every extra hour on social media costs ~{-np.polyfit(df.social_media_hours, df.marks, 1)[0]:.1f} marks")
print(f"   • Best sleep range: {best} hours")
print(f"   • Toppers vs Scroll Addicts gap: {profile.marks.max() - profile.loc[profile.social_media_hours.idxmax()].marks:.0f} marks")
