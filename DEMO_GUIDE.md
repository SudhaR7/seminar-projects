# 🎤 Seminar Demo Guide — "From Zero to AI: 12 Projects"

## ⚡ NO-INSTALL MODE (use this tomorrow)

Open this start page in Chrome, signed in to Claude: **https://claude.ai/artifact/3a2XEKCyxbrMFuAEV4btMh**
Every project card has an **▶ Open live demo** button. Nothing to install. AI projects (8, 10, 11) run on your Claude account, no Gemini key needed. The first time, click **Allow** when it asks to use Claude.

Each Python project page has 3 tabs: **Live demo** · **Python output** (real results) · **Python source**. Show the demo first, then flip to the source tab: "idhu thaan andha Python code."

In the live versions, P10 JARVIS uses page tools (calculator, course database, tasks, timer, colour change) instead of internet tools, and P12 SkyCast shows simulated data inside Claude (the badge says DEMO DATA). Open `docs/p12.html` from GitHub Pages for real live weather.

The links are private to you. To let students open them, use **Share** on each page.

The setup below is only needed if you want to run the original code locally.

---

Open **START_HERE.html** first — it's your opening slide and the menu for all 12 projects.

---

## 🛠️ TONIGHT — Setup checklist (do it before sleeping!)

| Install | Why | Check command |
|---|---|---|
| Python 3.10+ | Projects 4–11 | `python --version` |
| Node.js 18+ | Project 3 (MERN) | `node -v` |
| MongoDB Community **or** free MongoDB Atlas URL | Project 3 database | — |
| VS Code + "Live Server" extension | Projects 1, 2, 12 | — |
| Free Gemini API key → https://aistudio.google.com/apikey | Projects 8, 10, 11 | — |

```bash
# Python libraries (one time)
pip install pandas numpy matplotlib seaborn scipy scikit-learn streamlit openpyxl pillow google-genai

# Set the Gemini key (Windows CMD)
set GEMINI_API_KEY=paste_your_key_here
# (PowerShell)   $env:GEMINI_API_KEY="paste_your_key_here"
# (Mac/Linux)    export GEMINI_API_KEY=paste_your_key_here

# MERN — one time
cd p03_mern_expense/server && npm install && copy .env.example .env
cd ../client && npm install
```

> If Gemini says "model not found", check the current model name in AI Studio and run `set GEMINI_MODEL=<that-name>`.

**⚠️ Run EVERY project once tonight.** Keep a mobile hotspot ready — AI projects (8, 10, 11) and Project 12 need internet. Projects 1–7 and 9 work fully offline.

**Backup plan:** run Projects 5, 7, 9 tonight and keep the output images (`student_dashboard.png`, `sales_dashboard.png`, certificates) + run Project 11 once and keep `report.html`. If Wi-Fi fails, show these.

---

## ⏱️ 90-minute Timeline

| Time | Segment | What you show |
|---|---|---|
| 0–8 min | **Opening hook** | START_HERE.html — "What is a project? Why important?" |
| 8–28 min | **Web journey** | P1 → P2 (the big JS reveal) → P3 MERN |
| 28–50 min | **Python & Data** | P4 → P5 → P7 → P6 |
| 50–80 min | **AI Era** | P9 → P12 → P8 → P10 → P11 (grand finale) |
| 80–90 min | **Close + call to action** | Roadmap + "join the class" |

---

## 🎬 Opening (0–8 min)

**Hook line (Tanglish):**
> "Ungala yaarukkachum oru company-la interview-la *'Neenga enna build pannirukkeenga?'* nu kettaanga-na… enna solluveenga? Marks illa, certificate illa — **project** thaan answer. Inniku 90 nimishathula, oru simple web page-la start panni, thaniya yosichu velai seyyura AI agents varaikkum — 12 real projects live-a paakka porom."

**What is a project?** A real, working solution to a real problem, built with code.
**Why important?** Recruiters hire proof, not promises · GitHub = new resume · building > memorising · freelancing & startup ideas.

**Which technology for which project:**

