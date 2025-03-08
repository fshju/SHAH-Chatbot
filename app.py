import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
import time

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Check API key
if not API_KEY:
    st.error("🚨 API key is missing! Please add your API key in the .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# Streamlit UI Configuration
st.set_page_config(page_title="🤖 AI Chatbot", page_icon="🤖", layout="centered")
st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stChatMessage { padding: 10px; border-radius: 10px; }
        .user { background-color: #1E88E5; color: white; align-self: flex-end; }
        .assistant { background-color: #424242; color: white; align-self: flex-start; }
    </style>
""", unsafe_allow_html=True)

st.title("💬🤖 SHAH AI Chatbot")
st.caption("🚀 A fun and interactive chatbot experience with emojis and smooth UI!")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages with bubbles and emojis
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(f"{msg['content']}")

# User input
user_input = st.chat_input("Ask me anything...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": f"🧑‍💻 {user_input}"})
    with st.chat_message("user"):
        st.markdown(f"🧑 {user_input}")
    
    try:
        # Generate response using Gemini AI
        model = genai.GenerativeModel("gemini-1.5-pro")  # Ensure correct model name
        response = model.generate_content(user_input)
        bot_reply = response.text
        
        # Adding emoji reactions
        bot_reply = f"🤖 {bot_reply} 😊"
        
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

    except Exception as e:
        st.error(f"❌ Error: {e}")
