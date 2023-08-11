import os
import re
import tempfile
import unicodedata

from urllib.parse import  urljoin
import requests
from pydantic import BaseModel


class CrawlWebsite(BaseModel):
    url: str
    js: bool = False
    depth: int = int(os.getenv("CRAWL_DEPTH","1"))
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
            return None

    def process(self):
        visited_list=[]
        self._process_level(self.url, 0, visited_list)
        return visited_list

    def _process_level(self, url, level_depth, visited_list):
        content = self._crawl(url)
        if content is None:
            return
        
        
        # Create a file
        file_name = slugify(url) + ".html"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(content)  # pyright: ignore reportPrivateUsage=none
            # Process the file

        if content:
            visited_list.append((temp_file_path, file_name))
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html5lib')
            links = soup.findAll('a')
            if level_depth < self.depth:
                for a in links:
                    if not a.has_attr('href'):
                        continue
                    new_url = a['href']
                    file_name = slugify(new_url) + ".html"
                    already_visited = False
                    for (fpath,fname) in visited_list:
                        if fname == file_name :
                            already_visited = True
                            break
                    if not already_visited:
                        self._process_level(urljoin(url,new_url),level_depth + 1,visited_list)



    def checkGithub(self):
        if "github.com" in self.url:
            return True
        else:
            return False


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text
