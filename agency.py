from agents.job_scout import JobScout
from agents.resume_architect import ResumeArchitect
from agents.career_strategist import CareerStrategist
import os
import json

def main():
    print("--- Initializing JobAssistant Agency ---")
    scout = JobScout()
    architect = ResumeArchitect()
    strategist = CareerStrategist()

    # Phase 1: Job Search
    print("\n--- Phase 1: Market Research (Job Scout) ---")
    jobs = scout.run(query="Python Developer", location="Remote")
    if jobs:
        print(f"Top job found: {jobs[0].get('title')} at {jobs[0].get('company')}")
    else:
        print("No jobs found (API might be rate limited or offline), proceeding with mock data.")

    # Phase 2: Career Strategy
    print("\n--- Phase 2: Career Strategy (Career Strategist) ---")
    dummy_profile = {
        "professional_title": "Python Developer",
        "skills": [{"name": "Python"}, {"name": "Flask"}, {"name": "SQL"}],
        "experiences": [{"role": "Junior Developer", "company": "StartUp Inc."}]
    }
    summaries = strategist.run(dummy_profile) # Note: The agent method is actually run() which calls generate_summary internally
    print(f"Selected Summary: {summaries[0]}")

    # Phase 3: Resume Generation
    print("\n--- Phase 3: Document Generation (Resume Architect) ---")
    
    # Structure for template needs keys like 'candidate' and lists
    template_data = {
         "candidate": {
             "full_name": "Agent Generated User",
             "email": "agent@example.com",
             "phone": "555-0123",
             "linkedin": "linkedin.com/in/agentuser",
             "github": "github.com/agentuser",
             "portfolio": "agentuser.dev",
             "summary": summaries[0],
             "location": "Cyberspace",
             "professional_title": "Python Developer"
         },
         "experiences": [
             {
                 "company": "StartUp Inc.", 
                 "role": "Junior Developer", 
                 "start_date": "2022-01", 
                 "end_date": "Present", 
                 "location": "Remote",
                 "description": "Led backend API development using Flask and PostgreSQL. Optimized query performance by 40%."
             }
         ],
         "educations": [
             {
                 "institution": "University of Code",
                 "degree": "B.S. Computer Science",
                 "field": "Software Engineering",
                 "start_date": "2018",
                 "end_date": "2022",
                 "description": "Graduated with honors."
             }
         ],
         "skills": [
             {"name": "Python", "level": "Expert"}, 
             {"name": "Flask", "level": "Advanced"},
             {"name": "SQLAlchemy", "level": "Intermediate"}
         ],
         "languages": [
             {"name": "English", "level": "Native"},
             {"name": "Spanish", "level": "Intermediate"}
         ],
         "certifications": [],
         "projects": [],
         "links": []
    }
    
    # Ensure output directory exists or just use root
    output_file = "agent_generated_cv.pdf"
    output_msg = architect.run(template_data, style="modern", output_path=output_file)
    
    if os.path.exists(output_file):
        print(f"Success! CV generated at {os.path.abspath(output_msg)}")
    else:
        print("Error: CV file was not created.")

if __name__ == "__main__":
    main()
