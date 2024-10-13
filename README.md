# RAG-based Question Answering System

This project implements a Retrieval-Augmented Generation (RAG) based question answering system with both command-line and web-based interfaces.

## Command-line Functionality

The system provides the following command-line functionalities:

1. **Create Vector Store**: 
   ```
   python rag.py create
   ```
   Creates a new vector store for document indexing.

2. **Add Documents**: 
   ```
   python rag.py add <file_path>
   ```
   Adds documents from the specified file path to the vector store.

3. **Add Images**: 
   ```
   python rag.py add_image <image_path>
   ```
   Adds images from the specified path to the vector store.

4. **Add Webpages**: 
   ```
   python rag.py add_webpages <webpage_urls>
   ```
   Adds content from specified webpage URLs to the vector store.

5. **Query Vector Store**: 
   ```
   python rag.py query "<query_string>"
   ```
   Searches the vector store for documents similar to the query string.

6. **List Documents**: 
   ```
   python rag.py list
   ```
   Lists all documents in the vector store.

7. **Remove Document**: 
   ```
   python rag.py remove <doc_id>
   ```
   Removes a specific document from the vector store.

8. **Clear Vector Store**: 
   ```
   python rag.py clear
   ```
   Removes all documents from the vector store.

9. **Ask Question**: 
   ```
   python qa.py --question "<question>"
   ```
   Asks a question to the RAG-based QA system and returns an answer.

## Web UI Functionality

The web interface provides three main pages:

1. **Indexing Page** (`/`):
   - Upload files for indexing
   - Add website links for indexing
   - Submit files and links to be added to the vector store

2. **Generation Page** (`/generation`):
   - Enter a question
   - Receive an AI-generated answer based on the indexed information

3. **Chat Page** (`/chat`):
   - Engage in a conversational interface with the AI
   - Ask questions and receive responses in a chat-like format

To run the web server:
```
python server.py
```

This will start the server and you can access the web interface through your browser at `http://localhost:8000`. 
