import requests
from pydantic import BaseModel
import requests
import re
import unicodedata
import tempfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse

class CrawlWebsite(BaseModel):
    url: str
    js: bool = True
    depth: int = 2
    max_pages: int = 100
    max_time: int = 60

    def _crawl(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ["http", "https"]:
            return None
        
        print(parsed_url)
        self.js = False
        if self.js:
            # Configure Selenium with Chrome options
            print('chrome')
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # Set up Selenium WebDriver with Chrome
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

            # Wait for JavaScript to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//body")))

            # Get the rendered page source
            content = driver.page_source

            # Close the browser
            driver.quit()
        else:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
            else:
                content = None

        return content


    def process(self):
        visited_urls = set()
        queue = []
        crawled_pages = 0
        all_content = ""

        # Fetch the initial page content
        initial_content = self._crawl(self.url)
        if initial_content:
            all_content += initial_content
            crawled_pages += 1

            # Extract links from the initial page
            links = self._extract_links(initial_content, self.url)
            print(links)

            # Add links to the queue
            queue.extend([(link, 1) for link in links])
            print(queue)

        while crawled_pages < self.max_pages:
            if not queue:
                break

            url, depth = queue.pop(0)

            if url in visited_urls or depth > self.depth:
                continue

            visited_urls.add(url)
            content = self._crawl(url)

            if content:
                all_content += content
                crawled_pages += 1

                # Extract links from the page
                # links = self._extract_links(content, url)

                # Add links to the queue for further crawling
                # queue.extend([(link, depth + 1) for link in links])

        # Create a file
        print(all_content)
        print(crawled_pages)
        file_name = slugify(self.url) + ".html"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(all_content)
            # Process the file
            print(temp_file)

        return temp_file_path, file_name

    def _extract_links(self, content, base_url):
        links = []
        pattern = r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1'

        for match in re.findall(pattern, content, re.IGNORECASE):
            url = match[1]
            url = urljoin(base_url, url)

            # Filter out external links (uncomment if desired)
            # if urlparse(url).netloc == urlparse(base_url).netloc:
            links.append(url)

        return links


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text
