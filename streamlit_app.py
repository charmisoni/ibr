"""
Variable-by-Variable Explainer — AI-Driven Claims Verification in Indian Motor Insurance
------------------------------------------------------------------------------------------
Run locally:
    pip install streamlit plotly pandas
    streamlit run streamlit_app.py

Everything is self-contained (no external data files needed) — all numbers and quotes
come from your SmartPLS 4 output (n=105), your two expert interviews, and the 94
open-text survey answers, exactly as discussed in your analysis.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Claims Verification — Variable Explainer",
    page_icon="📊",
    layout="wide",
)

# ----------------------------------------------------------------------------------
# COLOR SYSTEM (matches your cream / navy / coral design identity)
# ----------------------------------------------------------------------------------
NAVY = "#1F2A44"
CORAL = "#E8735A"
CREAM = "#F5EFE6"
MUTED = "#6B6B6B"
GREEN = "#3F7A5C"
GOLD = "#C9A227"
RED = "#A83E35"

VERDICT_COLOR = {
    "Converged & strong": GREEN,
    "Hidden gap": GOLD,
    "Confirmed null": RED,
    "Mixed": NAVY,
}

# ----------------------------------------------------------------------------------
# DATA — every variable's quant result, plain-language meaning, and real quotes
# ----------------------------------------------------------------------------------
VARIABLES = [
    {
        "code": "RA",
        "name": "Relative Advantage",
        "verdict": "Converged & strong",
        "stats": {
            "β → Decision Speed": "0.716 (p<.001)",
            "β → Fraud Detection": "0.476 (p<.001)",
            "f² (Decision Speed)": "0.81 — large",
            "Reliability (α)": "0.861",
        },
        "meaning": (
            "People's belief that AI genuinely works better than the old manual way is the "
            "single biggest reason it gets adopted and used well. Both survey questions for "
            "this topic agreed with each other closely, so the measurement is clean, and this "
            "is your strongest and most trustworthy finding."
        ),
        "interview": (
            "\"AI has flagged the possible fraudulent claims basis our past experiences for "
            "which prompts or scenarios were given to the system.\" — R1 (zonal claims manager)"
        ),
        "opentext": [
            "\"AI can be a game changer in claim management.\" (said identically by 5 different respondents)",
            "\"Auto Process and less manual process so reduce time and work more efficient.\"",
        ],
    },
    {
        "code": "FDC",
        "name": "Fraud Detection Capacity (mediator)",
        "verdict": "Converged & strong",
        "stats": {
            "β → Operational Efficiency": "0.426 (p=.001)",
            "R²": "0.653",
            "Reliability (α)": "0.913",
            "Outer loadings": "0.963 / 0.956",
        },
        "meaning": (
            "Of everything AI does, catching fraud is where it earns its keep most clearly and "
            "measurably — and this is one of the best-measured parts of your whole survey."
        ),
        "interview": (
            "\"...they are using AI primarily for fraud and leakage detection, and that's where "
            "the ROI of AI is highest anyway.\" — R2"
        ),
        "opentext": [
            "\"Fraud detection\" (a respondent's entire answer)",
            "\"Claim inspection records and past lost history can help to identify duplicate / "
            "old claim before it get processed.\"",
        ],
    },
    {
        "code": "DMS",
        "name": "Decision-Making Speed (mediator)",
        "verdict": "Converged & strong",
        "stats": {
            "β → Operational Efficiency": "0.410 (p=.003)",
            "R²": "0.636",
            "Reliability (α)": "0.786",
            "Outer loadings": "0.911 / 0.904",
        },
        "meaning": (
            "Speed gains are real and are one of the two main routes (along with fraud "
            "detection) through which AI actually improves the business."
        ),
        "interview": (
            "Implied throughout rather than named directly — R1's verification wins and R2's "
            "\"real-time photo-based inspection, real-time estimates\" both describe speed gains."
        ),
        "opentext": [
            "\"Auto Process and less manual process so reduce time and work more efficient.\"",
            "\"Due to AI more help settle claim.\"",
        ],
    },
    {
        "code": "CDA",
        "name": "Customer Digital Adoption",
        "verdict": "Mixed",
        "stats": {
            "β → Decision Speed": "0.174 (p=.151, ns)",
            "β → Fraud Detection": "0.354 (p<.001)",
            "f² (Fraud Detection)": "0.233 — medium/large",
            "Reliability (α)": "0.493",
        },
        "meaning": (
            "Split result: customer readiness feeds directly into fraud detection (digital "
            "photos and submissions become raw material for the system) but doesn't "
            "significantly affect internal decision speed, which is more about the company's "
            "own workflow than what the customer does."
        ),
        "interview": (
            "\"IOT has picked up extremely well in India... it has deeply penetrated even in "
            "the rural belts.\" — R1"
        ),
        "opentext": [
            "No direct match on digital-skill readiness in the open text.",
            "A related but different concern appears instead: \"Machine has no empathy. In "
            "death and injury claims the customer needs a person to talk to, not a bot.\"",
        ],
    },
    {
        "code": "DQA",
        "name": "Data Quality & Accuracy",
        "verdict": "Hidden gap",
        "stats": {
            "β → Decision Speed": "0.080 (p=.299, ns)",
            "β → Fraud Detection": "0.216 (p=.079, closest to sig.)",
            "SmartPLS-reported α": "0.443",
            "Recomputed α (consistent coding)": "0.767",
        },
        "meaning": (
            "Officially \"no effect\" — but the two survey questions for this topic didn't "
            "agree well with each other, which weakens any conclusion. Likely the measuring "
            "tool wasn't sharp enough here, not that data quality genuinely doesn't matter."
        ),
        "interview": (
            "\"...it has to be a correct and efficient collection of the data about all claims "
            "since AI will need accurate data.\" — R1's one piece of closing advice"
        ),
        "opentext": [
            "\"Less hallucinations and more learning backed by data which is scattered now at "
            "multiple sources.\"",
            "\"If the claims processed data of leading companies is merged to train AI it can "
            "get more effective.\"",
            "\"Structured machine readable information.\"",
        ],
    },
    {
        "code": "SIC",
        "name": "System Integration Compatibility",
        "verdict": "Hidden gap",
        "stats": {
            "β → Decision Speed": "0.069 (p=.383, ns)",
            "β → Fraud Detection": "-0.005 (p=.953, ~zero)",
            "Reliability (α)": "0.581",
            "Open-text mentions": "12 of 105 (15%)",
        },
        "meaning": (
            "No significant effect — most people already rated their systems as \"good "
            "enough, not great,\" so there wasn't much variation left to explain other "
            "outcomes."
        ),
        "interview": (
            "Neither expert discussed this directly, though R1's fraud-catching examples "
            "quietly depend on systems being connected to government databases."
        ),
        "opentext": [
            "\"Integrate AI with policy and claims systems, improve document verification and "
            "fraud detection.\"",
            "\"Our legacy portal does not support any API integration, so AI tool has to work "
            "separately which defeats the purpose.\" (said by 3 different respondents)",
        ],
    },
    {
        "code": "EC",
        "name": "Employee Competence",
        "verdict": "Hidden gap",
        "stats": {
            "β → Decision Speed": "-0.006 (p=.932, ~zero)",
            "β → Fraud Detection": "0.002 (p=.984, ~zero)",
            "SmartPLS-reported α": "0.367",
            "Recomputed α (consistent coding)": "0.778",
        },
        "meaning": (
            "The flattest result in the whole study — but when raw answers were recoded with "
            "consistent polarity, this topic looked reliable. Very likely a data-entry/coding "
            "issue, not a true absence of effect. Also the #1 most-mentioned theme in the "
            "open-text data (13 of 105, unprompted)."
        ),
        "interview": (
            "\"We have seen people taking this change as complete non sense... after some time "
            "when some cases highlighted by system helped them... they start adopting and "
            "accepting these things.\" — trust builds gradually, which one survey question "
            "can't capture."
        ),
        "opentext": [
            "\"Need professional training on AI tools and adaption of AI technology.\"",
            "\"Proper training is required for claim handlers, otherwise they will not trust "
            "the output and will do manual check anyway.\"",
        ],
    },
    {
        "code": "TMS",
        "name": "Top Management Support",
        "verdict": "Hidden gap",
        "stats": {
            "β → Decision Speed": "0.045 (p=.493, ns)",
            "β → Fraud Detection": "0.004 (p=.955, ~zero)",
            "SmartPLS-reported α": "0.395",
            "Recomputed α (consistent coding)": "0.738",
        },
        "meaning": (
            "No significant effect — same likely measurement-issue story as Employee "
            "Competence."
        ),
        "interview": (
            "Neither expert addressed this directly, though R2's ROI-skepticism (\"you're not "
            "subtracting cost, you're adding it\") is itself a management-level hesitation."
        ),
        "opentext": [
            "Fewer voices (6 of 105) but sharp: \"Top management support is there on paper but "
            "budget is not sanctioned.\" (said by 2 respondents)",
            "\"Top leadership investment.\"",
        ],
    },
    {
        "code": "SCP",
        "name": "Regulatory Clarity",
        "verdict": "Confirmed null",
        "stats": {
            "β → Decision Speed": "-0.085 (p=.402, ns)",
            "β → Fraud Detection": "-0.218 (p=.298, ns)",
            "SCP1 outer loading": "-0.670 (negative)",
            "Open-text mentions": "0 of 105",
        },
        "meaning": (
            "Not a measurement mistake — one item (\"rules are clear\") and the other (\"we're "
            "closely monitored\") genuinely point in different directions, which makes "
            "real-world sense: regulators often watch more closely exactly when things aren't "
            "settled yet. Every source agrees this genuinely isn't the problem."
        ),
        "interview": (
            "\"I don't know how IRDAI can impose use of AI on the insurers... it is up to the "
            "insurance companies.\" — R1, dismissing it outright"
        ),
        "opentext": [
            "Zero. Not one of 105 respondents mentioned regulation as something that needs to "
            "change.",
        ],
    },
    {
        "code": "OE",
        "name": "Operational Efficiency (outcome)",
        "verdict": "Mixed",
        "stats": {
            "R²": "0.627",
            "DV3 outer loading": "0.968",
            "DV1 / DV2 / DV4 loadings": "0.32 – 0.40",
            "AVE": "0.331 (below 0.50 threshold)",
        },
        "meaning": (
            "Well explained overall — but the four questions measuring \"efficiency\" secretly "
            "split into two ideas: a Speed pair that agree closely with each other (r=.88), and "
            "a Resource-Use pair that barely relate to the speed pair (r=.04–.20). People "
            "answer these as two separate mental questions, not one."
        ),
        "interview": (
            "R2's framing fits exactly: efficiency gains are concentrated in a specific slice "
            "of claims (small, simple, digitally comfortable, no third party) rather than "
            "applying evenly everywhere."
        ),
        "opentext": [
            "Efficiency comments are scattered across many quotes already shown above (speed, "
            "auto-processing, resource use) rather than forming one distinct cluster — "
            "consistent with \"efficiency\" not being one single idea.",
        ],
    },
]

# Max |beta| on any path, used for the overview chart (kept in sync with VARIABLES order)
MAX_BETA = [0.716, 0.426, 0.410, 0.354, 0.216, 0.069, 0.006, 0.045, 0.218, 0.968]

# ----------------------------------------------------------------------------------
# SIDEBAR — variable picker
# ----------------------------------------------------------------------------------
st.sidebar.title("📊 Variable Explainer")
st.sidebar.caption("AI-Driven Claims Verification — Indian Motor Insurance")
st.sidebar.markdown("---")

labels = [f"{v['code']} — {v['name']}" for v in VARIABLES]
choice = st.sidebar.radio("Choose a variable", labels, index=0)
selected = VARIABLES[labels.index(choice)]

st.sidebar.markdown("---")
st.sidebar.markdown("**Legend**")
for verdict, color in VERDICT_COLOR.items():
    st.sidebar.markdown(
        f"<span style='color:{color}; font-weight:700;'>●</span> {verdict}",
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------------
# MAIN AREA
# ----------------------------------------------------------------------------------
st.title("What each PLS-SEM result means, and what people actually said about it")
st.caption(
    "Every card below is built from your SmartPLS 4 output (n=105), your two expert "
    "interviews, and the 94 open-text survey answers."
)

col_main, col_side = st.columns([1.4, 1])

with col_main:
    badge_color = VERDICT_COLOR[selected["verdict"]]
    st.markdown(
        f"<span style='background:{badge_color}22; color:{badge_color}; "
        f"font-weight:700; padding:4px 12px; border-radius:4px; font-size:12px; "
        f"text-transform:uppercase; letter-spacing:0.03em;'>{selected['verdict']}</span>",
        unsafe_allow_html=True,
    )
    st.header(selected["name"])

    # Stat row
    stat_cols = st.columns(len(selected["stats"]))
    for c, (label, value) in zip(stat_cols, selected["stats"].items()):
        with c:
            st.metric(label, value)

    st.markdown("#### What this means")
    st.write(selected["meaning"])

with col_side:
    st.markdown("#### Where every variable sits")
    fig = go.Figure(
        go.Bar(
            x=MAX_BETA,
            y=[v["code"] for v in VARIABLES],
            orientation="h",
            marker_color=[VERDICT_COLOR[v["verdict"]] for v in VARIABLES],
        )
    )
    fig.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Max |β| on any path",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

qcol1, qcol2 = st.columns(2)

with qcol1:
    st.markdown("#### 🎙️ What the interview says")
    st.info(selected["interview"])

with qcol2:
    st.markdown("#### 📝 What the survey's open-text answers say")
    for q in selected["opentext"]:
        st.success(q)

st.markdown("---")
st.caption(
    "Data pack: IBR_Analysis_Data_Pack.xlsx · Interviews: Document6 (R1), interview_2 (R2) · "
    "Open-text: 94 of 105 respondents answered the free-text survey question."
)
