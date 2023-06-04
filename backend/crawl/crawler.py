import requests
from pydantic import BaseModel
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
import queue
from bs4 import BeautifulSoup

class CrawlWebsite(BaseModel):
    url: str
    js: bool = True
    max_depth: int = 1
    max_pages: int = 10
    max_time: int = 60

    def _crawl(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ["http", "https"]:
            return None
        
        if self.js:
            content = None
        else:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
            else:
                content = None

        return content

    def process(self):
        # parsing the url
        _max_pages = self.max_pages
        max_depth = self.max_depth
        parsed_url = urlparse(self.url)
        scheme = parsed_url.scheme
        loc = parsed_url.netloc
        path = parsed_url.path
        print(parsed_url)
        # domain = scheme + "://" + loc

        # initialize variables
        text = ""
        links = queue.Queue()
        visited = set()

        links.put(path)
        
        # Configure Selenium with Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up Selenium WebDriver with Chrome
        driver = webdriver.Chrome(options=chrome_options)
        while not links.empty() and _max_pages > 0:
            print(_max_pages)
            text+=self.scrape(driver, links, visited, scheme, loc)
            _max_pages -= 1
        driver.quit()

        file_name = slugify(self.url) + ".html"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        # Process the file
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(text)

        return temp_file_path, file_name

    def get_links(self, soup: BeautifulSoup, original_loc: str, path: str) -> list: 
        links = soup.find_all('a', href=True)
        internal_links = []
        for link in links:
            href = link.get('href')
            # print('hrefhref', link)
            if urlparse(href).netloc == original_loc:
                internal_links.append(urlparse(href).path)
            elif not urlparse(href).netloc and href and href[0]!='#':
                internal_links.append(path + href) if path != "/" else internal_links.append(href)
        # internal_links = [link.get('href') for link in links if '://' not in link.get('href')]
        return internal_links

    def scrape(self, driver: webdriver.Chrome, links: queue.Queue, visited: set, scheme: str, loc: str):
        path = links.get()
        path = "/" + path if path[0] != "/" else path
        # print("scrape_path", path)
        if path in visited:
            return ""
        url = scheme + "://" + loc + path
        print(url)
        # domain = urlparse(url).netloc
        # path = urlparse(url).path
        visited.add(path)
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))

        # Get the rendered page source
        content = driver.page_source
        text = ""
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            footer = soup.find('footer')
            if footer:
                footer.extract()
            internal_links = self.get_links(soup, loc, path)
            [links.put(internal_link) for internal_link in internal_links]
            # adding path name 
            text += path + "\n"
            # adding file content after formating it
            text += slugify(soup.get_text(), type='html') + "\n"
        return text

def slugify(text, type=None):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    if type == 'html':
        text = re.sub(r'[-\s]+', ' ', text)
    else:
        text = re.sub(r'[-\s]+', '-', text)
    return text
