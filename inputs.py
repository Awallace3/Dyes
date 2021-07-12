
import os
import subprocess


# Input smiles string
# Adds smiles string depending on if theres a BBA or BBD or both in the string
# Depending on whether there is a BBA or BBD place the file in the directory

#name = input('What is name of chemdraw stucture without the Kr and Ar: ')
#smile = input('What is the smile string from Chemdraw (Place Ar for electron acceptor connection and Kr for electron donor connection): ')
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
def typeofstruct(pa,pd,pb,smi):
    '''
    Places Smiles in file and inputs in correct directory
    '''
  #  smi = arkysmiconv(smile)
    print(smi)
    if 'BBA' in smi and 'BBD' not in smi:
       # print('acceptor')
        os.chdir('..')
        #print(len(os.listdir(os.getcwd())))
        numoffiles = 0
        for x in list(os.scandir(pa)):
            if x.is_file():
                numoffiles += 1
        os.chdir(pa)
        print(numoffiles)
        os.system('ls')
        x = 'acceptor'
        print('This structure is an acceptor')


    elif 'BBD' in smi and 'BBA' not in smi:
        numoffiles = 0
        for x in list(os.scandir(pd)):
            if x.is_file():
                numoffiles += 1
        os.chdir(pd)
        print(numoffiles)
        x = 'donor'
        print('This structure is an donor')
    elif 'BBD' in smi and 'BBA' in smi:
        numoffiles = 0
        for x in list(os.scandir(pb)):
            if x.is_file():
                numoffiles += 1
        os.chdir(pb)
        print(numoffiles)
        print('This structure is an backbone') 
        x = 'backbone'
    else:
        print('Error')
    return x
#typeofstruct()

def CreatesInchlKey(smile):
    print(smile)
    filename = open('creator.smi','w+')
    filename.write(str(smile))
    filename.close()
    key = 'obabel creator.smi -oinchikey'
    carts = subprocess.check_output(key, shell=True)
        #subprocess.call(cmd, shell=True)
    carts = str(carts)
    l = []
    for i in carts:
        #print(i)
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

def InchlKeyDicBackbone(pb):
    InchlKeyBackboneDict = {}
    for h in os.listdir(pb):
        if '.smi' in h:
            with open(pb+'/' + str(h)) as f:
                data = f.readlines()[2].rstrip('\n')
                #print(data)
                InchlKeyBackboneDict[data] = data
    return InchlKeyBackboneDict

def InchlKeyDicAcceptor(pa):
    InchlKeyAcceptorDict = {}
    for h in os.listdir(pa):
        if '.smi' in h:
            with open(pa+ '/' +str(h)) as f:
            #    print(f)
               # data = f.readlines()[2].rstrip('\n')
                data = f.readlines()
                smiles = data[0].rstrip('\n')
                key = data[2].rstrip('\n')
                
             #   data = f.readlines()
              #  print(data[2])
                InchlKeyAcceptorDict[key] = key
    return InchlKeyAcceptorDict

def InchlKeyDicDonor(pd):
    InchlKeyDonorsDict = {}
    for h in os.listdir(pd):
        if '.smi' in h:
            with open(pd+'/' + str(h)) as f:
                data = f.readlines()[2].rstrip('\n')
                #print(data)
                InchlKeyDonorsDict[data] = data
    return InchlKeyDonorsDict
def inchlkeychecker(pb,pa,pd,struct,smi,bb,aa,dd,inchlkey,name):
    '''
    Checks whether the backbone,acceptor or donor has been made before 
    '''
    if struct == 'backbone':
        BackboneDict = bb
        if inchlkey in BackboneDict.keys():
            for i in BackboneDict.keys():
                print(i)
            print('exists')
        elif inchlkey not in BackboneDict.keys():
            for i in BackboneDict.keys():
                print(i)
            numoffiles = 0
            for x in list(os.scandir(pb)):
                if x.is_file():
                    numoffiles += 1
            os.chdir(pb)
            filename = open(str(numoffiles+1)+'b.smi','x+')
            filename.write(str(smi))
            filename.write('\n')
            filename.write(str(name))
            filename.write('\n')
            filename.write(str(inchlkey))
            filename.close()
            
    if struct == 'acceptor':
        AcceptorDict = aa
        if inchlkey in AcceptorDict.keys():
            for i in AcceptorDict.keys():
                print(i)

            print('exists')
        elif inchlkey not in AcceptorDict.keys():
            for i in AcceptorDict.keys():
                print(i)
            numoffiles = 0
            for x in list(os.scandir(pa)):
                if x.is_file():
                    numoffiles += 1
            os.chdir(pa)
            filename = open(str(numoffiles+1)+'ea.smi','x+')
            filename.write(str(smi))
            filename.write('\n')
            filename.write(str(name))
            filename.write('\n')
            filename.write(str(inchlkey))
            filename.close()
  
    if struct == 'donor':
        DonorDict = dd    
        if inchlkey in DonorDict.keys():
            for i in DonorDict.keys():
                print(i)
            print('exists')
        elif inchlkey not in DonorDict.keys():
            for i in DonorDict.keys():
                print(i)
            numoffiles = 0
            for x in list(os.scandir(pd)):
                if x.is_file():
                    numoffiles += 1
            os.chdir(pd)
            filename = open(str(numoffiles+1)+'ed.smi','x+')
            filename.write(str(smi))
            filename.write('\n')
            filename.write(str(name))
            filename.write('\n')
            filename.write(str(inchlkey))
            filename.close()
         

    return



def main():
    path_to_acceptors = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/eAcceptors'
    path_to_donors = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/eDonors'
    path_to_backbone = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/backbones'
    name = input('What is name of chemdraw stucture without the Kr and Ar: ')
  #  name = 'ffff'
    smile = input('What is the smile string from Chemdraw (Place Ar for electron acceptor connection and Kr for electron donor connection): ')
  #  smile = 'CCC[Kr]CCC[Ar]'
    inchlkey = CreatesInchlKey(smile)
    smi = arkysmiconv(smile)
    struct = typeofstruct(path_to_acceptors,path_to_donors,path_to_backbone,smi)
    inchlkeychecker(path_to_backbone,path_to_acceptors,path_to_donors,struct,smi,InchlKeyDicBackbone(path_to_backbone),InchlKeyDicAcceptor(path_to_acceptors),InchlKeyDicDonor(path_to_donors),CreatesInchlKey(smile),name)
    

    return

main()










