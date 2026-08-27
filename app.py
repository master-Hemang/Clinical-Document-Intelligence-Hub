import streamlit as st
from google import genai
from google.genai import types
import json

# --- Configuration & API Setup ---
st.set_page_config(page_title="Clinical Intelligence Hub", page_icon="🏥", layout="wide")

# ⚠️ HARDCODE YOUR API KEY HERE ⚠️
API_KEY = "YOUR_API_KEY_HERE" 
# --- UI Styling & Sidebar ---
st.markdown("""
    <style>
    .big-font {font-size:22px !important; font-weight: bold; color: #1E3A8A;}
    .metric-card {background-color: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.title("Admin Panel")
    st.markdown("Upload patient records to automatically extract structured intelligence, risk profiles, and next steps.")
    st.info("Supported formats: TXT, PDF, PNG, JPG")
    st.divider()

# --- Main Header ---
st.title("🏥 Clinical Document Intelligence Hub")
st.markdown("<p class='big-font'>Automated Triage & Structuring System</p>", unsafe_allow_html=True)
st.divider()

# --- Multi-File Uploader ---
uploaded_files = st.file_uploader(
    "Upload Clinical Documents (Intake forms, Discharge notes, Lab results)", 
    type=["txt", "pdf", "png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

SYSTEM_PROMPT = """
You are an expert clinical AI assistant. Extract key information from the provided medical document.
Return ONLY a valid JSON object with the exact following keys (do not include markdown code blocks like ```json):
{
  "patient_summary": "A 2-sentence clinical summary.",
  "key_findings": ["Finding 1", "Finding 2"],
  "risk_flag": "Low, Medium, or High",
  "recommended_next_step": "One actionable recommendation",
  "confidence_score": 95
}
"""

# --- Processing Logic ---
if st.button("Process Documents", type="primary") and uploaded_files:
    if API_KEY == "YOUR_API_KEY_HERE":
        st.error("🚨 Please enter your real API Key in the app.py script (Line 10) before processing.")
        st.stop()

    client = genai.Client(api_key=API_KEY)
    
    with st.spinner(f"Analyzing {len(uploaded_files)} document(s)..."):
        tabs = st.tabs([file.name for file in uploaded_files])
        
        for i, file in enumerate(uploaded_files):
            with tabs[i]:
                try:
                    # 1. Prepare Document for Gemini
                    mime_type = file.type
                    file_bytes = file.getvalue()

                    if mime_type == "text/plain":
                        # If text, decode to string
                        doc_data = file_bytes.decode("utf-8")
                    else:
                        # If PDF or Image, pass bytes directly using the genai types module
                        doc_data = types.Part.from_bytes(
                            data=file_bytes,
                            mime_type=mime_type
                        )
                    
                    # 2. Call the Model
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[SYSTEM_PROMPT, doc_data]
                    )

                    # 3. Parse JSON safely
                    raw_text = response.text.strip()
                    if raw_text.startswith("```json"):
                        raw_text = raw_text[7:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]
                    
                    data = json.loads(raw_text.strip())
                    risk = data.get("risk_flag", "Unknown")
                    
                    # --- 4. Render Polished Output ---
                    col1, col2, col3 = st.columns(3)
                    
                    if risk == "High":
                        col1.error(f"🚨 **Risk Flag:** {risk}")
                    elif risk == "Medium":
                        col1.warning(f"⚠️ **Risk Flag:** {risk}")
                    else:
                        col1.success(f"✅ **Risk Flag:** {risk}")
                        
                    col2.metric("AI Confidence Score", f"{data.get('confidence_score', 0)}%")
                    col3.metric("Action Required", "Urgent" if risk in ["High"] else "Routine")

                    st.markdown("---")
                    
                    left_col, right_col = st.columns([1.5, 1])
                    
                    with left_col:
                        st.subheader("📋 Patient Summary")
                        st.write(data.get("patient_summary"))
                        
                        st.subheader("🔍 Key Findings")
                        for finding in data.get("key_findings", []):
                            st.markdown(f"- {finding}")
                            
                    with right_col:
                        st.subheader("🩺 Recommended Next Step")
                        st.info(data.get("recommended_next_step"))
                        
                        with st.expander("View Raw JSON Output"):
                            st.json(data)
                            
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
