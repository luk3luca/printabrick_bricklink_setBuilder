import json
import os, subprocess
from pathlib import Path

dirs = os.listdir('D:\\Download\\3d\\printabrick\\files')

setPath = 'D:\\Download\\3d\\sets'
cwd = Path.cwd()

with open('list.json', 'r') as myfile:
    data = myfile.read()
bricks = json.loads(data)

# Find the codes in the bricks folder
code = input('Search code: ')
while(code != 'STOP'):
    if code in bricks:
        print(bricks[code])
        open = input('open y, no n: ')
        if(open == 'y'):
            zipPath = Path(cwd, 'files', bricks[code])
            subprocess.Popen(r'explorer "%s"' % zipPath)
    else:
        print('NOT FOUND')

    code = input('Search code: ')