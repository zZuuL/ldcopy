#!/usr/bin/env python3

import os, shutil
from argparse import ArgumentParser


def make_symlinks(library: str):
    basename = os.path.basename(library)
    filename_parts = basename.split('.')
    if len(filename_parts) > 2:
        sym_names = list()
        folder = os.path.dirname(library)
        name = f'{filename_parts[0]}.{filename_parts[1]}'
        sym_names.append(name)

        '''make symbolic links names'''
        for i in filename_parts[2:-1]:
            name = f'{name}.{i}'
            sym_names.append(name)

        '''create symbolic links'''
        for name in sym_names:
            os.system(f'ln -sf {basename} {os.path.join(folder, name)}')


def copy(library: str, outpath: str):
    if os.path.islink(library):
        library = os.path.join(
                    os.path.dirname(library),
                    os.readlink(library))

    make_symlinks(shutil.copy(library, outpath))


def main():
    parser = ArgumentParser()
    parser.add_argument('--library', type=str, help='Input library', required=True)
    parser.add_argument('--outdir', type=str, help='Output directory', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.library):
        print(f'Input library not existe: {args.library}')
        exit(1)
    if not os.path.exists(args.outdir):
        print(f'Output dir not existe: {args.outdir}')
        exit(1)
    if not os.path.isdir(args.outdir):
        print(f'{args.outdir} is not directory')
        exit(1)

    copy(args.library, args.outdir)


if __name__ == '__main__':
    main()