| # | Project | Technology | Career role |
|---|---|---|---|
| 1 | TechVerse landing page | HTML, CSS | UI / Web Designer |
| 2 | TechVerse + JS | JavaScript, DOM, localStorage | Frontend Developer |
| 3 | SpendSmart | MongoDB, Express, React, Node | Full Stack Developer |
| 4 | Password Guardian | Core Python | Python Developer |
| 5 | Student Success Science | Pandas, NumPy, SciPy, K-Means | Data Scientist |
| 6 | PlaceMe AI | scikit-learn, Streamlit | ML Engineer |
| 7 | ShopSense | Pandas, Matplotlib, Excel | Data Analyst |
| 8 | BuddyAI | Gemini LLM API, Streamlit | Gen AI Developer |
| 9 | AutoPilot | Python, Pillow, SMTP | Automation Engineer |
| 10 | JARVIS Mini | LLM + Function calling | AI Engineer |
| 11 | AI Startup Crew | Multi-agent, self-review loop | Agentic AI Engineer |
| 12 | SkyCast | REST APIs, fetch, JSON, Chart.js | Backend / Integration Dev |

---

## 🌐 Level 1 — Web (8–28 min)

### P1 · HTML + CSS (5 min)
Open `p01_html_css/index.html`.
- Hover the cards, flip cards, hover the scrolling strip (it pauses).
- **Say:** "Idhula oru line JavaScript kooda illa. Fully HTML & CSS."
- **Trap moment 🪤:** Go to the form, type rubbish, click Register → *nothing happens*. "Paakka azhaga irukku, aana **moolai illa**."

### P2 · Same page + JavaScript (8 min) — 🔥 BIG REVEAL
Open `p02_html_css_js/index.html` side by side with P1.
1. Click 🌙 → theme changes. Refresh → it **remembers**.
2. Typing effect + live countdown ticking.
3. Scroll → numbers count up.
4. Click a track card → form auto-fills.
5. Submit empty → red errors. Wrong email → error. Correct → 🎉 confetti, seats drop, name added. **Refresh → still there.**
6. Show the comparison table at the bottom.
- **Golden line:** "HTML = Skeleton 🦴, CSS = Beauty 💄, JavaScript = Brain 🧠."

### P3 · MERN (7 min)
Terminal 1: `cd p03_mern_expense/server && npm run dev`
Terminal 2: `cd p03_mern_expense/client && npm run dev` → open http://localhost:5173
- Add 5–6 expenses (Biryani ₹250, Bus pass ₹800, Laptop EMI ₹4500, Course ₹3000…).
- Watch chart & budget bar update; cross 80% → warning.
- **Refresh browser** → data still there (MongoDB!). Open http://localhost:5000/api/expenses to show raw API.
- **Explain M-E-R-N** on a whiteboard: React (what you see) → Express/Node (waiter) → MongoDB (kitchen store room).

---

## 🐍 Level 2 — Python & Data (28–50 min)

### P4 · Password Guardian (4 min)
`python password_guardian.py`
- Ask a student for a "typical password" (e.g. `abc123`, `kumar@123`) → **WEAK, cracked instantly**. Crowd reaction guaranteed 😄
- Option 3 → passphrase → "millions of years 🦕".

### P5 · Data Science (6 min)
`python student_success.py` → open `student_dashboard.png`
- **Hook question:** "Instagram paakkaradhunaala marks kurayudha? Proof venuma?"
- Show correlation bars, the **p-value** ("this is scientific proof"), and the AI-discovered personas: Toppers vs Scroll Addicts — ~27 marks gap.

### P7 · Data Analysis (5 min)
`python sales_analysis.py` → open `sales_dashboard.png` + `ShopSense_Report.xlsx`
- "Ivanga boss kekkura question: Diwali-ku enna stock pannanum?"
- Point at the Diwali spike, UPI 52%, weekend effect. Show cleaning: "100 bad rows removed — real data is always messy."
- **Difference:** Data Analyst = *what happened?* · Data Scientist (P5) = *why, and prove it*.

