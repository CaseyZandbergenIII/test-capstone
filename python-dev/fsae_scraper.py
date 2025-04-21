import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from pathlib import Path


def download_pdfs_from_url(url):
    downloads_path = str(Path.home() / "Downloads")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": url,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    pdf_links = [
        urljoin(url, a["href"])
        for a in soup.find_all("a", href=True)
        if a["href"].lower().endswith(".pdf")
    ]

    if not pdf_links:
        print("No PDF files found on the webpage.")
        return

    print(f"Found {len(pdf_links)} PDF(s). Starting download...")

    for pdf_url in tqdm(pdf_links, desc="Downloading PDFs"):
        filename = os.path.basename(urlparse(pdf_url).path)
        filepath = os.path.join(downloads_path, filename)

        try:
            with requests.get(pdf_url, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(filepath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
        except Exception as e:
            print(f"Failed to download {pdf_url}: {e}")

    print("All available PDFs downloaded to your Downloads folder.")


download_pdfs_from_url(
    "https://www.sae.org/attend/student-events/formula-sae-michigan/awards-results"
)
