# 🎥 AI News Avatar Video Generator

A production-ready end-to-end pipeline that scrapes recent news articles, summarizes them using AI, generates a professional news anchor script, and creates an AI avatar video with lip-sync.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## 🎯 Overview

This project automates the entire news video creation process:
1. **Scrapes** 5 recent news articles from reputable sources
2. **Summarizes** each article using OpenAI's GPT models
3. **Generates** a professional news anchor script (30-45 seconds)
4. **Creates** an AI avatar video with realistic lip-sync using D-ID
5. **Exposes** everything through a FastAPI REST endpoint

## ✨ Features

- ✅ Automated news scraping from multiple sources (BBC, Reuters, AP News, etc.)
- ✅ AI-powered article summarization (OpenAI GPT-4)
- ✅ Professional news script generation
- ✅ High-quality AI avatar videos with lip-sync (D-ID)
- ✅ RESTful API with FastAPI
- ✅ Comprehensive error handling and logging
- ✅ Production-ready code structure
- ✅ Easy configuration via environment variables

## 🏗️ Architecture

```
┌─────────────────┐
│   User Request  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│      FastAPI Application            │
│  POST /generate-news-video          │
└────────┬───────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Step 1: News Scraper               │
│  - Scrapes 5 articles               │
│  - Extracts title, content, URL     │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Step 2: LLM Summarizer             │
│  - OpenAI GPT API                   │
│  - 3-4 sentence summaries           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Step 3: Script Generator           │
│  - Combines summaries               │
│  - News anchor format               │
│  - 30-45 second script              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Step 4: Avatar Video Generator     │
│  - D-ID API                         │
│  - High-quality lip-sync            │
│  - 720p+ resolution                 │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Response                           │
│  - Video URL                        │
│  - Script text                      │
│  - Article list                     │
└─────────────────────────────────────┘
```

## 📦 Prerequisites