### P6 · Machine Learning (7 min)
`cd p06_ml_placement && streamlit run app.py`
- Move sliders live. Increase backlogs → chance drops; add internship → jumps.
- Show "AI-recommended moves" and the **algorithm battle**.
- **Say:** "Naan rules ezhudhala. 3,000 students data-la irundhu computer **thaanaa kathukittadhu**. Adhu thaan Machine Learning."
- Interactive: call a student, enter their CGPA etc. live (keep it fun, not embarrassing).

---

## 🤖 Level 3 — AI Era (50–80 min)

### P9 · Automation (5 min)
`python autopilot.py` → **A** → 50 certificates in ~5 sec. Open the folder + `ALL_CERTIFICATES.pdf`.
- "Idhu manually Canva-la panna 2–3 mani neram. Python-ku 5 second."
- **B** → messy folder organised instantly.
- Tip: put the real attendee names in `attendees.csv` before the seminar → give them their certificates! 🤯

### P12 · API Project (4 min)
Open `p12_api_weather/index.html` → search Madurai, London, Tokyo.
- Background changes with weather. Show AQI.
- Open "Behind the scenes" → show the URL & raw JSON. "API = restaurant waiter. You order (request), he brings food (JSON)."

### P8 · Gen AI Chatbot (6 min)
`cd p08_genai_chatbot && streamlit run app.py`
- Career Mentor: "I'm a 2nd year ECE student, how to become an AI engineer in 1 year?"
- Switch to 🗣️ Tamil Tutor: "What is an API?" → answers in Tanglish (crowd loves it).
- 🔥 Roast Bot: "I sleep at 3am and study at the last minute" 😂
- Upload a photo (whiteboard / a circuit) → ask about it.
- Explain: LLM, prompt, system instruction (= personality), temperature (= creativity).

### P10 · AI Agent (6 min)
`python jarvis_agent.py`
- "What's the weather in Chennai and Delhi right now? Which one is hotter?"
- "Convert 250 dollars to rupees and tell me how many 1500-rupee pizzas I can buy."
- Point at the yellow **🔧 tool** lines: "Paarunga — adhuve yosichu, endha tool use pannanum nu **decide** pannudhu."
- **Chatbot vs Agent:** Chatbot = brain that talks 🗣️ · Agent = brain + hands 🦾.

### P11 · Agentic AI — 🏆 GRAND FINALE (8 min)
`python agent_crew.py` → ask the audience for a goal, e.g.
*"Launch a filter-coffee startup for college students in Chennai"*
- Narrate live: Planner breaks it down → Researcher uses Wikipedia → Writer drafts → **Critic gives 6/10 and rejects it** → Writer improves → 8/10 ✅.
- The HTML report opens automatically.
- **Say:** "Oru manager, researcher, writer, reviewer — 4 per oda team velai. Naan oru line type panninen. Idhu thaan **Agentic AI** — 2026-oda biggest skill."

---

## 🎯 Closing (80–90 min) — the "brain wash" 😉

**Story:** "Inniku start pannadhu oru simple HTML page. Mudichadhu thaniya plan panni, research panni, review panni improve pannura AI team. **Rendukkum naduvula irukkuradhu just 12 steps** — andha 12 steps thaan en class."

**Three powerful lines:**
1. "AI unga job-a edukkadhu. **AI use panna theriyira oruthar** thaan unga job-a eduppaanga."
2. "Degree unga door-a open pannum. **Projects thaan unga job-a confirm pannum.**"
3. "Inniku neenga paatha 12 projects-um — class mudiyumbodhu **neengale build pannuveenga.** Unga GitHub-la. Unga name-la."

**Call to action:** show the roadmap (Web → Full Stack → Python → Data → ML → Gen AI → Agents → Agentic AI), share a QR/registration form, and offer the certificate (generated by P9!) to everyone who registers today.

---

## 💡 Pro tips
- Zoom VS Code / terminal font to 150% so the back row can read.
- Keep each project in its own terminal tab, pre-opened.
- Get students involved: their password (P4), their CGPA (P6), their goal (P11), their city (P12).
- Don't explain code line by line — show the **result first**, then 1–2 key lines of code. Wow first, logic second.
