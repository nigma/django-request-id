=================
django-request-id
=================


.. image:: https://img.shields.io/pypi/l/dj-cmd.svg
    :target: https://raw.githubusercontent.com/nigma/django-request-id/master/LICENSE
    :alt: License

.. image:: https://img.shields.io/pypi/v/django-request-id.svg
    :target: https://pypi.python.org/pypi/django-request-id/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/wheel/django-request-id.svg
    :target: https://pypi.python.org/pypi/django-request-id/
    :alt: Supports Wheel format

Augments each request with unique ``request_id`` attribute and provides
request id logging helpers.

Developed and used at `en.ig.ma software shop <http://en.ig.ma>`_.


Quickstart
----------

1. Include ``django-request-id`` in your ``requirements.txt`` file.

2. Add ``request_id`` to ``INSTALLED_APPS`` (necessary only if you are
   going to use the ``{% request_id %}`` template tag).

3. Add ``request_id.middleware.RequestIdMiddleware`` at the top of
   the ``MIDDLEWARE`` Django setting.

4. The app integrates with the standard Python/Django logging by defining
   a filter that puts a ``request_id`` variable in scope of every log message.

   First add a filter definition to the Django ``LOGGING`` settings:

   .. code-block:: python

       "filters": {
           "request_id": {
               "()": "request_id.logging.RequestIdFilter"
           }
       }

   Then enable the filter for related handlers:

   .. code-block:: python

       "handlers": {
           "console": {
               ...
               "filters": ["request_id"],
           }
        }

   And finally modify formatter output format to include the ``%(request_id)`` placeholder:

   .. code-block:: python

       "formatters": {
           "console": {
               "format": "%(asctime)s - %(levelname)-5s [%(name)s] request_id=%(request_id)s %(message)s"
           }
       }

   A full Django logging config example may look like this:

   .. code-block:: python


       LOGGING= {
           "version": 1,
           "disable_existing_loggers": False,
           "filters": {
               "request_id": {
                   "()": "request_id.logging.RequestIdFilter"
               }
           },
           "formatters": {
               "console": {
                   "format": "%(asctime)s - %(levelname)-5s [%(name)s] request_id=%(request_id)s %(message)s",
                   "datefmt": "%H:%M:%S"
               }
           },
           "handlers": {
               "console": {
                   "level": "DEBUG",
                   "filters": ["request_id"],
                   "class": "logging.StreamHandler",
                   "formatter": "console"
               }
           },
           "loggers": {
               "": {
                   "level": "DEBUG",
                   "handlers": ["console"]
               }
           }
       }

5. Make sure that your web server adds a ``X-Request-ID`` header to each request
   (and logs it in the server log for further matching of the server and app log entries).

   - Heroku handles this `automatically <https://devcenter.heroku.com/articles/http-request-id>`_.
   - On Nginx you may require a separate module (see
     `nginx_requestid <https://github.com/hhru/nginx_requestid>`_ or
     `nginx-x-rid-header <https://github.com/newobj/nginx-x-rid-header>`_).
   - On Apache you need to ``a2enmod`` the `unique_id <https://httpd.apache.org/docs/2.4/mod/mod_unique_id.html>`_
     module and set ``REQUEST_ID_HEADER = "UNIQUE_ID"`` in the Django project
     settings.

   If you can't generate the `X-Request-Id` header at the web server level then
   simply set ``REQUEST_ID_HEADER = None`` in your project settings and the
   app will generate a unique id value automatically instead of retrieving
   it from the wsgi environment.

   For more info on server configs see
   `server-config <http://django-request-id.rtfd.org/en/latest/server-config.html>`_.

Dependencies
------------

None.

Documentation and demo
----------------------

The full documentation is at http://django-request-id.rtfd.org.

There's also an instant demo example that can be run from the cloned repository::

    python demo.py

See the integration in action on Heroku:

.. image:: https://www.herokucdn.com/deploy/button.svg
   :alt: Deply
   :target: https://heroku.com/deploy?template=https://github.com/nigma/django-request-id

License
-------

``django-request-id`` is released under the MIT license.

Other Resources
---------------

- GitHub repository - https://github.com/nigma/django-request-id
- PyPi Package site - http://pypi.python.org/pypi/django-request-id


Commercial Support
------------------

This app and many other help us build better software
and focus on delivering quality projects faster.
We would love to help you with your next project so get in touch
by dropping an email at en@ig.ma.
