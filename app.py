from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sqlite3

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "cv.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_db() as conn:
        conn.executescript(schema)


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

    candidate_fields = (
        data.get("full_name", "").strip(),
        data.get("professional_title", "").strip(),
        data.get("location", "").strip(),
        data.get("phone", "").strip(),
        data.get("email", "").strip(),
        data.get("linkedin", "").strip(),
        data.get("portfolio", "").strip(),
        data.get("github", "").strip(),
        data.get("summary", "").strip(),
        created_at,
    )

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO candidates (
                full_name,
                professional_title,
                location,
                phone,
                email,
                linkedin,
                portfolio,
                github,
                summary,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            candidate_fields,
        )
        candidate_id = cur.lastrowid

        def insert_many(table: str, columns: list[str], rows: list[tuple]) -> None:
            if not rows:
                return
            placeholders = ",".join(["?"] * len(columns))
            column_names = ",".join(columns)
            cur.executemany(
                f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})",
                rows,
            )

        def has_values(item: dict, fields: list[str]) -> bool:
            return any((item.get(field) or "").strip() for field in fields)

        experiences = []
        for exp in data.get("experiences", []) or []:
            if not has_values(exp, ["company", "role", "location", "start_date", "end_date", "description", "achievements"]):
                continue
            experiences.append(
                (
                    candidate_id,
                    exp.get("company", "").strip(),
                    exp.get("role", "").strip(),
                    exp.get("location", "").strip(),
                    exp.get("start_date", "").strip(),
                    exp.get("end_date", "").strip(),
                    exp.get("description", "").strip(),
                    exp.get("achievements", "").strip(),
                )
            )
        insert_many(
            "experiences",
            [
                "candidate_id",
                "company",
                "role",
                "location",
                "start_date",
                "end_date",
                "description",
                "achievements",
            ],
            experiences,
        )

        educations = []
        for edu in data.get("educations", []) or []:
            if not has_values(edu, ["institution", "degree", "field", "start_date", "end_date", "description"]):
                continue
            educations.append(
                (
                    candidate_id,
                    edu.get("institution", "").strip(),
                    edu.get("degree", "").strip(),
                    edu.get("field", "").strip(),
                    edu.get("start_date", "").strip(),
                    edu.get("end_date", "").strip(),
                    edu.get("description", "").strip(),
                )
            )
        insert_many(
            "educations",
            [
                "candidate_id",
                "institution",
                "degree",
                "field",
                "start_date",
                "end_date",
                "description",
            ],
            educations,
        )

        skills = []
        for skill in data.get("skills", []) or []:
            if not has_values(skill, ["name", "level", "category"]):
                continue
            skills.append(
                (
                    candidate_id,
                    skill.get("name", "").strip(),
                    skill.get("level", "").strip(),
                    skill.get("category", "").strip(),
                )
            )
        insert_many(
            "skills",
            ["candidate_id", "name", "level", "category"],
            skills,
        )

        languages = []
        for lang in data.get("languages", []) or []:
            if not has_values(lang, ["name", "level"]):
                continue
            languages.append(
                (
                    candidate_id,
                    lang.get("name", "").strip(),
                    lang.get("level", "").strip(),
                )
            )
        insert_many(
            "languages",
            ["candidate_id", "name", "level"],
            languages,
        )

        certifications = []
        for cert in data.get("certifications", []) or []:
            if not has_values(cert, ["name", "issuer", "date", "url"]):
                continue
            certifications.append(
                (
                    candidate_id,
                    cert.get("name", "").strip(),
                    cert.get("issuer", "").strip(),
                    cert.get("date", "").strip(),
                    cert.get("url", "").strip(),
                )
            )
        insert_many(
            "certifications",
            ["candidate_id", "name", "issuer", "date", "url"],
            certifications,
        )

        projects = []
        for project in data.get("projects", []) or []:
            if not has_values(project, ["name", "role", "description", "url", "technologies"]):
                continue
            projects.append(
                (
                    candidate_id,
                    project.get("name", "").strip(),
                    project.get("role", "").strip(),
                    project.get("description", "").strip(),
                    project.get("url", "").strip(),
                    project.get("technologies", "").strip(),
                )
            )
        insert_many(
            "projects",
            ["candidate_id", "name", "role", "description", "url", "technologies"],
            projects,
        )

        links = []
        for link in data.get("links", []) or []:
            if not has_values(link, ["label", "url"]):
                continue
            links.append(
                (
                    candidate_id,
                    link.get("label", "").strip(),
                    link.get("url", "").strip(),
                )
            )
        insert_many(
            "links",
            ["candidate_id", "label", "url"],
            links,
        )

    return jsonify({"status": "ok", "candidate_id": candidate_id})


init_db()


if __name__ == "__main__":
    app.run(debug=True)
