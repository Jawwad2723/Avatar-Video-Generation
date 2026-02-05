"""
FastAPI Main Application
Orchestrates the news video generation pipeline
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
import logging
from datetime import datetime

from app.scraper import NewsScraper
from app.summarizer import NewsSummarizer
from app.script_generator import ScriptGenerator
from app.avatar import AvatarVideoGenerator
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI News Avatar Video Generator",
    description="End-to-end pipeline for generating AI avatar news videos",
    version="1.0.0"
)

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
    Root endpoint - health check
    """
    return {
        "message": "AI News Avatar Video Generator API",
        "status": "running",
        "endpoints": {
            "generate": "/generate-news-video",
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