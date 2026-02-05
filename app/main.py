"""
FastAPI Main Application
Orchestrates the news video generation pipeline
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, AsyncGenerator
import logging
from datetime import datetime
import json
import asyncio
import os
from pathlib import Path

from app.scraper import NewsScraper
from app.summarizer import NewsSummarizer
from app.script_generator import ScriptGenerator
from app.avatar import AvatarVideoGenerator
from app.config import settings


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI News Avatar Video Generator",
    description="End-to-end pipeline for generating AI avatar news videos",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Custom logging handler to capture logs
class LogCapture(logging.Handler):
    """Handler to capture logs for streaming"""
    def __init__(self):
        super().__init__()
        self.logs = []
    
    def emit(self, record):
        self.logs.append(self.format(record))
    
    def get_logs(self):
        return self.logs

# Global log capturer
log_capturer = LogCapture()
log_capturer.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))

# Response models
class Article(BaseModel):
    title: str
    url: str
    summary: str

class NewsVideoResponse(BaseModel):
    status: str
    script: str
    video_url: str
    articles: List[Article]
    generated_at: str

@app.get("/")
async def root():
    """
    Root endpoint - returns UI or health status
    """
    static_dir = Path(__file__).parent.parent / "static" / "index.html"
    if static_dir.exists():
        return FileResponse(str(static_dir))
    
    return {
        "message": "AI News Avatar Video Generator API",
        "status": "running",
        "endpoints": {
            "ui": "/",
            "generate": "/generate-news-video",
            "stream": "/generate-news-video-stream",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
#UI Streaming Endpoint
@app.get("/generate-news-video-stream")
async def generate_news_video_stream():
    """
    Streaming endpoint for video generation with real-time progress updates
    Uses Server-Sent Events (SSE) to stream logs and progress
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            logger.info("Starting news video generation pipeline")
            yield f"data: {json.dumps({'type': 'log', 'message': 'Initializing generation pipeline...', 'progress': 0})}\n\n"
            await asyncio.sleep(0.1)
            
            # Step 1: Scrape news articles
            logger.info("Step 1: Scraping news articles...")
            yield f"data: {json.dumps({'type': 'log', 'message': 'Step 1: Scraping news articles from multiple sources...', 'progress': 10})}\n\n"
            
            scraper = NewsScraper()
            articles = scraper.scrape_articles(num_articles=5)
            
            if not articles:
                yield f"data: {json.dumps({'type': 'log', 'message': 'Error: Failed to scrape articles', 'progress': 10})}\n\n"
                raise ValueError("Failed to scrape articles")
            
            logger.info(f"Successfully scraped {len(articles)} articles")
            yield f"data: {json.dumps({'type': 'log', 'message': f'✓ Successfully scraped {len(articles)} articles', 'progress': 25})}\n\n"
            await asyncio.sleep(0.1)
            
            # Step 2: Summarize articles
            logger.info("Step 2: Summarizing articles with LLM...")
            yield f"data: {json.dumps({'type': 'log', 'message': 'Step 2: Summarizing articles with AI...', 'progress': 30})}\n\n"
            
            summarizer = NewsSummarizer()
            summarized_articles = []
            
            for i, article in enumerate(articles):
                try:
                    article_title = article.get('title', 'Unknown')[:60]
                    msg = f'Summarizing article {i+1}/{len(articles)}: {article_title}...'
                    yield f"data: {json.dumps({'type': 'log', 'message': msg, 'progress': 30 + (i * 5)})}\n\n"
                    
                    summary = summarizer.summarize_article(
                        title=article['title'],
                        content=article['content']
                    )
                    summarized_articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'summary': summary
                    })
                    await asyncio.sleep(0.1)
                except Exception as e:
                    logger.warning(f"Failed to summarize article: {str(e)}")
                    article_title = article.get('title', 'Unknown')[:40]
                    msg = f'⚠ Skipped article: {article_title}...'
                    yield f"data: {json.dumps({'type': 'log', 'message': msg, 'progress': 30 + (i * 5)})}\n\n"
                    continue
            
            if not summarized_articles:
                yield f"data: {json.dumps({'type': 'log', 'message': 'Error: No articles could be summarized', 'progress': 50})}\n\n"
                raise ValueError("Failed to summarize articles")
            
            logger.info(f"Successfully summarized {len(summarized_articles)} articles")
            yield f"data: {json.dumps({'type': 'log', 'message': f'✓ Successfully summarized {len(summarized_articles)} articles', 'progress': 55})}\n\n"
            await asyncio.sleep(0.1)
            
            # Step 3: Generate script
            logger.info("Step 3: Generating news anchor script...")
            yield f"data: {json.dumps({'type': 'log', 'message': 'Step 3: Generating professional news script...', 'progress': 60})}\n\n"
            
            script_gen = ScriptGenerator()
            script = script_gen.generate_script(summarized_articles)
            
            if not script:
                yield f"data: {json.dumps({'type': 'log', 'message': 'Error: Failed to generate script', 'progress': 60})}\n\n"
                raise ValueError("Failed to generate script")
            
            logger.info(f"Successfully generated script ({len(script.split())} words)")
            yield f"data: {json.dumps({'type': 'log', 'message': f'✓ Generated script with {len(script.split())} words', 'progress': 70})}\n\n"
            await asyncio.sleep(0.1)
            
            # Step 4: Generate avatar video
            logger.info("Step 4: Generating avatar video with D-ID...")
            yield f"data: {json.dumps({'type': 'log', 'message': 'Step 4: Creating avatar video (this may take a moment)...', 'progress': 75})}\n\n"
            
            avatar_gen = AvatarVideoGenerator()
            video_url = avatar_gen.generate_video(script)
            
            if not video_url:
                yield f"data: {json.dumps({'type': 'log', 'message': 'Error: Failed to generate avatar video', 'progress': 75})}\n\n"
                raise ValueError("Failed to generate avatar video")
            
            logger.info(f"Successfully generated video: {video_url}")
            yield f"data: {json.dumps({'type': 'log', 'message': '✓ Avatar video generated successfully!', 'progress': 95})}\n\n"
            await asyncio.sleep(0.1)
            
            # Prepare completion response
            logger.info("Pipeline completed successfully")
            response_data = {
                'type': 'complete',
                'status': 'success',
                'script': script,
                'video_url': video_url,
                'articles': summarized_articles,
                'generated_at': datetime.utcnow().isoformat(),
                'progress': 100
            }
            
            yield f"data: {json.dumps(response_data)}\n\n"
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            error_response = {
                'type': 'error',
                'message': str(e),
                'error': True
            }
            yield f"data: {json.dumps(error_response)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        }
    )

