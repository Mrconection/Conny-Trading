import requests
import re
import sys

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
    # Strict validation to ensure you don't map the wrong node to the wrong board
    if len(PINTEREST_BOARD_URLS) != len(AMAZON_NODES):
        print(f"[🚨] STRICT FATAL: You provided {len(PINTEREST_BOARD_URLS)} URLs but there are {len(AMAZON_NODES)} Amazon Nodes. They must match exactly. Aborting.")
        sys.exit(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("[*] Booting Scraper to extract 18-digit Board IDs...\n")
    print("TECH_EMPIRE_MAP = {")

    for i, url in enumerate(PINTEREST_BOARD_URLS):
        try:
            response = requests.get(url, headers=headers, timeout=10)
        except Exception as net_err:
            print(f"[🚨] STRICT FATAL: Network crash when attempting to reach {url}. Error: {net_err}. Aborting.")
            sys.exit(1)
            
        # Regex engine hunting the initial-state JSON for the exact Board ID
        match = re.search(r'\"board_id\":\"(\d+)\"', response.text)
        
        if not match:
            # Secondary regex in case Pinterest localized the DOM structure
            match = re.search(r'\"id\":\"(\d{18})\",\"type\":\"board\"', response.text)

        if not match:
            print(f"\n[🚨] STRICT FATAL: Regex engine could not find Board ID for {url}. The DOM structure may have changed. Aborting.")
            sys.exit(1)

        board_id = match.group(1)
        amazon_node = AMAZON_NODES[i]
        
        # Extracts the clean board name from the URL slug for code readability
        board_slug = url.strip("/").split("/")[-1].replace("-", " ").title()
        
        # Prints the exact formatted dictionary syntax
        print(f'    # {board_slug}')
        print(f'    "{amazon_node}": "{board_id}",')

    print("}")
    print("\n[SUCCESS] Extraction complete. Copy the dictionary above into your main script.")

if __name__ == "__main__":
    generate_empire_map()
