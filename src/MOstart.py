import os





def MO(smiles,coords):
    filename = open(str(smiles) + '.com','w+')
    filename.write('%mem=8gb\n')
    filename.write('#N CAM-B3LYP/6-311G(d,p) SP GFINPUT POP=FULL\n')
    filename.write('\n')
    filename.write('2Naph\n')
    filename.write('\n')
    filename.write('0 1\n')
    for i in coords:
        
      #  i = i.replace('  0  ', ' ')
        print(i)
            #print(i[16:])
        filename.write(i)
     #   filename.write('\n')
    filename.write('\n')
    filename.close()    

    return 


def xyzgrabber(name,path):
    print(path)
    with open(path,'r') as file:
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
    #    for i in a:
    #        print(i)
     #   atomnum = int(amountofatoms)
     #   print(atomnum)
        
        #xyzcoords = data[standnum[-1]+5:standnum[-1]+atomnum+5]        
        for i in xyzcoords:
            a = i.replace('  0  ',' ')
            atom = a[10:20]
            xcoord = a[30:45]
            ycoord = a[43:56]
            zcoord = a[57:67]
            
        #    zcoord = 0.000
            total = atom + '   ' +  str(xcoord) +'   ' +  str(ycoord) + '   ' + str(zcoord)
           # print(total)
            total2.append(total)

    
    return total2


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
        with open('%s/%s.pbs' % ('mo', smiles), 'w+') as fp:
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

def runjobs(name,number):
  #  a = number
    os.chdir(name)
    os.system('qsub ' + str(number) + '.pbs')
    os.chdir('../')  
    return




def main():
   # path = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark/results'
    path = '/ddn/home3/r2652/chem/Dyes/results'
    path_2 = '/ddn/home6/r2532/chem/Dyes/MOdyes_1' 
    os.chdir(path)
    #xyz = xyzgrabber('DQ5','DQ5/mex.out')
    #print(xyz)
  #  MO(path+'mo/'+str(i),xyz)
   # MO('/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark/results/DQ5/mo/DQ5',xyz)
  #  xyz = list(xyz)
  #  MO(str(i),xyz)
    leftoverdict = ['5ed_16b_4ea', '7ed_16b_5ea', '6ed_16b_4ea', '6ed_16b_5ea', '1ed_16b_4ea', '3ed_16b_5ea', '5ed_16b_5ea', '2ed_16b_4ea', '7ed_16b_4ea', '2ed_16b_5ea', '3ed_16b_4ea', '5ed_16b_1ea', '1ed_16b_5ea', '5ed_16b_9ea', '6ed_16b_1ea', '6ed_16b_7ea', '6ed_16b_6ea', '1ed_16b_1ea', '1ed_16b_9ea', '6ed_16b_10ea', '6ed_16b_9ea', '7ed_16b_1ea', '3ed_16b_7ea', '7ed_16b_6ea', '5ed_16b_10ea', '5ed_16b_6ea', '5ed_16b_11ea', '5ed_16b_7ea', '2ed_16b_1ea', '6ed_16b_11ea', '6ed_16b_2ea', '7ed_16b_9ea', '3ed_16b_1ea', '5ed_16b_3ea', '7ed_16b_11ea', '1ed_16b_6ea', '3ed_16b_6ea', '6ed_16b_3ea', '1ed_16b_11ea', '1ed_16b_10ea', '7ed_16b_10ea', '1ed_16b_7ea', '3ed_16b_10ea', '2ed_16b_6ea', '7ed_16b_7ea', '3ed_16b_9ea', '2ed_16b_10ea', '2ed_16b_9ea', '3ed_16b_11ea', '2ed_16b_11ea', '1ed_16b_8ea', '5ed_16b_8ea', '7ed_16b_2ea', '1ed_16b_3ea', '2ed_16b_2ea', '1ed_16b_2ea', '2ed_16b_7ea', '2ed_16b_3ea', '5ed_16b_2ea', '3ed_16b_2ea', '7ed_16b_3ea', '3ed_16b_3ea', '6ed_16b_8ea', '5ed_1b_4ea', '2ed_16b_8ea', '6ed_1b_4ea', '7ed_16b_8ea', '6ed_26b_8ea', '6ed_20b_4ea', '1ed_1b_4ea', '2ed_26b_9ea']

  #  for i in os.listdir():
    for i in leftoverdict:
    #    print(i)
        #print(i)
        try:
    #        os.system('pwd')
            xyz = xyzgrabber(str(i),str(i) + '/' + 'mex.out')
            os.chdir(path_2)
            os.mkdir(str(i))
            os.chdir(str(i))
            os.mkdir('mo')
        #   # print(i)
            MO('mo'+ '/' + str(i),xyz)
            pbsfilecreator('seq',str(i),'',path+'/'+ str(i) +'/' + 'mo',str(i))
            runjobs(path_2 + '/' + str(i) +'/' + 'mo',str(i))
            os.chdir(path)
        except FileExistsError:
            #print(i)
            xyz = xyzgrabber(str(i),'mex.out')
            MO('mo'+ '/' + str(i),xyz)
            pbsfilecreator('seq',str(i),'',path+'/'+ str(i) +'/' + 'mo',str(i))
            os.chdir(path)

          #  os.chdir(str(i))
        #    os.system('pwd')
    
       #     print(i)
       #     print('AAAAAAAAAAAAAAAAAAAAAAAA')
           # xyz = xyzgrabber(str(i), str(i) + '/' + 'mex.out')
       #     os.chdir(str(i))
       #     print(i)
           # MO(str(i),xyz)
       #     os.chdir(path)
            #os.system('pwd')
    return
main()


