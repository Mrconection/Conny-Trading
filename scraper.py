import os
import requests
import re
import sys

# --- PULL THE TUNNEL KEY ---
SCRAPERAPI_KEY = os.environ.get("SCRAPERAPI_KEY")

# --- 1. THE 14 NEW PINTEREST BOARD URLS ---
PINTEREST_BOARD_URLS = [
    "https://www.pinterest.com/WeExplainTech/aesthetic-desk-setup-organization/",
    "https://www.pinterest.com/WeExplainTech/aesthetic-charging-stations-docks/",
    "https://www.pinterest.com/WeExplainTech/travel-tech-gadget-organizers/",
    "https://www.pinterest.com/WeExplainTech/smart-kitchen-gadgets-tech/",
    "https://www.pinterest.com/WeExplainTech/gaming-room-setup-organization/",
    "https://www.pinterest.com/WeExplainTech/aesthetic-smart-lighting-led-decor/",
    "https://www.pinterest.com/WeExplainTech/minimalist-home-office-laptop-stands/",
    "https://www.pinterest.com/WeExplainTech/tv-media-console-organization/",
    "https://www.pinterest.com/WeExplainTech/headphone-stands-audio-decor/",
    "https://www.pinterest.com/WeExplainTech/smart-humidifiers-air-purifiers/",
    "https://www.pinterest.com/WeExplainTech/tech-tools-diy-gadgets/",
    "https://www.pinterest.com/WeExplainTech/smart-home-security-management/",
    "https://www.pinterest.com/WeExplainTech/digital-tools-precision-gear/",
    "https://www.pinterest.com/WeExplainTech/aesthetic-tool-garage-organization/"
]

# --- 2. THE 14 AMAZON POPULARITY NODES ---
AMAZON_NODES = [
    "https://www.amazon.com/s?rh=n%3A490624011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A12557637011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A3015429011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A289913&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A14775003011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A2314207011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A3015408011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A3230976011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A229575&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A267557011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A551236&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A4954983011&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A553270&s=exact-aware-popularity-rank",
    "https://www.amazon.com/s?rh=n%3A13400551&s=exact-aware-popularity-rank"
]

def generate_empire_map():
    if not SCRAPERAPI_KEY:
        print("[🚨] STRICT FATAL: SCRAPERAPI_KEY is missing from environment. Aborting.")
        sys.exit(1)

    if len(PINTEREST_BOARD_URLS) != len(AMAZON_NODES):
        print(f"[🚨] STRICT FATAL: URL/Node mismatch. Aborting.")
        sys.exit(1)

    print("[*] Engaging ScraperAPI Stealth Tunnel to bypass Pinterest Firewalls...\n")
    print("TECH_EMPIRE_MAP = {")

    for i, url in enumerate(PINTEREST_BOARD_URLS):
        try:
            # Route request through the stealth tunnel
            payload = {'api_key': SCRAPERAPI_KEY, 'url': url, 'premium': 'true', 'render': 'true'}
            response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
            
            if response.status_code != 200:
                print(f"[🚨] Tunnel failed with status {response.status_code} for {url}. Retrying next run.")
                continue

        except Exception as net_err:
            print(f"[🚨] STRICT FATAL: Network crash. Error: {net_err}. Aborting.")
            sys.exit(1)
            
        # Multi-stage Regex Hunter
        html = response.text
        board_id = None
        
        # Target 1: Mobile Deep Link (Highly reliable, rarely obfuscated)
        match = re.search(r'pinterest://board/(\d+)', html)
        if not match:
            # Target 2: Initial State JSON ID
            match = re.search(r'\"board_id\":\"(\d+)\"', html)
        if not match:
            # Target 3: Alternate JSON format
            match = re.search(r'\"id\":\"(\d{18})\",\"type\":\"board\"', html)
            
        if match:
            board_id = match.group(1)
            amazon_node = AMAZON_NODES[i]
            board_slug = url.strip("/").split("/")[-1].replace("-", " ").title()
            
            print(f'    # {board_slug}')
            print(f'    "{amazon_node}": "{board_id}",')
        else:
            print(f"    # [🚨] FAILED TO EXTRACT ID FOR: {url}")

    print("}")
    print("\n[SUCCESS] Extraction complete.")

if __name__ == "__main__":
    generate_empire_map()
