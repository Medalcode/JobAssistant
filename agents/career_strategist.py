from .base import BaseAgent

class CareerStrategist(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Career Strategist",
            role="Personal Career Coach",
            goal="Analyze profiles and generate professional summaries.", 
            backstory="A seasoned career counselor who knows how to highlight a candidate's strengths."
        )

    def analyze_seniority(self, years_exp: int) -> str:
        if years_exp == 0: return "Entry-Level"
        if years_exp < 3: return "Junior"
        if years_exp < 6: return "Mid-Level"
        if years_exp < 10: return "Senior"
        return "Lead/Principal"

    def identify_gaps(self, title: str, skills: list) -> list:
        """Simple gap analysis based on title keywords and missing skills."""
        title_lower = title.lower()
        skill_names = [s.lower() for s in skills]
        suggestions = []

        if "full stack" in title_lower:
            if not any(x in skill_names for x in ["react", "vue", "angular"]):
                suggestions.append("Consider learning a modern frontend framework (React/Vue).")
            if not any(x in skill_names for x in ["node", "python", "java", "c#", "php"]):
                suggestions.append("Strengthen your backend skills (Node/Python/Java).")

        if "data" in title_lower:
             if not any(x in skill_names for x in ["sql", "pandas", "python"]):
                suggestions.append("Data roles require strong SQL and Python foundations.")

        return suggestions

    def run(self, profile_data: dict) -> dict:
        """
        Returns a dict with: 
        - summaries: list of strings
        - analysis: dict with 'seniority', 'suggestions'
        """
        title = profile_data.get('professional_title', 'Profesional')
        skills = [s.get('name') for s in profile_data.get('skills', [])]
        roles = [e.get('role') for e in profile_data.get('experiences', [])]
        years_exp = len(profile_data.get('experiences', [])) * 2 # Crude heuristic: 2 years per role? better to just count entries for now.
        
        print(f"[{self.name}] Analyzing profile for {title}...")

        # 1. Determine Seniority Level
        seniority = self.analyze_seniority(len(profile_data.get('experiences', [])))
        
        # 2. Gap Analysis
        gaps = self.identify_gaps(title, skills)
        if gaps:
            print(f"[{self.name}] Advisory: {gaps}")

        # 3. Generate Summaries based on Seniority
        top_skills = ", ".join(skills[:5]) if skills else "habilidades clave"
        last_role = roles[0] if roles else "Profesional"
        
        summaries = []
        
        # Strategy A: Experience-based (High seniority)
        if seniority in ["Senior", "Lead/Principal"]:
            summaries.append(f"{title} nivel {seniority} con sólida trayectoria como {last_role}. Liderazgo técnico en {top_skills}. Enfocado en arquitecturas escalables y mentoría de equipos.")
        else:
            summaries.append(f"{title} con experiencia como {last_role}. Competente en {top_skills}. Busco oportunidades para aplicar mis conocimientos en proyectos desafiantes.")
            
        # Strategy B: Skill-focused
        summaries.append(f"Especialista en {top_skills} con enfoque en resultados. Experiencia práctica en {last_role}, comprometido con la calidad de código y las mejores prácticas.")

        # Strategy C: Impact-focused
        summaries.append(f"{title} proactivo y orientado a objetivos. Historial demostrado en {last_role}. Capacidad para {top_skills} y resolución de problemas complejos.")

        return {
            "summaries": summaries,
            "analysis": {
                "seniority": seniority,
                "suggestions": gaps
            }
        }
