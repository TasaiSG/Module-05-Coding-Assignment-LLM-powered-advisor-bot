"""
CSC-128 Assignment 5 starter: LLM-powered advisor bot
Your name here

Run:  streamlit run app.py

Before you start:
  1. Create .streamlit/secrets.toml with your GROQ_API_KEY
  2. Confirm .streamlit/secrets.toml is listed in .gitignore
  3. Only then make your first commit
"""
import streamlit as st
from groq import Groq, APIError, RateLimitError

MODEL = "llama-3.1-8b-instant"
MAX_HISTORY = 10

# TODO 1: write a system prompt that names the bot's job, lists exactly what
# it can do, states what it must never do, and says what to do when asked
# something out of scope.
SYSTEM_PROMPT = """"""

GREETING = ""


def get_client():
    """TODO 2: read the key from st.secrets and fail with a clear message."""
    return None


def build_messages(history):
    """TODO 3: system prompt plus the last MAX_HISTORY messages."""
    return []


def stream_reply(client, history, placeholder):
    """
    TODO 4: call the API with stream=True and paint tokens as they arrive.

    TODO 5: catch RateLimitError and APIError separately and return a
    message the user can actually act on. Do not let a traceback reach
    the page.
    """
    return ""


def main():
    st.title("Program Assistant")
    st.caption("You are chatting with an automated assistant, not a person.")
    # TODO 6: session state, redraw loop, chat input, streamed reply


if __name__ == "__main__":
    main()
