import os
import glob

os.chdir('/ddn/home3/r2652/chem/Dyes/results')
a = glob.glob('/ddn/home3/r2652/chem/Dyes/results/*')
direct = []
for i in a:
    i = i.split('/')
    direct.append(i[-1])
topdyes = []
for name in direct:
    try:
#        filename = open(str(name) + '/mexc/mexc.out','r')
        filename = open(str(name) + '/mexc/mexc.out','r')
        data = filename.readlines()
#print(direct)
        for i in data:
         #print(i)
            if 'Excited State   1:' in i:
                if float(i[50:58]) > 600:

             #          print((name,float(i[50:58])))
                       topdyes.append((name,float(i[50:58])))
    except FileNotFoundError:
           continue 

topdyesdict = {}
for i in range(len(topdyes)):
    a = str(topdyes[i][0])
    b = float(topdyes[i][1])
    
    topdyesdict[a] = b
#mexclis = ['5ed_16b_4ea', '7ed_16b_5ea', '6ed_16b_4ea', '6ed_16b_5ea', '1ed_16b_4ea', '3ed_16b_5ea', '5ed_16b_5ea', '2ed_16b_4ea', '7ed_16b_4ea', '2ed_16b_5ea', '3ed_16b_4ea', '5ed_16b_1ea', '1ed_16b_5ea', '5ed_16b_9ea', '6ed_16b_1ea', '6ed_16b_7ea', '6ed_16b_6ea', '1ed_16b_1ea', '1ed_16b_9ea', '6ed_16b_10ea', '6ed_16b_9ea']

mexclis = ['5ed_16b_10ea','5ed_16b_11ea','5ed_16b_1ea','5ed_16b_2ea','5ed_16b_3ea','5ed_16b_5ea','5ed_16b_6ea','5ed_16b_7ea','5ed_16b_8ea','5ed_16b_9ea','5ed_1b_4ea']  

for i in mexclis:
    print((topdyesdict[i],i))
#    print((1239.84/topdyesdict[i])*-0.35894991)



#print(sorted(topdyesdict.items(),reverse=False))
k = sorted(topdyesdict.items(),reverse=True)
mo = []
for aaa in k:
    print(aaa)
    mo.append(aaa[0])
#print(mo)
for i in mo:
    i
   # print(1239.84/i)
