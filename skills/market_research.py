import sys
import os

# Ensure parent directory is in path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import scrape_jobs

class MarketResearchSkill:
    """Skill capability for Market Research (Job Searching)"""
    
    @staticmethod
    def search_jobs(query: str, location: str = "") -> list:
        """
        Searches for jobs using the underlying scraper.
        """
        print(f"[Skill:MarketResearch] Searching for '{query}' in '{location}'...")
        return scrape_jobs(query, location)
