broken = []


def http_errors(page):
    status = page.status_code
    if status >= 400:
        print('Status [{0}] for URL: {1}'.format(status, page))
        broken.append(page)
