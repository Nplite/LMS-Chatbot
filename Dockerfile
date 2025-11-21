# Dockerfile - Standalone Version
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (for local LLM support)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies directly (no requirements.txt needed)
RUN pip install --no-cache-dir \
    streamlit==1.31.0 \
    pandas==2.2.0 \
    PyPDF2==3.0.1 \
    python-docx==1.1.0 \
    ollama==0.1.6 \
    watchdog==4.0.0

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p input output

# Expose ports
EXPOSE 8501 11434

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Create entrypoint script inline
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🚀 Starting Ollama service..."\n\
ollama serve &\n\
echo "⏳ Waiting for Ollama to start..."\n\
sleep 5\n\
echo "📥 Pulling qwen3:8b model..."\n\
ollama pull qwen3:8b || echo "Model pull failed, will retry on first use"\n\
echo "✅ Ollama is ready!"\n\
echo "🌐 Starting Streamlit app..."\n\
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.fileWatcherType=none \
    --server.headless=true \
    --browser.gatherUsageStats=false' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]





# docker build -t question-bank-app .
# docker run -d   --name question_bank   -p 8501:8501   -v $(pwd)/input:/app/input   -v $(pwd)/output:/app/output   question-bank-app
# http://localhost:8501/
