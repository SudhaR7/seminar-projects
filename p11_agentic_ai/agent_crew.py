"""
PROJECT 11 — AI Startup Crew 🚀  (Agentic AI = a TEAM of AI agents working together)

You give ONE goal. A crew of 4 AI agents plans, researches, writes, reviews and IMPROVES —
with no human in between:

   🧭 Planner    → breaks the goal into tasks
   🔎 Researcher → works on each task (uses a Wikipedia tool for facts)
   ✍️ Writer     → turns the research into a polished report
   🧐 Critic     → scores the report /10 and sends it back if it's not good enough
                   (the Writer revises until score ≥ 8 — self-improvement loop!)

Output: a beautiful report.html that opens automatically.

Try goals like:
  "Launch a filter-coffee startup for college students in Chennai"
  "A 30-day plan for a 2nd-year student to become an AI engineer"
  "Start a YouTube channel teaching Python in Tamil"

Setup:  pip install -r requirements.txt     set GEMINI_API_KEY=your_key
Run:    python agent_crew.py
"""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
import webbrowser
from google import genai
from google.genai import types

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
COL = {"Planner": "\033[95m", "Researcher": "\033[96m", "Writer": "\033[92m", "Critic": "\033[93m"}
END = "\033[0m"
os.system("")  # enables colours on Windows terminals

client = None


def wikipedia(topic: str) -> dict:
    """Get a short factual summary about a topic, company, technology or place from Wikipedia."""
    print(f"      {COL['Researcher']}🔧 tool: wikipedia({topic!r}){END}")
    try:
        req = urllib.request.Request("https://en.wikipedia.org/api/rest_v1/page/summary/"
                                     + urllib.parse.quote(topic.replace(" ", "_")), headers={"User-Agent": "AgentCrew/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return {"summary": json.loads(r.read()).get("extract", "")}
    except Exception:
        return {"summary": "not found"}


def agent(name, role, prompt, json_mode=False, tools=None):
    """One agent = one role (system instruction) + one job."""
    print(f"{COL[name]}▶ {name} is working...{END}")
    cfg = types.GenerateContentConfig(system_instruction=role, temperature=0.7, tools=tools,
                                      response_mime_type="application/json" if json_mode else None)
    for attempt in range(3):
        try:
            text = client.models.generate_content(model=MODEL, contents=prompt, config=cfg).text
            return json.loads(text) if json_mode else text
        except Exception as e:
            print(f"   retrying ({e.__class__.__name__})...")
            time.sleep(3)
    raise RuntimeError(f"{name} failed")


PLANNER = "You are a sharp project planner. Break goals into 4-5 concrete, research-able tasks."
RESEARCHER = ("You are a diligent researcher focused on India. Use the wikipedia tool when a fact would help. "
              "Give specific numbers, costs in ₹, tools, names and examples. Max 180 words.")
WRITER = ("You are an expert writer. Write a clear, exciting, well-structured Markdown report with ## headings, "
          "bullet points, a table where useful, and a final '## Action Plan' with numbered steps.")
CRITIC = "You are a tough reviewer. Judge reports on accuracy, specificity, practicality and clarity."


def run(goal):
    t0 = time.time()
    plan = agent("Planner", PLANNER,
                 f'Goal: {goal}\nReturn JSON: {{"title": str, "tasks": [{{"task": str, "why": str}}]}}', json_mode=True)
    print(f"   📋 {plan['title']}")
    for i, t in enumerate(plan["tasks"], 1):
        print(f"      {i}. {t['task']}")

    notes = []
    for t in plan["tasks"]:
        print(f"   🔎 {t['task']}")
        notes.append(f"### {t['task']}\n" + agent("Researcher", RESEARCHER, f"Goal: {goal}\nTask: {t['task']}", tools=[wikipedia]))

    research = "\n\n".join(notes)
    report = agent("Writer", WRITER, f"Goal: {goal}\nTitle: {plan['title']}\n\nResearch notes:\n{research}")

    history = []
    for round_no in range(1, 4):
        review = agent("Critic", CRITIC,
                       f"Goal: {goal}\n\nReport:\n{report}\n\nReturn JSON: "
                       '{"score": int 1-10, "strengths": [str], "fixes": [str]}', json_mode=True)
        history.append(review)
        print(f"   🧐 Round {round_no}: score {review['score']}/10")
        for f in review.get("fixes", [])[:3]:
            print(f"      ✏️ {f}")
        if review["score"] >= 8:
            print("   ✅ Critic approved!")
            break
        report = agent("Writer", WRITER,
                       f"Improve this report using the reviewer's fixes.\nFixes: {review['fixes']}\n\nReport:\n{report}")

    save(plan["title"], goal, report, history, time.time() - t0)


def md_to_html(md):
    """Tiny Markdown → HTML converter (headings, bullets, numbered lists, tables, bold)."""
    out, in_table = [], False
    for line in md.splitlines():
        s = html.escape(line.strip())
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        if s.startswith("|"):
            if re.match(r"^\|[\s\-:|]+\|$", s):
                continue
            cells = "".join(f"<td>{c.strip()}</td>" for c in s.strip("|").split("|"))
            out.append(("<table>" if not in_table else "") + f"<tr>{cells}</tr>")
            in_table = True
            continue
        if in_table:
            out.append("</table>")
            in_table = False
        if s.startswith("### "): out.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("## "): out.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("# "): out.append(f"<h1>{s[2:]}</h1>")
        elif re.match(r"^[-*] ", s): out.append(f"<li>{s[2:]}</li>")
        elif re.match(r"^\d+\. ", s): out.append(f"<li class='num'>{s}</li>")
        elif s: out.append(f"<p>{s}</p>")
    if in_table:
        out.append("</table>")
    return "\n".join(out)


def save(title, goal, report, reviews, secs):
    scores = " → ".join(str(r["score"]) for r in reviews)
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body{{font-family:Segoe UI,system-ui,sans-serif;background:#07070f;color:#e9ebff;max-width:900px;margin:auto;padding:40px 20px;line-height:1.7}}
h1{{font-size:2.4rem;background:linear-gradient(90deg,#7c5cff,#00d4ff);-webkit-background-clip:text;color:transparent}}
h2{{color:#00d4ff;border-bottom:1px solid #2a2a44;padding-bottom:6px;margin-top:36px}} h3{{color:#ff4fa3}}
li{{margin:6px 0 6px 20px}} li.num{{list-style:none;margin-left:0}} b{{color:#ffd23f}}
table{{border-collapse:collapse;width:100%;margin:16px 0}} td{{border:1px solid #2a2a44;padding:8px 12px}} tr:first-child td{{background:#1a1a33;font-weight:600}}
.meta{{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}} .meta span{{background:#15152a;border:1px solid #2a2a44;padding:8px 14px;border-radius:99px;font-size:.9rem}}
</style></head><body>
<h1>{html.escape(title)}</h1>
<div class="meta"><span>🎯 {html.escape(goal)}</span><span>🤖 4 AI agents</span><span>🧐 Critic scores: {scores}</span><span>⏱️ {secs:.0f} sec</span></div>
{md_to_html(report)}
</body></html>"""
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(page)
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n🎉 Done in {secs:.0f}s → report.html")
    webbrowser.open("file://" + os.path.abspath("report.html"))


if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY first (free key: https://aistudio.google.com/apikey)")
    client = genai.Client(api_key=key)
    print("\n🚀 AI STARTUP CREW — Planner · Researcher · Writer · Critic\n")
    goal = input("🎯 Give the crew a goal: ").strip() or "Launch a filter-coffee startup for college students in Chennai"
    run(goal)
