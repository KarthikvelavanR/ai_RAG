🎓 College Admission Assistant (RAG-based Chatbot)

## Overview

This project is an AI-powered chatbot that provides guidance on college admissions. It uses **Retrieval-Augmented Generation (RAG)** to answer user queries based on a structured dataset of universities, admission requirements, and application details.

The system retrieves relevant information from a dataset and generates accurate, context-aware responses using a Large Language Model (LLM).

## 🚀 Features

* 🔍 Semantic search using FAISS vector database
* 🤖 LLM-powered responses using Groq (Llama 3)
* 📊 Handles admission queries (GRE, TOEFL, CGPA, deadlines, etc.)
* 🧠 Supports reasoning-based queries (profile evaluation)
* 🚫 Out-of-domain detection (prevents irrelevant answers)
* 💻 Custom frontend using HTML, CSS, JavaScript
* ⚡ FastAPI backend for efficient API handling

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** HTML, CSS, JavaScript
* **Vector Database:** FAISS
* **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **LLM:** Groq (Llama 3.1)
* **Language:** Python

## 🧠 How It Works (RAG Pipeline)

1. Dataset is converted into structured text documents
2. Text is converted into embeddings using Sentence Transformers
3. Embeddings are stored in FAISS vector database
4. User query is converted into embedding
5. FAISS retrieves most relevant documents
6. Retrieved context + query is sent to LLM (Groq)
7. LLM generates final response
8. Response is displayed in UI

## 📁 Project Structure

```
AI_MINI/
├── main.py                  # FastAPI backend
├── app.py                   # (optional older version)
├── frontend/                # UI files
│   ├── index.html
│   ├── style.css
│   └── script.js
├── faiss_index/             # Vector DB (ignored in Git)
├── final_dataset_expanded.csv
├── processed_documents.csv
├── processed_documents.txt
├── .gitignore
├── .env                     # API key (ignored)
```

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Add environment variables

Create a `.env` file and add:

```
GROQ_API_KEY=your_api_key_here
```

### 4️⃣ Run the backend

```
uvicorn main:app --reload
```

### 5️⃣ Open the application

```
http://127.0.0.1:8000
```

## 💡 Example Queries

* Give details of University of Toronto
* List universities in USA
* I have GRE 305 and TOEFL 91, suggest colleges
* What documents are required for MIT?

---

## ⚠️ Limitations

* Depends on dataset quality
* No real-time updates
* Approximate reasoning for unseen queries

## 🔐 Security Note

* `.env` file is excluded from Git
* API keys are not exposed

