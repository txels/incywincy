"""Incy Wincy Spider.

Usage:
    spider.py [--level=<level>] <settings> <url> [<start>]
    spider.py -h | --help

Options:
    -h --help        Show this screen.
    --version        Show version.
    --level=<level>  Set logging level (0: Debug to 3: Error) - [default: 2].
"""
if __name__ == '__main__':
    from docopt import docopt
    from incywincy import __version__, config, report

    arguments = docopt(__doc__, version='Incy Wincy ' + __version__)
    print arguments
    config.settings = config.Settings(arguments['<settings>'])
    settings = config.settings
    report.THRESHOLD = int(arguments['--level'])

    settings.root = arguments['<url>']
    if settings.root.endswith('/'):
        settings.root = settings.root[:-1]

    settings.start = arguments['<start>']
    if settings.start is None:
        settings.start = settings.root

    from incywincy.http import visit
    visit(settings.start, settings.root)
