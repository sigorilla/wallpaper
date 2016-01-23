#!/usr/bin/env python3

import sys
from os.path import join, isdir, expanduser, normpath
from os import mkdir, chmod, getcwd
import stat
import argparse
from plistlib import dump, load

PLIST_LABEL = 'ru.yandex.wallpaper'
PLIST_DEST = expanduser('~/Library/LaunchAgents/%s.plist' % PLIST_LABEL)
PLIST_PROGRAM_ARGS = [
    '-u',
    'https://yandex.ru/images/today?size=1920x1200'
]


def getpath(path):
    return normpath(join(getcwd(), expanduser(path)))


def plist(source, args=[]):
    return dict(
        Label=PLIST_LABEL,
        Program=source,
        ProgramArguments=args,
        RunAtLoad=True,
        StartInterval=21600,
    )


def main(path):
    source = getpath('./wallpaper.py')
    chmod(source, stat.S_IRWXU + stat.S_IRWXG + stat.S_IRWXO)
    if path:
        files_path = getpath(path)
        if not isdir(files_path):
            mkdir(files_path)
        PLIST_PROGRAM_ARGS.fromlist(['-p', files_path])
    with open(PLIST_DEST, 'wb') as fp:
        dump(plist(source, PLIST_PROGRAM_ARGS), fp)
    print('Wallpaper is installed!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup for wallpaper')
    parser.add_argument('-p', '--path', type=str, help='Path for wallpapers directory.')

    args = parser.parse_args()
    main(path=args.path)