@app.post("/generate-news-video", response_model=NewsVideoResponse)
async def generate_news_video():
    """
    Main endpoint: Generate AI avatar news video
    
    Process:
    1. Scrape 5 recent news articles
    2. Summarize each article using LLM
    3. Generate news anchor script
    4. Create avatar video with lip-sync
    5. Return complete response
    
    Returns:
        NewsVideoResponse: Contains script, video URL, and article details
    """
    try:
        logger.info("Starting news video generation pipeline")
        
        # Step 1: Scrape news articles
        logger.info("Step 1: Scraping news articles...")
        scraper = NewsScraper()
        articles = scraper.scrape_articles(num_articles=5)
        
        if not articles:
            raise HTTPException(
                status_code=500,
                detail="Failed to scrape articles. Please try again."
            )
        
        logger.info(f"Successfully scraped {len(articles)} articles")
        
        # Step 2: Summarize articles using LLM
        logger.info("Step 2: Summarizing articles with LLM...")
        summarizer = NewsSummarizer()
        summarized_articles = []
        
        for article in articles:
            try:
                summary = summarizer.summarize_article(
                    title=article['title'],
                    content=article['content']
                )
                summarized_articles.append({
                    'title': article['title'],
                    'url': article['url'],
                    'summary': summary
                })
            except Exception as e:
                logger.warning(f"Failed to summarize article '{article['title']}': {str(e)}")
                continue
        
        if not summarized_articles:
            raise HTTPException(
                status_code=500,
                detail="Failed to summarize articles. Please check API credentials."
            )
        
        logger.info(f"Successfully summarized {len(summarized_articles)} articles")
        
        # Step 3: Generate news anchor script
        logger.info("Step 3: Generating news anchor script...")
        script_gen = ScriptGenerator()
        script = script_gen.generate_script(summarized_articles)
        
        if not script:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate script"
            )
        
        logger.info("Successfully generated script")
        
        # Step 4: Generate avatar video
        logger.info("Step 4: Generating avatar video...")
        avatar_gen = AvatarVideoGenerator()
        video_url = avatar_gen.generate_video(script)
        
        if not video_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate avatar video. Please check API credentials."
            )
        
        logger.info(f"Successfully generated video: {video_url}")
        
        # Prepare response
        response = NewsVideoResponse(
            status="success",
            script=script,
            video_url=video_url,
            articles=[Article(**article) for article in summarized_articles],
            generated_at=datetime.utcnow().isoformat()
        )
        
        logger.info("Pipeline completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/test-components")
async def test_components():
    """
    Test endpoint to verify all components are configured correctly
    """
    results = {
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "did_configured": bool(settings.DID_API_KEY),
        "scraper_ready": True
    }
    
    return {
        "status": "component_check",
        "results": results,
        "all_ready": all(results.values())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)