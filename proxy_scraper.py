import aiohttp
import asyncio
import random
import time
from datetime import datetime
import os

# List of high-quality free proxy APIs (constantly updated)
PROXY_SOURCES = [
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.openproxylist.xyz/http.txt",
    "https://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
]

OUTPUT_FILE = "live_proxies.txt"

async def fetch_source(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                text = await resp.text()
                return text.splitlines()
            else:
                print(f"[-] Failed {url} | Status: {resp.status}")
                return []
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return []

async def scrape_all_proxies():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_source(session, url) for url in PROXY_SOURCES]
        results = await asyncio.gather(*tasks)

        all_proxies = []
        seen = set()

        for lines in results:
            for line in lines:
                line = line.strip()
                if not line or "//" in line or "@" in line or ":" not in line:
                    continue
                if line in seen:
                    continue
                try:
                    host, port = line.split(":")
                    if host.replace(".", "").isdigit():  # IPv4 check
                        if 1 <= int(port) <= 65535:
                            seen.add(line)
                            all_proxies.append(line)
                except Exception:
                    continue
        
        # Save clean list
        with open(OUTPUT_FILE, 'w') as f:
            f.write('\n'.join(all_proxies))

        print(f"[+] Saved {len(all_proxies)} unique proxies to {OUTPUT_FILE}")
    
    return len(all_proxies)

# Auto-run every 1800 seconds (30 mins)
async def auto_scrape(interval_seconds=1800):
    while True:
        print(f"🔄 [{datetime.now()}] Starting proxy scrape cycle...")
        await scrape_all_proxies()
        
        print(f"💤 Waiting {interval_seconds} seconds before next scrape...")
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    # For testing one-time run: remove loop for deploy on Railway cron later
    asyncio.run(scrape_all_proxies())
          
