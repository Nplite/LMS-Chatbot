import streamlit as st
import ollama
from src.document_processor import DocumentProcessor
import tempfile
import os



class Ai_chatbot:
    def __init__(self, model_name="qwen3:8b"):
        self.model_name = model_name
        self.document_content = ""
        self.processor = DocumentProcessor()
        self.max_context_length = 8000
    
    def load_document(self, file_path):
        try:
            self.document_content = self.processor.extract_text(file_path)
            
            if not self.document_content.strip():
                return False, "Document appears to be empty"
            
            return True, f"Document loaded successfully ({len(self.document_content)} characters)"
            
        except Exception as e:
            return False, f"Error loading document: {str(e)}"
    
    def _create_prompt(self, question):
        context = self.document_content[:self.max_context_length]
        
        if len(self.document_content) > self.max_context_length:
            context += "\n\n[Note: Document truncated due to length]"
        
        prompt = f"""You are a course assistant chatbot. Your role is to answer student questions based STRICTLY on the provided course material.

CRITICAL RULES:
1. Answer ONLY using information present in the course material below
2. If the question cannot be answered from the material, respond with EXACTLY: "This question is outside the provided material."
3. Do NOT use any external knowledge or information
4. Be accurate, concise, and helpful
5. If you're unsure, say the question is outside the material

COURSE MATERIAL:
---
{context}
---

STUDENT QUESTION: {question}

ANSWER (Remember: only from the material above):"""
        
        return prompt
    
    def query(self, question):
        if not self.document_content:
            return "❌ Error: No document loaded. Please load a document first."
        
        if not question.strip():
            return "❌ Error: Please provide a valid question."
        
        try:
            prompt = self._create_prompt(question)
            
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful course assistant that answers only from provided material.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.2,
                    'top_p': 0.9,
                    'num_predict': 500
                }
            )
            
            answer = response['message']['content'].strip()
            return answer
            
        except Exception as e:
            return f"❌ Error querying the model: {str(e)}\nMake sure Ollama is running with: ollama serve"
