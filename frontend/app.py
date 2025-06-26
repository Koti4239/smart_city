import streamlit as st
import requests
import pandas as pd
import io

st.set_page_config(page_title="Sustainable Smart City Assistant", layout="wide")
st.title("🌆 Sustainable Smart City Assistant")

menu = ["Policy Summarizer", "KPI Forecasting", "Anomaly Detection"]
choice = st.sidebar.selectbox("Select a Module", menu)

API_URL = "http://127.0.0.1:8000"  # Update this if deployed

# Common helper
def upload_and_post(file, endpoint, file_type="text/csv"):
    try:
        files = {"file": (file.name, file, file_type)}
        with st.spinner("⏳ Processing..."):
            response = requests.post(f"{API_URL}/{endpoint}", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"🚫 Request failed: {e}")
    return None

# --- Module 1: Policy Summarizer ---
if choice == "Policy Summarizer":
    st.header("📄 Upload City Policy Document")
    file = st.file_uploader("Upload a .txt file", type=["txt"])
    if file:
        result = upload_and_post(file, "summarize", file_type="text/plain")
        if result:
            st.success("✅ Summary:")
            st.write(result["summary"])

# --- Module 2: KPI Forecasting ---
elif choice == "KPI Forecasting":
    st.header("📈 Upload KPI CSV File")
    file = st.file_uploader("Upload a CSV file", type=["csv"])
    if file:
        result = upload_and_post(file, "forecast")
        if result:
            st.success(f"📊 Forecasted Value: {result['forecast']:.2f}")

# --- Module 3: Anomaly Detection ---
elif choice == "Anomaly Detection":
    st.header("⚠️ Upload KPI Data for Anomaly Detection")
    file = st.file_uploader("Upload a CSV file", type=["csv"])
    if file:
        result = upload_and_post(file, "anomaly")
        if result:
            anomalies = result.get("anomalies", [])
            if anomalies:
                st.error("🚨 Anomalies Found:")
                df = pd.DataFrame(anomalies)
                st.dataframe(df)

                # Add download option
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Anomalies as CSV", data=csv, file_name="anomalies.csv", mime="text/csv")
            else:
                st.success("✅ No anomalies detected.")
