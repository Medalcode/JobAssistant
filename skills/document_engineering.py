import sys
import os

# Ensure parent directory is in path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf_templates import ClassicPDF, ModernPDF, TemplateUnoPDF

class DocumentEngineeringSkill:
    """Skill capability for generating PDF documents."""

    @staticmethod
    def generate_pdf(data: dict, style: str, output_path: str) -> str:
        """
        Generates a PDF resume based on the data and style.
        Returns the path to the generated file.
        """
        print(f"[Skill:DocumentEngineering] Generating {style} PDF at {output_path}...")
        
        if style == "modern":
            pdf = ModernPDF(data)
        elif style == "uno":
            pdf = TemplateUnoPDF(data)
        else:
            pdf = ClassicPDF(data)
            
        pdf.generate()
        pdf.output(output_path, 'F')
        return output_path
