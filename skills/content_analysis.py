
import re
from collections import Counter

class ContentAnalysisSkill:
    """
    Skill for analyzing text content (ATS Simulation).
    """

    @staticmethod
    def extract_keywords(text: str) -> list:
        """
        Extracts significant keywords from a text.
        Simple heuristic: words > 3 chars, ignoring common stop words.
        """
        text = text.lower()
        # Remove special chars
        text = re.sub(r'[^a-z0-9\s]', '', text)
        words = text.split()
        
        stop_words = {
            "the", "and", "for", "with", "that", "this", "from", "your", "will", 
            "have", "work", "team", "experience", "skill", "year", "role", "knowledge",
            "proficiency", "ability", "strong", "excellent", "proven", "track", "record"
        }
        
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        return keywords

    @staticmethod
    def calculated_ats_score(resume_text: str, job_description: str) -> dict:
        """
        Compares Resume vs Job Description.
        Returns:
            - score (0-100)
            - missing_keywords (list)
            - matched_keywords (list)
        """
        job_keywords = ContentAnalysisSkill.extract_keywords(job_description)
        resume_keywords = ContentAnalysisSkill.extract_keywords(resume_text)
        
        job_counter = Counter(job_keywords)
        resume_counter = Counter(resume_keywords)
        
        # Calculate overlap
        matched = []
        missing = []
        
        total_weight = sum(job_counter.values())
        if total_weight == 0:
            return {"score": 100, "missing": [], "matched": []}
            
        score_points = 0
        
        for word, count in job_counter.items():
            if word in resume_counter:
                matched.append(word)
                score_points += count
            else:
                missing.append(word)
                
        final_score = int((score_points / total_weight) * 100)
        
        # Sort missing by frequency (importance)
        missing_sorted = sorted(missing, key=lambda w: job_counter[w], reverse=True)

        return {
            "score": final_score,
            "missing": missing_sorted[:10], # Top 10 missing
            "matched": matched
        }
