
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random
import unicodedata
import urllib.parse
import sys

def normalize_string(text):
    """Normalize string for URL (remove accents, lowercase, replace spaces with hyphens)"""
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower().strip()
    return text.replace(" ", "-")

def scrape_computrabajo(query, location=""):
    """
    Scrapes jobs from Computrabajo (Chile domain by default).
    Returns a list of job dicts.
    """
    results = []
    
    # URL Base (Chile)
    base_url = "https://cl.computrabajo.com" 
    
    # Construct optimized URL path
    # Example: https://cl.computrabajo.com/trabajo-de-programador-en-santiago
    # Query path
    clean_query = normalize_string(query)
    path = f"trabajo-de-{clean_query}"
    
    # Location path (optional)
    if location:
        clean_loc = normalize_string(location)
        path += f"-en-{clean_loc}"

    url = f"{base_url}/{path}"
    
    print(f"[ComputrabajoScraper] Visiting: {url}")
    sys.stdout.flush()

    try:
        with sync_playwright() as p:
            # Launch browser (headless=True usually, but False helps debug visual blocks)
            # Add extra args to mimic real user better
            browser = p.chromium.launch(headless=True, args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ])
            
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080},
                locale="es-CL"
            )
            
            page = context.new_page()
            
            # Go to page
            try:
                # Wait until dom content loaded, not just network idle
                response = page.goto(url, timeout=30000, wait_until="domcontentloaded")
                
                # Check for blocking status codes
                if response and response.status in [403, 429, 503]:
                    print(f"[ComputrabajoScraper] BLOCKED! Status code: {response.status}")
                    return []
                
            except Exception as e:
                print(f"[ComputrabajoScraper] Navigation error: {e}")
                return []

            # Wait for content to load properly
            # Try to wait for the job list container
            try:
                page.wait_for_selector("#offersGridOfferContainer", timeout=5000)
            except:
                pass # Maybe different layout

            # Scroll down to trigger lazy loading if any
            page.mouse.wheel(0, 1000)
            time.sleep(2)
            
            # Get content
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Debug: check if we hit a "No results" page
            if "No hemos encontrado ofertas" in content or "0 ofertas de trabajo" in content:
                print("[ComputrabajoScraper] No jobs found for this query.")
                return []

            # Selectors
            # New layout: <article class="box_offer"> inside #offersGridOfferContainer
            articles = soup.select('article.box_offer')
            
            if not articles:
                 # Fallback for old layouts
                 articles = soup.select('div.bClick')
            
            print(f"[ComputrabajoScraper] Found {len(articles)} articles.")
            sys.stdout.flush()

            for article in articles:
                try:
                    # Title
                    title_elem = article.select_one('h1 a.js-o-link') or \
                                 article.select_one('h2 a.js-o-link') or \
                                 article.select_one('a.js-o-link')
                    
                    if not title_elem: continue
                    
                    title = title_elem.text.strip()
                    link = title_elem.get('href', '')
                    if link and link.startswith("/"):
                        link = base_url + link
                        
                    # Company
                    company_elem = article.select_one('p.fs16.fc_base.mt5 a') or \
                                   article.select_one('a.empr') or \
                                   article.select_one('p.fs16 span') 
                                   
                    company = company_elem.text.strip() if company_elem else "Confidencial"
                    
                    # Location
                    loc_elem = article.select_one('p.fs16 span.fc_base') or \
                               article.select_one('span[itemprop="addressLocality"]')
                    
                    loc = loc_elem.text.strip() if loc_elem else location

                    # Description snippet
                    desc_elem = article.select_one('p.fs13.fc_aux') or \
                                article.select_one('div.fs13')
                    
                    description = desc_elem.text.strip() if desc_elem else ""
                    
                    # Date
                    date_elem = article.select_one('span.fc_aux')
                    date_posted = date_elem.text.strip() if date_elem else ""

                    job = {
                        'title': title,
                        'company': company,
                        'location': loc,
                        'url': link,
                        'description': description, 
                        'date_posted': date_posted,
                        'source': 'Computrabajo',
                        'logo': '' # Hard to get without loading details page
                    }
                    results.append(job)
                    
                except Exception as e:
                    # print(f"Error parsing job: {e}")
                    continue

            browser.close()
            
    except Exception as e:
        print(f"[ComputrabajoScraper] Critical Error: {e}")
        return []
        
    return results[:15]
