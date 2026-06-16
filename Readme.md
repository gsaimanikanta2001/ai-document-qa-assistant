# Sai AI Assistant — Multi-Mode AI Chatbot with Document Q&A

Sai AI Assistant is a multi-mode AI chatbot built using Python, Streamlit, and the OpenAI API. The application allows users to chat with an AI assistant, switch between different assistant modes, upload PDF or TXT documents, and ask questions based on the uploaded document using a Retrieval-Augmented Generation (RAG) workflow.

This project was built to demonstrate practical skills in AI application development, document processing, embeddings, semantic search, and interactive web app design.

## Project Overview

The goal of this project is to create a simple but useful AI assistant that can answer general questions and also respond based on uploaded documents.

Users can upload a PDF or TXT file, generate embeddings for the document, and ask questions about the content. The app retrieves the most relevant document chunks and sends them to the AI model as context, allowing the assistant to provide document-aware answers.

If the answer is not available in the uploaded document, the assistant is instructed to clearly say that the information was not found in the document.

## Key Features

* Built an interactive AI chatbot using Streamlit and OpenAI API
* Added multiple assistant modes for different use cases
* Supported PDF and TXT document upload
* Extracted text from uploaded documents using PyPDF
* Split document text into smaller overlapping chunks
* Generated embeddings using OpenAI `text-embedding-3-small`
* Implemented cosine similarity to compare user questions with document chunks
* Retrieved the top relevant chunks for document-based question answering
* Added RAG-style document context to improve answer accuracy
* Included chat history using Streamlit session state
* Added sidebar controls for model selection, creativity level, assistant mode, and document upload
* Added clear chat functionality for better user experience

## Assistant Modes

The application includes multiple assistant modes:

* General Assistant
* Coding Tutor
* Resume Helper
* SQL Interview Coach
* Python Practice Coach

Each mode uses a different system prompt, allowing the assistant to respond in a way that matches the selected use case.

## Tech Stack

* Python
* Streamlit
* OpenAI API
* OpenAI Embeddings
* PyPDF
* Python-dotenv
* Cosine Similarity
* Retrieval-Augmented Generation
* Session State Management

## How It Works

1. The user uploads a PDF or TXT document.
2. The application extracts text from the uploaded file.
3. The extracted text is split into smaller chunks.
4. Embeddings are created for each document chunk.
5. When the user asks a question, the question is also converted into an embedding.
6. The app compares the question embedding with document chunk embeddings using cosine similarity.
7. The most relevant chunks are selected.
8. The selected chunks are passed to the AI model as document context.
9. The assistant answers based on the retrieved document context.

## Project Workflow
Upload Document
        ↓
Extract Text
        ↓
Split Text into Chunks
        ↓
Create Embeddings
        ↓
User Asks Question
        ↓
Retrieve Relevant Chunks
        ↓
Send Context to OpenAI Model
        ↓
Generate Document-Based Answer

## Skills Demonstrated

This project demonstrates practical experience with:

* AI chatbot development
* Prompt engineering
* OpenAI API integration
* Embedding-based semantic search
* Document Q&A
* Retrieval-Augmented Generation
* Python application development
* Streamlit web app development
* PDF text extraction
* User interface design
* Session state handling
* Real-world problem solving

## Future Improvements

Possible future improvements include:

* Add support for multiple document uploads
* Store embeddings in a vector database
* Add source citation for retrieved document chunks
* Add login/user authentication
* Deploy the application online
* Improve UI layout and styling
* Add downloadable chat history

## Why I Built This Project

I built this project to strengthen my practical understanding of AI-powered applications and document-based question answering. The project helped me understand how embeddings, semantic search, and RAG workflows can be combined to create useful AI tools for real-world use cases such as resume analysis, document summarization, interview preparation, and knowledge search.

## Project Status

Completed core version.

The application currently supports chatbot interaction, assistant modes, document upload, text extraction, chunking, embeddings, semantic retrieval, and document-based responses.
