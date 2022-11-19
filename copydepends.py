#!/usr/bin/env python3

import ldcopy
import os, subprocess
from argparse import ArgumentParser

__excludes = list()
__temporary_file='/tmp/copydepends.tmp'


def __is_valid_path(path: str):
    for exclude in __excludes:
        if exclude in path:
            return False
    return True


def __clear_line(line: str):
    line = line.replace('\n', '')
    line = line.replace('\t', '')
    return line


def add_excludes(excludes_line:str):
    global __excludes
    __excludes = excludes_line.split(',')


def process_binary_file(file:str, outdir:str):
    os.system(f'ldd {file} > {__temporary_file}')
    if (os.path.exists(__temporary_file)):
        with open(__temporary_file, 'r') as file:
            for line in file.readlines():
                line = __clear_line(line)
                parts = line.split(' ')

                if len(parts) == 4:
                    libname = parts[0]
                    libpath = parts[2]

                    if __is_valid_path(libpath):
                        print(f'{libname} => {libpath}')
                        ldcopy.copy(libpath, outdir)

        os.remove(__temporary_file)


def main():
    parser = ArgumentParser('Get binary file dependencies')
    parser.add_argument('--file',     type=str, help='Input binary file', required=True)
    parser.add_argument('--outdir',   type=str, help='Output directory',  required=True)
    parser.add_argument('--excludes', type=str, help='Excludes libs path')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'Input binary file not existe: {args.file}')
        exit(1)
    if not os.path.exists(args.outdir):
        print(f'Output dir not existe: {args.outdir}')
        exit(1)
    if not os.path.isdir(args.outdir):
        print(f'{args.outdir} is not directory')
        exit(1)
    if not args.excludes is None:
        add_excludes(args.excludes)

    process_binary_file(args.file, args.outdir)


if __name__ == '__main__':
    main()
