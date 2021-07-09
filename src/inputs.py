
import os
import subprocess


# Input smiles string
# Adds smiles string depending on if theres a BBA or BBD or both in the string
# Depending on whether there is a BBA or BBD place the file in the directory
name = input('What is name of chemdraw stucture without the Kr and Ar: ')
smile = input('What is the smile string from Chemdraw (Place Ar for electron acceptor connection and Kr for electron donor connection): ')
#inchlkey = input('Copy and paste the inchlkey with the Ar and Kr: ')
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
        #os.chdir('..')
        #print(len(os.listdir(os.getcwd())))
       # numoffiles = 0
       # for x in list(os.scandir('../eAcceptors')):
       #     if x.is_file():
       #         numoffiles += 1
       # os.chdir('eAcceptors/')
       # print(numoffiles)
      #  os.system('ls')
        x = 'acceptor'
        print('This structure is an acceptor')
      #  os.chdir('../../')

    elif 'BBD' in smi and 'BBA' not in smi:
      #  os.chdir('..')
      #  numoffiles = 0
      ##  for x in list(os.scandir('../eDonors')):
       #     if x.is_file():
       #         numoffiles += 1
    #    os.chdir('eDonors/')
      #  print(numoffiles)
        x = 'donor'
        print('This structure is an donor')
    #    os.chdir('../../')
    elif 'BBD' in smi and 'BBA' in smi:
   #    for x in list(os.scandir('../eDonors')):
   #         if x.is_file():
   #             numoffiles += 1
    #    os.chdir('eDonors/')
   #     print(numoffiles)
        print('This structure is an backbone') 
     #   os.chdir('../../')
        x = 'backbone'
    else:
        print('Error')
    return x
#typeofstruct()

def CreatesInchlKey(smile):
    filename = open('creator.smi','w+')
    filename.write(str(smile))
    filename.close()
    key = 'obabel creator.smi -oinchikey'
    carts = subprocess.check_output(key, shell=True)
        #subprocess.call(cmd, shell=True)
    carts = str(carts)
    
    l = []
    for i in carts:
        l.append(i)
    l.remove('b')
    l.remove("'")
    l.remove("'")
    l.remove('n')
    l.remove("\\")
    inchlkey = ''
    for i in l:
        inchlkey += str(i)
    os.remove('creator.smi')

    return inchlkey

def InchlKeyDicBackbone():
    InchlKeyBackboneDict = {}
    for h in os.listdir('../backbones/'):
        if '.smi' in h:
            with open('../backbones/'+str(h)) as f:
                data = f.readlines()[2].rstrip('\n')
                print(data)
                InchlKeyBackboneDict[data] = data
    return InchlKeyBackboneDict

def InchlKeyDicAcceptor():
    InchlKeyAcceptorDict = {}
    for h in os.listdir('../eAcceptors/'):
        if '.smi' in h:
            with open('../eAcceptors/'+str(h)) as f:
                data = f.readlines()[2].rstrip('\n')
                print(data)
                InchlKeyAcceptorDict[data] = data
    return InchlKeyAcceptorDict

def InchlKeyDicDonor():
    InchlKeyDonorsDict = {}
    for h in os.listdir('../eDonors/'):
        if '.smi' in h:
            with open('../eDonors/'+str(h)) as f:
                data = f.readlines()[2].rstrip('\n')
                print(data)
                InchlKeyDonorsDict[data] = data
    return InchlKeyDonorsDict
def inchlkeychecker():
    '''
    Checks whether the backbone,acceptor or donor has been made before 
    '''
    struct = typeofstruct()
    smi = arkysmiconv(smile)
    inchlkey = CreatesInchlKey(smile)
    if struct == 'backbone':
        BackboneDict = InchlKeyDicBackbone()
        if inchlkey in BackboneDict.keys():
            print('exists')
        elif inchlkey not in BackboneDict.keys():
            numoffiles = 0
            for x in list(os.scandir('../backbones')):
                if x.is_file():
                    numoffiles += 1
         #   os.chdir('Dyes/backbones/')
            filename = open('../backbones/' + str(numoffiles+1)+'b.smi','x+')
            filename.write(str(smi))
            filename.write('\n')
            filename.write(str(name))
            filename.write('\n')
            filename.write(str(inchlkey))
            filename.close()
        #    os.chdir('../../')
    if struct == 'acceptor':
        AcceptorDict = InchlKeyDicAcceptor()
        if inchlkey in AcceptorDict.keys():
            print('exists')
        elif inchlkey not in AcceptorDict.keys():
            numoffiles = 0
            for x in list(os.scandir('../eAcceptors')):
                if x.is_file():
                    numoffiles += 1
        #    os.chdir('Dyes/eAcceptors/')
            filename = open('../eAcceptors/' + str(numoffiles+1)+'ea.smi','x+')
            filename.write(str(smi))
            filename.write('\n')
            filename.write(str(name))
            filename.write('\n')
            filename.write(str(inchlkey))
            filename.close()
         #   os.chdir('../../')   
    if struct == 'donor':
        DonorDict = InchlKeyDicDonor()    
        if inchlkey in DonorDict.keys():
            print('exists')
        elif inchlkey not in DonorDict.keys():
            numoffiles = 0
            for x in list(os.scandir('../eDonors')):
                if x.is_file():
                    numoffiles += 1
        #    os.chdir('Dyes/eDonors/')
            filename = open('../eDonors/' +str(numoffiles+1)+'ed.smi','x+')
            filename.write(str(smi))
            filename.write('\n')
            filename.write(str(name))
            filename.write('\n')
            filename.write(str(inchlkey))
            filename.close()
       #     os.chdir('../../')           

    return
inchlkeychecker()










