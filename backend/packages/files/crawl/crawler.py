import os
import re
import tempfile
import unicodedata
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from newspaper import Article
from pydantic import BaseModel


class CrawlWebsite(BaseModel):
    url: str
    js: bool = False
    depth: int = int(os.getenv("CRAWL_DEPTH", "1"))
    max_pages: int = 100
    max_time: int = 60

    def _crawl(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            print(e)
            raise

    def extract_content(self, url):
        article = Article(url)
        try:
            article.download()
            article.parse()
        except Exception as e:
            print(f"Error downloading or parsing article: {e}")
            return None
        return article.text

    def _process_recursive(self, url, depth, visited_urls):
        if depth == 0 or url in visited_urls:
            return ""

        visited_urls.add(url)

        content = self.extract_content(url)
        raw_html = self._crawl(url)

        if not raw_html:
            return content

        soup = BeautifulSoup(raw_html, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True)]
        for link in links:
            full_url = urljoin(url, link)
            # Ensure we're staying on the same domain
            if self.url in full_url:
                content += self._process_recursive(full_url, depth - 1, visited_urls)  # type: ignore

        return content

    def process(self):
        # Extract and combine content recursively
        visited_urls = set()
        extracted_content = self._process_recursive(self.url, self.depth, visited_urls)

        # Create a file
        file_name = slugify(self.url) + ".txt"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(extracted_content)  # type: ignore

        return temp_file_path, file_name

    def checkGithub(self):
        return "github.com" in self.url


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text
