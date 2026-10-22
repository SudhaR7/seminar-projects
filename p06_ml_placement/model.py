"""
PROJECT 6 — PlaceMe AI 🎯  (Python + Machine Learning)
Predicts: 1) Will this student get PLACED?  (Classification - Random Forest)
          2) Expected SALARY package        (Regression - Gradient Boosting)

Run training + CLI demo:  python model.py
Run web app:              streamlit run app.py
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split

FEATURES = ["cgpa", "internships", "projects", "certifications", "aptitude", "communication", "backlogs", "hackathons"]


def make_data(n=3000, seed=7):
    """Realistic simulated campus placement dataset."""
    r = np.random.default_rng(seed)
    d = pd.DataFrame({
        "cgpa": r.normal(7.4, 1.0, n).clip(5, 10).round(2),
        "internships": r.poisson(0.9, n).clip(0, 4),
        "projects": r.poisson(2, n).clip(0, 7),
        "certifications": r.poisson(1.5, n).clip(0, 6),
        "aptitude": r.normal(65, 15, n).clip(20, 100).round(0),
        "communication": r.integers(1, 11, n),
        "backlogs": r.choice([0, 0, 0, 0, 1, 2, 3], n),
        "hackathons": r.poisson(0.6, n).clip(0, 5),
    })
    score = (1.3 * (d.cgpa - 7) + 0.9 * d.internships + 0.45 * d.projects + 0.25 * d.certifications
             + 0.05 * (d.aptitude - 60) + 0.3 * (d.communication - 5) - 0.9 * d.backlogs + 0.4 * d.hackathons
             + r.normal(0, 1, n))
    d["placed"] = (score > 1.3).astype(int)
    salary = (3 + 0.9 * (d.cgpa - 6) + 1.1 * d.internships + 0.35 * d.projects + 0.6 * d.hackathons
              + 0.04 * (d.aptitude - 50) + 0.2 * d.communication + r.normal(0, 0.8, n)).clip(2.8, 30)
    d["salary_lpa"] = np.where(d.placed == 1, salary.round(2), 0)
    return d


def train(verbose=True):
    d = make_data()
    X, y = d[FEATURES], d.placed
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

    # Compare 3 algorithms — classic ML demo
    results = {}
    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=1),
        "Random Forest": RandomForestClassifier(n_estimators=300, random_state=1),
    }
    for name, m in models.items():
        m.fit(Xtr, ytr)
        results[name] = accuracy_score(yte, m.predict(Xte))
    best_name = max(results, key=results.get)   # automatically pick the winner
    clf = models[best_name]

    placed = d[d.placed == 1]
    Xs_tr, Xs_te, ys_tr, ys_te = train_test_split(placed[FEATURES], placed.salary_lpa, test_size=0.2, random_state=1)
    reg = GradientBoostingRegressor(random_state=1).fit(Xs_tr, ys_tr)
    pred = reg.predict(Xs_te)
    reg_stats = {"r2": r2_score(ys_te, pred), "mae": mean_absolute_error(ys_te, pred)}

    importance = pd.Series(models["Random Forest"].feature_importances_, index=FEATURES).sort_values(ascending=False)
    if verbose:
        print(f"\n📚 Trained on {len(d):,} students  |  Placement rate: {d.placed.mean():.0%}")
        print("\n⚔️  Algorithm battle (accuracy on unseen students):")
        for k, v in results.items():
            print(f"   {k:20s} {'█' * int(v * 30)} {v:.1%}" + ("  🏆 winner" if k == best_name else ""))
        print(f"\n💰 Salary model: R² = {reg_stats['r2']:.2f}, average error = ±{reg_stats['mae']:.2f} LPA")
        print("\n🔑 What matters most for placement:")
        for k, v in importance.items():
            print(f"   {k:15s} {'▇' * int(v * 60)} {v:.0%}")
    return clf, reg, results, reg_stats, importance, d


def predict(clf, reg, student: dict):
    x = pd.DataFrame([student])[FEATURES]
    prob = clf.predict_proba(x)[0][1]
    salary = float(reg.predict(x)[0])
    return prob, salary


def improvement_tips(clf, reg, student):
    """Try small realistic improvements and show how much the chance increases."""
    base, _ = predict(clf, reg, student)
    tries = {
        "Do 1 more internship": ("internships", 1),
        "Build 2 more projects": ("projects", 2),
        "Join a hackathon": ("hackathons", 1),
        "Raise CGPA by 0.5": ("cgpa", 0.5),
        "Improve aptitude by 10": ("aptitude", 10),
        "Clear 1 backlog": ("backlogs", -1),
    }
    out = []
    for tip, (k, delta) in tries.items():
        s = dict(student)
        s[k] = max(0, s[k] + delta)
        if s == student:
            continue
        p, _ = predict(clf, reg, s)
        out.append((tip, p - base))
    return sorted(out, key=lambda t: -t[1])[:3]


if __name__ == "__main__":
    clf, reg, *_ = train()
    print("\n🎓 Enter student details (press Enter for sample values)")
    sample = {"cgpa": 7.2, "internships": 0, "projects": 2, "certifications": 1, "aptitude": 60,
              "communication": 6, "backlogs": 1, "hackathons": 0}
    s = {}
    for k, v in sample.items():
        val = input(f"   {k} [{v}]: ").strip()
        try:
            s[k] = float(val) if val else v
        except ValueError:
            s[k] = v
    prob, sal = predict(clf, reg, s)
    print(f"\n🎯 Placement chance: {prob:.0%}")
    print(f"💰 Expected package: {sal:.1f} LPA" if prob >= 0.5 else "💰 Package: improve your chances first!")
    print("\n🚀 Smartest moves to boost your chance:")
    for tip, gain in improvement_tips(clf, reg, s):
        print(f"   • {tip}: +{gain:.0%}")
