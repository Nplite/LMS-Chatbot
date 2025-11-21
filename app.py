import streamlit as st
import json
import pandas as pd
from pathlib import Path
import tempfile
import os
from src.document_processor import DocumentProcessor
from src.question_generator import QuestionGenerator

# Page configuration
st.set_page_config(
    page_title="Question Bank Generator",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = False
if 'all_questions' not in st.session_state:
    st.session_state.all_questions = None
if 'combined_df' not in st.session_state:
    st.session_state.combined_df = None

def process_document(uploaded_file):
    """Process uploaded document and extract text"""
    processor = DocumentProcessor()
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    try:
        if uploaded_file.name.endswith('.pdf'):
            content = processor.extract_text_from_pdf(tmp_path)
        else:
            content = processor.extract_text_from_docx(tmp_path)
        return content
    finally:
        os.unlink(tmp_path)

def generate_questions(content, num_mcqs, num_short, model_name):
    """Generate questions from content"""
    generator = QuestionGenerator(model_name=model_name)
    
    # Generate questions
    mcqs = generator.generate_mcqs(content, num_questions=num_mcqs)
    short_answers = generator.generate_short_answer(content, num_questions=num_short)
    
    return mcqs, short_answers

# Header
st.markdown('<p class="main-header">📚 Question Bank Generator</p>', unsafe_allow_html=True)
st.markdown("Generate MCQs and short-answer questions from PDF or DOCX documents using AI")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "Select AI Model",
        ["qwen3:8b", "llama2", "mistral", "qwen:14b"],
        index=0,
        help="Choose the language model for question generation"
    )
    
    st.divider()
    
    # Question counts
    st.subheader("Question Settings")
    num_mcqs = st.slider("Number of MCQs", min_value=1, max_value=20, value=5)
    num_short = st.slider("Number of Short Answer Questions", min_value=1, max_value=10, value=2)
    
    st.divider()
    
    st.info("💡 **Tip:** Upload your document and click 'Generate Questions' to start!")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=['pdf', 'docx'],
        help="Upload the document you want to generate questions from"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size / 1024:.2f} KB")

with col2:
    st.subheader("🎯 Generate Questions")
    
    if uploaded_file:
        if st.button("🚀 Generate Questions", type="primary", use_container_width=True):
            with st.spinner("Processing document..."):
                try:
                    # Extract text
                    progress_bar = st.progress(0)
                    st.write("📄 Extracting text from document...")
                    content = process_document(uploaded_file)
                    progress_bar.progress(33)
                    
                    st.write(f"✅ Extracted {len(content):,} characters")
                    
                    # Generate questions
                    st.write(f"🤖 Generating questions using {model_name}...")
                    progress_bar.progress(50)
                    
                    mcqs, short_answers = generate_questions(
                        content, num_mcqs, num_short, model_name
                    )
                    progress_bar.progress(90)
                    
                    # Structure output
                    all_questions = {
                        "mcqs": mcqs,
                        "short_answer": short_answers,
                        "metadata": {
                            "total_mcqs": len(mcqs),
                            "total_short_answer": len(short_answers),
                            "source_document": uploaded_file.name,
                            "model_used": model_name
                        }
                    }
                    
                    # Create DataFrame
                    mcq_df = pd.DataFrame(mcqs)
                    short_df = pd.DataFrame(short_answers)
                    
                    if not mcq_df.empty:
                        mcq_df['type'] = 'MCQ'
                    if not short_df.empty:
                        short_df['type'] = 'Short Answer'
                    
                    combined_df = pd.concat([mcq_df, short_df], ignore_index=True)
                    
                    # Save to session state
                    st.session_state.all_questions = all_questions
                    st.session_state.combined_df = combined_df
                    st.session_state.questions_generated = True
                    
                    progress_bar.progress(100)
                    st.success("✅ Questions generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👆 Please upload a document first")

# Display results
if st.session_state.questions_generated:
    st.divider()
    st.header("📊 Generated Questions")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Questions", 
                 len(st.session_state.combined_df))
    with col2:
        st.metric("MCQs", 
                 st.session_state.all_questions['metadata']['total_mcqs'])
    with col3:
        st.metric("Short Answer", 
                 st.session_state.all_questions['metadata']['total_short_answer'])
    with col4:
        if 'difficulty' in st.session_state.combined_df.columns:
            most_common = st.session_state.combined_df['difficulty'].mode()[0]
            st.metric("Most Common Difficulty", most_common)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📝 MCQs", "✍️ Short Answer", "📈 Analytics"])
    
    with tab1:
        if st.session_state.all_questions['mcqs']:
            for idx, mcq in enumerate(st.session_state.all_questions['mcqs'], 1):
                with st.expander(f"Question {idx}: {mcq.get('question', 'N/A')[:100]}..."):
                    st.write(f"**Difficulty:** {mcq.get('difficulty', 'N/A')}")
                    st.write(f"**Question:** {mcq.get('question', 'N/A')}")
                    
                    options = mcq.get('options', [])
                    for i, option in enumerate(options, 1):
                        st.write(f"{i}. {option}")
                    
                    st.success(f"✅ **Correct Answer:** {mcq.get('correct_answer', 'N/A')}")
                    st.info(f"💡 **Explanation:** {mcq.get('explanation', 'N/A')}")
        else:
            st.info("No MCQs generated")
    
    with tab2:
        if st.session_state.all_questions['short_answer']:
            for idx, sa in enumerate(st.session_state.all_questions['short_answer'], 1):
                with st.expander(f"Question {idx}: {sa.get('question', 'N/A')[:100]}..."):
                    st.write(f"**Difficulty:** {sa.get('difficulty', 'N/A')}")
                    st.write(f"**Question:** {sa.get('question', 'N/A')}")
                    st.info(f"💡 **Sample Answer:** {sa.get('model_answer', 'N/A')}")
        else:
            st.info("No short answer questions generated")
    
    with tab3:
        if 'difficulty' in st.session_state.combined_df.columns:
            st.subheader("Difficulty Distribution")
            difficulty_counts = st.session_state.combined_df['difficulty'].value_counts()
            st.bar_chart(difficulty_counts)
            
            st.subheader("Question Type Distribution")
            type_counts = st.session_state.combined_df['type'].value_counts()
            st.bar_chart(type_counts)
        
        st.subheader("Full Data")
        st.dataframe(st.session_state.combined_df, use_container_width=True)
    
    # Download buttons
    st.divider()
    st.subheader("💾 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON download
        json_str = json.dumps(st.session_state.all_questions, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name="questions.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # CSV download
        csv = st.session_state.combined_df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="questions.csv",
            mime="text/csv",
            use_container_width=True
        )

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Made with ❤️ using Streamlit | Powered by AI</p>
    </div>
""", unsafe_allow_html=True)