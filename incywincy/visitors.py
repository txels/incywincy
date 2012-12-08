broken = None


def http_errors(page):
    status = page.status_code
    if status == 404:
        print('Not found: [{0}] in [{1}]'.format(page, page.parent))
        broken.append({'url': page, 'parent': page.parent})
    elif status >= 400:
        print('Status [{0}] for URL: {1}'.format(status, page))
