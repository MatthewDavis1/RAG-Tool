#!/usr/bin/env python3

from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
from rag import RAGVectorStore
from qa import QAChat
import os
import uuid
import json

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Initialize RAGVectorStore and QAChat
rag_store = RAGVectorStore()
qa_chat = QAChat()

# Store chat history
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("rag_index.html", {"request": request})

@app.get("/generation", response_class=HTMLResponse)
async def generation(request: Request):
    return templates.TemplateResponse("generation.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "chat_history": chat_history})

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        user_message = json.loads(data)["message"]
        chat_history.append({"role": "user", "content": user_message})
        
        # Generate AI response
        ai_response = qa_chat.ask_question(user_message)
        chat_history.append({"role": "ai", "content": ai_response})
        
        await websocket.send_json({"message": ai_response})

@app.post("/index")
async def index_files(files: List[UploadFile] = File(...), websites: List[str] = Form(...)):
    # Validate inputs
    if not files and not websites:
        raise HTTPException(status_code=400, detail="No files or websites provided.")

    # Process uploaded files
    for file in files:
        if not file.filename:
            continue  # Skip files without a filename
        try:
            contents = await file.read()
            temp_filename = f"temp_{uuid.uuid4().hex}_{file.filename}"
            with open(temp_filename, "wb") as f:
                f.write(contents)
            rag_store.add_documents([temp_filename])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process file {file.filename}: {str(e)}")
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)  # Clean up temporary file

    # Process websites
    if websites:
        website_list = [website.strip() for website in websites if website.strip()]
        if website_list:
            try:
                rag_store.add_webpages(website_list)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process websites: {str(e)}")

    return {"message": "Indexing completed successfully"}

@app.post("/generate")
async def generate(question: str = Form(...)):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        answer = qa_chat.ask_question(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)