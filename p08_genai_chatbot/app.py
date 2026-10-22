"""
PROJECT 8 — BuddyAI 🤖💬  (Gen AI Chatbot with Google Gemini)
- ChatGPT-style UI with live streaming answers
- Switch personalities: Career Mentor, Interview Coach, Code Explainer, Tamil Tutor, Roast Bot 😄
- Remembers the conversation (chat memory)
- Upload an image and ask questions about it (multimodal AI)

Setup:
  pip install -r requirements.txt
  Get a FREE key: https://aistudio.google.com/apikey
  Windows : set GEMINI_API_KEY=your_key      Mac/Linux: export GEMINI_API_KEY=your_key
  streamlit run app.py
"""
import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

PERSONAS = {
    "🎓 Career Mentor": "You are a warm, practical career mentor for Indian college students. Give clear roadmaps, "
                        "skills, free resources and realistic salary ranges. Use short bullet points and emojis.",
    "💼 Interview Coach": "You are a strict but friendly HR + technical interviewer. Ask ONE interview question at a time, "
                         "wait for the answer, then rate it out of 10 and show a better answer.",
    "💻 Code Explainer": "You explain code and programming concepts like a great teacher, using simple analogies "
                        "and tiny examples. Always end with a 1-line summary.",
    "🗣️ Tamil Tutor": "You reply in simple Tanglish (Tamil written in English letters) mixed with English tech words, "
                     "like a friendly senior anna/akka explaining to a junior.",
    "🔥 Roast Bot": "You are a funny roast comedian. Lightly and kindly roast the user's message (never hurtful, no "
                   "insults about identity), then give genuinely useful advice.",
}

st.set_page_config(page_title="BuddyAI", page_icon="🤖")
st.markdown("""<style>
.stApp{background:radial-gradient(circle at 10% 0%,#221a4d,#07070f 55%)}
h1{background:linear-gradient(90deg,#7c5cff,#00d4ff);-webkit-background-clip:text;color:transparent!important}
</style>""", unsafe_allow_html=True)
st.title("BuddyAI — your personal AI 🤖")

key = os.getenv("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API key", type="password")
if not key:
    st.info("👈 Paste your free Gemini API key (from aistudio.google.com/apikey) to start.")
    st.stop()


@st.cache_resource
def get_client(k):
    return genai.Client(api_key=k)


client = get_client(key)

with st.sidebar:
    persona = st.radio("Choose a personality", list(PERSONAS))
    creativity = st.slider("Creativity (temperature)", 0.0, 1.5, 0.8)
    image_file = st.file_uploader("📷 Ask about an image", type=["png", "jpg", "jpeg"])
    if st.button("🧹 New chat"):
        st.session_state.messages = []
    st.caption(f"Model: {MODEL}")

if "messages" not in st.session_state or st.session_state.get("persona") != persona:
    st.session_state.messages = []
    st.session_state.persona = persona

if not st.session_state.messages:
    st.chat_message("assistant").write(f"Hi! I'm your **{persona}**. Ask me anything 👇")

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["text"])

if prompt := st.chat_input("Type your message..."):
    st.chat_message("user").write(prompt)

    # memory: send the whole previous conversation to the model
    history = [types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part(text=m["text"])])
               for m in st.session_state.messages]
    chat = client.chats.create(
        model=MODEL,
        history=history,
        config=types.GenerateContentConfig(system_instruction=PERSONAS[persona], temperature=creativity),
    )
    message = [prompt]
    if image_file:
        message.insert(0, Image.open(image_file))

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(c.text for c in chat.send_message_stream(message) if c.text)
        except Exception as e:
            reply = f"⚠️ Error: {e}"
            st.error(reply)

    st.session_state.messages += [{"role": "user", "text": prompt}, {"role": "assistant", "text": reply}]
