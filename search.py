import json
import os
import subprocess
# read file
with open('list.json', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)

def find(q):
    out = []
    for i in obj:
        tmp = []
        nk = obj[i]
        nkhr = nk.lower()
        nkhr = nkhr.split("_")
        qhr = q.lower()
        qhr = qhr.split(' ')
        max = len(qhr) * len(nkhr)
        for x in qhr:
            for y in nkhr:
                if x == y:
                    tmp.append([i,nk])
        #print(len(tmp),max)
        if len(qhr) != 1:
            if len(tmp) >= len(qhr):
                for i in tmp:
                    if i not in out:
                        out.append(i)
        else:
            for i in tmp:
                 if i not in out:
                    out.append(i)

    return out




# search
query = input('what are you looking for? ')
counter = 0
print('---')
dataset = find(query)
for i in dataset:
    print("[" + str(counter) + "] " + i[0] + " - " + i[1])
    counter = counter + 1
selection = int(input('please select one 0-' + str(len(dataset)-1) + ": "))
url = ''.join((os.getcwd() + '/files/' + dataset[selection][1]))
n = "\ "
n = n[0]
url = url.replace("/",n)
sub = ('explorer /select,"%s"' % url)
subprocess.Popen(r'explorer /select,"%s"' % url)