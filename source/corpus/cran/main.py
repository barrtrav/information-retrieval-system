
f = open('cran.all.1400').readlines()

for i in range(len(f)):
    ID = ''
    if f[i][:-2] == '.I': 
        ID = f[i][2:]
        i+= 1
    
    TITLE = ''
    if f[i][:-2] == '.T':
        while f[i][:-2] != '.A':
            i+= 1
            TITLE += f[i]
    
    
