#!/usr/bin/env python3

import sys
from os.path import expanduser, join, isfile
import subprocess
from urllib import request
import re

YANDEX_TODAY_URL = 'https://yandex.ru/images/today?size=1440x900'
DB_PATH = expanduser('~/Library/Application Support/Dock/desktoppicture.db')
DIR_PATH = expanduser('~/Pictures/wallpapers/')

def script(code):
    return subprocess.call(
        ['bash', '-c', code],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

def set_wallpaper(file):
    print('Changing wallpaper...')
    query = 'UPDATE data SET value = \'%s\'' % file
    assert script('''
        sqlite3 '%(db_path)s' '%(query)s'
        killall Dock
    ''' % {
        'db_path': DB_PATH,
        'query': query
    }) == 0, 'Failed to restart Dock'

def main():
    try:
        with request.urlopen(YANDEX_TODAY_URL) as response:
            assert response.getcode() == 200, 'Got unexpected HTTP response'
            attachment = response.getheader('Content-Disposition')
            filename = re.search('.+\"(?P<filename>.+)\"', attachment).group('filename')
            file = join(DIR_PATH, filename)
            if isfile(file):
                print('File exists: %s' % file)
            else:
                with open(file, 'wb') as fd:
                    print('Downloading...')
                    fd.write(response.read())
                    print('File is downloaded: %s' % file)
            set_wallpaper(file)
    except Exception as err:
        print('Something wrong with network or filesystem: %s' % err)

if __name__ == '__main__':
    main()
