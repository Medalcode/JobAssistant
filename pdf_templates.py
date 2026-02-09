from fpdf import FPDF

class BasePDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.candidate = data['candidate']
        self.experiences = data['experiences']
        self.educations = data['educations']
        self.skills = data['skills']
        self.languages = data['languages']
        self.certifications = data['certifications']
        self.projects = data['projects']
        self.links = data['links']
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Default header (blank)
        pass

    def footer(self):
        # Default footer (page number)
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def generate(self):
        self.add_page()
        self.draw_content()
        return self

    def draw_content(self):
        raise NotImplementedError("Subclasses must implement draw_content")


class ClassicPDF(BasePDF):
    def draw_content(self):
        self.set_font("Arial", "B", 16)
        
        # Header
        self.cell(0, 10, self.candidate["full_name"], ln=True, align="C")
        self.set_font("Arial", "", 12)
        if self.candidate["professional_title"]:
            self.cell(0, 7, self.candidate["professional_title"], ln=True, align="C")
            
        contact_info = []
        if self.candidate["email"]: contact_info.append(self.candidate["email"])
        if self.candidate["phone"]: contact_info.append(self.candidate["phone"])
        if self.candidate["location"]: contact_info.append(self.candidate["location"])
        
        self.ln(5)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, " | ".join(contact_info), align="C")
        
        # Links
        links_info = []
        if self.candidate["linkedin"]: links_info.append(f"LinkedIn: {self.candidate['linkedin']}")
        if self.candidate["github"]: links_info.append(f"GitHub: {self.candidate['github']}")
        if self.candidate["portfolio"]: links_info.append(f"Portfolio: {self.candidate['portfolio']}")
        
        if links_info:
            self.ln(2)
            self.multi_cell(0, 5, " | ".join(links_info), align="C")

        self.ln(10)

        # Summary
        if self.candidate["summary"]:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Professional Summary", ln=True)
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 5, self.candidate["summary"])
            self.ln(5)

        # Experience
        if self.experiences:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Experience", ln=True)
            for exp in self.experiences:
                self.set_font("Arial", "B", 10)
                self.cell(0, 6, f"{exp['role']} at {exp['company']}", ln=True)
                self.set_font("Arial", "I", 9)
                date_range = f"{exp['start_date']} - {exp['end_date']}"
                if exp['location']:
                    date_range += f" | {exp['location']}"
                self.cell(0, 5, date_range, ln=True)
                
                if exp['description']:
                    self.set_font("Arial", "", 10)
                    self.multi_cell(0, 5, exp['description'])
                self.ln(3)
            self.ln(2)

        # Education
        if self.educations:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Education", ln=True)
            for edu in self.educations:
                self.set_font("Arial", "B", 10)
                self.cell(0, 6, f"{edu['institution']}", ln=True)
                self.set_font("Arial", "", 10)
                self.cell(0, 5, f"{edu['degree']} in {edu['field']}", ln=True)
                self.set_font("Arial", "I", 9)
                self.cell(0, 5, f"{edu['start_date']} - {edu['end_date']}", ln=True)
                if edu['description']:
                    self.set_font("Arial", "", 9)
                    self.multi_cell(0, 4, edu['description'])
                self.ln(3)
            self.ln(2)

        # Skills
        if self.skills:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Skills", ln=True)
            self.set_font("Arial", "", 10)
            skills_list = []
            for skill in self.skills:
                s = skill['name']
                if skill['level']: s += f" ({skill['level']})"
                skills_list.append(s)
            self.multi_cell(0, 5, ", ".join(skills_list))
            self.ln(5)

        # Languages
        if self.languages:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Languages", ln=True)
            self.set_font("Arial", "", 10)
            langs = []
            for lang in self.languages:
                l = lang['name']
                if lang['level']: l += f" ({lang['level']})"
                langs.append(l)
            self.multi_cell(0, 5, ", ".join(langs))
            self.ln(5)
            
        # Projects, Certs... omitted for brevity in base model but added if requested. 
        # I'll include Projects and Certs to be complete with previous implementation.
        
        # Projects
        if self.projects:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Projects", ln=True)
            for proj in self.projects:
                self.set_font("Arial", "B", 10)
                title = proj['name']
                if proj['role']: title += f" - {proj['role']}"
                self.cell(0, 6, title, ln=True)
                if proj['url']:
                    self.set_font("Arial", "U", 9)
                    self.cell(0, 4, proj['url'], ln=True)
                if proj['technologies']:
                    self.set_font("Arial", "I", 9)
                    self.cell(0, 4, f"Tech: {proj['technologies']}", ln=True)
                if proj['description']:
                    self.set_font("Arial", "", 9)
                    self.multi_cell(0, 4, proj['description'])
                self.ln(3)
            self.ln(2)

        # Certifications
        if self.certifications:
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Certifications", ln=True)
            self.set_font("Arial", "", 10)
            for cert in self.certifications:
                text = f"{cert['name']} - {cert['issuer']}"
                if cert['date']: text += f" ({cert['date']})"
                self.multi_cell(0, 5, text)
            self.ln(5)


