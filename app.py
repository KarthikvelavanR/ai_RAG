import streamlit as st
import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="College Admission Chatbot", layout="wide")

st.title("College Admission Assistant")
st.write("Ask anything about college admissions (eligibility, deadlines, documents, etc.)")

# -----------------------------
# LOAD FAISS (CACHE FOR SPEED)
# -----------------------------
@st.cache_resource
def load_vector_db():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

vector_db = load_vector_db()

# -----------------------------
# GROQ SETUP
# -----------------------------
client = Groq(api_key=api_key)

# -----------------------------
# RAG FUNCTION
# -----------------------------
def ask_chatbot(query):
    docs = vector_db.similarity_search(query, k=15)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are an intelligent college admission assistant.

    Use the provided context to answer the question.
    If exact information is not available, analyze similar universities and provide a reasonable estimate.

    Do NOT say "Not available" immediately.
    Try to infer based on similar data.
    If the prompt is out of topic or domain, just don't make assumptions on your own.Just say out of domain.

    Context:
    {context}

    Student Profile:
    {query}

    Answer clearly with reasoning:
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# -----------------------------
# CHAT INTERFACE
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("Enter your question:")

if st.button("Ask") and query:
    answer = ask_chatbot(query)

    st.session_state.chat_history.append(("You", query))
    st.session_state.chat_history.append(("Bot", answer))

# -----------------------------
# DISPLAY CHAT
# -----------------------------
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")