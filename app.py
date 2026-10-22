import time

import streamlit as st
from strands import Agent
from strands.models import BedrockModel

from decision_pattern.router import decide_route, CONFIDENCE_THRESHOLD

REGION = "eu-north-1"
MODELS = {
    "small": ("Nova Lite", "eu.amazon.nova-lite-v1:0"),
    "large": ("Nova Pro", "eu.amazon.nova-pro-v1:0"),
}
SYSTEM_PROMPT = "You are a friendly coding tutor. Keep answers clear and concise."
GREEN, AMBER = "#16a34a", "#f59e0b"

st.set_page_config(page_title="Router Tutor", page_icon="🧭", layout="centered")

st.markdown(
    """
<style>
/* remove the empty gap at the top */
header[data-testid="stHeader"] {display: none;}
.block-container {padding-top: 1.2rem !important; padding-bottom: 2rem;}

/* light-to-deeper indigo background */
.stApp {background: linear-gradient(160deg, #eef2ff 0%, #e0e7ff 45%, #c7d2fe 100%);}

/* deep indigo sidebar with white text */
[data-testid="stSidebar"] {background: linear-gradient(180deg, #312e81 0%, #4f46e5 100%);}
[data-testid="stSidebar"] * {color: #ffffff !important;}

/* buttons */
.stButton > button {border-radius: 12px; border: 1px solid #a5b4fc; background: #ffffff; color: #3730a3;}
.stButton > button:hover {border-color: #4f46e5; color: #4f46e5;}
.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border: none; font-weight: 700;}

/* hero banner */
.hero {padding: 28px 24px; border-radius: 16px; margin-bottom: 18px; color: white;
       background: linear-gradient(135deg, #3730a3 0%, #6d28d9 55%, #a855f7 100%);
       box-shadow: 0 8px 24px rgba(79,70,229,0.25);}
.hero h1 {margin: 0; font-size: 2rem; color: white;}
.hero p {margin: 6px 0 0 0; opacity: 0.92;}

/* cards */
.card {padding: 18px 20px; border-radius: 14px; margin: 10px 0;
       border: 1px solid #c7d2fe; background: rgba(255,255,255,0.75);
       box-shadow: 0 2px 10px rgba(79,70,229,0.08);}
.card h4 {margin: 0 0 10px 0; color: #3730a3;}
.meter {position: relative; height: 20px; border-radius: 10px; margin: 8px 0 4px 0; background: #e0e7ff;}
.meter-fill {height: 100%; border-radius: 10px;}
.marker {position: absolute; top: -5px; width: 3px; height: 30px; background: #1e1b4b; border-radius: 2px;}
.small-note {font-size: 0.8rem; opacity: 0.75;}
.prow {display: flex; align-items: center; gap: 10px; margin: 6px 0;}
.plabel {width: 70px; font-weight: 600;}
.pbar {flex: 1; height: 14px; border-radius: 7px; background: #e0e7ff;}
.pfill {height: 100%; border-radius: 7px; background: linear-gradient(90deg, #6366f1, #a855f7);}
.badge {display: inline-block; padding: 8px 16px; border-radius: 999px; color: white; font-weight: 700; margin: 6px 0;}
.big {font-size: 2.2rem; font-weight: 800; line-height: 1; color: #312e81;}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>🧭 Router Tutor</h1>'
    "<p>Strands Decider 2B judges your question in one step. "
    "Amazon Bedrock picks the right model to answer it.</p></div>",
    unsafe_allow_html=True,
)

if "log" not in st.session_state:
    st.session_state.log = []
if "q" not in st.session_state:
    st.session_state.q = ""


def set_q(text):
    st.session_state.q = text


st.caption("Try an example:")
c1, c2, c3 = st.columns(3)
c1.button("🟢 Easy", on_click=set_q, args=("What does len() return?",), use_container_width=True)
c2.button(
    "🟠 Hard",
    on_click=set_q,
    args=("Explain how a red-black tree stays balanced after insertion and compare it with an AVL tree",),
    use_container_width=True,
)
c3.button(
    "🤔 Borderline",
    on_click=set_q,
    args=("Compare optimistic and pessimistic locking in database transactions and when to use each",),
    use_container_width=True,
)

question = st.text_input("Ask a coding question", key="q", placeholder="Type your own question...")
ask = st.button("Ask", type="primary", use_container_width=True)

if ask and question.strip():
    with st.spinner("Decider is deciding..."):
        d = decide_route(question)

    conf = max(0.0, min(1.0, d["confidence"]))
    trusted = conf >= CONFIDENCE_THRESHOLD
    meter_color = GREEN if trusted else AMBER

    st.markdown("### 1 · The Decider decision")
    left, right = st.columns(2)

    with left:
        st.markdown(
            f'<div class="card"><h4>Decision</h4>'
            f'<div class="big">{d["choice"].upper()}</div>'
            f'<p style="margin:10px 0 0 0">Confidence <b>{conf:.2f}</b></p>'
            f'<div class="meter"><div class="meter-fill" '
            f'style="width:{conf * 100:.0f}%; background:{meter_color}"></div>'
            f'<div class="marker" style="left:{CONFIDENCE_THRESHOLD * 100:.0f}%"></div></div>'
            f'<div class="small-note">Black line = trust threshold ({CONFIDENCE_THRESHOLD})</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with right:
        rows = ""
        for label, p in d["probabilities"].items():
            rows += (
                f'<div class="prow"><div class="plabel">{label}</div>'
                f'<div class="pbar"><div class="pfill" style="width:{p * 100:.0f}%"></div></div>'
                f"<div>{p:.2f}</div></div>"
            )
        st.markdown(f'<div class="card"><h4>Probabilities</h4>{rows}</div>', unsafe_allow_html=True)

    name, model_id = MODELS[d["route"]]
    badge_color = GREEN if d["route"] == "small" else AMBER
    badge_text = "Cheaper model" if d["route"] == "small" else "Stronger model"
    st.markdown(
        f'<span class="badge" style="background:{badge_color}">→ {name} · {badge_text}</span> '
        f'<span class="small-note">{d["reason"]}</span>',
        unsafe_allow_html=True,
    )

    st.markdown("### 2 · The answer")
    agent = Agent(
        model=BedrockModel(model_id=model_id, region_name=REGION),
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )
    start = time.time()
    with st.spinner(f"{name} is answering..."):
        reply = str(agent(question))
    bedrock_ms = (time.time() - start) * 1000

    st.write(reply)
    st.caption(f"⏱ Decider {d['latency_ms']:.0f} ms · {name} {bedrock_ms:.0f} ms")

    st.session_state.log.append({"q": question, "route": d["route"], "conf": conf})

log = st.session_state.log
st.sidebar.markdown("## 📊 Scoreboard")
st.sidebar.metric("Questions asked", len(log))
small_n = sum(1 for x in log if x["route"] == "small")
st.sidebar.metric("Cheaper model", small_n)
st.sidebar.metric("Stronger model", len(log) - small_n)
if log:
    st.sidebar.progress(small_n / len(log))
    st.sidebar.caption(f"{small_n / len(log):.0%} answered by the cheaper model")
    st.sidebar.markdown("**History**")
    for x in reversed(log[-6:]):
        icon = "🟢" if x["route"] == "small" else "🟠"
        st.sidebar.caption(f"{icon} {x['conf']:.2f} · {x['q'][:38]}")