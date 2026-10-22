"""
PROJECT 10 — JARVIS Mini 🦾  (AI Agent = LLM brain + TOOLS + decisions)

A chatbot only TALKS.  An AGENT can THINK → choose a TOOL → ACT → read the result → answer.
Watch the terminal: you'll see exactly which tool JARVIS decides to use, live.

Tools JARVIS can use:
  🌦️ live weather (Open-Meteo API)    💱 live currency rates     🧮 calculator
  📖 Wikipedia lookup                 🕒 current date/time       📝 save notes to a file

Try:
  "What's the weather in Chennai and Bangalore? Which is hotter?"
  "Convert 250 US dollars to rupees and tell me how many 1500-rupee pizzas I can buy"
  "Who is APJ Abdul Kalam? Save a 3-line summary to my notes"

Setup:  pip install -r requirements.txt      set GEMINI_API_KEY=your_key
Run:    python jarvis_agent.py
"""
import json
import math
import os
import urllib.parse
import urllib.request
from datetime import datetime
from google import genai
from google.genai import types

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
os.system("")  # enables colours on Windows terminals
C, Y, G, D, E = "\033[96m", "\033[93m", "\033[92m", "\033[2m", "\033[0m"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "JarvisMini/1.0 (student demo)"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def log(tool, args):
    print(f"{Y}   🔧 JARVIS is using tool → {tool}({', '.join(f'{k}={v!r}' for k, v in args.items())}){E}")


# ------------------------- TOOLS (normal Python functions!) -------------------------
def get_weather(city: str) -> dict:
    """Get the current live weather for a city."""
    log("get_weather", {"city": city})
    geo = _get("https://geocoding-api.open-meteo.com/v1/search?count=1&name=" + urllib.parse.quote(city))
    if not geo.get("results"):
        return {"error": f"City {city} not found"}
    p = geo["results"][0]
    w = _get(f"https://api.open-meteo.com/v1/forecast?latitude={p['latitude']}&longitude={p['longitude']}"
             "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation")
    return {"city": p["name"], "country": p.get("country"), **w["current"]}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert money between currencies using live exchange rates. Use 3-letter codes like USD, INR, EUR."""
    log("convert_currency", {"amount": amount, "from": from_currency, "to": to_currency})
    data = _get(f"https://open.er-api.com/v6/latest/{from_currency.upper()}")
    rate = data["rates"].get(to_currency.upper())
    if rate is None:
        return {"error": "Unknown currency"}
    return {"rate": rate, "result": round(amount * rate, 2), "updated": data.get("time_last_update_utc")}


def calculator(expression: str) -> dict:
    """Evaluate a math expression exactly, e.g. '(250*88.5)/1500' or 'sqrt(144)'."""
    log("calculator", {"expression": expression})
    allowed = {k: getattr(math, k) for k in ["sqrt", "pow", "sin", "cos", "tan", "log", "pi", "e", "floor", "ceil"]}
    try:
        return {"result": eval(expression, {"__builtins__": {}}, allowed)}
    except Exception as ex:
        return {"error": str(ex)}


def wikipedia(topic: str) -> dict:
    """Look up a short factual summary of a person, place or topic on Wikipedia."""
    log("wikipedia", {"topic": topic})
    try:
        d = _get("https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(topic.replace(" ", "_")))
        return {"title": d.get("title"), "summary": d.get("extract")}
    except Exception:
        return {"error": "No page found"}


def current_datetime() -> dict:
    """Get today's date, day and the current time."""
    log("current_datetime", {})
    now = datetime.now()
    return {"date": now.strftime("%d %B %Y"), "day": now.strftime("%A"), "time": now.strftime("%I:%M %p")}


def save_note(text: str) -> dict:
    """Save a note for the user into my_notes.txt."""
    log("save_note", {"text": text[:40] + "..."})
    with open("my_notes.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%d-%m-%Y %H:%M}] {text}\n")
    return {"saved": True, "file": os.path.abspath("my_notes.txt")}


TOOLS = [get_weather, convert_currency, calculator, wikipedia, current_datetime, save_note]

SYSTEM = ("You are JARVIS, a smart, witty AI agent. ALWAYS use tools for live data, maths and facts instead of guessing. "
          "You may call several tools, one after another, to finish a task. Keep final answers short and friendly.")


def main():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return print("Set GEMINI_API_KEY first (free key: https://aistudio.google.com/apikey)")
    client = genai.Client(api_key=key)
    chat = client.chats.create(model=MODEL, config=types.GenerateContentConfig(
        system_instruction=SYSTEM, tools=TOOLS,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(maximum_remote_calls=10)))

    print(f"""{C}
     ╦╔═╗╦═╗╦  ╦╦╔═╗   ┌┬┐┬┌┐┌┬
     ║╠═╣╠╦╝╚╗╔╝║╚═╗   │││││││││
    ╚╝╩ ╩╩╚═ ╚╝ ╩╚═╝   ┴ ┴┴┘└┘┴   AI Agent with {len(TOOLS)} tools{E}
    Type 'exit' to quit.\n""")
    while True:
        q = input(f"{G}You ➤ {E}").strip()
        if q.lower() in {"exit", "quit", "bye"}:
            break
        if not q:
            continue
        print(f"{D}   🧠 thinking...{E}")
        try:
            r = chat.send_message(q)
            print(f"{C}JARVIS ➤ {E}{r.text}\n")
        except Exception as ex:
            print(f"⚠️ {ex}\n")


if __name__ == "__main__":
    main()
