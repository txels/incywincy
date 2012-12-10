# Inciwincy - a spider testing framework

The purpose of ``incywincy`` is to make it easy to write tests that need to
perform checks on every page of a website.

``incywincy`` implements the *visitor* pattern, by spidering through all the
links in a website from a starting point, parsing each into a ``Page`` 
object and passing it to all registered *visitors*. A visitor is a function
that receives a page and can analyse it and report on something specific.

``incywincy`` includes general-purpose visitors, and allows you to create
your own project-specific ones.

## Built-in visitors

* ``http_errors``: reports pages that have HTTP status >= 400
* ``absolute_links``: reports pages that contain internal links that are
  full-fledged URLs.

## Credits

As you may have guessed, I named this project after spending many hours
singing with my toddler son.
