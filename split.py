import os
import re

def isWeird(query):
    dRegex = re.compile(r'(\d){3}[a-zA-Z]|(\d){4}[a-zA-Z]|(\d){5}[a-zA-Z]')
    # print(bool(dRegex.match(query)))
    if bool(dRegex.match(query)):
        return True
    return False
    

dirs = os.listdir('D:\\Download\\3d\\printabrick\\files')

n = 0


for d in dirs:
    if isWeird(d):
        print(d)
        n += 1

print(len(dirs))
print(n)