- **Python**: 3.10 or higher
- **OpenAI API Key**: [Get one here](https://platform.openai.com/api-keys)
- **D-ID API Key**: [Sign up here](https://www.d-id.com/)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd news-avatar-pipeline
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
# OpenAI API Key
OPENAI_API_KEY=sk-proj-your-actual-key-here

# D-ID API Key
DID_API_KEY=your-actual-did-key-here
```

### Step 2: Get Your API Keys

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key and paste it in `.env`

#### D-ID API Key
1. Go to [D-ID Studio](https://studio.d-id.com/)
2. Sign up for a free account
3. Go to Account Settings → API Key
4. Copy the key and paste it in `.env`

**Note**: D-ID offers a free tier with limited credits. You may need to add payment info for production use.

## 🎬 Usage

### Start the Server

#### Option 1: Using the run script
```bash
chmod +x run.sh
./run.sh
```

#### Option 2: Using uvicorn directly
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### Access the API

#### Interactive Documentation (Swagger UI)
Open your browser and navigate to:
```
http://localhost:8000/docs
```

#### Alternative Documentation (ReDoc)
```
http://localhost:8000/redoc
```

### Make an API Request

#### Using cURL
```bash
curl -X POST "http://localhost:8000/generate-news-video" \
  -H "Content-Type: application/json"
```

#### Using Python
```python
import requests

response = requests.post("http://localhost:8000/generate-news-video")
data = response.json()

print(f"Status: {data['status']}")
print(f"Video URL: {data['video_url']}")
print(f"Script: {data['script']}")
```

#### Using the Swagger UI
1. Go to `http://localhost:8000/docs`
2. Click on `POST /generate-news-video`
3. Click "Try it out"
4. Click "Execute"
5. View the response with video URL and script

### Example Response

```json
{
  "status": "success",
  "script": "Good day. Here are today's top stories for February 05, 2026.\n\nIn our lead story, researchers have discovered a new treatment for Alzheimer's disease that shows promising results in early trials...\n\nNext, global markets responded positively to the Federal Reserve's decision to maintain interest rates...\n\nIn other news, a major technology company announced plans to invest $10 billion in renewable energy infrastructure...\n\nMeanwhile, international climate talks in Geneva reached a breakthrough agreement on carbon emissions...\n\nAnd finally, the World Health Organization reported significant progress in malaria prevention programs across Africa...\n\nThat's all for now. Stay informed and have a great day.",
  "video_url": "https://d-id-talks-prod.s3.us-west-2.amazonaws.com/...",
  "articles": [
    {
      "title": "Breakthrough in Alzheimer's Research",
      "url": "https://www.bbc.com/news/health-...",
      "summary": "Researchers have discovered a new treatment..."
    },
    ...
  ],
  "generated_at": "2026-02-05T10:30:45.123456"
}
```

## 📚 API Documentation

### Endpoints

#### `GET /`
Health check and API information
- **Response**: Basic API information and available endpoints

#### `GET /health`
Server health status
- **Response**: Health status and timestamp

#### `POST /generate-news-video`
Generate news avatar video
- **Response**: Complete video generation result
- **Processing Time**: 2-5 minutes (includes video rendering)

#### `GET /test-components`
Test API configuration
- **Response**: Configuration status of all components

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| status | string | "success" or "error" |
| script | string | Generated news anchor script |
| video_url | string | URL to download/view the video |
| articles | array | List of articles with summaries |
| generated_at | string | ISO timestamp of generation |

## 🧪 Testing

### Test Individual Components

```bash
# Test configuration
curl http://localhost:8000/test-components

# Test health
curl http://localhost:8000/health
```

### Test Full Pipeline

```bash
# Generate a complete news video
curl -X POST http://localhost:8000/generate-news-video
```

### Expected Processing Time
- **Scraping**: 10-30 seconds
- **Summarization**: 20-40 seconds
- **Script Generation**: 1-2 seconds
- **Video Generation**: 60-180 seconds
- **Total**: 2-5 minutes

## 🔧 Troubleshooting

### Common Issues

#### 1. "OpenAI authentication failed"
**Solution**: Check that your `OPENAI_API_KEY` in `.env` is correct and has available credits.

#### 2. "D-ID authentication failed"
**Solution**: Verify your `DID_API_KEY` in `.env` and ensure you have D-ID credits.

#### 3. "Failed to scrape articles"
**Solution**: 
- Check your internet connection
- Some news sites may block scraping; the system will try multiple sources
- Verify that `requests` and `beautifulsoup4` are installed

#### 4. "Module not found" errors
**Solution**: Ensure you've activated the virtual environment and installed all requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### 5. Video generation timeout
**Solution**: D-ID can take 2-3 minutes to generate videos. The default timeout is 5 minutes. If it times out, check D-ID's status page.

### Debug Mode

Enable debug logging by setting in `.env`:
```bash
DEBUG=True
```

Then restart the server to see detailed logs.

### Check Logs

All operations are logged. Check the console output for detailed information about each step.

## 📁 Project Structure

```
news-avatar-pipeline/
│
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI application & endpoints
│   ├── config.py             # Configuration & environment variables
│   ├── scraper.py            # News scraping logic
│   ├── summarizer.py         # LLM summarization
│   ├── script_generator.py   # Script generation
│   └── avatar.py             # D-ID video generation
│
├── docs/
│   └── code_explanation.md   # Line-by-line code explanation
│
├── .env.example              # Example environment variables
├── .env                      # Your actual environment variables (create this)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── run.sh                    # Startup script
```

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your API keys private
- Use environment variables for all sensitive data
- The `.env.example` file shows required variables without actual keys

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [code_explanation.md](docs/code_explanation.md) for detailed code walkthrough
3. Check API documentation at `/docs` when server is running

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [D-ID API Documentation](https://docs.d-id.com/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Built with ❤️ using FastAPI, OpenAI, and D-ID**