
import pytest
import json

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Formulario de CV" in rv.data

def test_submit_valid_data(client):
    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "experiences": [],
        "educations": []
    }
    rv = client.post('/api/submit', json=payload)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert "candidate_id" in data

def test_submit_missing_fields(client):
    payload = {
        "full_name": "", # Missing name
        "email": "john@example.com"
    }
    rv = client.post('/api/submit', json=payload)
    assert rv.status_code == 400
    assert b"Missing required fields" in rv.data

def test_search_jobs(client):
    # This hits the real scraper unless mocked. 
    # For integration test we might accept real network call or Mock it.
    # Let's mock it in test_scraper.py specifically and here just check endpoint structure.
    # If scraper fails it returns empty list, so it's safe-ish.
    rv = client.get('/api/search?q=test')
    assert rv.status_code == 200
    assert isinstance(json.loads(rv.data), list)

def test_apply_job(client):
    # First create a candidate
    payload = {"full_name": "Jane Doe", "email": "jane@example.com"}
    rv = client.post('/api/submit', json=payload)
    candidate_id = json.loads(rv.data)['candidate_id']
    
    # Now apply
    job_payload = {
        "candidate_id": candidate_id,
        "job": {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "url": "http://example.com/job/123",
            "source": "Test"
        }
    }
    rv = client.post('/api/apply', json=job_payload)
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['status'] == 'success'
    assert 'job_id' in data
