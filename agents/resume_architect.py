from .base import BaseAgent
from skills.document_engineering import DocumentEngineeringSkill

class ResumeArchitect(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Resume Architect",
            role="Senior CV Designer",
            goal="Create professional, ATS-friendly PDF resumes.",
            backstory="A design-focused agent obsessed with typography and layout."
        )
        self.add_tool("generate_pdf", DocumentEngineeringSkill.generate_pdf)

    def run(self, candidate_data: dict, style: str = "classic", output_path: str = "output.pdf") -> str:
        print(f"[{self.name}] Received task: Generate {style} resume for {candidate_data.get('candidate', {}).get('full_name')}")
        result_path = self.act("generate_pdf", data=candidate_data, style=style, output_path=output_path)
        print(f"[{self.name}] Resume generated at: {result_path}")
        return result_path
