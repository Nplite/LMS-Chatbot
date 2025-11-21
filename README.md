# LMS-Chatbot
# AI-Based Question Bank Generator

## Overview
This project demonstrates an AI-powered question bank generator for Learning Management Systems (LMS) using Ollama with Qwen3:8b model. The application provides an intuitive web interface built with Streamlit that allows users to upload course documents and automatically generate high-quality questions for assessments.

## Features
- **Multiple Question Types**: Generates MCQs with 4 options each and short-answer questions
- **Flexible Question Count**: Configure the number of questions (1-20 MCQs, 1-10 short answers)
- **Difficulty Tagging**: Automatically tags questions as Easy/Medium/Hard
- **Multiple Output Formats**: Export questions in JSON and CSV formats
- **Document Support**: Processes both PDF and DOCX files
- **Interactive UI**: User-friendly Streamlit interface with real-time progress tracking
- **Analytics Dashboard**: View difficulty distribution and question statistics
- **Model Selection**: Choose from multiple AI models (Qwen3:8b, Llama2, Mistral, Qwen:14b)

## Requirements
- Python 3.9+
- Ollama installed with qwen3:8b model
- Windows OS or Ubuntu
- Docker (optional, for containerized deployment)

## Installation

### Install & Verify Ollama 
### 1. Check if Ollama is installed

Open Command Prompt and run:
```ollama --version```

### Download from the official site:

👉 ```https://ollama.com/download```

### After installation, pull the model:

```ollama pull qwen3:8b```

Set Up Python Environment
1. Create Conda Environment
```conda create -p lmsenv python==3.12 -y```

Activate environment:
```conda activate lmsenv```


### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```
### Requirements File (`requirements.txt`)

```
PyPDF2==3.0.1
ollama==0.1.7
pandas==2.1.4
numpy==1.26.4
python-docx==1.1.0
jupyter==1.0.0
streamlit==1.51.0
```

## Usage

### Option 1: Using Streamlit (Local Development)

1. **Run the Streamlit Application**:
```bash
streamlit run app.py
```

2. **Access the Application**:
   - Open your browser and navigate to `http://localhost:8501`
   - Upload a PDF or DOCX document
   - Configure question settings in the sidebar
   - Click "Generate Questions" to start
   - Download results in JSON or CSV format

### Option 2: Using Docker (Recomeded)

1. **Pull Docker Image**:
```bash
docker pull npkite/question-bank-app:latest
```

2. **Run Docker Container**:
```bash
docker run -d \
  --name question_bank \
  -p 8501:8501 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  npkite/question-bank-app:latest

```

3. **Access the Application**:
   - Open your browser and navigate to `http://localhost:8501`

**Note**: Ensure Ollama service is accessible from within the Docker container. You may need to configure network settings or run Ollama on the host machine.

## Project Structure
```

├── app.py                      # Main Streamlit application
├── src/
│   ├── __init__.py 
│   ├── main.py                 # Terminal based question generation
│   ├── document_processor.py   # PDF/DOCX text extraction
│   └── question_generator.py   # AI question generation logic
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
└── README.md                   # This file
```

## Approach & Assumptions

### Approach:
1. **Document Processing**: Extract text content from PDF/DOCX files using PyPDF2 and python-docx
2. **Prompt Engineering**: Use structured prompts to ensure consistent and high-quality question generation
3. **AI Generation**: Leverage Qwen3:8b via Ollama API for intelligent question creation
4. **Structured Output**: Generate questions with metadata (difficulty, explanations, correct answers)
5. **Export Options**: Provide JSON and CSV formats for easy LMS integration

### Assumptions:
- Course documents are typically 10-15 pages
- Content is in English language
- Document text is extractable (not scanned images without OCR)
- Ollama service is running locally and accessible
- Questions generated may require manual review for accuracy

### Scalability Considerations:
- **Batch Processing**: Can process multiple documents sequentially
- **Modular Design**: Easy to switch between different AI models
- **LMS Integration**: Output format compatible with standard LMS databases
- **Extensible**: Can be extended to generate additional question types (True/False, Fill-in-the-blank, etc.)
- **Containerization**: Docker support enables easy deployment and scaling

## Output Format

### JSON Structure:
```json
{
  "mcqs": [...],
  "short_answer": [...],
  "metadata": {...}
}
```

### CSV Format:
    Columns include: question, options, correct_answer, difficulty, explanation, type, model_answer

## Features in Detail

### Configuration Options
- **AI Model Selection**: Choose from multiple language models
- **Question Quantity**: Adjust number of MCQs (1-20) and short answers (1-10)
- **Real-time Progress**: Track document processing and question generation

### Analytics Dashboard
- Difficulty distribution visualization
- Question type breakdown
- Complete data table view

### Download Options
- **JSON**: Complete structured output with metadata
- **CSV**: Spreadsheet format for easy import into LMS

## Limitations
- Requires good quality source material for optimal question generation
- Question quality depends on AI model performance and document content
- Manual review recommended for accuracy and relevance
- Scanned documents (images) require OCR preprocessing
- Local Ollama installation required (not cloud-based)
- Ollama must be running before starting the app
- Long documents take more time to generate questions

## Troubleshooting

### Common Issues:
1. **Ollama Connection Error**: Ensure Ollama service is running (`ollama serve`)
2. **Model Not Found**: Pull the required model (`ollama pull qwen3:8b`)
3. **Document Extraction Fails**: Check if PDF is text-based (not scanned image)
4. **Port Already in Use**: Change port with `streamlit run app.py --server.port 8502`

## Future Enhancements
- Support for more question types (True/False, matching, fill-in-the-blank)
- Bulk document processing
- Question difficulty customization
- Integration with popular LMS platforms (Moodle, Canvas, Blackboard)
- Cloud deployment options
- Question quality scoring and validation

## Contributing
Contributions are welcome! Please feel free to submit issues or pull requests.

## License
This project is available for educational and commercial use.

---

**Made with ❤️ using Streamlit | Powered by Namdeo Patil**