from .base import BaseAgent
from skills.market_research import MarketResearchSkill
import time

class JobScout(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Job Scout",
            role="Recruitment Intelligence Specialist", 
            goal="Identify high-quality job opportunities matching the candidate's profile.",
            backstory="An expert recruiter algorithm designed to filter through noise and identify high-quality job listings.",
        )
        self.add_tool("search_jobs", MarketResearchSkill.search_jobs)

        # Knowledge Base simple (Synonyms map)
        self.synonyms = {
            "python": ["django", "flask", "backend developer", "software engineer"],
            "react": ["frontend developer", "javascript", "typescript", "next.js"],
            "node": ["backend developer", "javascript", "express"],
            "data scientist": ["data analyst", "machine learning", "python"],
            "devops": ["sre", "cloud engineer", "aws", "docker"],
        }

    def expand_query(self, query: str) -> list:
        """Expands a single query into related terms based on knowledge base."""
        query_lower = query.lower()
        expanded = [query]
        
        for key, distinct_terms in self.synonyms.items():
            if key in query_lower:
                expanded.extend(distinct_terms)
        
        # Deduplicate and limit to 3 extra terms to avoid spamming
        return list(dict.fromkeys(expanded))[:3]

    def run(self, query: str, location: str = "") -> list:
        print(f"[{self.name}] Received task: Search jobs for '{query}' in '{location}'")
        
        # 1. Expand Query
        search_terms = self.expand_query(query)
        print(f"[{self.name}] Strategy: Expanded search terms -> {search_terms}")
        
        all_jobs = []
        seen_urls = set()

        # 2. Parallel/Sequential Exec (Sequential for now)
        for term in search_terms:
            print(f"[{self.name}] Searching specifically for: '{term}'...")
            jobs = self.act("search_jobs", query=term, location=location)
            
            for job in jobs:
                if job['url'] not in seen_urls:
                    all_jobs.append(job)
                    seen_urls.add(job['url'])
            
            # Politeness delay between batches
            if len(search_terms) > 1:
                time.sleep(2)

        print(f"[{self.name}] Found {len(all_jobs)} unique jobs after deductive reasoning.")
        return all_jobs
