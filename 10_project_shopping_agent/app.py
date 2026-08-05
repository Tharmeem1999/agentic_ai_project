"""Simple Streamlit chat UI for the shopping agent."""

import os
import sys

import streamlit as st
from dotenv import load_dotenv

# Make the local module importable when Streamlit is launched from elsewhere
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load env vars (GROQ_API_KEY, etc.) before importing the agent
load_dotenv()

from shopping_agent import agent  # noqa: E402

st.set_page_config(page_title="Shopping Assistant", page_icon="🛒", layout="centered")
st.title("🛒 Shopping Assistant")
st.caption("Chat with the agent to search products, check ratings, and place orders.")

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept new user input
if prompt := st.chat_input("What are you looking for today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = agent.invoke({"messages": st.session_state.messages})
            response = result["messages"][-1].content
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
