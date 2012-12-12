from incywincy.config import settings
from incywincy.report import log


def http_errors(page):
    status = page.status_code
    if status >= 400:
        log(page, 'Status [{0}]'.format(status))


def absolute_links(page):
    for link in page.links:
        if link.startswith(settings.root):
            log(page, 'Absolute internal URL [{0}]'.format(link))


def redirects(page):
    if page.history:
        log(page, 'Was a redirect from: {0}'.format(page.url))
