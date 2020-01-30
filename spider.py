import requests
import re
from urllib.parse import urljoin


target_url = 'http://10.0.2.7/mutillidae/'
target_links = []


def extract_links_from(url):
    response = requests.get(target_url)
    # not greedy
    return re.findall(
        '(?:href=")(.*?)"', response.content.decode('utf-8'))


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urljoin(url, link)

        if '#' in link:
            link = link.split('#')[0]

        if url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


crawl(target_url)
