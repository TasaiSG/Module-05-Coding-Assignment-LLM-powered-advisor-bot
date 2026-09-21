"""
CSC-128 Assignment 5: LLM-powered advisor bot
Tasai Smith-Gandy

Run:  streamlit run app.py

Before you start:
  1. Create .streamlit/secrets.toml with your GROQ_API_KEY
  2. Confirm .streamlit/secrets.toml is listed in .gitignore
  3. Only then make your first commit
"""

import streamlit as st
from groq import Groq, APIError, RateLimitError

MODEL = "openai/gpt-oss-20b"
MAX_HISTORY = 10

SYSTEM_PROMPT = """
You are a Program Assistant for CSC-128.

Your job is to help students with programming and computer science topics.

You can:
- Explain programming concepts and terminology.
- Explain Python code and programming errors.
- Help debug code and explain how to fix errors.
- Help students understand programming assignments and instructions.
- Suggest approaches for solving programming problems.
- Explain why a particular programming solution works.

You must never:
- Pretend to be a human.
- Claim that you completed work when you did not.
- Reveal, request, or reproduce API keys, passwords, or other secrets.
- Help with requests that are unrelated to programming or computer science.

If a request is outside your scope, politely say that you are a
programming assistant and can only help with programming and
computer-science-related questions.
"""

GREETING = (
    "Hi! I'm the CSC-128 Program Assistant. "
    "I'm software, not a person, and I can help with programming "
    "and computer-science questions."
)


def get_client():
    """Read the Groq API key from Streamlit secrets."""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error(
            "GROQ_API_KEY was not found. "
            "Check that .streamlit/secrets.toml exists and contains "
            'GROQ_API_KEY = "your-key-here".'
        )
        st.stop()

    return Groq(api_key=api_key)


def build_messages(history):
    """Return the system prompt plus the most recent conversation."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history[-MAX_HISTORY:],
    ]


def stream_reply(client, history, placeholder):
    """Send the conversation to Groq and stream the response."""
    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=build_messages(history),
            stream=True,
        )

        response = ""

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                placeholder.markdown(response)

        return response

    except RateLimitError:
        message = (
            "The API rate limit was reached. "
            "Please wait a little while and try again."
        )
        placeholder.error(message)
        return message

    except APIError:
        message = (
            "The Groq API returned an error. "
            "Please check your API key and try again."
        )
        placeholder.error(message)
        return message


def main():
    st.title("Program Assistant")
    st.caption("You are chatting with an automated assistant, not a person.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a programming question...")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            client = get_client()

            response = stream_reply(
                client,
                st.session_state.messages,
                placeholder,
            )

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )


if __name__ == "__main__":
    main()
