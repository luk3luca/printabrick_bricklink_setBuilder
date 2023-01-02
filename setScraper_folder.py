from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import re
import json
import os, subprocess
from pathlib import Path
from zipfile import ZipFile
from os.path import join
from os import listdir, rmdir
from shutil import move

# Remove geckodriver.log
PATH_TO_DEV_NULL = 'nul'
FIREFOX_DRIVER_PATH = 'D:\\path\\to\\geckodriver.exe'

# Split code to get the original piece
def getOgCode(query):
     digit_pattern = re.compile(r'\D+')
     digits = re.split(digit_pattern, query)
     return digits[0]

# Get the Set code from the link
def getSetCode(query):
     codeRegex = re.compile(r'(\d){3,5}(-(\d){1,2})?')
     code = codeRegex.search(query)
     return code.group()

"""
# Sort the codes 
def sortDictionary(d):
    keys = []
    for k in d.keys():
        try:
            keys.append(int(k))
        except:
            keys.append(int(getOgCode(k)))
    keys.sort()
    
    tmpD = {}
    for k in keys:
        tmpD[checkCode(str(k))] = d[checkCode(str(k))]
        # tmpD[str(k)] = d[str(k)]
    return tmpD
"""
# Chooses one of multple choiches
def checkCode(code):
    match code:
        case '3049' | '3049a' | '3049b' | '3049c':
            return '3049b'
        case '3062' | '3062a' | '3062b':
            return '3062b'
        case '3068' | '3068a' | '3068b':
            return '3068b'
        case '3069' | '3069a' | '3069b':
            return '3069b'
        case '3070' | '3070a' | '3070b':
            return '3070b'
        case '3245' | '3245a' | '3245b' | '3245c':
            return '3245b'   # with inside axelholder
        case '3794' | '3794a' | '3794b':
            return '3794b'
        case '4032' | '4032a' | '4032b':
            return '4032a'
        case '4085' | '4085a' | '4085b' | '4085c' | '4085d':
            return '4085c'      # 4085a is C shaped thin, 4085c is U shaped thick
        case _:
            return getOgCode(code)


# Get list of pieces from link
def getListOfCodes(searchUrl):
    url = searchUrl
    driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH, service_log_path=PATH_TO_DEV_NULL)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html,'html5lib')
    table = soup.find('table', class_= "pciinvMainTable")
    tr_codes = table.find_all('tr', class_='pciinvItemRow')

    nPcs = []
    codes = []
    ogCodes = []
    names = []
    for tr in tr_codes:
        td_tags = tr.find_all('td')
        np = int(td_tags[2].text)
        code = td_tags[3].text
        ogCode = checkCode(code)
        name = td_tags[4].text.split('Catalog:')[0]
        if (name not in names):
            nPcs.append(np)
            codes.append(code)
            ogCodes.append(ogCode)
            names.append(name)    

    pd.set_option('display.max_rows', None)
    df = pd.DataFrame((codes, ogCodes, nPcs, names))
    df = df.T
    df.columns = ['Code |', 'Universal Code |','Quantity |', 'Brick Info']
    # print(df)

    # Dictionary for codes and number of piece, sum
    briefCodes = {}
    for i in range(len(ogCodes)):
        if(ogCodes[i] not in briefCodes):
            briefCodes[ogCodes[i]] = nPcs[i]
        else:
            briefCodes[ogCodes[i]] += nPcs[i]
    print(json.dumps(briefCodes, indent=4))

    return df, ogCodes, briefCodes

# --------------------------------------------------------- #
# Get url and list of codes
url = input('bricklink.com (v2) set url: ')
setName = getSetCode(url)           # Name of the set
setCodes = getListOfCodes(url)      # 
df = setCodes[0]                    # Full set codes with infos
ogCodes = setCodes[1]               # Only universal codes with number of pieces (duplicates)
briefCodes = setCodes[2]            # Dictionary with universal codes and number of pieces per unit

# path for set folder
setPath = 'D:\\Download\\3d\\sets'  # Path with 
cwd = Path.cwd()

# Read list.json file
with open('list.json', 'r') as myfile:
    data = myfile.read()
# Parse file
bricks = json.loads(data)

# Dictionary of codes found and not found
found = {}
notFound = {}

# Create a new folder for the set
setPath = Path(setPath, setName)
print(setPath)
if not os.path.exists(setName):
    os.makedirs(setPath)
# Create a new folder for the stl files
brickPath = Path(setPath, 'bricks')
if not os.path.exists('bricks'):
    os.makedirs(brickPath)

for key, value in briefCodes.items():
    code = key
    print(code)
    # Check if the code is in the .json
    if code in bricks:
        # print(bricks[code])
        zipPath = Path(cwd, 'files', bricks[code])
        # Store the codes found
        found[key] = value
        # root folder for the bricks
        root = Path(brickPath)
        # print(root)

        with ZipFile(zipPath, 'r') as zipRef:
            listOfFile = zipRef.namelist()
            # Files in the .zip dir
            for elem in listOfFile:
                head = os.path.split(elem)[0]
                tail = os.path.split(elem)[1]
                ext = os.path.splitext(elem)[-1]
                # exctract only the stl
                if ext == '.stl':
                    print('FOUND')
                    zipRef.extract(elem, path=brickPath)
                    # Move .stl to parent and delete the old folder
                    move(join(root, head, tail), join(root, tail))
                    rmdir(join(root, head))
    else:
        print('NOT FOUND')
        # Store the codes foun
        notFound[key] = value


# for keys in briefCodes:
#    keys = getOgCode(keys)
"""
briefCodes = sortDictionary(briefCodes)
found = sortDictionary(found)
notFound = sortDictionary(notFound)
"""
# Save a file with all the set info
with open(Path(setPath, 'setInfo.txt'), 'w') as f:
    f.write(f'Full {setName} set info')
    f.write(str(df))
    f.write('\n\n-------------------------------------\n')
    f.write('Needed pieces')
    f.write(json.dumps(briefCodes, indent=4, sort_keys = True))
    f.write('\n\n-------------------------------------\n')
    f.write('PIECES FOUND')
    f.write(json.dumps(found, indent=4, sort_keys = True))
    f.write('\n\n-------------------------------------\n')
    f.write('PIECES NOT FOUND')
    f.write(json.dumps(notFound, indent=4, sort_keys = True))
    f.close()







