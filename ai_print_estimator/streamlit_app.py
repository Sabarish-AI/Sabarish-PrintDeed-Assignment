import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/orders/intake"

st.set_page_config(
    page_title="AI Print Estimator",
    page_icon="🖨️",
    layout="centered"
)

st.title("🖨️ AI Print Estimator")
st.caption(
    "AI-powered print order estimation with pricing, feasibility checks, "
    "and competitor market benchmarking"
)

st.divider()

# ----------------------------
# INPUT SECTION
# ----------------------------
st.subheader("📥 Order Input")

input_mode = st.radio(
    "Select input type",
    ["Text", "Email", "PDF / Image"],
    horizontal=True
)

text_input = None
email_subject = None
email_body = None
uploaded_file = None

if input_mode == "Text":
    text_input = st.text_area(
        "Customer Order",
        placeholder="Example:\n1000 A3 posters, 200 GSM paper, full color, gloss finish, delivery in 2 days",
        height=150
    )

elif input_mode == "Email":
    email_subject = st.text_input("Email Subject")
    email_body = st.text_area(
        "Email Body",
        placeholder="Please quote for 500 flyers printed on 170 GSM paper...",
        height=150
    )

elif input_mode == "PDF / Image":
    uploaded_file = st.file_uploader(
        "Upload PDF or Image",
        type=["pdf", "png", "jpg", "jpeg"]
    )

st.divider()

# ----------------------------
# SUBMIT BUTTON
# ----------------------------
if st.button("🚀 Generate Estimate", use_container_width=True):

    with st.spinner("Processing order..."):

        files = None
        data = {}

        if text_input:
            data["text"] = text_input

        if email_subject or email_body:
            data["email_subject"] = email_subject or ""
            data["email_body"] = email_body or ""

        if uploaded_file:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

        if not (text_input or email_subject or uploaded_file):
            st.error("Please provide at least one input.")
        else:
            response = requests.post(
                API_URL,
                data=data,
                files=files,
                timeout=120
            )

            if response.status_code != 200:
                st.error("Failed to generate estimate")
                st.code(response.text)
            else:
                result = response.json()

                st.success("Estimate generated successfully")

                st.subheader("📄 Extracted Specifications")
                st.json(result["specs"])

                st.subheader("💰 Pricing Breakdown")
                pricing = result["pricing"]

                cols = st.columns(3)
                cols[0].metric("Material Cost", f"₹{pricing['material_cost']}")
                cols[1].metric("Print Cost", f"₹{pricing['print_cost']}")
                cols[2].metric("Finishing Cost", f"₹{pricing['finishing_cost']}")

                cols = st.columns(3)
                cols[0].metric("Rush Fee", f"₹{pricing['rush_fee']}")
                cols[1].metric("Margin", f"₹{pricing['margin']}")
                cols[2].metric("Total Price", f"₹{pricing['total_price']}")

                st.subheader("⚠️ Validation & Feasibility")
                if result["validations"]:
                    for v in result["validations"]:
                        st.warning(f"{v['severity'].upper()}: {v['issue']}")
                else:
                    st.success("No issues detected. Order looks feasible.")

                if result.get("market_comparison"):
                    st.subheader("📊 Market Price Comparison")
                    mc = result["market_comparison"]
                    st.write(f"**Position:** {mc['position']}")
                    if mc.get("market_min"):
                        st.write(f"Market Range: ₹{mc['market_min']} – ₹{mc['market_max']}")
                    if mc.get("sources"):
                        st.write(f"Sources: {', '.join(mc['sources'])}")

st.divider()
st.caption(
    "Built as part of an AI Print Estimator technical assessment. "
    "AI is used only for spec extraction; pricing and validation are deterministic."
)