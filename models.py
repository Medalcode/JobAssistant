
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Candidate(BaseModel):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    professional_title = db.Column(db.String)
    location = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    linkedin = db.Column(db.String)
    portfolio = db.Column(db.String)
    github = db.Column(db.String)
    summary = db.Column(db.Text)
    created_at = db.Column(db.String, nullable=False, default=datetime.utcnow().isoformat)

    experiences = db.relationship('Experience', backref='candidate', cascade='all, delete-orphan')
    educations = db.relationship('Education', backref='candidate', cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='candidate', cascade='all, delete-orphan')
    languages = db.relationship('Language', backref='candidate', cascade='all, delete-orphan')
    certifications = db.relationship('Certification', backref='candidate', cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='candidate', cascade='all, delete-orphan')
    links = db.relationship('Link', backref='candidate', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='candidate', cascade='all, delete-orphan')

class Experience(BaseModel):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    company = db.Column(db.String)
    role = db.Column(db.String)
    location = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    description = db.Column(db.Text)

class Education(BaseModel):
    __tablename__ = 'educations'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    institution = db.Column(db.String)
    degree = db.Column(db.String)
    field = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    description = db.Column(db.Text)

class Skill(BaseModel):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    name = db.Column(db.String)
    level = db.Column(db.String)
    category = db.Column(db.String)

class Language(BaseModel):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    name = db.Column(db.String)
    level = db.Column(db.String)

class Certification(BaseModel):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    name = db.Column(db.String)
    issuer = db.Column(db.String)
    date = db.Column(db.String)
    url = db.Column(db.String)

class Project(BaseModel):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    name = db.Column(db.String)
    role = db.Column(db.String)
    description = db.Column(db.Text)
    url = db.Column(db.String)
    technologies = db.Column(db.String)

class Link(BaseModel):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    label = db.Column(db.String)
    url = db.Column(db.String)

class Job(BaseModel):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    company = db.Column(db.String)
    location = db.Column(db.String)
    description = db.Column(db.Text)
    url = db.Column(db.String, unique=True)
    source = db.Column(db.String)
    date_posted = db.Column(db.String)
    logo = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='job', cascade='all, delete-orphan')

class Application(BaseModel):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    status = db.Column(db.String, default='Applied')
    tailored_cv_path = db.Column(db.String)
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
