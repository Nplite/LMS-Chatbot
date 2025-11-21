import streamlit as st
import ollama
from src.document_processor import DocumentProcessor
from src.ai_tutor import Ai_chatbot
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Course Document Chatbot",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'document_loaded' not in st.session_state:
    st.session_state.document_loaded = False



# Header
st.title("📚 Course Document Chatbot")
st.markdown("Upload a course document (PDF/DOCX) and ask questions about it!")

# Sidebar for document upload and settings
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "Select Model",
        ["qwen3:8b", "llama2", "mistral", "phi"],
        index=0
    )
    
    st.divider()
    
    # File upload
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=['pdf', 'docx'],
        help="Upload your course material document"
    )
    
    if uploaded_file is not None:
        if st.button("Load Document", type="primary"):
            with st.spinner("Loading document..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Initialize chatbot with selected model
                st.session_state.chatbot = Ai_chatbot(model_name=model_name)
                
                # Load document
                success, message = st.session_state.chatbot.load_document(tmp_path)
                
                # Clean up temp file
                os.unlink(tmp_path)
                
                if success:
                    st.session_state.document_loaded = True
                    st.session_state.messages = []  # Clear chat history
                    st.success(message)
                else:
                    st.error(message)
    
    st.divider()
    
    # Document info
    if st.session_state.document_loaded and st.session_state.chatbot:
        st.header("📊 Document Info")
        doc_content = st.session_state.chatbot.document_content
        st.metric("Characters", f"{len(doc_content):,}")
        st.metric("Words", f"{len(doc_content.split()):,}")
    
    st.divider()
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
if not st.session_state.document_loaded:
    st.info("👈 Please upload a document from the sidebar to get started!")
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the document..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.query(prompt)
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>💡 Tip: The chatbot answers only from the uploaded document content</p>
    <p>🔄 Make sure Ollama is running: <code>ollama serve</code></p>
</div>
""", unsafe_allow_html=True)