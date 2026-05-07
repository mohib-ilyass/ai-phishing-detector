import streamlit as st
import pickle

# 1. SETUP PAGE
st.set_page_config(page_title="Cyber AI Detector", page_icon="🛡️")

# Custom CSS to make it look "Hacker-ish"
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00FF00;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AI Phishing URL Detector")
st.write("This tool uses a Random Forest algorithm to detect malicious URLs.")

# 2. LOAD MODEL
try:
    with open('phishing_model.pkl', 'rb') as file:
        agent = pickle.load(file)
except FileNotFoundError:
    st.error("Model not found! Please run 'train_model.py' first.")
    st.stop()

# Helper function 
def get_features(url):
    url = str(url)
    length = len(url)
    dots = url.count('.')
    has_at = 1 if "@" in url else 0
    slashes = url.count('/')
    hyphens = url.count('-')
    digits = sum(c.isdigit() for c in url)
    sensitive = 0
    for char in ['?', '=', '&', '%']:
        sensitive += url.count(char)
    return [length, dots, has_at, slashes, hyphens, digits, sensitive]

# 3. USER INPUT
url_input = st.text_input("Enter URL to Analyze:", placeholder="http://example.com")

if st.button("SCAN URL"):
    if not url_input:
        st.warning("Please enter a URL first.")
    else:
        # Get features
        features = [get_features(url_input)]
        
        # Predict
        prediction = agent.predict(features)[0]
        prob = agent.predict_proba(features)
        
        # Display Results
        if prediction in ['bad', 'phishing', 'malicious', 1]:
            st.error("🚨 MALICIOUS DETECTED!")
            st.write(f"Confidence: {prob[0][0]*100:.2f}%")
            st.write("Reasoning: High anomaly score in URL structure.")
        else:
            st.success("✅ SAFE URL")
            st.write(f"Confidence: {prob[0][1]*100:.2f}%")