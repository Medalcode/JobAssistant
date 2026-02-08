import os
import json
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def handler(request):
    """Vercel Python Serverless function handler.

    Expect a JSON POST body similar to the existing `/api/submit` payload.
    Inserts into Supabase REST endpoints. The Supabase project must have
    the tables created (use `schema.sql`).
    """
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"}),
            "headers": {"Content-Type": "application/json"},
        }

    if not SUPABASE_URL or not SUPABASE_KEY:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Missing SUPABASE_URL or SUPABASE_KEY env vars"}),
            "headers": {"Content-Type": "application/json"},
        }

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON"}),
            "headers": {"Content-Type": "application/json"},
        }

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    # Insert candidate
    candidate_payload = {
        "full_name": data.get("full_name", "").strip(),
        "professional_title": data.get("professional_title", "").strip(),
        "location": data.get("location", "").strip(),
        "phone": data.get("phone", "").strip(),
        "email": data.get("email", "").strip(),
        "linkedin": data.get("linkedin", "").strip(),
        "portfolio": data.get("portfolio", "").strip(),
        "github": data.get("github", "").strip(),
        "summary": data.get("summary", "").strip(),
        "created_at": data.get("created_at") or None,
    }

    resp = requests.post(f"{SUPABASE_URL}/rest/v1/candidates", headers=headers, data=json.dumps(candidate_payload))
    if resp.status_code not in (200, 201):
        return {"statusCode": resp.status_code, "body": resp.text, "headers": {"Content-Type": "application/json"}}

    candidate = resp.json()[0]
    candidate_id = candidate.get("id")

    def insert_rows(table, rows):
        if not rows:
            return
        for r in rows:
            r["candidate_id"] = candidate_id
        r = requests.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=headers, data=json.dumps(rows))
        if r.status_code not in (200, 201):
            raise RuntimeError(f"Failed to insert into {table}: {r.status_code} {r.text}")

    try:
        insert_rows("experiences", data.get("experiences", []))
        insert_rows("educations", data.get("educations", []))
        insert_rows("skills", data.get("skills", []))
        insert_rows("languages", data.get("languages", []))
        insert_rows("certifications", data.get("certifications", []))
        insert_rows("projects", data.get("projects", []))
        insert_rows("links", data.get("links", []))
    except Exception as exc:
        return {"statusCode": 500, "body": json.dumps({"error": str(exc)}), "headers": {"Content-Type": "application/json"}}

    return {"statusCode": 200, "body": json.dumps({"status": "ok", "candidate_id": candidate_id}), "headers": {"Content-Type": "application/json"}}
