"""
Script Generator Module
Converts article summaries into news anchor script
"""

import logging
from typing import List, Dict
from datetime import datetime
from app.config import settings

logger = logging.getLogger(__name__)

class ScriptGenerator:
    """
    Generates professional news anchor scripts from article summaries
    """
    
    def __init__(self):
        logger.info("Initialized ScriptGenerator")
    
    def generate_script(self, articles: List[Dict]) -> str:
        """
        Generate a complete news anchor script from article summaries
        OPTIMIZED FOR D-ID FREE TIER (short, concise script)
        
        Args:
            articles: List of article dictionaries with 'title' and 'summary'
            
        Returns:
            Complete news script (30-45 seconds = ~75-110 words for free tier)
        """
        try:
            logger.info(f"Generating script from {len(articles)} articles")
            
            # Build script components - SHORTENED for free tier
            opening = self._create_opening_short()
            headlines = self._create_headlines_short(articles)
            closing = self._create_closing_short()
            
            # Combine into full script
            script = f"{opening} {headlines} {closing}"
            
            # Log script details
            word_count = len(script.split())
            estimated_seconds = word_count / 2.5  # Average speaking rate
            
            logger.info(f"Generated script: {word_count} words, ~{estimated_seconds:.0f} seconds")
            
            # Warn if too long for free tier
            if estimated_seconds > 180:  # 3 minutes max for free tier
                logger.warning(f"Script may be too long for D-ID free tier ({estimated_seconds:.0f}s > 180s)")
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            raise ValueError(f"Failed to generate script: {str(e)}")
    
    def _create_opening_short(self) -> str:
        """
        Create SHORT opening line for news broadcast (free tier optimized)
        
        Returns:
            Opening sentence
        """
        current_date = datetime.utcnow().strftime("%B %d, %Y")
        return f"Here are today's top stories for {current_date}."
    
    def _create_headlines_short(self, articles: List[Dict]) -> str:
        """
        Create CONCISE headlines section from articles (free tier optimized)
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Formatted headlines text (shortened summaries)
        """
        headlines = []
        
        for idx, article in enumerate(articles, 1):
            summary = article.get('summary', '')
            
            # Shorten each summary to first 2 sentences only
            sentences = summary.split('.')
            short_summary = '. '.join(sentences[:2]).strip()
            if short_summary and not short_summary.endswith('.'):
                short_summary += '.'
            
            # Simple transitions for brevity
            if idx == 1:
                headline = short_summary
            else:
                headline = short_summary
            
            headlines.append(headline)
        
        return " ".join(headlines)
    
    def _create_closing_short(self) -> str:
        """
        Create SHORT closing line for news broadcast (free tier optimized)
        
        Returns:
            Closing sentence
        """
        return "That's your news update."
    
    def _create_opening(self) -> str:
        """
        Create opening line for news broadcast
        
        Returns:
            Opening sentence
        """
        current_date = datetime.utcnow().strftime("%B %d, %Y")
        
        openings = [
            f"Good day. Here are today's top stories for {current_date}.",
            f"Welcome to your news update for {current_date}. Here's what's happening around the world.",
            f"Hello and welcome. These are the headlines for {current_date}.",
            f"Good day, everyone. Here's your news briefing for {current_date}."
        ]
        
        # Use first opening for consistency
        return openings[0]
    
    def _create_headlines(self, articles: List[Dict]) -> str:
        """
        Create the main headlines section from articles
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Formatted headlines text
        """
        headlines = []
        
        for idx, article in enumerate(articles, 1):
            summary = article.get('summary', '')
            
            # Format each headline with transition words
            if idx == 1:
                headline = f"In our lead story, {summary}"
            elif idx == len(articles):
                headline = f"And finally, {summary}"
            else:
                transitions = ["Next,", "In other news,", "Also today,", "Meanwhile,"]
                transition = transitions[min(idx - 2, len(transitions) - 1)]
                headline = f"{transition} {summary}"
            
            headlines.append(headline)
        
        return "\n\n".join(headlines)
    
    def _create_closing(self) -> str:
        """
        Create closing line for news broadcast
        
        Returns:
            Closing sentence
        """
        closings = [
            "That's all for now. Stay informed and have a great day.",
            "Those are today's top stories. Thank you for watching.",
            "And that wraps up today's news briefing. We'll see you next time.",
            "That concludes our news update. Stay safe and stay informed."
        ]
        
        # Use first closing for consistency
        return closings[0]
    
    def estimate_reading_time(self, script: str) -> int:
        """
        Estimate reading time in seconds
        
        Args:
            script: Full script text
            
        Returns:
            Estimated seconds (assumes 150 words per minute)
        """
        words = len(script.split())
        seconds = (words / 150) * 60
        return int(seconds)
    
    def optimize_script_length(self, script: str, target_seconds: int = 40) -> str:
        """
        Optimize script to target length
        
        Args:
            script: Original script
            target_seconds: Target length in seconds
            
        Returns:
            Optimized script
        """
        current_time = self.estimate_reading_time(script)
        
        if current_time <= target_seconds:
            logger.info(f"Script length OK: {current_time}s (target: {target_seconds}s)")
            return script
        
        logger.info(f"Script too long: {current_time}s (target: {target_seconds}s)")
        
        # Simple optimization: return original
        # In production, could use LLM to condense
        return script