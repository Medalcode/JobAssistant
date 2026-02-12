from .base import BaseAgent
from skills.market_research import MarketResearchSkill
from skills.content_analysis import ContentAnalysisSkill
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
        self.add_tool("analyze_match", ContentAnalysisSkill.calculated_ats_score)

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

    def run(self, query: str, location: str = "", profile_data: dict = None) -> list:
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
            
                if len(search_terms) > 1:
                    time.sleep(2)

        print(f"[{self.name}] Found {len(all_jobs)} unique jobs after deductive reasoning.")

        # 3. Rank by Profile Match (if profile provided)
        if profile_data:
            print(f"[{self.name}] Ranking {len(all_jobs)} jobs against candidate profile...")
            ranked_jobs = []
            
            # Construct a simple text represention of the profile
            skills_text = " ".join([s.get('name', '') for s in profile_data.get('skills', [])])
            title_text = profile_data.get('professional_title', '')
            profile_text = f"{title_text} {skills_text}"

            for job in all_jobs:
                # Use description if available, else title + company
                job_text = job.get('description', '') or f"{job['title']} {job['company']}"
                
                match_result = self.act("analyze_match", resume_text=profile_text, job_description=job_text)
                job['match_score'] = match_result['score']
                ranked_jobs.append(job)
            
            # Sort by score desc
            all_jobs = sorted(ranked_jobs, key=lambda x: x['match_score'], reverse=True)
            
        return all_jobs
