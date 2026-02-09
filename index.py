
from app import app

# This file exists to explicitly expose the 'app' variable for WSGI servers
# Vercel looks for 'app' in index.py, api/index.py, or other entrypoints.
# We will point vercel.json to this file or app.py, but having a clean import helps.

if __name__ == "__main__":
    app.run()
