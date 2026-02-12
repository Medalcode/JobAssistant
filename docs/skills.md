# Skills Registry

This document measures the technical capabilities (Skills) available to the agents. Each skill maps to specific modules in the codebase.

## 1. Market Research
**Description:** The ability to interface with external job boards and data sources.
**Owner:** Job Scout Agent
**Implementation:** `scraper.py`
**Tools:**
- `scrape_jobs(query, location)`: Fetches live data from RemoteOK API.

## 2. Document Engineering
**Description:** The capability to programmatically generate complex documents.
**Owner:** Resume Architect Agent
**Implementation:** `pdf_templates.py`
**Tools:**
- `ClassicPDF`: Traditional, clean layout generation.
- `ModernPDF`: Stylized, contemporary design generation.
- `TemplateUnoPDF`: Minimalist, high-impact layout generation.

## 3. Data Persistence
**Description:** The ability to store and retrieve structured data reliably.
**Owner:** System (Shared)
**Implementation:** `models.py`, `app.py` (SQLAlchemy)
**Tools:**
- `Candidate` Management: CRUD operations for user profiles.
- `Application` Tracking: Linking candidates to jobs.
- `Session` Handling: Transaction management.

## 4. Profile Analytics
**Description:** The ability to synthesize raw data into insights.
**Owner:** Career Strategist Agent
**Implementation:** `app.py` (`generate_summary`)
**Tools:**
- `generate_summary`: Algorithmic creation of professional bios based on title, skills, and experience.
