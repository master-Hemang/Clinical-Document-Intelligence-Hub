# Clinical-Document-Intelligence-Hub

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

### Installation Steps
1. Clone this repository or download the source code.
2. Install the required Python dependencies:
   ```bash
   pip install streamlit google-genai
