import json
import os, subprocess
from pathlib import Path
from zipfile import ZipFile
from os.path import join
from os import listdir, rmdir
from shutil import move
import re

def isWeird(query):
    # dRegex = re.compile(r'(\d){3}[a-zA-Z]|(\d){4}[a-zA-Z]|(\d){5}[a-zA-Z]')
    # print(bool(dRegex.match(query)))
    dRegex = re.compile(r'(\d){4}[a-zA-Z]')
    if bool(dRegex.match(query)):
        return True
    return False

dirs = os.listdir('D:\\Download\\3d\\printabrick\\files')
n = 0
toCheck = []

for d in dirs:
    if isWeird(d):
        toCheck.append(d)

print(len(dirs))
print(n)


setPath = 'D:\\Download\\3d\\sets'
cwd = Path.cwd()

with open('list.json', 'r') as myfile:
    data = myfile.read()
bricks = json.loads(data)

# Find the codes in the bricks folder
for c in toCheck:
    code = c
    if code in bricks:
        print(bricks[code])
        open = input('open y, no n: ')
        if(open == 'y'):
            zipPath = Path(cwd, 'files', bricks[code])
            subprocess.Popen(r'explorer "%s"' % zipPath)
    else:
        print('NOT FOUND')