
import os


# Input smiles string
# Adds smiles string depending on if theres a BBA or BBD or both in the string
# Depending on whether there is a BBA or BBD place the file in the directory
name = input('What is name of chemdraw stucture without the Kr and Ar: ')
smile = input('What is the smile string from Chemdraw (Place Ar for electron acceptor connection and Kr for electron donor connection): ')
inchlkey = input('Copy and paste the inchlkey with the Ar and Kr: ')
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

def inchlkeychecker():
    '''
    use results.json to figure out if inchlkeys are different

    '''
    


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
        filename.write('\n')
        filename.write(str(name))
        filename.write('\n')
        filename.write(str(inchlkey))
        os.system('ls')
        x = 'acceptor'
        print('This structure is an acceptor')
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
        filename.write('\n')
        filename.write(str(name))
        filename.write('\n')
        filename.write(str(inchlkey))
        os.system('ls')
        x = 'donor'
        print('This structure is an donor')
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
        filename.write('\n')
        filename.write(str(name))
        filename.write('\n')
        filename.write(str(inchlkey))
        os.system('ls')
        print('This structure is an backbone') 
        filename.close()
        os.chdir('../../')
        x = 'backbone'
    else:
        print('Error')
    return x
typeofstruct()


def checkifsamefile():
    #reads the 
    os.system('ls')

    return
checkifsamefile()




