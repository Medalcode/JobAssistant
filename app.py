from __future__ import annotations

from datetime import datetime
from pathlib import Path
import os

from flask import Flask, jsonify, render_template, request, make_response
from pdf_templates import ClassicPDF, ModernPDF, TemplateUnoPDF
from scraper import scrape_jobs
from models import (
    db, Candidate, Experience, Education, Skill, Language, 
    Certification, Project, Link, Job, Application
)

BASE_DIR = Path(__file__).resolve().parent

# Database Config
# If DATABASE_URL is set (Vercel/Prod), use it. 
# If on Vercel without DB, use /tmp (ephemeral).
# Otherwise use local data directory.
database_url = os.environ.get('DATABASE_URL')

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if not database_url:
    if os.environ.get('VERCEL'):
        # Ephemeral DB in /tmp for Vercel
        db_path = Path("/tmp/cv.db")
    else:
        # Local Persistent DB
        db_path = BASE_DIR / "data" / "cv.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
    
    sqlite_uri = f"sqlite:///{db_path}"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
else:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables if they don't exist (for Vercel/Prod)
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database tables: {e}")




@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/submit")
def submit():
    data = request.get_json(silent=True) or {}

    required = ["full_name", "email"]
    missing = [field for field in required if not (data.get(field) or "").strip()]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400

    created_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    # Create Candidate
    candidate = Candidate(
        full_name=data.get("full_name", "").strip(),
        professional_title=data.get("professional_title", "").strip(),
        location=data.get("location", "").strip(),
        phone=data.get("phone", "").strip(),
        email=data.get("email", "").strip(),
        linkedin=data.get("linkedin", "").strip(),
        portfolio=data.get("portfolio", "").strip(),
        github=data.get("github", "").strip(),
        summary=data.get("summary", "").strip(),
        created_at=created_at
    )
    db.session.add(candidate)
    db.session.flush() # Get ID

    def has_values(item: dict, fields: list[str]) -> bool:
        return any((item.get(field) or "").strip() for field in fields)

    # Experiences
    for exp in data.get("experiences", []) or []:
        if not has_values(exp, ["company", "role"]): continue
        db.session.add(Experience(
            candidate_id=candidate.id,
            company=exp.get("company", "").strip(),
            role=exp.get("role", "").strip(),
            location=exp.get("location", "").strip(),
            start_date=exp.get("start_date", "").strip(),
            end_date=exp.get("end_date", "").strip(),
            description=exp.get("description", "").strip()
        ))

    # Educations
    for edu in data.get("educations", []) or []:
        if not has_values(edu, ["institution", "degree"]): continue
        db.session.add(Education(
            candidate_id=candidate.id,
            institution=edu.get("institution", "").strip(),
            degree=edu.get("degree", "").strip(),
            field=edu.get("field", "").strip(),
            start_date=edu.get("start_date", "").strip(),
            end_date=edu.get("end_date", "").strip(),
            description=edu.get("description", "").strip()
        ))

    # Skills
    for skill in data.get("skills", []) or []:
        if not has_values(skill, ["name"]): continue
        db.session.add(Skill(
            candidate_id=candidate.id,
            name=skill.get("name", "").strip(),
            level=skill.get("level", "").strip(),
            category=skill.get("category", "").strip()
        ))

    # Languages
    for lang in data.get("languages", []) or []:
        if not has_values(lang, ["name"]): continue
        db.session.add(Language(
            candidate_id=candidate.id,
            name=lang.get("name", "").strip(),
            level=lang.get("level", "").strip()
        ))

    # Certifications
    for cert in data.get("certifications", []) or []:
        if not has_values(cert, ["name"]): continue
        db.session.add(Certification(
            candidate_id=candidate.id,
            name=cert.get("name", "").strip(),
            issuer=cert.get("issuer", "").strip(),
            date=cert.get("date", "").strip(),
            url=cert.get("url", "").strip()
        ))

    # Projects
    for proj in data.get("projects", []) or []:
        if not has_values(proj, ["name"]): continue
        db.session.add(Project(
            candidate_id=candidate.id,
            name=proj.get("name", "").strip(),
            role=proj.get("role", "").strip(),
            description=proj.get("description", "").strip(),
            url=proj.get("url", "").strip(),
            technologies=proj.get("technologies", "").strip()
        ))

    # Links
    for link in data.get("links", []) or []:
        if not has_values(link, ["url"]): continue
        db.session.add(Link(
            candidate_id=candidate.id,
            label=link.get("label", "").strip(),
            url=link.get("url", "").strip()
        ))

    db.session.commit()
    return jsonify({"status": "ok", "candidate_id": candidate.id})


