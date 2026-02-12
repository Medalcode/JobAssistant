from .base import BaseAgent

class CareerStrategist(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Career Strategist",
            role="Personal Career Coach",
            goal="Analyze profiles and generate professional summaries.", 
            backstory="A seasoned career counselor who knows how to highlight a candidate's strengths."
        )
        # In a real scenario, this would use an LLM API. 
        # Here we use heuristic logic as a 'tool' implementation.

    def generate_summary(self, title: str, skills: list, experience_roles: list) -> list:
        """
        Generates professional summaries based on heuristics 
        (mirroring app.py logic but encapsulated in the agent).
        """
        top_skills = ", ".join(skills[:5]) if skills else "habilidades clave"
        last_role = experience_roles[0] if experience_roles else "Profesional"
        
        options = []
        # Option 1: Standard
        options.append(f"{title} con experiencia sólida como {last_role}. EXPERTO en {top_skills}. Busco aportar mis conocimientos en proyectos desafiantes.")
        # Option 2: Passionate
        options.append(f"Apasionado {title} especializado en {top_skills}. Con trayectoria probada en {', '.join(experience_roles[:2])}, enfocado en la entrega de soluciones de alta calidad.")
        # Option 3: Impact
        options.append(f"{title} altamente motivado con enfoque en resultados. Dominio de {top_skills}. Historial comprobado de éxito en entornos dinámicos.")
        
        return options

    def run(self, profile_data: dict) -> list:
        print(f"[{self.name}] Received task: Analyze profile for {profile_data.get('professional_title', 'Unknown')}")
        
        skills = [s.get('name') for s in profile_data.get('skills', [])]
        roles = [e.get('role') for e in profile_data.get('experiences', [])]
        title = profile_data.get('professional_title', 'Profesional')

        summaries = self.generate_summary(title, skills, roles)
        print(f"[{self.name}] Generated {len(summaries)} summary options.")
        return summaries
