
import pytest
import os
from pdf_templates import ClassicPDF, ModernPDF, TemplateUnoPDF

@pytest.fixture
def sample_data():
    return {
        "candidate": {
            "full_name": "Test User",
            "professional_title": "Developer",
            "email": "test@test.com",
            "phone": "123456789",
            "location": "Test City",
            "linkedin": "http://linkedin.com",
            "github": "http://github.com",
            "portfolio": "http://portfolio.com",
            "summary": "This is a summary."
        },
        "experiences": [
            {
                "company": "Comp A", 
                "role": "Role A", 
                "start_date": "2020", 
                "end_date": "2021", 
                "description": "Desc",
                "achievements": "Did great things",
                "location": "Remote"
            }
        ],
        "educations": [
            {
                "institution": "Univ A", 
                "degree": "Degree A", 
                "start_date": "2016", 
                "end_date": "2020",
                "field": "CS",
                "description": "Learned stuff"
            }
        ],
        "skills": [
            {"name": "Python", "level": "Expert", "category": "Backend"}, 
            {"name": "Flask", "level": "Advanced", "category": "Backend"}
        ],
        "languages": [{"name": "English", "level": "C1"}],
        "certifications": [],
        "projects": [],
        "links": []
    }

def test_classic_pdf(sample_data):
    pdf = ClassicPDF(sample_data)
    pdf.generate()
    output = pdf.output(dest='S').encode('latin-1')
    assert output.startswith(b'%PDF')

def test_modern_pdf(sample_data):
    pdf = ModernPDF(sample_data)
    pdf.generate()
    output = pdf.output(dest='S').encode('latin-1')
    assert output.startswith(b'%PDF')

def test_uno_pdf(sample_data):
    pdf = TemplateUnoPDF(sample_data)
    pdf.generate()
    output = pdf.output(dest='S').encode('latin-1')
    assert output.startswith(b'%PDF')
