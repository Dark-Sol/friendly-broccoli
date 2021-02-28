from pathlib import Path
from itertools import islice
from ctypes import wintypes, windll
from functools import cmp_to_key
import sys

space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '



def winsort(data):
    _StrCmpLogicalW = windll.Shlwapi.StrCmpLogicalW
    _StrCmpLogicalW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR]
    _StrCmpLogicalW.restype  = wintypes.INT
    cmp_fnc = lambda psz1, psz2: _StrCmpLogicalW(psz1, psz2)
    return sorted(data, key=cmp_to_key(cmp_fnc))

def tree(dir_path: Path, level: int=-1, limit_to_directories: bool=True,
         length_limit: int=10000, file=sys.stdout):
    """Given a directory Path object print a visual tree structure"""
    userdir = input ("Input the directory you want scanned: ")
    dir_path = Path(userdir)
    files = 0
    directories = 0
    def inner(dir_path: Path, prefix: str='', level=-1):
        nonlocal files, directories
        if not level: 
            return # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else: 
            contents = list(dir_path.iterdir())
        #contents = winsort(contents)
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space 
                yield from inner(path, prefix=prefix+extension, level=level-1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1
    print(dir_path.name, file=file)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line, file=file)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:', file=file)
    print(f'\n{directories} directories' + (f', {files} files' if files else ''), file=file)

with open('C:/code/test2.txt', mode='w', encoding='utf8') as f:
    tree(Path.home() / 'My Music' , file=f)
