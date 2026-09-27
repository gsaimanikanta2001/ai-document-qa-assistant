# Sai AI Assistant | Document Q&A

A **Python + Streamlit** chat app with five assistant modes and single-document question answering. Users can upload a PDF or TXT file, extract its text, create embeddings, retrieve relevant chunks using cosine similarity, and send those chunks to an OpenAI chat model as context.

![Document Q&A screen](Ai_search_assistant_q%24a.png)

## What is implemented

- General Assistant, Coding Tutor, Resume Helper, SQL Interview Coach, and Python Practice Coach modes
- PDF text extraction with PyPDF and TXT upload
- Overlapping, character-based chunks; `text-embedding-3-small` embeddings
- Top-three cosine-similarity retrieval and an OpenAI chat completion
- Streamlit chat history, model and temperature controls, and a clear-chat button

[Inspect the application code](app.py) and [additional screenshots](Ai_search_assistant_welcomepage.png).

## Run locally

1. Install Python 3 and run `pip install -r Requirements.txt`.
2. Obtain an OpenAI API key. Create a local `.env` file beside `app.py` containing `OPEN_API_KEY=your_key_here`, or set that environment variable in your shell. Never commit the key or `.env`. Do not commit your key or `.env`.
3. Run `streamlit run app.py`.
4. Upload a text-based PDF or TXT document and select **Create Document Embeddings**, then ask a question. OpenAI API requests for embeddings and chat may incur charges.

The current app does not extract text from scanned-image PDFs. It handles one uploaded document at a time.

## How document answers work

`upload → extract text → split into overlapping chunks → embed chunks → embed question → rank by cosine similarity → pass top chunks to chat model`

Document text is sent to the OpenAI API for embeddings and retrieved chunks are sent as chat context. Use a non-sensitive sample document when trying the demo.

## Limitations and next steps

This is a small in-memory RAG demonstration, not a validated knowledge system. The interface does not display source citations or retrieval scores. It has no vector database, persistence, or documented answer-quality benchmark. The app asks the model to say when an answer is absent, but that prompt alone cannot guarantee grounded answers. The app rebuilds embeddings when a different document is uploaded; embeddings still live only in the current session.

Next improvements: passage citations with page numbers, a small evaluation set with expected answers, and a deployment guide.

## Skills shown

Python, Streamlit, PDF text extraction, OpenAI API integration, embeddings, similarity search, prompt design, and interactive application development.
