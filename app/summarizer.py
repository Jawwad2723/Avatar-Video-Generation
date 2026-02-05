"""
News Summarizer Module
Uses OpenAI LLM to generate article summaries
"""

import openai
from openai import OpenAI
import logging
from typing import Dict
from app.config import settings

logger = logging.getLogger(__name__)

class NewsSummarizer:
    """
    Summarizes news articles using OpenAI's GPT models
    """
    
    def __init__(self):
        """
        Initialize OpenAI client with API key
        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        logger.info(f"Initialized NewsSummarizer with model: {self.model}")
    
    def summarize_article(self, title: str, content: str) -> str:
        """
        Generate a concise summary of a news article
        OPTIMIZED FOR D-ID FREE TIER - Creates 2 sentence summaries
        
        Args:
            title: Article title
            content: Full article text
            
        Returns:
            2 sentence summary in neutral, factual tone
        """
        try:
            logger.info(f"Summarizing article: {title[:60]}...")
            
            # Create the prompt for summarization
            prompt = self._create_summary_prompt(title, content)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional news editor. Create ultra-concise "
                            "summaries of news articles in EXACTLY 2 sentences. "
                            "Use neutral, objective tone. Focus on the most important fact only. "
                            "Each sentence should be under 20 words. Be brief and direct."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Low temperature for factual consistency
                max_tokens=80  # Reduced from 150 for shorter summaries
            )
            
            # Extract summary from response
            summary = response.choices[0].message.content.strip()
            
            logger.info(f"Successfully generated summary ({len(summary)} chars)")
            return summary
            
        except openai.AuthenticationError:
            logger.error("OpenAI authentication failed. Check API key.")
            raise ValueError("Invalid OpenAI API key")
        
        except openai.RateLimitError:
            logger.error("OpenAI rate limit exceeded")
            raise ValueError("OpenAI rate limit exceeded. Please try again later.")
        
        except Exception as e:
            logger.error(f"Error in summarization: {str(e)}")
            raise ValueError(f"Failed to summarize article: {str(e)}")
    
    def _create_summary_prompt(self, title: str, content: str) -> str:
        """
        Create the prompt for article summarization
        OPTIMIZED FOR FREE TIER - Asks for very short summaries
        
        Args:
            title: Article title
            content: Full article text
            
        Returns:
            Formatted prompt string
        """
        # Truncate content if too long (to avoid token limits)
        max_content_length = 2000  # Reduced from 3000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        prompt = f"""
Title: {title}

Article Content:
{content}

Task: Provide a summary in EXACTLY 2 short sentences (under 20 words each).
Focus only on the single most important fact.
Use simple, clear language suitable for a brief news update.
"""
        return prompt
    
    def batch_summarize(self, articles: list) -> list:
        """
        Summarize multiple articles
        
        Args:
            articles: List of article dictionaries with 'title' and 'content'
            
        Returns:
            List of summaries in same order as input
        """
        summaries = []
        
        for idx, article in enumerate(articles, 1):
            try:
                logger.info(f"Summarizing article {idx}/{len(articles)}")
                summary = self.summarize_article(
                    title=article.get('title', ''),
                    content=article.get('content', '')
                )
                summaries.append(summary)
            except Exception as e:
                logger.warning(f"Failed to summarize article {idx}: {str(e)}")
                # Use title as fallback
                summaries.append(f"Summary unavailable: {article.get('title', 'Unknown')}")
        
        return summaries