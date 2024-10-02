#!/usr/bin/env python3

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
from rag import RAGVectorStore
from qa import QAChat
import os

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Initialize RAGVectorStore and QAChat
rag_store = RAGVectorStore()
qa_chat = QAChat()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("rag_index.html", {"request": request})

@app.get("/generation", response_class=HTMLResponse)
async def generation(request: Request):
    return templates.TemplateResponse("generation.html", {"request": request})

@app.post("/index")
async def index_files(files: List[UploadFile] = File(...), websites: str = Form(...)):
    # Process uploaded files
    for file in files:
        contents = await file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)
        rag_store.add_documents([file.filename])
        os.remove(file.filename)  # Clean up temporary file

    # Process websites
    if websites:
        website_list = [website.strip() for website in websites.split(',') if website.strip()]
        rag_store.add_webpages(website_list)

    return {"message": "Indexing completed successfully"}

@app.post("/generate")
async def generate(question: str = Form(...)):
    answer = qa_chat.ask_question(question)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
