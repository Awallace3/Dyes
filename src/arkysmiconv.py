import os

path = '../backbones/9b.smi' 
def TheBBDBBAadder(filename):
    '''
    Argon is where the acceptor connects to backbone
    Krypton is where the Donor connects to backbone

    '''
    filename = open(str(filename),'r')
    
    a = []
    for i in filename.readlines():
        #print(i)
    
        a.append(str(i))
    a = a[0].replace('[Ar]','(BBA)')  
    a = a.replace('[Kr]','(BBD)')
    if a[0:5] == '(BBA)' or a[0:5] == '(BBD)':
      #  str(a[0:5]), a[5] = a[5], str(a[0:5])
        a = a[5] + a[0:5] + a[6:] 
        #print(a)

    filename.close()

    return a

newstring = TheBBDBBAadder(path)
print(newstring)
filename = open(path,'w+')
filename.write(newstring)

   

