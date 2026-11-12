import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.express as px

# ============================================================
# Load Files
# ============================================================

model = joblib.load("models/tuned_xgboost_model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="AI Network Security Threat Detection",
    page_icon="🔐",
    layout="wide"
)

# ============================================================
# CSS Styling
# ============================================================

st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #102A43;
}
.sub-title {
    font-size: 17px;
    color: #52616B;
}
.card {
    background-color: #F8FAFC;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}
.metric-card {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 16px;
    border-left: 5px solid #2563EB;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}
.attack-box {
    background-color: #FEE2E2;
    padding: 18px;
    border-radius: 14px;
    color: #991B1B;
    font-weight: 700;
}
.safe-box {
    background-color: #DCFCE7;
    padding: 18px;
    border-radius: 14px;
    color: #166534;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("Use sample values or enter custom network traffic features.")

mode = st.sidebar.radio(
    "Choose Input Mode",
    ["Sample Traffic", "Manual Input", "CSV Batch Prediction"]
)

sample_type = None

if mode == "Sample Traffic":
    sample_type = st.sidebar.selectbox(
        "Select Sample Traffic Type",
        [
            "Normal Traffic",
            "DDoS Style Traffic",
            "PortScan Style Traffic",
            "Brute Force Style Traffic",
            "Botnet Style Traffic"
        ]
    )

st.sidebar.markdown("---")
st.sidebar.info(
    "Tip: For presentation, use Sample Traffic first. "
    "For real testing, use CSV Batch Prediction."
)

# ============================================================
# Default Input Generator
# ============================================================

def get_default_value(feature, sample_type):
    f = feature.lower()

    defaults = {
        "normal": 0.05,
        "ddos": 0.80,
        "portscan": 0.45,
        "bruteforce": 0.35,
        "botnet": 0.55
    }

    if sample_type == "Normal Traffic":
        base = defaults["normal"]
    elif sample_type == "DDoS Style Traffic":
        base = defaults["ddos"]
    elif sample_type == "PortScan Style Traffic":
        base = defaults["portscan"]
    elif sample_type == "Brute Force Style Traffic":
        base = defaults["bruteforce"]
    elif sample_type == "Botnet Style Traffic":
        base = defaults["botnet"]
    else:
        base = 0.05

    if "duration" in f:
        return base * 100000
    elif "packet" in f:
        return base * 100
    elif "bytes" in f:
        return base * 1000
    elif "iat" in f:
        return base * 10000
    elif "flag" in f:
        return 1.0 if base > 0.4 else 0.0
    elif "port" in f:
        return 80.0
    else:
        return base


# ============================================================
# Header
# ============================================================

st.markdown('<div class="main-title">🔐 AI-Based Network Security Threat Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Machine Learning framework for network intrusion detection and mitigation recommendation</div>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# Main Dashboard Cards
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card"><h4>Final Model</h4><h2>XGBoost</h2></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card"><h4>Model Accuracy</h4><h2>94.37%</h2></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card"><h4>Features Used</h4><h2>{}</h2></div>'.format(len(feature_columns)), unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card"><h4>Classes</h4><h2>{}</h2></div>'.format(len(label_encoder.classes_)), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# Mitigation Strategy
# ============================================================

mitigation_map = {
    "BENIGN": "No action required. Traffic appears normal.",
    "DDoS": "Apply rate limiting, block suspicious IPs, enable DDoS protection.",
    "DoS Hulk": "Limit request rate, block source IP, monitor server resource usage.",
    "DoS GoldenEye": "Apply HTTP request filtering and block repeated malicious requests.",
    "DoS slowloris": "Reduce connection timeout and limit incomplete HTTP connections.",
    "DoS Slowhttptest": "Use web server hardening and connection timeout controls.",
    "PortScan": "Block scanning IP, close unused ports, enable firewall logging.",
    "FTP-Patator": "Apply account lockout, strong passwords, and monitor FTP login attempts.",
    "SSH-Patator": "Disable password SSH login, use key-based auth, block brute-force IPs.",
    "Bot": "Isolate infected host, scan endpoint, block C2 communication.",
    "Web Attack Brute Force": "Enable CAPTCHA, account lockout, and web login monitoring.",
    "Web Attack XSS": "Apply input validation, output encoding, and web application firewall rules."
}

# ============================================================
# Prediction Function
# ============================================================

def predict_attack(input_df):
    input_df = input_df[feature_columns]
    scaled = scaler.transform(input_df)
    pred = model.predict(scaled)
    label = label_encoder.inverse_transform(pred)
    return label


# ============================================================
# Tabs
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Prediction",
    "📊 Dataset / Model Info",
    "🛡️ Mitigation Strategy",
    "📁 Batch Prediction"
])

# ============================================================
# Tab 1: Prediction
# ============================================================

with tab1:
    st.markdown("### 🔍 Network Traffic Prediction")

    if mode in ["Sample Traffic", "Manual Input"]:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        input_values = {}

        st.markdown("#### Input Network Features")

        cols = st.columns(3)

        for i, feature in enumerate(feature_columns):
            default_value = get_default_value(feature, sample_type)

            with cols[i % 3]:
                input_values[feature] = st.number_input(
                    feature,
                    value=float(default_value),
                    step=0.01,
                    format="%.4f"
                )

        st.markdown('</div>', unsafe_allow_html=True)

        predict_btn = st.button("🚀 Predict Threat", use_container_width=True)

        if predict_btn:
            input_df = pd.DataFrame([input_values])
            predicted_label = predict_attack(input_df)[0]

            st.markdown("### Result")

            if predicted_label == "BENIGN":
                st.markdown(
                    f'<div class="safe-box">✅ Normal Traffic Detected: {predicted_label}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="attack-box">⚠️ Cyber Threat Detected: {predicted_label}</div>',
                    unsafe_allow_html=True
                )

            st.markdown("### Recommended Mitigation")
            st.info(mitigation_map.get(predicted_label, "Investigate traffic and apply security controls."))

    else:
        st.warning("CSV Batch Prediction mode selected. Please use the Batch Prediction tab.")


# ============================================================
# Tab 2: Dataset / Model Info
# ============================================================

with tab2:
    st.markdown("### 📊 Project Information")

    st.markdown("""
    **Dataset Used:** CICIDS2017  
    **Purpose:** Network intrusion detection  
    **Final Model:** Tuned XGBoost  
    **Preprocessing Applied:**  
    - Missing value removal  
    - Duplicate removal  
    - Constant feature removal  
    - Highly correlated feature removal  
    - Class balancing  
    - Feature scaling  
    - Hyperparameter tuning  
    """)

    classes_df = pd.DataFrame({
        "Attack Classes": label_encoder.classes_
    })

    st.dataframe(classes_df, use_container_width=True)


# ============================================================
# Tab 3: Mitigation Strategy
# ============================================================

with tab3:
    st.markdown("### 🛡️ Threat Mitigation Strategy")

    mitigation_df = pd.DataFrame({
        "Threat Type": list(mitigation_map.keys()),
        "Recommended Mitigation": list(mitigation_map.values())
    })

    st.dataframe(mitigation_df, use_container_width=True)


# ============================================================
# Tab 4: Batch Prediction
# ============================================================

with tab4:
    st.markdown("### 📁 CSV Batch Prediction")

    uploaded_file = st.file_uploader("Upload CSV file with same feature columns", type=["csv"])

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)

        st.write("Uploaded Data Preview")
        st.dataframe(batch_df.head(), use_container_width=True)

        missing_cols = [col for col in feature_columns if col not in batch_df.columns]

        if missing_cols:
            st.error("Missing required columns:")
            st.write(missing_cols)
        else:
            if st.button("Run Batch Prediction", use_container_width=True):
                predictions = predict_attack(batch_df)
                batch_df["Predicted_Threat"] = predictions

                st.success("Batch prediction completed.")
                st.dataframe(batch_df.head(20), use_container_width=True)

                threat_counts = batch_df["Predicted_Threat"].value_counts().reset_index()
                threat_counts.columns = ["Threat", "Count"]

                fig = px.bar(
                    threat_counts,
                    x="Threat",
                    y="Count",
                    title="Predicted Threat Distribution"
                )

                st.plotly_chart(fig, use_container_width=True)

                csv = batch_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download Prediction Results",
                    csv,
                    "network_threat_predictions.csv",
                    "text/csv",
                    use_container_width=True
                )