class ModernPDF(BasePDF):
    def draw_content(self):
        # Modern Look: Left sidebar with contact/skills, right content
        # For simplicity in logic within draw_content, we'll mimic a clean modern header
        # with lines and different fonts if possible (standard fonts only in fpdf without importing ttf).
        
        self.set_font("Times", "B", 24)
        self.set_text_color(50, 50, 150) # Blueish title
        self.cell(0, 15, self.candidate["full_name"].upper(), ln=True, align="L")
        
        self.set_font("Times", "I", 14)
        self.set_text_color(100, 100, 100) # Gray
        if self.candidate["professional_title"]:
            self.cell(0, 10, self.candidate["professional_title"], ln=True, align="L")
            
        # Horizontal Rule
        self.set_draw_color(50, 50, 150)
        self.set_line_width(1)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        
        # Contact Info (Small, right aligned or just below)
        self.set_font("Arial", "", 9)
        self.set_text_color(0, 0, 0)
        
        contact_lines = []
        if self.candidate["email"]: contact_lines.append(self.candidate["email"])
        if self.candidate["phone"]: contact_lines.append(self.candidate["phone"])
        if self.candidate["location"]: contact_lines.append(self.candidate["location"])
        
        # Links
        if self.candidate["linkedin"]: contact_lines.append(f"LinkedIn: {self.candidate['linkedin']}")
        if self.candidate["github"]: contact_lines.append(f"GitHub: {self.candidate['github']}")
        if self.candidate["portfolio"]: contact_lines.append(f"Portfolio: {self.candidate['portfolio']}")

        for line in contact_lines:
            self.cell(0, 5, line, ln=True, align="R")
            
        self.ln(10)
        
        # Summary
        if self.candidate["summary"]:
             self.section_title("PROFILE")
             self.set_font("Times", "", 11)
             self.multi_cell(0, 5, self.candidate["summary"])
             self.ln(5)

        # Experience
        if self.experiences:
            self.section_title("PROFESSIONAL EXPERIENCE")
            for exp in self.experiences:
                self.set_font("Arial", "B", 11)
                self.cell(0, 6, exp['company'].upper(), ln=True)
                
                self.set_font("Arial", "BI", 10)
                self.cell(130, 6, exp['role'])
                self.set_font("Arial", "I", 9)
                self.cell(0, 6, f"{exp['start_date']} - {exp['end_date']}", align="R", ln=True)
                
                if exp['location']:
                    self.set_font("Arial", "I", 9)
                    self.cell(0, 5, exp['location'], ln=True)
                
                if exp['description']:
                    self.set_font("Times", "", 10)
                    self.multi_cell(0, 5, exp['description'])
                self.ln(4)

        # Education
        if self.educations:
            self.section_title("EDUCATION")
            for edu in self.educations:
                self.set_font("Arial", "B", 11)
                self.cell(140, 6, edu['institution'])
                self.set_font("Arial", "I", 9)
                self.cell(0, 6, f"{edu['start_date']} - {edu['end_date']}", align="R", ln=True)
                
                self.set_font("Times", "", 10)
                self.cell(0, 5, f"{edu['degree']} in {edu['field']}", ln=True)
                if edu['description']:
                    self.multi_cell(0, 5, edu['description'])
                self.ln(3)

        # Skills & Languages side by side (using columns logic is complex without MultiCell support for columns)
        # We'll just stack them cleaner
        if self.skills or self.languages:
            self.section_title("SKILLS & LANGUAGES")
            if self.skills:
                self.set_font("Arial", "B", 10)
                self.cell(30, 6, "Skills:")
                self.set_font("Times", "", 10)
                skills_list = [s['name'] for s in self.skills]
                self.multi_cell(0, 6, ", ".join(skills_list))
            
            if self.languages:
                self.set_font("Arial", "B", 10)
                self.cell(30, 6, "Languages:")
                self.set_font("Times", "", 10)
                langs = [f"{l['name']} ({l['level']})" for l in self.languages]
                self.multi_cell(0, 6, ", ".join(langs))
            self.ln(5)

        # Projects
        if self.projects:
             self.section_title("PROJECTS")
             for proj in self.projects:
                 self.set_font("Arial", "B", 10)
                 self.cell(0, 6, proj['name'], ln=True)
                 if proj['role']:
                     self.set_font("Arial", "I", 9)
                     self.cell(0, 4, proj['role'], ln=True)
                 if proj['description']:
                     self.set_font("Times", "", 10)
                     self.multi_cell(0, 5, proj['description'])
                 self.ln(3)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(50, 50, 150)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_text_color(0, 0, 0)

