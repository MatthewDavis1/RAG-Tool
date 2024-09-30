#!/usr/bin/env python3

import argparse
import os
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader

# Get VECTOR_STORE_PATH from environment variable
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH")
if not VECTOR_STORE_PATH:
    print("Error: VECTOR_STORE_PATH environment variable is not set.")
    sys.exit(1)

def create_vector_store():
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(persist_directory=os.path.abspath(VECTOR_STORE_PATH), embedding_function=embeddings)
    print(f"Vector store created at '{VECTOR_STORE_PATH}'")

def add_documents(file_path):
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(persist_directory=os.path.abspath(VECTOR_STORE_PATH), embedding_function=embeddings)
    loader = TextLoader(file_path, encoding='utf8')
    documents = loader.load()
    vector_store.add_documents(documents)
    print(f"Added documents from '{file_path}' to the vector store.")

def query_vector_store(query):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(persist_directory=os.path.abspath(VECTOR_STORE_PATH), embedding_function=embeddings)
    docs = vector_store.similarity_search(query)
    for doc in docs:
        print(f"Document ID: {doc.metadata['source']}")
        print(f"Content: {doc.page_content}\n")

def list_documents():
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(persist_directory=os.path.abspath(VECTOR_STORE_PATH), embedding_function=embeddings)
    docs = vector_store.get()
    if docs["ids"] and docs["documents"]:
        for id, document in zip(docs["ids"], docs["documents"]):
            print(f"Document ID: {id}")
            print(f"Document: {document[:100]}")
            print("\n-----------------------------------\n")
    else:
        print("No documents found.")

def remove_document(doc_id):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(persist_directory=os.path.abspath(VECTOR_STORE_PATH), embedding_function=embeddings)
    vector_store.delete(ids=[doc_id])
    print(f"Removed document with ID '{doc_id}' from the vector store.")

def main():
    parser = argparse.ArgumentParser(description="RAG Script with LangChain")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create vector store
    subparsers.add_parser("create", help="Create a new vector store")

    # Add documents
    add_parser = subparsers.add_parser("add", help="Add documents to the vector store")
    add_parser.add_argument("file_path", type=str, help="Path to the document file")

    # Query
    query_parser = subparsers.add_parser("query", help="Query the vector store")
    query_parser.add_argument("query", type=str, help="Query string")

    # List documents
    subparsers.add_parser("list", help="List all documents in the vector store")

    # Remove document
    remove_parser = subparsers.add_parser("remove", help="Remove a document from the vector store")
    remove_parser.add_argument("doc_id", type=str, help="ID of the document to remove")

    args = parser.parse_args()

    if args.command == "create":
        create_vector_store()
    elif args.command == "add":
        add_documents(args.file_path)
    elif args.command == "query":
        query_vector_store(args.query)
    elif args.command == "list":
        list_documents()
    elif args.command == "remove":
        remove_document(args.doc_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()