import re

from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

import settings


UA = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
visited = set()
exceptions = []


def absolutize(url):
    """
    Convert url to absolute address, based on page root.
    """
    if ':' in url[:20]:
        return url
    else:
        if settings.root.endswith('/') and url.startswith('/'):
            url = url[1:]
        return settings.root + url


def find_links(html):
    """
    Find all links in the HTML page.
    """
    soup = BeautifulSoup(html)
    links = filter(lambda a: 'href' in a.attrs, soup.find_all('a'))
    return [a['href'] for a in links]


def normalised(links, start):
    """
    Return a set of normalised links.

    These will all be absolute URLs, and no repeats.
    """
    links = [absolutize(link) for link in links]
    return set(filter(lambda x: x.startswith(start), links))


class Page(object):
    """
    A web page, that can be processed by a visitor.

    Contains useful information about the page, such as the status code,
    content, list of links, and referrer (the page where we found a link to
    this one).
    """
    def __init__(self, url, referrer):
        self.referrer = referrer
        self.url = url
        headers = {'User-Agent': UA}
        self.response = requests.get(url, auth=auth, headers=headers)
        self._links = []

    def __getattr__(self, attr):
        return getattr(self.response, attr)

    def __str__(self):
        if isinstance(self.referrer, Page):
            referrer_url = self.referrer.url
        else:
            referrer_url = self.referrer
        return "{url} [from: {ref}]".format(url=self.url, ref=referrer_url)

    @property
    def links(self):
        if not self._links:
            if self.response.status_code == 200:
                content_type = self.headers['Content-Type']
                if content_type.startswith('text/html'):
                    self._links = find_links(self.text)
        return self._links

    def normalised_links(self, start):
        return normalised(self.links, start)


def visit(url, parent=None):
    """
    Recursively visit all pages from this URL.

    Will keep track of visited pages, so as to avoid processing links twice.
    """
    visited.add(url)
    print('Opening: ' + url)
    try:
        page = Page(url, parent)
    except Exception as e:
        print('Exception in {0}'.format(page))
        exceptions.append({'page': page, 'error': e})
    else:
        status = page.status_code
        for pattern, visitor in settings.visitors:
            url_path = url[len(settings.root):]
            if re.match(pattern, url_path):
                visitor(page)
        # recurse while successful
        if status == 200:
            links = page.normalised_links(settings.start)
            links.difference_update(visited)
            # print("New links:\n" + "\n".join(links))
            for link in links:
                visit(link, page)


if __name__ == '__main__':
    try:
        auth = HTTPBasicAuth(settings.user, settings.password)
    except:
        auth = None

    import sys
    settings.root = sys.argv[1]
    if settings.root.endswith('/'):
        settings.root = settings.root[:-1]
    try:
        settings.start = sys.argv[2]
    except:
        settings.start = settings.root
    visit(settings.start, settings.root)
