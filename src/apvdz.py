import os
import pandas as pd

def checkifreadyfornextstep(path):
        os.chdir(path)
        os.system("grep -rl 'Normal termination' */*.out | xargs sed -i 's/Normal termination/Has been brought to apvdz/g'")
        return

def pbsfilecreator(cluster,types,typeofnaph,path,smiles):
    '''
    creates pbs scripts
    '''
    
    
    outName = str(types) +  typeofnaph  + str(smiles)
    mem_pbs_opt ='10'
    baseName = str(smiles)
    output_num = ''
    smiles = str(smiles)

    if cluster == 'seq':
        with open('%s/%s.pbs' % (path + '/' + smiles, smiles), 'w+') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
            fp.write("export g09root=/usr/local/apps/\n. $g09root/g09/bsd/g09.profile\n\n")
            fp.write("scrdir=/tmp/bnp.$PBS_JOBID\n\nmkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
            fp.write("printf 'exec_host = '\nhead -n 1 $PBS_NODEFILE\n\ncd $PBS_O_WORKDIR\n\n")
            fp.write("/usr/local/apps/bin/g09setup %s.com %s.out%s" % (baseName, baseName, output_num))
    elif cluster == 'map':
        with open('%s/%s.pbs' % (path + '/' + smiles, smiles), 'w+') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l" % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
                # r410 node
            fp.write("#PBS -q r410\n")
            fp.write(
                "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
            fp.write(
                "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
            fp.write(
                """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
            fp.write("then\n")
            fp.write(
                "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
            fp.write(
                """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
            fp.write(
                "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
            fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
            fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
            fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
            fp.write("cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 {0}.com {0}.out".format(baseName, baseName) +
                    str(output_num) + "\n\nrm -r $scrdir\n")

    return




def energydict(path,path_to_src):
    '''
    gather all the energies from the output files

    '''
    #totenergydict = {}
    totenergylist = []
    filnumber = []
    os.chdir(path)
    for i in os.listdir():
        print(i)

        with open(str(i) + '/' + str(i)+ '.out','r') as file:
            data = file.readlines()
                    #print(data)
                    
            for x in data:
                if 'Normal termination' in x :
                    iterenergy = []
                    for num in data:
                        if 'SCF Done' in num:
                                
                            iterenergy.append(num)
                                #  print((i,iterenergy[-1][23:23+21]))
                    #    print(i,iterenergy[-1][23:23+21])
                        # print(x)
                #print(len(iterenergy))
        #  print(iterenergy)
        
                    totenergylist.append(float(iterenergy[-1][23:23+21])*627.509) #kcal/mol
                    filnumber.append(i) 

    os.chdir(path_to_src)
    return filnumber, totenergylist
#print(energydict(smileweeder()))

def pandadataframe(path,filelist,energylist):
    d = {'filename': filelist, 'energy (kcal/mol)': energylist}
    df = pd.DataFrame(data=d).sort_values('energy (kcal/mol)')
    df.to_csv('energy.csv',index=False)
    with open('energy'+ '.csv','r') as file:
        data = file.readlines()
        data.pop(0)
        uptdata = []
        for i in data:
            i = i.replace(',',' ')
            uptdata.append(i)
        #print(uptdata)
        remainderdir = []
        for i in range(1,len(uptdata)):
            differ = float(uptdata[i-1][2:])-float(uptdata[i][2:])
            print(differ)
            remainderdir.append(int(uptdata[i-1][0:2]))
            if abs(differ) <= .0005:
                num = int(uptdata[i-1][0:2])
                print(str(num) + 'SAME')
               # print(str(uptdata[i-1][0:2]))
              #  for x in os.listdir(path + '/' + str(num)):
                    #print(str(uptdata[i-1][0:2]))
             #       os.remove(path +'/'+ str(num)  + '/' + x)
                    
             #   os.rmdir(path + '/'+ str(num))
        
      #  for abc in os.listdir(path):
      #      remainderdir.append(abc)
        #print(data)
             
    return remainderdir

#filelist, totalenergylist = energydict(path,smileweeder())
#pandadataframe(path,filelist, totalenergylist)
def xyzgrabber(name,path):
    print((path,'AAAAAAAAAA'))
    with open(path + '/' + str(name) + '/' + str(name) + '.out','r') as file:
        data =file.readlines()
        #print(data)

        #print(ycoord)
        total2 = []
        startgeom = []
        endgeom = []
        for num,line in enumerate(data):
            zcoord = data[num][33:]
            #print(zcoord)
            if 'Standard orientation' in line:
                startgeom.append(num)
            if '---------------------------------------------------------------------' in line:
                endgeom.append(num)

        xyzcoords = data[startgeom[-1]+5:endgeom[-1]]
      #  for i in xyzcoords:
      #      print(i)
     #   atomnum = int(amountofatoms)
     #   print(atomnum)
        
        #xyzcoords = data[standnum[-1]+5:standnum[-1]+atomnum+5]        
        for i in xyzcoords:
            a = i.replace('  0  ',' ')
            atom = a[10:20]
            xcoord = a[30:45]
            ycoord = a[43:56]
            zcoord = 0.0
            
        #    zcoord = 0.000
            total = atom + '   ' +  str(xcoord) +'   ' +  str(ycoord) + '   ' + str(zcoord)
           # print(total)
            total2.append(total)
        #    for i in total2:
        #        print(i)
        return total2

#def gatheroptxyzcoords(path,smiles):
#    atomnum = 0
#    with open(path +'/' + str(smiles) + '/' + str(smiles) + '.com') as file:
#        data = file.readlines()
#        atomnum = len(data[5:])-1


#    with open(path +'/' + str(smiles) + '/' + str(smiles) + '.out') as file:
   # with open(path + '/' + '0' + + '/' + '0' + '.out' ) as file:
#        data = file.readlines()
#        standnum = []
#        for num,i in enumerate(data):
#            if  'Standard orientation' in data[num]:
#                standnum.append(num)
#        print((atomnum,smiles))
#        minxyzguesscoords = data[standnum[-1]+5:standnum[-1]+atomnum+5] 
      #  print(minxyzguesscoords)   
      #  amountoflinesbelowstand = 6
        # print(data[abc[-1]-6][5:7])
      #  lastatomnum = int(data[abc[-1]-6][5:7])
      #  print(lastatomnum)
        
      #  minxyzguesscoords = data[abc[-1]-lastatomnum-amountoflinesabovepop:abc[-1]-amountoflinesabovepop]
 #       file.close()


 #   return minxyzguesscoords



def optmizedinputfile(Type,path,coords,smiles):
        #print(x)
    filename = open(path +'/' + str(smiles) + '/' + str(smiles) + '.com','w+')
    filename.write('#N B3LYP/aug-cc-pVDZ OPT \n')
    filename.write('\n')
    filename.write('2Naph\n')
    filename.write('\n')
    if Type == 'anion' or Type == 'Anion':
            ## If Anion -1 1 and if Radical 0 2
        filename.write('-1 1\n')
                #print(data)
    elif Type == 'radical' or Type == 'Radical':
        filename.write('0 2\n')

  #  filename.write('\n')
    for i in coords:
        
      #  i = i.replace('  0  ', ' ')
        print(i)
            #print(i[16:])
        filename.write(i)
        filename.write('\n')
    filename.write('\n')
    filename.close()
    #print(x)
    return
        
def runjobs(name,number):
  #  a = number
    os.chdir(name)
    os.chdir(str(number) + '/')
    os.system('qsub ' + str(number) + '.pbs')
    os.chdir('../')  
    return

def Main():
    nonfunctionalizedsmi = 'c1cccc2c1cccc2'
    types = ''
    basis = 'apvdz'
    onefunctional = ''
    otherfunctional = ''
    typeofnaph = ''
    #path = '../' + str(types) + '/' + str(basis) + '/' + typeofnaph 
    path_to_minao = '/Users/tsantaloci/Desktop/PAHcode/CNCN/minao/1Naph'
    path_to_apvdz = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/1Naph'
    path_to_src = '/Users/tsantaloci/Desktop/PAHcode/src'
    typeofcluster = 'seq'
    name = path_to_apvdz.split('/')
   # print(name)
    for i in name:
        i = i.upper()
    #    print(i)
        types = i
        if i == 'OHOH':
            onefunctional = 'O'
            otherfunctional = 'O'
        if i == 'C2HC2H':
            onefunctional = 'C#C'
            otherfunctional = 'C#C'
        if i == 'CNCN':
            onefunctional = 'C#N'
            otherfunctional = 'C#N'
        if i == 'CNC2H' or i == 'C2HCN':
            onefunctional = 'C#N'
            otherfunctional = 'C#C'
        if i == 'CNOH' or i == 'OHCN':
            onefunctional = 'C#N'
            otherfunctional = 'O'
        if i == 'C2HOH' or i == 'OHC2H':
            onefunctional = 'C#C'
            otherfunctional = 'O'
    for x in name:
        x = x.upper()
        if x == '1NAPH':
            typeofnaph = '1Naph/'
        if x == '2NAPH':
            typeofnaph = '2Naph/'

    
    #print(onefunctional)
    #print(otherfunctional)
    #print(types)
    #p

        #pbsfilecreator('map',path,smiles)
   # filelist, totalenergylist = energydict(path_to_minao,path_to_src)
   # print(len(smiles))
  #  leftoverdirect = pandadataframe(path_to_minao,filelist, totalenergylist)
    leftoverdirect = [0,1,2,3,4,5,6]
  #  checkifreadyfornextstep(path_to_minao)
    for smiles in leftoverdirect:
        try:
            coords = xyzgrabber(smiles,path_to_minao)
            print(coords)
            #coords = gatheroptxyzcoords(path_to_minao,smiles)
            #print(coords)
            os.mkdir(str(path_to_apvdz) + '/' + str(smiles))
            optmizedinputfile('anion',path_to_apvdz,coords,str(smiles))
            pbsfilecreator(typeofcluster,'','',path_to_apvdz,str(smiles))
            runjobs(path_to_apvdz,smiles)
        except FileExistsError:
            coords = xyzgrabber(smiles,path_to_minao)
            print(coords)
            optmizedinputfile('anion',path_to_apvdz,coords,str(smiles))
            pbsfilecreator(typeofcluster,'','',path_to_apvdz,str(smiles))
            #runjobs(path_to_apvdz,smiles)
            print('Directory exists already ' + str(smiles))
            runjobs(path_to_apvdz,smiles)
            pass
        






    return
Main()
