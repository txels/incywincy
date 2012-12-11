# Inciwincy - a spider testing framework

The purpose of ``incywincy`` is to make it easy to write tests that need to
perform checks on every page of a website. It is especially convenient for 
applications whose URLs can be changed and extended by users, i.e. any
site that can be built via user-edited content (such as a CMS).

``incywincy`` implements the *visitor* pattern, by spidering through all the
links in a website from a starting point, parsing each into a ``Page`` 
object and passing it to a set of *visitors*.
A visitor is a function that receives a page and can analyse it and report
on something specific.

``incywincy`` includes general-purpose visitors, and allows you to create
your own project-specific ones.

You decide which visitors to run on each page based on URL matching via
regular expressions.

## Built-in visitors

* ``http_errors``: reports pages that have HTTP status >= 400
* ``absolute_links``: reports pages that contain internal links that are
  full-fledged URLs.

## Run

    python -m incywincy.spider <settings_module> <url>

E.g.:

    python -m incywincy.spider incywincy.sample_settings http://eden.uktv.co.uk

...where settings module is a python module that contains a variable 
``visitors``.

See ``incywincy.sample_settings`` for an example:

    from incywincy.visitors import http_errors, absolute_links

    def nature(page):
        """A custom visitor."""
        print('Nature! [{0}]'.format(page.url))

    visitors = (
        ('.*', http_errors),      # check for HTTP errors on all pages
        ('.*', absolute_links),   # check for absolute links on all pages
        (r'^/nature/', nature),   # custom visitor for pages under /nature
    )

## Credits

As you may have guessed, I named this project after spending many hours
singing with my toddler son.
