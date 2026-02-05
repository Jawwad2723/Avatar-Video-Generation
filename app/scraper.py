"""
News Scraper Module
Scrapes recent news articles from multiple reputable sources
"""

import requests
from bs4 import BeautifulSoup
from newspaper import Article
import logging
from typing import List, Dict
from datetime import datetime
import time
from app.config import settings

logger = logging.getLogger(__name__)

class NewsScraper:
    """
    Scrapes news articles from multiple sources
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': settings.USER_AGENT
        }
        self.timeout = settings.REQUEST_TIMEOUT
    
    def scrape_articles(self, num_articles: int = 5) -> List[Dict]:
        """
        Scrape specified number of recent news articles
        
        Args:
            num_articles: Number of articles to scrape
            
        Returns:
            List of article dictionaries with title, content, and url
        """
        articles = []
        sources_tried = 0
        max_sources = len(settings.NEWS_SOURCES)
        
        logger.info(f"Starting to scrape {num_articles} articles")
        
        # Try different sources until we get enough articles
        for source_url in settings.NEWS_SOURCES:
            if len(articles) >= num_articles:
                break
            
            sources_tried += 1
            logger.info(f"Trying source {sources_tried}/{max_sources}: {source_url}")
            
            try:
                # Get article links from source homepage
                article_links = self._get_article_links(source_url)
                
                # Extract articles from links
                for link in article_links:
                    if len(articles) >= num_articles:
                        break
                    
                    try:
                        article_data = self._extract_article(link)
                        if article_data and self._is_valid_article(article_data):
                            articles.append(article_data)
                            logger.info(f"Scraped: {article_data['title'][:60]}...")
                        
                        # Small delay to be respectful to servers
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract article from {link}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.warning(f"Failed to scrape from {source_url}: {str(e)}")
                continue
        
        logger.info(f"Successfully scraped {len(articles)} articles from {sources_tried} sources")
        return articles[:num_articles]
    
    def _get_article_links(self, source_url: str, max_links: int = 10) -> List[str]:
        """
        Extract article links from a news source homepage
        
        Args:
            source_url: URL of news source
            max_links: Maximum number of links to extract
            
        Returns:
            List of article URLs
        """
        try:
            response = requests.get(
                source_url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            
            # Find all article links
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    href = urljoin(source_url, href)
                
                # Filter for article URLs (basic heuristic)
                if (href.startswith('http') and 
                    'article' in href.lower() or 
                    'news' in href.lower() or
                    '/story/' in href or
                    '/20' in href):  # Year in URL often indicates article
                    
                    if href not in links:
                        links.append(href)
                        
                        if len(links) >= max_links:
                            break
            
            logger.info(f"Found {len(links)} potential article links from {source_url}")
            return links
            
        except Exception as e:
            logger.error(f"Error getting links from {source_url}: {str(e)}")
            return []
    
    def _extract_article(self, url: str) -> Dict:
        """
        Extract article content using newspaper3k
        
        Args:
            url: Article URL
            
        Returns:
            Dictionary with article data
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'title': article.title,
                'content': article.text,
                'url': url,
                'scraped_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract article from {url}: {str(e)}")
            raise
    
    def _is_valid_article(self, article: Dict) -> bool:
        """
        Validate that article has minimum required content
        
        Args:
            article: Article dictionary
            
        Returns:
            True if valid, False otherwise
        """
        # Check for title
        if not article.get('title') or len(article['title']) < 10:
            logger.debug("Article rejected: title too short")
            return False
        
        # Check for content
        if not article.get('content') or len(article['content']) < 200:
            logger.debug("Article rejected: content too short")
            return False
        
        # Check for URL
        if not article.get('url'):
            logger.debug("Article rejected: no URL")
            return False
        
        return True
    
    def scrape_single_article(self, url: str) -> Dict:
        """
        Scrape a single article from a specific URL
        
        Args:
            url: Article URL
            
        Returns:
            Article dictionary
        """
        logger.info(f"Scraping single article: {url}")
        article_data = self._extract_article(url)
        
        if self._is_valid_article(article_data):
            return article_data
        else:
            raise ValueError("Article does not meet minimum quality requirements")