"""PlaceMe AI — Streamlit web app.  Run:  streamlit run app.py"""
import pandas as pd
import streamlit as st
from model import train, predict, improvement_tips

st.set_page_config(page_title="PlaceMe AI", page_icon="🎯", layout="wide")


@st.cache_resource
def load():
    return train(verbose=False)


clf, reg, results, reg_stats, importance, data = load()

st.markdown("<h1 style='text-align:center'>🎯 PlaceMe <span style='color:#00d4ff'>AI</span></h1>"
            "<p style='text-align:center;color:gray'>Machine Learning predicts your placement chance & salary</p>",
            unsafe_allow_html=True)

with st.sidebar:
    st.header("🎓 Your Profile")
    s = {
        "cgpa": st.slider("CGPA", 5.0, 10.0, 7.2, 0.1),
        "internships": st.slider("Internships", 0, 4, 0),
        "projects": st.slider("Projects", 0, 7, 2),
        "certifications": st.slider("Certifications", 0, 6, 1),
        "aptitude": st.slider("Aptitude score", 20, 100, 60),
        "communication": st.slider("Communication (1-10)", 1, 10, 6),
        "backlogs": st.slider("Backlogs", 0, 3, 1),
        "hackathons": st.slider("Hackathons", 0, 5, 0),
    }

prob, sal = predict(clf, reg, s)
c1, c2, c3 = st.columns(3)
c1.metric("Placement chance", f"{prob:.0%}")
c2.metric("Expected package", f"{sal:.1f} LPA" if prob >= 0.5 else "—")
c3.metric("Model accuracy", f"{max(results.values()):.1%}")
st.progress(float(prob))

if prob >= 0.8:
    st.success("🔥 Excellent! You are placement-ready.")
    st.balloons()
elif prob >= 0.5:
    st.info("👍 Good chance — a few improvements can make you unstoppable.")
else:
    st.warning("⚠️ Risky zone — but the AI shows exactly what to fix 👇")

st.subheader("🚀 AI-recommended moves")
for tip, gain in improvement_tips(clf, reg, s):
    st.write(f"**{tip}** → chance goes up by **+{gain:.0%}**")

l, r = st.columns(2)
with l:
    st.subheader("🔑 What matters most")
    st.bar_chart(importance)
with r:
    st.subheader("⚔️ Algorithm battle")
    st.bar_chart(pd.Series(results))

with st.expander("📂 See the training data"):
    st.dataframe(data.head(200))
