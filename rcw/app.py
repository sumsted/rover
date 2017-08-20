from bottle import run, template, static_file, route, get, TEMPLATE_PATH
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
TEMPLATE_PATH.insert(0, './templates')


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@get('/')
def get_index():
    return template('index')


if __name__ == '__main__':
    run(host=settings.client.host, port=settings.client.port)
