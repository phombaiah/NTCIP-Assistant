"""NTCIP Assistant — a Streamlit chat demo backed by Claude."""

from __future__ import annotations

import anthropic
import streamlit as st

from ntcip_context import NTCIP_CONTEXT

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096

EXAMPLE_QUESTIONS = [
    "What is NTCIP?",
    "What is NTCIP 1202?",
    "Which standards cover Dynamic Message Signs?",
    "Explain the NTCIP layered architecture",
    "Which standards apply to roadside units for V2X?",
    "How do major signal controller vendors differ in NTCIP 1202 implementation?",
    "Why are agencies still running NTCIP 2101 on legacy plant?",
    "STMP vs SNMP — when does each make sense in NTCIP?",
]


st.set_page_config(
    page_title="TransCore NTCIP Assistant (Demo)",
    page_icon="assets/transcore_favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo("assets/transcore_logo.png", size="large")


def password_ok() -> bool:
    """Optional shared-password gate. Active only if DEMO_PASSWORD is set in secrets."""
    if "DEMO_PASSWORD" not in st.secrets:
        return True
    if st.session_state.get("authed"):
        return True
    st.markdown("### NTCIP Assistant — Demo Access")
    st.caption("Enter the demo password to continue.")
    pw = st.text_input("Password", type="password", label_visibility="collapsed")
    if pw and pw == st.secrets["DEMO_PASSWORD"]:
        st.session_state["authed"] = True
        st.rerun()
    elif pw:
        st.error("Incorrect password.")
    return False


if not password_ok():
    st.stop()


api_key = st.secrets.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error(
        "`ANTHROPIC_API_KEY` is not configured. See `README.md` for setup."
    )
    st.stop()

client = anthropic.Anthropic(api_key=api_key)


with st.sidebar:
    st.markdown("## NTCIP Assistant")
    st.caption("TransCore — Trusted Transportation Solutions")
    st.markdown(
        "TransCore's NTCIP knowledge assistant. Ask anything about the "
        "**National Transportation Communications for ITS Protocol** family "
        "of standards — document numbers, scope, version history, and "
        "protocol architecture."
    )

    st.markdown("### Try a question")
    for q in EXAMPLE_QUESTIONS:
        if st.button(q, key=f"ex_{q}", use_container_width=True):
            st.session_state["pending_prompt"] = q
            st.rerun()

    st.divider()
    st.markdown(
        "**Disclaimer.** Demo built for TransCore. Answers may be "
        "inaccurate or incomplete — always verify against the official "
        "standard before relying on any answer. Knowledge snapshot: May 2026."
    )
    st.markdown("[Official NTCIP site ↗](https://www.ntcip.org/)")
    st.markdown(
        "[Document index ↗](https://www.ntcip.org/document-numbers-and-status/)"
    )

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()


st.title("TransCore NTCIP Assistant")
st.caption(
    "Demo · Ask anything about the National Transportation Communications "
    "for ITS Protocol — current standards, versions, scope, and architecture."
)


if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input("Ask about NTCIP...")
if not prompt and "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")


if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state["messages"]
    ]

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                thinking={"type": "disabled"},
                output_config={"effort": "low"},
                system=[
                    {
                        "type": "text",
                        "text": NTCIP_CONTEXT,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=api_messages,
            ) as stream:
                for text in stream.text_stream:
                    full += text
                    placeholder.markdown(full + "▌")
            placeholder.markdown(full)
        except anthropic.APIError as e:
            full = f"⚠️ API error: {e.message}"
            placeholder.error(full)

    st.session_state["messages"].append({"role": "assistant", "content": full})
