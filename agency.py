
from agents.job_scout import JobScout
from agents.resume_architect import ResumeArchitect
from agents.career_strategist import CareerStrategist
import os
import json

def main():
    print("--- 🧠 Initializing AI Agency v2.0 ---")
    scout = JobScout()
    architect = ResumeArchitect()
    strategist = CareerStrategist()

    # --- Phase 1: Intelligent Market Research ---
    # Will use expanded synonyms (Python -> Django, Flask...) and Computrabajo Scraper
    print("\n--- Phase 1: Market Research (Job Scout) ---")
    query = "Python Developer"
    
    # We need the profile first to rank properly, so let's define it here
    candidate_profile = {
        "professional_title": "Python Developer",
        "skills": [
            {"name": "Python", "level": "Expert"}, 
            {"name": "Flask", "level": "Advanced"}, 
            {"name": "SQL", "level": "Intermediate"},
            {"name": "Django", "level": "Intermediate"}
        ],
        "experiences": [
            {
                "role": "Backend Developer", 
                "company": "StartUp A",
                "start_date": "2023-01", 
                "end_date": "Present",
                "description": "Developed REST APIs using Flask.",
                "location": "Remote"
            }
        ]
    }

    jobs = scout.run(query=query, location="Santiago", profile_data=candidate_profile)
    
    target_job = None
    if not jobs:
        print("No jobs found via scraper. Using mock job for demo purposes.")
        target_job = {
            "title": "Senior Python Engineer",
            "company": "Tech Corp",
            "description": "We are looking for a Python expert with Django and AWS experience. Must know Docker and Kubernetes. Agile methodology is a plus.",
            "url": "#",
            "match_score": 85
        }
    else:
        print(f"\n[{'MATCH':^7}] {'TITLE':<40} {'COMPANY':<20}")
        print("-" * 70)
        for i, job in enumerate(jobs[:5]): # Show top 5
             print(f"[{job.get('match_score', 0):>3}%]   {job['title'][:38]:<40} {job['company'][:18]:<20}")
        
        target_job = jobs[0]
        # Ensure description is not empty for ATS check
        if not target_job.get('description'):
            target_job['description'] = target_job['title'] + " " + target_job['company']
            
        print(f"\nSelected Top Candidate: {target_job['title']} at {target_job['company']}")

    # --- Phase 2: Strategic Profiling ---
    print("\n--- Phase 2: Career Strategy (Career Strategist) ---")
    # A mid-level profile that has some gaps for the target job
    # (Profile defined in Phase 1)
    
    strategy = strategist.run(candidate_profile)
    print(f"Seniority Level: {strategy['analysis'].get('seniority', 'Unknown')}")
    if strategy['analysis'].get('suggestions'):
        print(f"Gap Analysis (Advisory): {', '.join(strategy['analysis']['suggestions'])}")
    
    selected_summary = strategy['summaries'][0]
    print(f"Generated Summary: \"{selected_summary[:100]}...\"")

    # --- Phase 3: Resume Architecture & ATS Audit ---
    print("\n--- Phase 3: Document Optimization (Resume Architect) ---")
    
    # 3.1 ATS Audit
    # Let's say we want to apply to the target job. 
    # We construct a text representation of the resume for analysis
    resume_text = f"{selected_summary} Skills: Python, Flask, SQL. Experience: Backend Developer, Junior Developer. developed APIs"
    job_desc = target_job.get('description', '') 
    
    audit_result = architect.audit_resume(resume_text, job_desc)
    
    # 3.2 Optimization & Generation
    # We feed the strategy back into the resume data
    template_data = {
         "candidate": {
             "full_name": "Agent Generated User",
             "email": "agent@example.com",
             "phone": "555-0123",
             "linkedin": "linkedin.com/in/agentuser",
             "github": "github.com/agentuser",
             "portfolio": "agentuser.dev",
             "summary": selected_summary,
             "location": "Santiago",
             "professional_title": query 
         },
         "experiences": candidate_profile['experiences'],
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
         "skills": candidate_profile['skills'],
         "languages": [{"name": "English", "level": "Native"}],
         "certifications": [],
         "projects": [],
         "links": []
    }
    
    output_file = "optimized_cv.pdf"
    
    try:
        output_msg = architect.run(template_data, style="modern", output_path=output_file)
        
        if os.path.exists(output_file):
            print(f"Success! Optimized CV generated at {os.path.abspath(output_msg)}")
            print(f"Note: This CV prioritized skills relevant to '{query}'")
        else:
            print("Error: CV file was not created.")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    main()
