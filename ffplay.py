#!/usr/bin/env python
import asyncio
from pathlib import Path
import shutil
import sys
from argparse import ArgumentParser

if sys.version_info < (3, 7):
    raise RuntimeError('Python >= 3.7 required')


FFPLAY = shutil.which('ffplay')
if not FFPLAY:
    raise FileNotFoundError('FFPLAY not found')


async def ffplay(filein: Path):
    """ Play media asynchronously """
    assert isinstance(FFPLAY, str)

    proc = await asyncio.create_subprocess_exec(*[FFPLAY, '-v', 'warning', str(filein)])

    ret = await proc.wait()

    if ret != 0:
        print(filein, 'playback failure', file=sys.stderr)


if __name__ == '__main__':
    p = ArgumentParser(
        description="Plays media files asynchronously with FFplay")
    p.add_argument('path', help='directory where media files are kept')
    p.add_argument('-suffix', help='file suffixes of desired media file types',
                   nargs='+', default=['.mp4', '.avi', '.ogv'])
    P = p.parse_args()

    path = Path(P.path).expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f'{path} is not a directory')

    flist = (f for f in path.iterdir() if f.is_file() and f.suffix in P.suffix)

    futures = [ffplay(f) for f in flist]

    asyncio.run(asyncio.wait(futures))