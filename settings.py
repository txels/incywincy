from incywincy.visitors import http_errors, absolute_links


# root = 'http://uktv.co.uk/'
# start = 'http://uktv.co.uk/eden/'
user, password = 'uktv', 'digitalrefresh'
user, password = 'uktvdev', 'analogrefresh'


def nature(page):
    print('Nature! [{0}]'.format(page.url))


visitors = (
    ('.*', http_errors),
    ('.*', absolute_links),
    (r'^/nature', nature)
)
