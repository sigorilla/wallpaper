#!/usr/bin/env python3

import sys
from os.path import normpath, expanduser, join, isfile, isdir
from os import mkdir, getcwd
import subprocess
from urllib import request
import re
import argparse

YANDEX_TODAY_URL = 'https://yandex.ru/images/today?size=1920x1200'
DB_PATH = expanduser('~/Library/Application Support/Dock/desktoppicture.db')
DIR_PATH = expanduser('~/Pictures/wallpapers/')


def script(code):
    return subprocess.call(
        ['bash', '-c', code],
        stdout=sys.stdout,
        stderr=sys.stderr
    )


def getpath(path):
    return normpath(join(getcwd(), expanduser(path)))


def set_wallpaper(file):
    print('Changing wallpaper...')
    query = 'UPDATE data SET value = "%s"' % file
    assert script('''
        sqlite3 '%(db_path)s' '%(query)s'
        killall Dock
    ''' % {
        'db_path': DB_PATH,
        'query': query
    }) == 0, 'Failed to restart Dock'


def main(path, file, url):
    # TODO: add all exception handlers
    # TODO: add tests
    path = getpath(path)
    if not file:
        file = ''
    else:
        file = getpath(file)
    try:
        if not isfile(file):
            with request.urlopen(url) as response:
                assert response.getcode() == 200, 'Got unexpected HTTP response'
                attachment = response.getheader('Content-Disposition')
                filename = re.search('.+\"(?P<filename>.+)\"', attachment).group('filename')
                if not isdir(path):
                    print('Path doesn\'t exist.')
                    mkdir(path)
                    print('Directory is created: %s' % path)
                file = join(path, filename)
                with open(file, 'wb') as fd:
                    print('Downloading...')
                    fd.write(response.read())
                    print('File is downloaded: %s' % file)
        set_wallpaper(file)
    except Exception as err:
        print('Something wrong with network or filesystem: %s' % err)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set wallpaper')
    parser.add_argument('-p', '--path', default=DIR_PATH, type=str,
                        help='Path for wallpapers directory. Default: %s' % DIR_PATH)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', type=str, help='Path to file for wallpaper')
    group.add_argument('-u', '--url', default=YANDEX_TODAY_URL, type=str,
                       help='Url to get wallpaper. Default: %s' % YANDEX_TODAY_URL)

    args = parser.parse_args()
    main(path=args.path, file=args.file, url=args.url)
