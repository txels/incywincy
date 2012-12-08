import requests
from bs4 import BeautifulSoup
from incywincy.visitors import http_errors

import settings


UA = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
visited = set()
exceptions = []
all_visitors = (
    http_errors,
)


class Page(object):
    def __init__(self, url, referrer):
        self.referrer = referrer
        self.url = url
        headers = {'User-Agent': UA}
        self.response = requests.get(url, auth=settings.auth, headers=headers)

    def __getattr__(self, attr):
        return getattr(self.response, attr)


def fetch(url, referrer):
    return Page(url, referrer)


def absolutize(url):
    if ':' in url[:20]:
        return url
    else:
        if root.endswith('/') and url.startswith('/'):
            url = url[1:]
        return root + url


def find_inner_links(data):
    soup = BeautifulSoup(data)
    links = filter(lambda a: 'href' in a.attrs, soup.find_all('a'))
    links = [absolutize(a['href']) for a in links]
    return set(filter(lambda x: x.startswith(start), links))


def visit(url, parent=None):
    visited.add(url)
    print('Opening: ' + url)
    try:
        page = fetch(url, parent)
    except Exception as e:
        print('Exception in [{0}] from [{1}]'.format(page.url, parent))
        exceptions.append({'url': page, 'parent': parent, 'error': e})
    else:
        status = page.status_code
        for visitor in all_visitors:
            visitor(page)
        if status == 200:
            content_type = page.headers['Content-Type']
            if content_type.startswith('text/html'):
                links = find_inner_links(page.text)
                links.difference_update(visited)
                # print("New links:\n" + "\n".join(links))
                for link in links:
                    visit(link, page)


if __name__ == '__main__':
    import sys
    root = sys.argv[1]
    try:
        start = sys.argv[2]
    except:
        start = root
    visit(start, root)
