import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/orders/text"

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Print Estimator",
    page_icon="🖨️",
    layout="centered"
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🖨️ AI Print Estimator")
st.caption(
    "AI-powered print order estimation with pricing, feasibility checks, "
    "and competitor market benchmarking"
)

st.markdown("---")

# -------------------------------------------------
# Input section
# -------------------------------------------------
order_text = st.text_area(
    "✍️ Customer Order",
    placeholder=(
        "Example:\n"
        "1000 A3 posters, 200 GSM paper, full color, gloss finish, delivery in 2 days"
    ),
    height=140
)

# -------------------------------------------------
# Submit
# -------------------------------------------------
if st.button("🚀 Generate Estimate", use_container_width=True):

    if not order_text.strip():
        st.warning("Please enter a customer order.")
    else:
        with st.spinner("Analyzing order using AI..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": order_text},
                    timeout=30
                )
            except Exception:
                st.error("Backend not reachable. Please start FastAPI server.")
                st.stop()

        if response.status_code != 200:
            st.error("Failed to generate estimate.")
            st.stop()

        data = response.json()

        # -------------------------------------------------
        # Extracted Specs
        # -------------------------------------------------
        st.subheader("📄 Extracted Specifications")
        st.json(data["specs"])

        # -------------------------------------------------
        # Pricing Breakdown
        # -------------------------------------------------
        st.subheader("💰 Pricing Breakdown")

        pricing = data["pricing"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Material Cost", f"₹{pricing['material_cost']}")
        col2.metric("Print Cost", f"₹{pricing['print_cost']}")
        col3.metric("Finishing Cost", f"₹{pricing['finishing_cost']}")

        col4, col5 = st.columns(2)
        col4.metric("Rush Fee", f"₹{pricing['rush_fee']}")
        col5.metric("Margin", f"₹{pricing['margin']}")

        st.success(f"💵 Total Price: ₹{pricing['total_price']}")

        # -------------------------------------------------
        # Validation & Risk
        # -------------------------------------------------
        st.subheader("⚠️ Validation & Feasibility")

        validations = data.get("validations", [])

        if not validations:
            st.success("✅ No issues detected. Order looks feasible.")
        else:
            high_risk = False
            for v in validations:
                if v["severity"].lower() == "high":
                    high_risk = True
                    st.error(f"HIGH: {v['issue']}")
                elif v["severity"].lower() == "medium":
                    st.warning(f"MEDIUM: {v['issue']}")
                else:
                    st.info(f"LOW: {v['issue']}")

            if high_risk:
                st.error("❌ Manual review required")
            else:
                st.warning("⚠️ Review recommended")

        # -------------------------------------------------
        # Market Comparison (Competitor Pricing)
        # -------------------------------------------------
        st.subheader("📊 Market Price Comparison")

        market = data.get("market_comparison")

        if market and market.get("position") != "unavailable":
            position = market["position"]

            if position == "below_market":
                st.success("💸 Your price is below market range")
            elif position == "within_market":
                st.info("📈 Your price is within market range")
            else:
                st.warning("💰 Your price is above market range")

            st.caption(
                f"Market range: ₹{market['market_min']} – ₹{market['market_max']} "
                f"(Sources: {', '.join(market['sources'])})"
            )
        else:
            st.caption("Competitor pricing data not available at the moment.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Built as part of an AI Print Estimator technical assessment. "
    "AI is used only for spec extraction; pricing and validation are deterministic."
)