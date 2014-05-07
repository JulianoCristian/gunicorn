#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# An example of a standalone application using the internal API of Gunicorn.
# 
#   $ python standalone_app.py
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

import gunicorn
import gunicorn.app.base
import multiprocessing

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def handler_app(environ, start_response):
    response_body = 'Works fine'
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Lenfth', str(len(response_body))),
    ]

    start_response(status, response_headers)

    return [response_body]


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = dict(options or {})
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        tmp_config = map(
            lambda item: (item[0].lower(), item[1]),
            self.options.iteritems()
        )

        config = dict(
            (key, value)
            for key, value in tmp_config
            if key in self.cfg.settings and value is not None
        )

        for key, value in config.iteritems():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
    }
    StandaloneApplication(handler_app, options).run()