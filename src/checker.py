
import os


# Input smiles string
# Adds smiles string depending on if theres a BBA or BBD or both in the string
# Depending on whether there is a BBA or BBD place the file in the directory

smile = input('What is the smile string from Chemdraw (Place Ar for electron acceptor connection and Kr for electron donor connection): ')
def arkysmiconv(smile):
    '''
    converts Ar and Kr to BBA and BBD
    '''
    a = smile
    #print(type(smile))
    a = a.replace('[Ar]','(BBA)')  
    a = a.replace('[Kr]','(BBD)')
    if a[0:5] == '(BBA)' or a[0:5] == '(BBD)':
        a = a[5] + a[0:5] + a[6:] 
        #print(a)
    #print(a)
    return a

def typeofstruct():
    '''
    Places Smiles in file and inputs in correct directory
    '''
    smi = arkysmiconv(smile)
    print(smi)
    if 'BBA' in smi and 'BBD' not in smi:
       # print('acceptor')
        os.chdir('..')
        #print(len(os.listdir(os.getcwd())))
        numoffiles = 0
        for x in list(os.scandir('eAcceptors')):
            if x.is_file():
                numoffiles += 1
        os.chdir('eAcceptors/')
        
        print(numoffiles)
        filename = open(str(numoffiles+1)+'ea.smi','x+')
        filename.write(str(smi))
        os.system('ls')
        x = 'acceptor'
        print('acceptor')
        filename.close()
        os.chdir('../../')

    elif 'BBD' in smi and 'BBA' not in smi:
        os.chdir('..')
        numoffiles = 0
        for x in list(os.scandir('eDonors')):
            if x.is_file():
                numoffiles += 1
        os.chdir('eDonors/')
        print(numoffiles)
        filename = open(str(numoffiles+1)+'ed.smi','x+')
        filename.write(str(smi))
        os.system('ls')
        x = 'donor'
        print('donor')
        filename.close()
        os.chdir('../../')
    elif 'BBD' in smi and 'BBA' in smi:
        os.chdir('..')
        #print(len(os.listdir(os.getcwd())))
        numoffiles = 0
        for x in list(os.scandir('backbones')):
            #print(x)
            if x.is_file():
                numoffiles += 1
        os.chdir('backbones/')
        print(numoffiles)
        filename = open(str(numoffiles+1)+'b.smi','x+')
        filename.write(str(smi))
        os.system('ls')
        print('backbone')
        filename.close()
        os.chdir('../../')
        x = 'backbone'
    else:
        print('Error')
    return x
typeofstruct()


def checkifsamefile():
    
    os.system('ls')

    return
checkifsamefile()