@app.route("/api/download/<int:candidate_id>")
def download_pdf(candidate_id):
    candidate = db.session.get(Candidate, candidate_id)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    # Convert to dictionary structure expected by template
    template_data = {
        "candidate": candidate.to_dict(),
        "experiences": [x.to_dict() for x in candidate.experiences],
        "educations": [x.to_dict() for x in candidate.educations],
        "skills": [x.to_dict() for x in candidate.skills],
        "languages": [x.to_dict() for x in candidate.languages],
        "certifications": [x.to_dict() for x in candidate.certifications],
        "projects": [x.to_dict() for x in candidate.projects],
        "links": [x.to_dict() for x in candidate.links]
    }

    style = request.args.get("style", "classic")
    
    if style == "modern":
        pdf = ModernPDF(template_data)
    elif style == "uno":
        pdf = TemplateUnoPDF(template_data)
    else:
        pdf = ClassicPDF(template_data)
        
    pdf.generate()

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=cv_{candidate_id}_{style}.pdf'
    return response


@app.post("/api/generate_summary")
def generate_summary():
    data = request.get_json(silent=True) or {}
    
    title = data.get("professional_title", "Profesional")
    skills = data.get("skills", []) # List of dicts {name, level}
    experiences = data.get("experiences", []) # List of dicts {company, role...}
    
    skill_names = [s.get("name", "") for s in skills if s.get("name")]
    top_skills = ", ".join(skill_names[:5]) if skill_names else "habilidades clave"
    
    exp_roles = [e.get("role", "") for e in experiences if e.get("role")]
    last_role = exp_roles[0] if exp_roles else "Profesional"
    years_exp = len(experiences) # Simple heuristic
    
    # Simple templates (in Spanish as requested)
    options = []
    
    # Option 1: Standard/Professional
    opt1 = f"{title} con experiencia sólida como {last_role}. EXPERTO en {top_skills}. Busco aportar mis conocimientos en proyectos desafiantes y continuar creciendo profesionalmente."
    options.append(opt1)
    
    # Option 2: Skill-driven
    opt2 = f"Apasionado {title} especializado en {top_skills}. Con trayectoria probada en {', '.join(exp_roles[:2]) if exp_roles else 'diferentes roles'}, enfocado en la entrega de soluciones de alta calidad y la mejora continua."
    options.append(opt2)
    
    # Option 3: Concise/Impact
    opt3 = f"{title} altamente motivado con enfoque en resultados. Dominio de {top_skills}. Historial comprobado de éxito en entornos dinámicos y capacidad para trabajar en equipo."
    options.append(opt3)
    
    return jsonify({"options": options})

@app.route("/api/search")
def search_jobs_route():
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    jobs = scrape_jobs(query, location)
    return jsonify(jobs)


@app.post("/api/apply")
def apply_job():
    data = request.get_json(silent=True) or {}
    candidate_id = data.get('candidate_id')
    job_data = data.get('job', {})
    
    if not candidate_id or not job_data:
         return jsonify({"error": "Missing candidate or job data"}), 400
         
    # Check if job exists
    job = Job.query.filter_by(url=job_data.get('url')).first()
    
    if not job:
        job = Job(
            title=job_data.get('title'),
            company=job_data.get('company'),
            location=job_data.get('location'),
            url=job_data.get('url'),
            source=job_data.get('source'),
            date_posted=job_data.get('date_posted'),
            logo=job_data.get('logo')
        )
        db.session.add(job)
        db.session.flush()
        
    # Create application
    application = Application(
        candidate_id=candidate_id,
        job_id=job.id,
        status='Applied'
    )
    db.session.add(application)
    db.session.commit()
        
    return jsonify({"status": "success", "job_id": job.id})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
