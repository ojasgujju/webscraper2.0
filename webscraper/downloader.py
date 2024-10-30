import os
import time
import requests
from utils.proxy_utils.proxy import Proxy
from utils.user_agent_utils.user_agent import UserAgent
import config

proxy_handler = Proxy()
ua_handler = UserAgent()

# Create the downloads directory if not exists
if not os.path.exists(config.DATA_DIR):
    os.makedirs(config.DATA_DIR)

def download_pdf(url, filename):
    headers = {'User-Agent': ua_handler.user_agent()}
    proxies = proxy_handler.generate_proxy() if config.USE_PROXY_SERVER else None

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=20)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    with open("pdf_urls.txt", "r") as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if not url.endswith(".pdf"):
            print(f"Skipping non-PDF URL: {url}")
            continue

        filename = os.path.join(config.DATA_DIR, os.path.basename(url))
        download_pdf(url, filename)
        time.sleep(1)  # Delay between downloads for safe scraping

if __name__ == "__main__":
    main()
