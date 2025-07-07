import streamlit as st
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load FAISS index
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("vectorstore", embedding, allow_dangerous_deserialization=True)

# Gemini setup
genai.configure(api_key="AIzaSyBSJtBrvboEoXGBL5U6eZHIQLy_r1r-ka8")
model = genai.GenerativeModel("gemini-2.5-pro") 

# Streamlit UI config
st.set_page_config(page_title="LawAIr", page_icon="⚖️")
st.title("⚖️ LawAIr – Indian Legal Assistant")
st.markdown("Ask questions from Indian Penal Code (IPC) and get answers.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
query = st.chat_input("Ask your question...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("Assistant"):
        with st.spinner("🤖 Thinking..."):
            docs = vectorstore.similarity_search(query)
            context = "\n\n".join([doc.page_content for doc in docs])

            prompt = f"""
You are an AI legal assistant, Lawyer trained on the Indian Penal Code (IPC).
Use the following legal sections to answer clearly and correctly.

Context:
{context}

Question: {query}
Answer:

"""
            response = model.generate_content(prompt)
            answer = response.text.strip()

            st.markdown(answer)
            st.session_state.messages.append({"role": "Assistant", "content": answer})