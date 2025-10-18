# ML Service Dockerfile for Recommendation Engine
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for ML libraries
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
    && rm -rf /var/lib/apt/lists/*

# Create requirements.txt for ML service
COPY <<EOF requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
motor==3.3.2
redis==5.0.1
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
nltk==3.8.1
textblob==0.17.1
sentence-transformers==2.2.2
python-multipart==0.0.6
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
aiofiles==23.2.1
logging==0.4.9.6
pymongo==4.6.0
EOF

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory
RUN mkdir -p models

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash mlservice \
    && chown -R mlservice:mlservice /app

USER mlservice

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run the ML service
CMD ["uvicorn", "ml_service:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]