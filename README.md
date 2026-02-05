# 📺 AI News Avatar Video Generator

An intelligent, end-to-end pipeline for automatically generating professional AI avatar news videos with real-time progress tracking and a modern web interface.

## 🎯 Features

- **Automated News Scraping**: Collects the latest news articles from 29 international news sources
- **AI-Powered Summarization**: Uses GPT-4 to create concise, professional summaries
- **Dynamic Script Generation**: Generates natural-sounding news anchor scripts from summaries
- **Avatar Video Creation**: Produces lip-synced avatar videos using D-ID's cutting-edge technology
- **Real-Time Progress Tracking**: Stream-based UI updates showing each pipeline step
- **Professional Web Interface**: Modern, responsive dashboard for easy interaction
- **Video Download**: Direct video downloads to your system after generation

## 🏗️ Architecture

The application follows a modular, pipeline-based architecture:

```
News Scraping → Summarization → Script Generation → Avatar Video Creation
     ↓              ↓                   ↓                    ↓
  BeautifulSoup   OpenAI GPT-4      Template             D-ID API
                                     Engine             (Lip-Sync)
```

## 📋 Project Structure

```
Avatar-Video-Generation/
│
├── app/
│   ├── main.py                 # FastAPI application & routing
│   ├── scraper.py              # News article scraping module
│   ├── summarizer.py           # LLM-based summarization module
│   ├── script_generator.py     # News script generation
│   ├── avatar.py               # D-ID API integration
│   └── config.py               # Configuration & environment settings
│
├── static/
│   ├── index.html              # Web UI (responsive dashboard)
│   ├── styles.css              # Modern styling
│   └── script.js               # Frontend logic & real-time updates
│
├── docs/
│   └── code_explanation.md     # Detailed code documentation
│
├── .env                        # Environment variables (Git-ignored)
├── .env.example                # Example configuration template
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── run.sh                      # Startup script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Required API Keys:
  - **OpenAI API Key** (for GPT-4o-mini summarization)
  - **D-ID API Key** (for avatar video generation)

### Installation

1. **Clone the repository**
   ```bash
   cd Avatar-Video-Generation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_key_here
   DID_API_KEY=your_did_api_key_here
   DID_PRESENTER_ID=amy-jcwCkr1grs  # Default avatar
   DID_VOICE_ID=en-US-JennyNeural   # Default voice
   ```

5. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Or use the provided script:
   ```bash
   bash run.sh
   ```

6. **Access the UI**
   Open your browser and navigate to: **http://localhost:8000**

## 📖 Usage Guide

### Via Web Interface (Recommended)

1. **Open Dashboard**: Navigate to http://localhost:8000
2. **Click "Generate News Video"**: Start the pipeline
3. **Monitor Progress**: Watch real-time logs showing each stage
4. **Review Results**: See generated script and preview video
5. **Download**: Click download button to save the video

### Via API (cURL/Postman)

**Stream with Progress Updates:**
```bash
curl http://localhost:8000/generate-news-video-stream
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

## 🔄 Pipeline Stages

### 1. **News Scraping** (~10-20 seconds)
- Connects to 29 international news sources
- Extracts article titles, URLs, and content
- Uses fallback sources for reliability
- Returns 5 recent articles

**Output**: List of articles with metadata

### 2. **Summarization** (~20-30 seconds)
- Processes each article with GPT-4o-mini
- Generates concise, professional summaries
- Maintains key information and context
- Target: 150-160 words per summary

**Output**: Summarized articles list

### 3. **Script Generation** (<1 second)
- Combines summaries into a cohesive script
- Formats as professional news anchor delivery
- Estimates reading time
- Average: ~130 words, ~50 seconds

**Output**: Complete news anchor script

### 4. **Avatar Video Creation** (~20-30 seconds)
- Sends script to D-ID API
- Generates lip-synced avatar video
- Creates professional news presentation
- Polls for completion status
- Max wait: 5 minutes (300 seconds)

**Output**: Direct video URL (MP4, playable/downloadable)

## ⚙️ Configuration

### Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...                    # Your OpenAI API key
OPENAI_MODEL=gpt-4o-mini                 # Model for summarization

# D-ID Configuration (Avatar)
DID_API_KEY=<your-api-key>               # Your D-ID API key
DID_PRESENTER_ID=amy-jcwCkr1grs         # Avatar character ID
DID_VOICE_ID=en-US-JennyNeural          # Voice synthesis model

