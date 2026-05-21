#!/usr/bin/env python3
"""
Simple CLI tool for PDF upload and queries
Usage: python cli.py --help
"""
import argparse
import requests
import json
import sys
from pathlib import Path

API_PROCESSOR = "http://localhost:8000"
API_QUERY = "http://localhost:8001"

def upload_pdfs(pdf_files):
    """Upload PDF files"""
    try:
        files = [('files', open(f, 'rb')) for f in pdf_files]
        response = requests.post(f"{API_PROCESSOR}/upload", files=files)
        
        for _, file in files:
            file.close()
        
        if response.status_code == 200:
            results = response.json()
            print("\n✅ Upload Results:")
            for filename, result in results.items():
                if result['status'] == 'success':
                    print(f"  ✓ {filename}: {result['chunks']} chunks")
                else:
                    print(f"  ✗ {filename}: {result['message']}")
        else:
            print(f"❌ Upload failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def query_documents(question, num_results=3):
    """Query documents"""
    try:
        payload = {"query": question, "num_results": num_results}
        response = requests.post(f"{API_QUERY}/query", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n🤖 Answer:\n{result['answer']}\n")
            print("📖 Sources:")
            for i, source in enumerate(result['sources'], 1):
                print(f"  {i}. {source['source']} (chunk {source['chunk_index']})")
        else:
            print(f"❌ Query failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def get_status():
    """Get system status"""
    try:
        response = requests.get(f"{API_PROCESSOR}/status")
        if response.status_code == 200:
            status = response.json()
            print(f"\n📊 System Status:")
            print(f"  Uploaded PDFs: {status['uploaded_pdfs']}")
            print(f"  Files: {', '.join(status['files']) if status['files'] else 'None'}")
    except Exception as e:
        print(f"❌ Error: {e}")

def interactive_query():
    """Interactive query mode"""
    print("\n🔍 Interactive Query Mode (type 'exit' to quit)")
    while True:
        try:
            question = input("\nYou: ").strip()
            if question.lower() == 'exit':
                break
            if question:
                query_documents(question)
        except KeyboardInterrupt:
            break

def main():
    parser = argparse.ArgumentParser(
        description="PDF RAG Pipeline CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --upload document.pdf another.pdf
  python cli.py --query "What is the main topic?"
  python cli.py --interactive
  python cli.py --status
        """
    )
    
    parser.add_argument('--upload', nargs='+', help='Upload PDF files')
    parser.add_argument('--query', type=str, help='Query the documents')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--num-results', type=int, default=3, help='Number of results')
    
    args = parser.parse_args()
    
    if args.upload:
        print("📤 Uploading PDFs...")
        upload_pdfs(args.upload)
    
    if args.query:
        print(f"❓ Querying: {args.query}")
        query_documents(args.query, args.num_results)
    
    if args.interactive:
        interactive_query()
    
    if args.status:
        get_status()
    
    if not any([args.upload, args.query, args.interactive, args.status]):
        parser.print_help()

if __name__ == "__main__":
    main()
