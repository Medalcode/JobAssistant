from .base import BaseAgent
from skills.document_engineering import DocumentEngineeringSkill
from skills.content_analysis import ContentAnalysisSkill

class ResumeArchitect(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Resume Architect",
            role="Senior CV Designer",
            goal="Create professional, ATS-friendly PDF resumes.",
            backstory="A design-focused agent obsessed with typography and layout."
        )
        self.add_tool("generate_pdf", DocumentEngineeringSkill.generate_pdf)
        self.add_tool("analyze_ats", ContentAnalysisSkill.calculated_ats_score)

    def optimize_content(self, data: dict, target_role: str = "") -> dict:
        """
        Prioritizes skills and experiences based on a target role.
        """
        optimized = data.copy()
        
        # 1. Skill Sorting
        # Move skills matching the target role/title to the top
        target_keywords = (target_role or data.get('candidate', {}).get('professional_title', '')).lower().split()
        
        def skill_score(skill):
            name = skill.get('name', '').lower()
            return sum(2 for k in target_keywords if k in name) + (1 if skill.get('level') in ['Expert', 'Advanced'] else 0)

        if 'skills' in optimized:
            optimized['skills'] = sorted(optimized['skills'], key=skill_score, reverse=True)
            print(f"[{self.name}] Re-ordered skills to prioritize relevance to '{target_role}'")

        return optimized

    def audit_resume(self, resume_text: str, job_description: str) -> dict:
        """
        Audits the resume against a job description simulating an ATS.
        """
        print(f"[{self.name}] Auditing resume against job description...")
        result = self.act("analyze_ats", resume_text=resume_text, job_description=job_description)
        print(f"[{self.name}] ATS Score: {result['score']}%")
        if result['missing']:
            print(f"[{self.name}] Critical Missing Keywords: {', '.join(result['missing'][:5])}")
        return result

    def run(self, candidate_data: dict, style: str = "classic", output_path: str = "output.pdf") -> str:
        role = candidate_data.get('candidate', {}).get('professional_title', '')
        print(f"[{self.name}] Received task: Generate {style} resume for {role}")
        
        # Optimize before generating
        final_data = self.optimize_content(candidate_data, target_role=role)
        
        result_path = self.act("generate_pdf", data=final_data, style=style, output_path=output_path)
        print(f"[{self.name}] Resume generated at: {result_path}")
        return result_path
