#!/usr/bin/env python3

import sys
from os.path import join, isdir, expanduser, normpath
from os import mkdir, chmod, getcwd
import stat
import argparse
from plistlib import dump, load

PLIST_LABEL = 'ru.yandex.wallpaper'
PLIST_DEST = expanduser('~/Library/LaunchAgents/%s.plist' % PLIST_LABEL)
PLIST = dict(
    Label=PLIST_LABEL,
    ProgramArguments=[
        '-u', 'https://yandex.ru/images/today?size=1920x1200'
    ],
    RunAtLoad=True,
    StartInterval=21600,
)


def getpath(path):
    return normpath(join(getcwd(), expanduser(path)))


def main(path):
    PLIST['Program'] = getpath('./wallpaper.py')
    chmod(PLIST['Program'], stat.S_IXUSR)
    if path:
        files_path = getpath(path)
        if not isdir(files_path):
            mkdir(files_path)
        PLIST['ProgramArguments'].fromlist(['-p', files_path])
    with open(PLIST_DEST, 'wb') as fp:
        dump(PLIST, fp)
    print('Wallpaper is installed!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup for wallpaper')
    parser.add_argument('-p', '--path', type=str, help='Path for wallpapers directory.')

    args = parser.parse_args()
    main(path=args.path)
