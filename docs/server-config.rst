==================
Web server configs
==================

Heroku
------

If the X-Request-ID header is not passed automatically you may need to
enable it using the labs command:

.. code-block:: bash

    heroku labs:enable http-request-id

See `http-request-id <https://devcenter.heroku.com/articles/http-request-id>`_ for more info.

The ``request_id`` will also appear in the Heroku Dyno logs so it is easy to match
application logs with Heroku request logs.

Nginx
-----

There's no built-in option in Nginx to generate a unique request id, but there
are several modules that provide this functionality:

    - `nginx_requestid <https://github.com/hhru/nginx_requestid>`_
    - `nginx-x-rid-header <https://github.com/newobj/nginx-x-rid-header>`_

Unfortunately this require Nginx binary recompilation.

Alternatively, if your Nginx has Lua scripting enabled, you can generate a random id
and add it to server logs using the following snippets:

.. code-block:: nginx

    http {
        ...

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for" '
                          'request_id=$request_id';
        ...
    }

.. code-block:: lua

    server {
        listen       80;
        server_name  localhost;

        access_log  logs/host.access.log  main;

        location / {
            set_by_lua $request_id '
                local function random_id()
                    local charset = "0123456789abcdefghijklmnopqrstuvwxyz"
                    local template = "xxxx-xxxxxxxx-xxxxxxxx"
                    local range = charset:len()
                    return string.gsub(template, "x", function (c)
                        return string.char(charset:byte(math.random(1, range)))
                    end)
                end
                local request_id = random_id()
                ngx.req.set_header("X-Request-Id", request_id)
                return request_id
            ';

            ...
        }

Apache
------

On Apache you need to ``a2enmod`` the `unique_id <https://httpd.apache.org/docs/2.4/mod/mod_unique_id.html>`_
module and set ``REQUEST_ID_HEADER = "UNIQUE_ID"`` in the Django project
settings.

Standalone
----------

If you can't generate the X-Request-Id header at the web server level then
simply set ``REQUEST_ID_HEADER = None`` in your project settings and the
app will generate a unique id value automatically instead of retrieving
it from the wsgi environment.

You can also use the :class:`request_id.wsgi.AddRequestIdHeaderMiddleware` WSGI
middleware for that purpose.
