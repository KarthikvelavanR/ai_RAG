import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

# LOAD ENV
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# INIT FASTAPI

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LOAD FAISS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#faiss loading error handling:
try:
    vector_db = FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    print("FAISS loaded successfully!")
except Exception as e:
    print("Error loading FAISS index:", str(e))
    vector_db = None

# GROQ
client = Groq(api_key=api_key)


# REQUEST MODEL
class QueryRequest(BaseModel):
    message: str

# HELPER FUNCTIONS
def is_relevant_query(query):
    keywords = ["university", "college", "admission", "gre", "toefl", "cgpa", "deadline", "documents"]
    return any(k in query.lower() for k in keywords)

def is_profile_query(query):
    keywords = ["i have", "my score", "can i", "profile", "chance"]
    return any(k in query.lower() for k in keywords)

# RAG FUNCTION
def ask_chatbot(query):

    if not is_relevant_query(query):
        return "This question is outside my domain."
    
    if vector_db is None:
        return "System error: Vector database not available."
    
    #retrieval safety
    try:
        docs = vector_db.similarity_search(query, k=15)
    except Exception as e:
        return "Error retrieving data. Please try again."
    
    #empty retrieval case:
    if not docs:
        return "No relevant data found for your query."
    
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are an intelligent college admission assistant.

    Use the provided context to answer the question.
    If exact information is not available, analyze similar universities and provide a reasonable estimate.

    Do NOT say "Not available" immediately.
    If unrelated → say "This question is outside my domain."

    Context:
    {context}

    User Query:
    {query}

    Answer clearly with reasoning:
    """

#GROQ api error handling:
    try:
        response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
        return response.choices[0].message.content

    except Exception as e:
        return "LLM service is currently unavailable. Please try again later."


# ROUTES
@app.get("/")
def serve_html():
    return FileResponse("frontend/index.html")


@app.post("/chat")
def chat(request: QueryRequest):
    answer = ask_chatbot(request.message)
    return {"response": answer}
