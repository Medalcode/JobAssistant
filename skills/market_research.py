
from agents.base import BaseAgent
from scrapers.computrabajo import scrape_computrabajo

class MarketResearchSkill:
    """Skill capability for Market Research (Job Searching)"""
    
    @staticmethod
    def search_jobs(query: str, location: str = "") -> list:
        """
        Searches for jobs using the underlying scraper.
        """
        print(f"[Skill:MarketResearch] Searching for '{query}' in '{location}' via Computrabajo...")
        return scrape_computrabajo(query, location)