class TemplateUnoPDF(BasePDF):
    def draw_content(self):
        # Template Uno: A distinct style with a dark sidebar or header
        
        # Header Background (Dark Blue/Black)
        self.set_fill_color(33, 47, 61)
        self.rect(0, 0, 210, 40, 'F')
        
        # Name
        self.set_y(10)
        self.set_font("Arial", "B", 24)
        self.set_text_color(255, 255, 255) # White
        self.cell(0, 10, self.candidate["full_name"].upper(), ln=True, align="C")
        
        # Title
        self.set_font("Arial", "", 14)
        self.set_text_color(220, 220, 220) # Light Gray
        if self.candidate["professional_title"]:
            self.cell(0, 8, self.candidate["professional_title"], ln=True, align="C")
            
        self.set_y(45) # Move cursor below header
        self.set_text_color(0, 0, 0) # Reset to black
        
        # Contact Info
        self.set_font("Arial", "", 9)
        contact_parts = []
        if self.candidate["email"]: contact_parts.append(self.candidate["email"])
        if self.candidate["phone"]: contact_parts.append(self.candidate["phone"])
        if self.candidate["location"]: contact_parts.append(self.candidate["location"])
        
        self.cell(0, 6, " | ".join(contact_parts), ln=True, align="C")
        
        # Links
        link_parts = []
        if self.candidate["linkedin"]: link_parts.append(f"LI: {self.candidate['linkedin']}")
        if self.candidate["github"]: link_parts.append(f"GH: {self.candidate['github']}")
        if self.candidate["portfolio"]: link_parts.append(f"Web: {self.candidate['portfolio']}")
        
        if link_parts:
            self.cell(0, 6, " | ".join(link_parts), ln=True, align="C")
            
        self.ln(5)
        
        # Two column layout attempt (simulated with indent/cells)
        col_width = 90
        
        # Summary
        if self.candidate["summary"]:
             self.section_header("PERFIL PROFESIONAL")
             self.set_font("Arial", "", 10)
             self.multi_cell(0, 5, self.candidate["summary"])
             self.ln(5)
             
        # Experience
        if self.experiences:
            self.section_header("EXPERIENCIA LABORAL")
            for exp in self.experiences:
                self.set_font("Arial", "B", 11)
                self.cell(0, 6, exp['company'], ln=True)
                
                self.set_font("Arial", "BI", 10)
                self.cell(0, 6, f"{exp['role']} | {exp['start_date']} - {exp['end_date']}", ln=True)
                
                if exp['location']:
                    self.set_font("Arial", "I", 9)
                    self.cell(0, 5, exp['location'], ln=True)
                
                if exp['description']:
                    self.set_font("Arial", "", 10)
                    self.multi_cell(0, 5, exp['description'])
                self.ln(4)

        # Education
        if self.educations:
            self.section_header("EDUCACIÓN")
            for edu in self.educations:
                self.set_font("Arial", "B", 11)
                self.cell(0, 6, f"{edu['institution']} - {edu['degree']}", ln=True)
                self.set_font("Arial", "I", 9)
                self.cell(0, 5, f"{edu['start_date']} - {edu['end_date']}", ln=True)
                if edu['field']:
                     self.set_font("Arial", "", 10)
                     self.cell(0, 5, edu['field'], ln=True)
                self.ln(3)

        # Skills
        if self.skills:
             self.section_header("HABILIDADES")
             skills_list = [s['name'] for s in self.skills]
             self.set_font("Arial", "", 10)
             self.multi_cell(0, 5, ", ".join(skills_list))
             self.ln(4)

        # Languages
        if self.languages:
             self.section_header("IDIOMAS")
             langs_list = [f"{l['name']} ({l['level']})" for l in self.languages]
             self.set_font("Arial", "", 10)
             self.multi_cell(0, 5, ", ".join(langs_list))
             self.ln(4)

        # Projects
        if self.projects:
             self.section_header("PROYECTOS")
             for proj in self.projects:
                 self.set_font("Arial", "B", 10)
                 self.cell(0, 6, proj['name'], ln=True)
                 if proj['role']:
                     self.set_font("Arial", "I", 9)
                     self.cell(0, 4, proj['role'], ln=True)
                 if proj['description']:
                     self.set_font("Arial", "", 10)
                     self.multi_cell(0, 5, proj['description'])
                 self.ln(3)

    def section_header(self, title):
        self.set_font("Arial", "B", 12)
        # Background for section header
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title.upper(), ln=True, fill=True, border='L')
        self.ln(2)
