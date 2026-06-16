import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import math
import os
# Load environment variables
load_dotenv(r"C:\ai_search_assistant\.env")

# Get API key
api_key = os.getenv("OPEN_API_KEY")
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

# Create OpenAI client
client = OpenAI(api_key=api_key)

def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        pdf_reader = PdfReader(uploaded_file)
        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    else:
        return ""

def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start = start + chunk_size - chunk_overlap

    return chunks

def create_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def create_embeddings_for_chunks(chunks):
    embeddings = []

    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

    return embeddings

def cosine_similarity(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))

    magnitude1 = math.sqrt(sum(a * a for a in vector1))
    magnitude2 = math.sqrt(sum(b * b for b in vector2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)

def retrieve_relevant_chunks(question, chunks, chunk_embeddings, top_k=3):
    question_embedding = create_embedding(question)

    similarities = []

    for index, chunk_embedding in enumerate(chunk_embeddings):
        score = cosine_similarity(question_embedding, chunk_embedding)
        similarities.append((score, index))

    similarities.sort(reverse=True)

    top_chunks = []

    for score, index in similarities[:top_k]:
        top_chunks.append(chunks[index])

    return top_chunks

st.set_page_config(
    page_title="Sai AI Assistant",
    page_icon="🤖",
    layout="centered")

st.sidebar.title("⚙️ Settings")
st.sidebar.write("Sai AI Assistant")
# App title
st.title("🤖 Sai AI Assistant")
st.write("A multi-mode AI assistant built with Streamlit and OpenAI API.")
selected_model = st.sidebar.selectbox("Choose Model",
    ["gpt-4o-mini", "gpt-4o"])
temperature = st.sidebar.slider("Creativity",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1)
assistant_mode = st.sidebar.selectbox(
    "Assistant Mode",["General Assistant",
        "Coding Tutor",
        "Resume Helper",
        "SQL Interview Coach",
        "Python Practice Coach"])
uploaded_file = st.sidebar.file_uploader(
    "Upload a document",
    type=["pdf", "txt"]
)

document_text = ""
document_chunks = []
if uploaded_file is not None:
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    document_text = extract_text_from_file(uploaded_file)

    if document_text:
        st.sidebar.write("Document text extracted successfully ✅")
        st.sidebar.write(f"Characters extracted: {len(document_text)}")
        document_chunks = split_text_into_chunks(document_text)
        st.sidebar.write(f"Chunks created: {len(document_chunks)}")
        if st.sidebar.button("Create Document Embeddings"):
            with st.spinner("Creating embeddings..."):
                st.session_state.chunk_embeddings = create_embeddings_for_chunks(document_chunks)
            st.sidebar.success(
                f"Embeddings created: {len(st.session_state.chunk_embeddings)}")
            
    else:
        st.sidebar.warning("No text could be extracted from this file."
            "Try uploading a text-based PDF or TXT file.")

if uploaded_file is not None and document_text:
    with st.expander("📄 Document Preview"):
        st.write(document_text[:1000])

if uploaded_file is not None and document_chunks:
    with st.expander("🧩 First Chunk Preview"):
        st.write(document_chunks[0])


if assistant_mode == "Coding Tutor":
    system_content = (
        "You are Sai's coding tutor. Explain programming concepts step by step "
        "in beginner-friendly language. Do not give full advanced code immediately. "
        "Teach one small step at a time."
    )

elif assistant_mode == "Resume Helper":
    system_content = (
        "You are Sai's resume and job application assistant. Help tailor resumes, "
        "cover letters, and recruiter messages in an honest, ATS-friendly, professional way."
    )

elif assistant_mode == "SQL Interview Coach":
    system_content = (
        "You are Sai's SQL interview coach. Give SQL practice questions, explain queries "
        "step by step, and focus on SELECT, WHERE, GROUP BY, HAVING, JOINs, and subqueries."
    )

elif assistant_mode == "Python Practice Coach":
    system_content = (
        "You are Sai's Python practice coach. Give beginner-friendly Python exercises "
        "on variables, lists, loops, functions, dictionaries, and problem solving."
    )

else:
    system_content = (
        "You are Sai's AI Assistant. Give clear, helpful, practical, and beginner-friendly answers."
    )

system_prompt = {
    "role": "system",
    "content": system_content
}
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Create chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunk_embeddings" not in st.session_state:
    st.session_state.chunk_embeddings = []

if len(st.session_state.messages) == 0:
    st.info("Welcome Sai 👋 Ask me anything below.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
user_question = st.chat_input("Ask anything:")

# Button click
if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.write(user_question)

    # Send request to OpenAI
    with st.spinner("Thinking..."):

        messages_to_send = [system_prompt] + st.session_state.messages

        if uploaded_file is not None and document_chunks and st.session_state.chunk_embeddings:
            relevant_chunks = retrieve_relevant_chunks(
                user_question,
                document_chunks,
                st.session_state.chunk_embeddings,
                top_k=3
            )

            document_context = "\n\n".join(relevant_chunks)

            document_prompt = {
                "role": "system",
                "content": (
                    "Use the following document context to answer the user's question. "
                    "If the answer is not found in the document, say that it is not found in the uploaded document.\n\n"
                    f"Document Context:\n{document_context}"
                )
            }

            messages_to_send = [system_prompt, document_prompt] + st.session_state.messages

        response = client.chat.completions.create(
            model=selected_model,
            messages=messages_to_send,
            temperature=temperature
        )

        ai_answer = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_answer}
    )

    with st.chat_message("assistant"):
        st.write(ai_answer)

#cd C:\ai_search_assistant
#py -m streamlit run app.py