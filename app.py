import streamlit as st
from google import genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Multi-Timeframe AI Chart Analyzer", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Multi-Timeframe SMC & Price Action Analyzer")
st.caption("Higher Timeframe (Context/Bias) + Lower Timeframe (Entry/Execution) combine karke top-down analysis paayein.")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Setup & Rules")
    api_key = st.text_input("Gemini API Key dalein:", type="password")
    
    st.subheader("Timeframe Mapping")
    htf_label = st.selectbox("Higher Timeframe (HTF):", ["1 Hour (1h)", "15 Minute (15m)", "4 Hour (4h)", "Daily (1D)"], index=1)
    ltf_label = st.selectbox("Lower Timeframe (LTF):", ["3 Minute (3m)", "5 Minute (5m)", "1 Minute (1m)"], index=0)
    
    trading_style = st.selectbox("Trading Style:", ["Scalping / Day Trading", "Intraday Momentum", "Swing Trading"])
    risk_reward = st.selectbox("Target Risk-Reward:", ["1:2", "1:3", "1:4+"])

# Two-column layout for file uploads
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"1. Higher Timeframe ({htf_label})")
    htf_file = st.file_uploader(f"{htf_label} ka screenshot upload karein", type=["png", "jpg", "jpeg"], key="htf")
    if htf_file:
        htf_image = Image.open(htf_file)
        st.image(htf_image, caption=f"HTF: {htf_label}", use_container_width=True)

with col2:
    st.subheader(f"2. Lower Timeframe ({ltf_label})")
    ltf_file = st.file_uploader(f"{ltf_label} ka screenshot upload karein", type=["png", "jpg", "jpeg"], key="ltf")
    if ltf_file:
        ltf_image = Image.open(ltf_file)
        st.image(ltf_image, caption=f"LTF: {ltf_label}", use_container_width=True)

st.markdown("---")

# Execution Button
if st.button("🚀 Run Multi-Timeframe Analysis", type="primary", use_container_width=True):
    if not api_key:
        st.error("Kripya sidebar me apni Gemini API Key dalein.")
    elif not htf_file or not ltf_file:
        st.warning("Dono timeframes (HTF aur LTF) ke screenshots upload karna zaroori hai.")
    else:
        with st.spinner("AI dono timeframes ka top-down alignment check kar raha hai..."):
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                You are an elite institutional technical analyst specializing in Multi-Timeframe Analysis, Smart Money Concepts (SMC), and Liquidity Dynamics.
                
                Input Details:
                - Higher Timeframe (Image 1): {htf_label}
                - Lower Timeframe (Image 2): {ltf_label}
                - Strategy Focus: {trading_style}
                - Desired Risk-Reward: {risk_reward}

                Perform a thorough Top-Down Analysis aligning Image 1 and Image 2:

                ### 1. Higher Timeframe Context ({htf_label} - Image 1):
                - **Overall Trend & Bias**: Bullish, Bearish, or Ranging.
                - **Major Structure**: Last BOS / CHoCH level.
                - **Key HTF Zones**: Major Order Blocks (OB), Fair Value Gaps (FVG), Premium/Discount balance.
                - **Major Liquidity**: External liquidity targets (BSL/SSL).

                ### 2. Lower Timeframe Execution ({ltf_label} - Image 2):
                - **Internal Structure**: Minor BOS/CHoCH inside the HTF zone.
                - **Liquidity Sweep / Manipulation**: Did price hunt stops before reversal?
                - **Refined Entry Zone**: Exact candle block or mitigation point.

                ### 3. Confluence & Alignment Verdict:
                - State clearly if HTF and LTF are aligned or conflicting.
                - **Verdict**: [STRONG BUY / STRONG SELL / WAIT FOR RETRACEMENT / AVOID]

                ### 4. Trade Execution Plan:
                - **Entry Level / Zone**: Specific price or tight entry zone.
                - **Invalidation / Stop Loss (SL)**: Logical invalidation (below/above structural swing or OB).
                - **Take Profit 1 (TP1)**: First liquidity target / recent high or low.
                - **Take Profit 2 (TP2)**: Major HTF liquidity objective.
                - **Calculated Risk:Reward**: (e.g., 1:2.8)

                ### 5. Invalidation & Risk Factors:
                - Exactly what price action would cancel this setup.

                Format the output cleanly in Markdown with bold key values and concise, bullet-pointed explanations in conversational Hinglish/English.
                """

                # Pass both images along with the prompt
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[htf_image, ltf_image, prompt]
                )

                st.success("✅ Multi-Timeframe Analysis Complete!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Analysis ke dauran error aayi: {str(e)}")
