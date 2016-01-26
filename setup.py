#!/usr/bin/env python3

from os.path import join, isdir, expanduser, normpath
from os import mkdir, chmod, getcwd
import stat
import argparse
from plistlib import dump

PLIST_LABEL = 'ru.yandex.wallpaper'
PLIST_DEST = expanduser('~/Library/LaunchAgents/%s.plist' % PLIST_LABEL)
PLIST_PROGRAM_ARGS = [
    '-u',
    'https://yandex.ru/images/today?size=1920x1200'
]
DIR_PATH = expanduser('~/Pictures/wallpapers/')


def getpath(path):
    """
    :param path: Path
    :return: Normalize path from root
    """
    return normpath(join(getcwd(), expanduser(path)))


def plist(source, arguments=None):
    """
    Create PLIST dictionary
    :type source: String
    :type arguments: Array
    :param source: Executable file
    :param arguments: Arguments for source
    :return:
    """
    if arguments is None:
        arguments = []
    return dict(
        Label=PLIST_LABEL,
        Program=source,
        ProgramArguments=arguments,
        RunAtLoad=True,
        StartInterval=600,
    )


def main(path):
    """
    Create PLIST file and set chmod to source
    :param path: Path for wallpapers directory
    """
    source = getpath('./wallpaper.py')
    chmod(source, stat.S_IRWXU + stat.S_IRWXG + stat.S_IRWXO)
    if path:
        files_path = getpath(path)
        if not isdir(files_path):
            mkdir(files_path)
        PLIST_PROGRAM_ARGS.extend(['-p', files_path])
    with open(PLIST_DEST, 'wb') as fp:
        dump(plist(source, PLIST_PROGRAM_ARGS), fp)
    print('Wallpaper is installed!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup for wallpaper')
    parser.add_argument('-p', '--path', default=DIR_PATH, type=str,
                        help='Path for wallpapers directory. Default: %s' % DIR_PATH)

    args = parser.parse_args()
    main(path=args.path)
