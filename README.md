# 🏥 Clinical Document Intelligence Hub

## 📌 Overview
The **Clinical Document Intelligence Hub** is a rapid proof-of-concept (PoC) designed to alleviate the administrative and clinical burden of manually reviewing unstructured patient records. 

By leveraging state-of-the-art multimodal Generative AI, this application ingests messy, unstructured healthcare documents (intake forms, clinical notes, scanned PDFs, and images) and instantly transforms them into structured, actionable Patient Summary Cards.

## 🚀 Approach & Architecture
Instead of relying on legacy, multi-step OCR (Optical Character Recognition) pipelines and separate NLP entity-extraction models, this solution uses a **single Multimodal LLM architecture**. 

1. **Ingestion:** A Streamlit frontend accepts batch uploads of various file types (TXT, PDF, PNG, JPG).
2. **Multimodal Processing:** The raw bytes of the documents are passed directly to Google's Gemini model.
3. **Structured Extraction:** Using strict prompt engineering, the LLM is forced to output a consistent JSON schema bypassing conversational filler.
4. **Dynamic Visualization:** The UI parses the JSON and renders it into a clinical dashboard, utilizing dynamic color-coding (Red/Yellow/Green) based on the AI-determined clinical risk flag.

## 🛠️ Tech Stack & Tools Used
* **Frontend UI:** [Streamlit](https://streamlit.io/) (Python) - Chosen for its rapid prototyping capabilities and clean, interactive components.
* **AI Engine:** Google Gemini 3.5 Flash (`google-genai` SDK) - Chosen for its native multimodal capabilities (ability to "read" PDFs and images natively) and blazing-fast inference speeds.
* **Data Parsing:** Native Python `json` library for schema enforcement.

## ⚙️ Setup and Installation

### Prerequisites
* Python 3.9 or higher
* A valid Google Gemini API Key

Open app.py in your code editor and ensure your API key is placed on Line 10:

Python
API_KEY = "YOUR_API_KEY_HERE"
(Note: For this 1-day rapid prototype, the API key is hardcoded. In a production environment, this would be managed via Streamlit Secrets or environment variables).

Run the application:

Bash
streamlit run app.py
The application will automatically open in your default web browser at http://localhost:8501.

🧠 Assumptions Made
Human-in-the-Loop: This tool is designed to assist administrative and clinical staff with triage and data extraction, not replace clinical judgment. All AI-generated outputs assume a human will verify the findings.

Language: The current prompt and extraction logic assume the input clinical documents are primarily in English.

Document Quality: The system generates a "Confidence Score" (1-100%). It assumes that heavily degraded, blurry, or illegible handwriting in images will yield lower confidence scores and flag the document for manual review.

📊 Example: Input and Output
Sample Input (Unstructured Text / PDF)
Radiology Report - 11/05/2026
Patient: Arthur Dent. Clinical Indication: 71-year-old male presenting with productive cough, fever, and hypoxia.
Findings: There is a dense focal consolidation in the right lower lobe with visible air bronchograms. Blunting of the right costophrenic angle, consistent with pleural effusion.
Impression: Right lower lobe consolidation highly suspicious for acute bacterial pneumonia. Recommend urgent clinical correlation and empiric antibiotics.

Sample AI Output (Structured JSON)
JSON
{
  "patient_summary": "71-year-old male presenting with hypoxia, fever, and a productive cough underwent a chest X-ray. Imaging reveals a right lower lobe consolidation and pleural effusion.",
  "key_findings": [
    "Dense focal consolidation in the right lower lobe",
    "Visible air bronchograms",
    "Right-sided pleural effusion",
    "Suspicion for acute bacterial pneumonia"
  ],
  "risk_flag": "High",
  "recommended_next_step": "Urgent clinical correlation and initiation of empiric antibiotic therapy.",
  "confidence_score": 98
}
In the UI, this output renders as a red, high-priority alert card, instantly notifying staff that this document requires immediate action.

Developed for the Clinical Document Intelligence Hub challenge.

### Installation Steps
1. Clone this repository or download the source code.
2. Install the required Python dependencies:
   ```bash
   pip install streamlit google-genai
