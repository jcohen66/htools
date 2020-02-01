import requests
import re
from urllib.parse import urljoin
import json


class Scanner:
    def __init__(self, url):
        self.target_url = url
        self.target_links = []

    def extract_links_from(self, url):
        response = requests.get(url)
        # parsed = json.loads(response.content)
        # print(parsed)
        return re.findall('(?:href=")(.*?)"', response.text)

    def crawl(self, url):
        href_links = self.extract_links_from(url)
        print(href_links)
        for link in href_links:
            link = urljoin(url, link)

            if '#' in link:
                link = link.split('#')[0]

            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                print(link)
                self.crawl(link)
