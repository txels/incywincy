import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

import settings


UA = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
visited = set()
broken = []


def fetch(url):
    headers = {'User-Agent': UA}
    response = requests.get(url, auth=settings.auth, headers=headers)
    return response


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


def save_image(data, filename):
    with open(filename, "wb") as f:
        f.write(data)


def find_broken(page, parent=None):
    visited.add(page)
    print('Opening: ' + page)
    try:
        response = fetch(page)
    except RequestException as e:
        print('HTTP Error: [{0}] in [{1}] from [{2}]'.format(e, page, parent))
        broken.append({'url': page, 'parent': parent, 'error': e})
    else:
        status = response.status_code
        if status == 200:
            content_type = response.headers['Content-Type'][:9]
            if content_type == 'text/html':
                links = find_inner_links(response.text)
                links.difference_update(visited)
                # print("New links:\n" + "\n".join(links))
                for link in links:
                    find_broken(link, page)
        elif status == 404:
            print('Not found: [{0}] in [{1}]'.format(page, parent))
            broken.append({'url': page, 'parent': parent})
        else:
            print('Status [{0}] for URL: {1}'.format(status, page))


if __name__ == '__main__':
    import sys
    root = sys.argv[1]
    try:
        start = sys.argv[2]
    except:
        start = root
    find_broken(start, root)
    print(broken)
