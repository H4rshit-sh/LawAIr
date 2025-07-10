import streamlit as st
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load FAISS index
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("vectorstore", embedding, allow_dangerous_deserialization=True)

# Gemini setup
genai.configure(api_key="YOUR API KEY")
model = genai.GenerativeModel("gemini-2.5-pro") 

# Streamlit UI config
st.set_page_config(page_title="LawAIr", page_icon="⚖️")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
            line-height: 1.5;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }

        .stChatMessage {
            padding: 0.75rem;
            border-radius: 0.75rem;
            margin: 0.5rem 0;
            max-width: 100%;
        }

        .stMarkdown {
            font-size: 15px !important;
            white-space: pre-wrap;
        }

        .block-container {
            padding: 1rem;
        }

        @media only screen and (max-width: 768px) {
            html, body {
                font-size: 15px;
                padding: 0.5rem;
            }

            .stChatMessage {
                font-size: 14px;
            }

            .block-container {
                padding: 0.5rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚖️ LawAIr – Indian Legal Assistant")
st.markdown("Get your Legal asistance from LawAIr, an expert AI legal assistant trained on Indian law.\n\n")

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
        with st.spinner("Thinking..."):
            docs = vectorstore.similarity_search(query)
            context_blocks = []
            for doc in docs:
                section = doc.metadata.get("section", "N/A")
                title = doc.metadata.get("title", "No Title")
                act = doc.metadata.get("act", "Unknown Act")
                context_blocks.append(f"{act}\n Section {section} – {title}\n\n{doc.page_content}")

            context = "\n\n---\n\n".join(context_blocks)

            prompt = f"""
You are an expert AI legal assistant trained on Indian law.

Based on the following legal sections, answer the user's legal query in a structured, clear, and concise way.

If some sections do not match the question, politely exclude them from your answer.
only include the relevent Act and Section number.

Use this format:
---
📜 Section:
Section <number> – <section title> : <act>

💡 Explanation:
<explanation here>
---

Context:
{context}

Question: {query}
Answer:

"""
            response = model.generate_content(prompt)
            answer = response.text.strip()

            st.markdown(answer)
            st.session_state.messages.append({"role": "Assistant", "content": answer})