import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv


st.markdown(
    """
    <style>
    body {
        color: #333;
        background-color: #f4f4f4;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .header {
        padding: 2rem 0;
        background: linear-gradient(45deg, #2e8b57, #3cb371);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .stApp {
        #max-width: 70%;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }
    .header-container {
        padding: 20px;
        text-align: center;
        background-color: #e9ecef;
        border-bottom: 1px solid #dee2e6;
    }
    h1 {
        color: #2c3e50;
        margin-bottom: 10px;
        font-weight: bold;
    }
    p {
        color: #555;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    .main-container {
        flex: 1;
        display: flex;
        flex-direction: column; /* Changed to column */
        padding: 20px;
        align-items: center; /* Added to center content horizontally */
    }
    .content-area {
        flex: 1;
        padding: 20px;
        border-radius: 10px;
        margin-top: 0;
        width: 100%; /* Make content area full width */
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
        font-size: 16px;
        width: 100%;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s ease;
        margin-top: 10px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stButton > button:active {
        background-color: #388e3c;
    }
    .stWarning {
        color: #856404;
        background-color: #fff3cd;
        border-left: 4px solid #ffeeba;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .stHeader {
        color: #2c3e50;
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stCodeBlock {
        background-color: #f0f0f0;
        border: 1px solid #e0e0e0;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        overflow-x: auto;
        font-family: monospace;
        font-size: 14px;
        line-height: 1.4;
    }
    .sample-prompt {
        background-color: #e9ecef;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #495057;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
FAISS_DB_PATH = "faiss_index"

@st.cache_resource(show_spinner="⚡ Loading Faiss vector store...")
def get_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    if os.path.exists(FAISS_DB_PATH):
        return FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        st.warning("⚠️ No existing Faiss DB found. Creating one...")

vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, max_tokens=500)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, make up the answer "
    "using your own knowledge. Must use bullet points. "
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Header 
header_container = st.container()
with header_container:
    st.markdown("<h1 style='text-align: center;'>AI-Powered Peatland & Carbon Footprint Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Get instant answers about peatlands, carbon sequestration, and related topics.</p>", unsafe_allow_html=True)


# Main content
main_container = st.container()
with main_container:
    content_area = st.container()

    with content_area:

        user_query = st.text_input("**Enter your question:**", placeholder="Ask me anything about peatlands...")

        if st.button("Ask AI"):
            if user_query:
                response = rag_chain.invoke({"input": user_query})
                st.subheader("🤖 AI Response")
                st.write(response["answer"])
            else:
                st.warning("⚠️ Please enter a question before asking the AI.")

        # st.markdown("<br><hr style='border:1px solid #ccc'><br>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("**Here are some sample prompts, customize as needed:**")
        sample_prompts = [
            "My peatland has NDVI of 0.45, NDMI of 0.52, and NDWI of 0.25. What does it mean for its health and restoration status?",
            "I have a peatland area of 50 hectares ,with an average depth of 2 meters. Estimate the carbon sequestration potential and how it can be improved.",
            "My NDVI is 0.62, NDMI is 0.67, and NDWI is 0.35. What conservation or restoration steps should I take based on these values?",
            "I'm monitoring a peatland in Riau, Indonesia. How do my NDVI and NDMI values compare to ideal peatland health benchmarks globally?",
            "My peatland has been drained and has a history of fire. What are the best restoration techniques I should consider to recover it?",
            "I have NDVI values from 2018 to 2024 showing a declining trend. What does this indicate about peatland degradation, and what actions should I take?",
            "How do peatlands help mitigate climate change and what role do NDVI, NDMI, and NDWI play in understanding that impact?",
        ]
        for prompt in sample_prompts:
            st.markdown(f"<div class='sample-prompt'>{prompt}</div>", unsafe_allow_html=True)


# @st.cache_resource(show_spinner="⚡ Loading FAISS vector store...")
# def get_vectorstore():
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     faiss_db_path = "./faiss_index"

#     if os.path.exists(faiss_db_path):
#         vectorstore = FAISS.load_local(faiss_db_path, embeddings, allow_dangerous_deserialization=True)
#     else:
#         st.warning("⚠️ No existing FAISS index found. Please create one first.")
#         vectorstore = None

#     return vectorstore

# from langchain_community.vectorstores import FAISS

# # Assuming you have a list of Documents already
# docs = [...]  # your documents from PDF or elsewhere
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# # Build FAISS
# vectorstore = FAISS.from_documents(docs, embeddings)

# # Save it to disk
# vectorstore.save_local("./faiss_index")

# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})

# @st.cache_resource(show_spinner="⚡ Loading FAISS vector store...")
# def get_vectorstore():
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
#     faiss_db_path = "./faiss_index"

#     if os.path.exists(faiss_db_path):
#         vectorstore = FAISS.load_local(faiss_db_path, embeddings, allow_dangerous_deserialization=True)
#     else:
#         st.warning("⚠️ No existing FAISS index found. Please create one first.")
#         vectorstore = None

#     return vectorstore

