import os
from tkinter.font import names

def file_reader(file):
    '''
    reads csv file of the theoretical dyes that need to go through MO calculations. boxer.py creates the csv.
    '''
    names = []
    with open(file,'r') as fp:
        data = fp.readlines()
        for line in data:
            line = line.split(',')
            name = line[0]
            names.append(name)

    print(len(names))
    return names
def job_creater_file(list_name):
    '''
    creates a file that will be used as a queaing system
    '''
    with open('../queaforMO/quea','w') as fp:
        for name in list_name:
            fp.write(name+'\n')
    return

def file_manager(file):
    job_manager = []
    with open(file,'r') as fp:
        data = fp.readlines()
        for num,line in enumerate(data):
            if num > 1900:
                break
            else:
                job_manager.append(line.replace('\n',''))
    print(job_manager)



    return job_manager





def xyzgrabber(name,path):
    #print(path)
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

def MO(smiles,coords):
    filename = open(str(smiles) + '.com','w+')
    filename.write('%mem=8gb\n')
    filename.write('#N PBE1PBE/6-311G(d,p) SP GFINPUT POP=FULL\n')
    filename.write('\n')
    filename.write('2Naph\n')
    filename.write('\n')
    filename.write('0 1\n')
    for i in coords:
        filename.write(i)
    filename.write('\n')
    filename.close()

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
        with open('%s/%s.pbs' % ('mo', smiles), 'w+') as fp:
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
    os.chdir(name)
    #os.system('qsub ' + str(number) + '.pbs')
    os.chdir('../')
    return





def main():
    filename = '../data_analysis/g_800_1000.csv'
    path = '/ddn/home3/r2652/chem/Dyes/results_cp/ds_all5'
    path_2 =  '/ddn/home6/r2532/chem/Dyes_2/Dyes/MO_start_test'
    

    names = file_reader(filename)
    job_creater_file(names)
    jobs = file_manager('../queaforMO/quea')
    os.chdir(path)


    
    for i in jobs:
        print(i)
        xyz = xyzgrabber(str(i),str(i) + '/' + 'mex.out')
        print(xyz)
        os.chdir(path_2)
        os.mkdir(str(i))
        os.chdir(str(i))
        os.mkdir('mo')
        MO('mo'+ '/' + str(i),xyz)
        os.system('pwd')
        pbsfilecreator('map',str(i),'',str(i) +'/' + 'mo',str(i))
        runjobs(path_2 + '/' + str(i) +'/' + 'mo',str(i))
        os.chdir(path)
    







    return
main()