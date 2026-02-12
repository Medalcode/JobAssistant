from .base import BaseAgent
from skills.market_research import MarketResearchSkill

class JobScout(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Job Scout",
            role="Recruitment Intelligence Specialist", 
            goal="Identify high-quality job opportunities matching the candidate's profile.",
            backstory="An expert recruiter algorithm designed to filter through noise and identify high-quality job listings.",
        )
        self.add_tool("search_jobs", MarketResearchSkill.search_jobs)

    def run(self, query: str, location: str = "") -> list:
        print(f"[{self.name}] Received task: Search jobs for '{query}' in '{location}'")
        jobs = self.act("search_jobs", query=query, location=location)
        print(f"[{self.name}] Found {len(jobs)} jobs.")
        return jobs