# Optional Settings
DEBUG=false                               # Enable debug logging
```

### API Keys

**OpenAI**:
- Go to: https://platform.openai.com/account/api-keys
- Create a new secret key
- Uses GPT-4o-mini model (~$0.15 per 1M tokens)

**D-ID**:
- Go to: https://www.d-id.com
- Create account and get API key
- Free tier: 10 credits/month (~1-2 videos)
- Professional: Pay-as-you-go pricing

## 📊 Monitoring & Logging

### Real-Time Progress Display
- **Logs Panel**: Shows all system activities with timestamps
- **Progress Bar**: Visual indicator of completion percentage
- **Status Messages**: Color-coded log entries (info/success/error)

### Log Levels
```
INFO:     Standard operations (blue)
SUCCESS:  Completed steps (green)
ERROR:    Failures & exceptions (red)
WARNING:  Skipped items (orange)
```

### Example Log Output
```
[14:30:00] Connecting to generation service...
[14:30:01] Step 1: Scraping news articles from multiple sources...
[14:30:15] Found 10 potential article links from https://www.bbc.com/news
[14:30:20] ✓ Successfully scraped 5 articles
[14:30:21] Step 2: Summarizing articles with AI...
[14:30:50] ✓ Successfully summarized 5 articles
[14:30:51] Step 3: Generating professional news script...
[14:30:52] ✓ Generated script with 132 words
[14:30:53] Step 4: Creating avatar video (this may take a moment)...
[14:31:10] ✓ Avatar video generated successfully!
```

### Complete Real-World Execution Log

Here's an actual successful run from our production environment:

```
(venv) jawwad@jawwad-Lenovo-V14-G3-IAP:~/Avatar-Video-Generation$ uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
INFO:     Will watch for changes in these directories: ['/home/jawwad/Avatar-Video-Generation']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [56765] using WatchFiles
INFO:     Started server process [56767]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:45990 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:45990 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:45990 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:45990 - "GET /static/styles.css HTTP/1.1" 304 Not Modified
INFO:     127.0.0.1:45990 - "GET /static/script.js HTTP/1.1" 304 Not Modified
INFO:     127.0.0.1:45996 - "GET /generate-news-video-stream HTTP/1.1" 200 OK
2026-02-05 07:13:34,230 - app.main - INFO - Starting news video generation pipeline
2026-02-05 07:13:34,331 - app.main - INFO - Step 1: Scraping news articles...
2026-02-05 07:13:34,332 - app.scraper - INFO - Starting to scrape 5 articles
2026-02-05 07:13:34,332 - app.scraper - INFO - Trying source 1/29: https://www.bbc.com/news
2026-02-05 07:13:34,749 - app.scraper - INFO - Found 10 potential article links from https://www.bbc.com/news
2026-02-05 07:13:35,357 - app.scraper - INFO - Scraped: Breaking news, video and the latest top stories from the U.S...
2026-02-05 07:13:43,550 - app.scraper - INFO - Scraped: Latest News & Updates...
2026-02-05 07:13:44,546 - app.scraper - INFO - Scraped: Latest News & Updates...
2026-02-05 07:13:45,987 - app.scraper - INFO - Trying source 2/29: https://apnews.com
2026-02-05 07:13:47,828 - app.scraper - INFO - Found 10 potential article links from https://apnews.com
2026-02-05 07:13:49,299 - app.scraper - INFO - Scraped: Associated Press News: Breaking News, Latest Headlines and V...
2026-02-05 07:13:51,521 - app.scraper - INFO - Scraped: World News...
2026-02-05 07:13:52,024 - app.scraper - INFO - Successfully scraped 5 articles from 2 sources
2026-02-05 07:13:52,026 - app.main - INFO - Successfully scraped 5 articles
INFO:     127.0.0.1:51436 - "GET /generate-news-video-stream HTTP/1.1" 200 OK
2026-02-05 07:13:52,028 - app.main - INFO - Starting news video generation pipeline
2026-02-05 07:13:52,127 - app.main - INFO - Step 2: Summarizing articles with LLM...
2026-02-05 07:13:52,209 - app.summarizer - INFO - Initialized NewsSummarizer with model: gpt-4o-mini
2026-02-05 07:13:52,209 - app.summarizer - INFO - Summarizing article: Breaking news, video and the latest top stories from the U.S...
2026-02-05 07:13:54,037 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:13:54,110 - app.summarizer - INFO - Successfully generated summary (184 chars)
2026-02-05 07:13:54,110 - app.summarizer - INFO - Summarizing article: Latest News & Updates...
2026-02-05 07:14:09,697 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:09,965 - app.summarizer - INFO - Successfully generated summary (150 chars)
2026-02-05 07:14:09,989 - app.summarizer - INFO - Summarizing article: Breaking news, video and the latest top stories from the U.S...
2026-02-05 07:14:12,458 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:12,460 - app.summarizer - INFO - Successfully generated summary (139 chars)
2026-02-05 07:14:12,460 - app.summarizer - INFO - Summarizing article: Latest News & Updates...
2026-02-05 07:14:13,656 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:13,666 - app.summarizer - INFO - Successfully generated summary (166 chars)
2026-02-05 07:14:13,667 - app.summarizer - INFO - Summarizing article: Latest News & Updates...
2026-02-05 07:14:14,583 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:14,605 - app.summarizer - INFO - Successfully generated summary (164 chars)
2026-02-05 07:14:14,605 - app.summarizer - INFO - Summarizing article: Associated Press News: Breaking News, Latest Headlines and V...
2026-02-05 07:14:15,983 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:15,984 - app.summarizer - INFO - Successfully generated summary (148 chars)
2026-02-05 07:14:15,985 - app.summarizer - INFO - Summarizing article: Latest News & Updates...
2026-02-05 07:14:17,692 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:17,715 - app.summarizer - INFO - Successfully generated summary (170 chars)
2026-02-05 07:14:17,716 - app.summarizer - INFO - Summarizing article: World News...
2026-02-05 07:14:19,119 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:19,121 - app.summarizer - INFO - Successfully generated summary (127 chars)
2026-02-05 07:14:19,121 - app.summarizer - INFO - Summarizing article: Associated Press News: Breaking News, Latest Headlines and V...
2026-02-05 07:14:20,144 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:20,146 - app.summarizer - INFO - Successfully generated summary (169 chars)
2026-02-05 07:14:20,147 - app.main - INFO - Successfully summarized 5 articles
2026-02-05 07:14:20,247 - app.summarizer - INFO - Summarizing article: World News...
2026-02-05 07:14:21,459 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-02-05 07:14:21,463 - app.summarizer - INFO - Successfully generated summary (178 chars)
2026-02-05 07:14:21,463 - app.main - INFO - Step 3: Generating news anchor script...
2026-02-05 07:14:21,464 - app.script_generator - INFO - Initialized ScriptGenerator
2026-02-05 07:14:21,464 - app.script_generator - INFO - Generating script from 5 articles
2026-02-05 07:14:21,464 - app.script_generator - INFO - Generated script: 142 words, ~57 seconds
2026-02-05 07:14:21,464 - app.main - INFO - Successfully generated script (142 words)
2026-02-05 07:14:21,564 - app.main - INFO - Successfully summarized 5 articles
2026-02-05 07:14:21,565 - app.main - INFO - Step 4: Generating avatar video with D-ID...
2026-02-05 07:14:21,566 - app.avatar - INFO - Initialized AvatarVideoGenerator with D-ID
2026-02-05 07:14:21,566 - app.avatar - INFO - Starting video generation with D-ID
2026-02-05 07:14:21,566 - app.avatar - INFO - Creating talk with D-ID API (Free Tier)
2026-02-05 07:14:21,566 - app.avatar - INFO - Script length: 861 characters
2026-02-05 07:14:28,203 - app.avatar - INFO - D-ID Response Status: 201
2026-02-05 07:14:28,204 - app.avatar - INFO - Talk created successfully. ID: tlk_wgFOEKNawwMhLZnnc4VeK
2026-02-05 07:14:28,206 - app.avatar - INFO - Waiting for video generation (max 300s)
2026-02-05 07:14:29,165 - app.avatar - INFO - Video status: created (elapsed: 0s)
2026-02-05 07:14:35,420 - app.avatar - INFO - Video status: started (elapsed: 6s)
2026-02-05 07:14:41,532 - app.avatar - INFO - Video status: started (elapsed: 12s)
2026-02-05 07:14:47,584 - app.avatar - INFO - Video status: done (elapsed: 18s)
2026-02-05 07:14:47,585 - app.avatar - INFO - Video generated successfully: https://d-id-talks-prod.s3.us-west-2.amazonaws.com/auth0%7C6983fbe54cc0e832419c5375/tlk_wgFOEKNawwMhLZnnc4VeK/1770257668035.mp4
2026-02-05 07:14:47,586 - app.main - INFO - Successfully generated video: https://d-id-talks-prod.s3.us-west-2.amazonaws.com/auth0%7C6983fbe54cc0e832419c5375/tlk_wgFOEKNawwMhLZnnc4VeK/1770257668035.mp4
2026-02-05 07:14:47,586 - app.main - INFO - Step 3: Generating news anchor script...
2026-02-05 07:14:47,587 - app.script_generator - INFO - Initialized ScriptGenerator
2026-02-05 07:14:47,587 - app.script_generator - INFO - Generating script from 5 articles
2026-02-05 07:14:47,587 - app.script_generator - INFO - Generated script: 143 words, ~57 seconds
2026-02-05 07:14:47,587 - app.main - INFO - Successfully generated script (143 words)
2026-02-05 07:14:47,687 - app.main - INFO - Pipeline completed successfully
2026-02-05 07:14:47,688 - app.main - INFO - Step 4: Generating avatar video with D-ID...
2026-02-05 07:14:47,688 - app.avatar - INFO - Initialized AvatarVideoGenerator with D-ID
2026-02-05 07:14:47,688 - app.avatar - INFO - Starting video generation with D-ID
2026-02-05 07:14:47,688 - app.avatar - INFO - Creating talk with D-ID API (Free Tier)
2026-02-05 07:14:47,688 - app.avatar - INFO - Script length: 906 characters
2026-02-05 07:14:51,272 - app.avatar - INFO - D-ID Response Status: 201
2026-02-05 07:14:51,273 - app.avatar - INFO - Talk created successfully. ID: tlk_A7LXb8cwz20j5mJE5bz7w
2026-02-05 07:14:51,275 - app.avatar - INFO - Waiting for video generation (max 300s)
2026-02-05 07:14:52,477 - app.avatar - INFO - Video status: started (elapsed: 0s)
2026-02-05 07:14:58,645 - app.avatar - INFO - Video status: started (elapsed: 6s)
2026-02-05 07:15:04,698 - app.avatar - INFO - Video status: started (elapsed: 12s)
2026-02-05 07:15:11,170 - app.avatar - INFO - Video status: done (elapsed: 18s)
2026-02-05 07:15:11,171 - app.avatar - INFO - Video generated successfully: https://d-id-talks-prod.s3.us-west-2.amazonaws.com/auth0%7C6983fbe54cc0e832419c5375/tlk_A7LXb8cwz20j5mJE5bz7w/1770257691050.mp4
2026-02-05 07:15:11,172 - app.main - INFO - Successfully generated video: https://d-id-talks-prod.s3.us-west-2.amazonaws.com/auth0%7C6983fbe54cc0e832419c5375/tlk_A7LXb8cwz20j5mJE5bz7w/1770257691050.mp4
2026-02-05 07:15:11,273 - app.main - INFO - Pipeline completed successfully
```

✅ **Complete Success!** Both videos generated successfully in under 20 seconds each.

## 🎬 Sample Output Videos

### Working Example Video
This is a complete working example of the generated avatar news video:

**[WorkingVideo.mp4 (Google Drive Link)](https://drive.google.com/file/d/16uDnTch7r0o5iOFyFmCKrwemSrVWTkFs/view?usp=sharing)** - Click to view or download

### Generated News Avatar Videos

Here are two example news avatar videos generated by the system:

**Video 1: News Avatar Video #1**
- [NewsAvatorVideo1.mp4](./NewsAvatorVideo1.mp4) - Download
- Generated from 5 news articles
- Professional news anchor presentation
- Duration: ~57 seconds

**Articles Used in NewsAvatorVideo1:**
1. Team GB curling victory (BBC News)
2. US intervention in Venezuela (BBC News)
3. Israel bans MSF in Gaza (BBC News)
4. Associated Press global news overview (AP News)
5. Associated Press world news (AP News)

---

**Video 2: News Avatar Video #2**
- [NewsAvatorVideo2.mp4](./NewsAvatorVideo2.mp4) - Download
- Generated from 5 news articles
- Professional news anchor presentation
- Duration: ~57 seconds

**Articles Used in NewsAvatorVideo2:**
1. Breaking news, video and the latest top stories from the U.S. and around the world (BBC News)
2. Latest News & Updates (BBC News)
3. Latest News & Updates - Alternative Coverage (BBC News)
4. Associated Press News: Breaking News, Latest Headlines and Videos (AP News)
5. World News (AP News)

### What to Expect
When you run the application, you'll get:
- ✅ High-quality MP4 video (720p+)
- ✅ Lip-synced avatar speaking the news script
- ✅ Professional news anchor tone and delivery
- ✅ Real-time progress updates in the UI
- ✅ Downloadable video file to your system

## 🔧 API Reference

### Endpoints

#### GET `/`
Returns UI or health status
```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T06:30:00"
}
```

#### GET `/generate-news-video-stream`
Server-Sent Events stream with real-time progress
- **Content-Type**: text/event-stream
- **Returns**: Stream of JSON objects with logs and progress
- **Format**: 
  ```json
  {
    "type": "log",
    "message": "Log message",
    "progress": 45
  }
  ```

#### GET `/health`
Simple health check
```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T06:30:00"
}
```

## 🐛 Troubleshooting

### Video Generation Fails
**Issue**: D-ID API returns error  
**Solution**: 
- Check API key and credentials
- Verify account has available credits
- Check internet connection

### Articles Won't Scrape
**Issue**: Scraping times out or returns no results  
**Solution**: 
- Verify internet connection
- Some sources may be temporarily blocked
- System tries 29 sources, at least one should work

### Summarization Errors
**Issue**: OpenAI API errors  
**Solution**: 
- Verify OpenAI API key
- Ensure account has API credits
- Check OpenAI account status

### Port Already in Use
**Solution**:
```bash
# Use different port
python -m uvicorn app.main:app --port 8001
```

### Module Not Found
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📈 Performance Metrics

| Stage | Typical Time | Range |
|-------|--------------|-------|
| Scraping | 15-20s | 10-30s |
| Summarization | 20-25s | 15-40s |
| Script Generation | <1s | <1s |
| Video Creation | 25-30s | 20-40s |
| **Total** | **60-75s** | **45-110s** |

## 🔐 Security Notes

- **Never commit `.env` file** (contains API keys)
- Use environment variables for sensitive data
- API keys are logged only in debug mode
- Videos are temporarily stored on D-ID servers
- All communications use HTTPS with D-ID API
- `.env` is in `.gitignore` for your protection

## 🎓 Code Structure

### Key Modules

**app/scraper.py**
- `NewsScraper`: Handles multi-source article collection
- Implements fallback logic for robustness
- Parses HTML with BeautifulSoup
- Extracts article content with newspaper3k

**app/summarizer.py**
- `NewsSummarizer`: GPT-4 powered summarization
- Maintains professional tone
- Handles errors gracefully
- Configured for fast responses

**app/script_generator.py**
- `ScriptGenerator`: Combines summaries into coherent script
- Formats for natural speech
- Estimates reading time
- Professional news anchor style

**app/avatar.py**
- `AvatarVideoGenerator`: D-ID API integration
- Handles video polling and status
- Manages free-tier limitations
- Implements retry logic

**app/config.py**
- `Settings`: Pydantic-based configuration
- Loads from .env file
- Provides type-safe access to settings
- Includes comprehensive news sources

**app/main.py**
- FastAPI application setup
- Route definitions
- Real-time streaming with Server-Sent Events
- Error handling middleware

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## ✨ Future Enhancements

- [ ] Multiple avatar options
- [ ] Custom voice selection
- [ ] Scheduled video generation
- [ ] Video storage & history
- [ ] Multi-language support
- [ ] Advanced script editing before generation
- [ ] Email notifications upon completion
- [ ] Batch video generation
- [ ] Analytics dashboard

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Check log files for detailed error messages
4. Verify all API keys are correctly configured

---

**Happy Generating! 🎬**
## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [D-ID API Documentation](https://docs.d-id.com/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Built with ❤️ using FastAPI, OpenAI, and D-ID**