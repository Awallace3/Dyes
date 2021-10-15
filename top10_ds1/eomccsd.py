import os

# dipole moment for dummy atom
# insert dummy atom into the xyz coords
# generate input file
# generate pbs file
# runscript



#path_to_exc_calcs = '/Users/tsantaloci/Desktop/PAHcode/CNCN/apvdz/EOM/apvDZ+8s6p2d/1Naph'


def grabxyz(filename,num):
    #print(str(filename))
    with open(str(filename) + '/' + 'mexc' + '/' + 'mexc'+ '.com') as file:
        data = file.readlines()
        optxyz = data[5:]
    return optxyz

def atom_num_to_letter(xyz):
    '''
    only works for atom numbers in single digits 

    '''
    #print(xyz[0])
    xyz2 = []
    for i in xyz:
        #i = i.strip('  ')
    #    i = str(i[6:9])
        
        
       
        a = i[6:9]
        #print(a)
        
        if a == ' 7 ':
            a = a.replace(a,'N') 
        if a == ' 6 ':
            a = a.replace(a,'C')
        if a == ' 8 ':
            a = a.replace(a,'O')
        if a == ' 1 ':
            a = a.replace(a,'H')
        if a == ' 16 ':
            a = a.replace(a,'S')

        #print(a)
        letxyz = a + i[10:]
        xyz2.append(letxyz)
        #print(letxyz)



           # print(i)
       # if i == 7:
       #     print(i)
    return xyz2

def inputcreator(xyz,num):
    #print(filename)
    filename = open(str(num) + '.com','w+')
    filename.write('***, PES for several lowest states of hydrogen fluoride\n')
    filename.write('memory,1500,m\n')
    filename.write('basis={default=avdz}\n')
#    filename.write('s,He,0.0252600,0.0062100,0.0015267,0.0003753,0.0000923,0.0000227,0.00000518,0.00000124;;\n')
#    filename.write('p,He,0.1020000,0.0268000,0.0070416,0.0018502,0.0004861,0.0001277,0.0000335,0.0000088;\n')
#    filename.write('d,He,0.2470000,0.0577000,0.0134789;\n}\n')

    filename.write('gthresh,compress=1.d-9\n')
    filename.write('geomtyp=xyz\n')
    filename.write('geometry={\n')
    xyz.pop(0)
    for i in xyz:
        filename.write(str(i))
    filename.write('}\n')
    filename.write('\n')
 #   filename.write('dummy,He\n')
    filename.write('hf,orbprint=75,maxit=100;wf,charge=0,spin=1;accu,20\n')
    filename.write('orbital,ignore_error;\n')
    filename.write('{ccsd,NOCHECK\n')
    filename.write('orbital,IGNORE_ERROR\n')
    filename.write('dm,5600.2 \n')
    filename.write('expec,qm \n')
    filename.write('eom,2.1,trans=1} \n')
    filename.write('\n')
    

    return


def excpbsfilecreator(cluster,smiles):
    '''
    creates pbs scripts
    '''
    
        
    outName =  str(smiles)
    mem_pbs_opt ='10'
    baseName = str(smiles)
    output_num = ''
    i = str(smiles)

    if cluster == 'seq':
        with open('%s.pbs' % (smiles), 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
            fp.write('\n')
            fp.write('module load intel\n')
            fp.write('module load mpt\n')
            fp.write('export PATH=/ptmp/bwhopkin/molpro_mpt/2012/molprop_2012_1_Linux_x86_64_i8/bin:$PATH\n')
            fp.write('\n')
            fp.write('export WORKDIR=$PBS_O_WORKDIR\n')
            fp.write('export TMPDIR=/tmp/$USER/$PBS_JOBID\n')
            fp.write('cd $WORKDIR\n')
            fp.write('mkdir -p $TMPDIR\n')
            fp.write('\n')
            fp.write('#process $PBS_NODEFILE to create the mpd.hosts file and start the MPD ring.\n')
            fp.write('\n')
            fp.write('#setenv NCPUS_TOTAL  `cat $PBS_NODEFILE | wc -l`\n')
            fp.write('#perl /usr/local/apps/bin/make_mpdhosts.pl $NCPUS_TOTAL $PBS_NODEFILE\n')
            fp.write('#setenv NODES  `cat mpd.hosts | wc -l`\n')
            fp.write('#echo $NODES\n')
            fp.write('#mpdboot -n $NODES\n')
            fp.write('\n')
            fp.write('date\n')
            fp.write("mpiexec molpro.exe %s.com \n" % (baseName))
            fp.write('date\n')
            fp.write('\n')
            fp.write('#mpdallexit\n')
            fp.write('\n')
            fp.write('rm -rf $TMPDIR\n')

    elif cluster == 'map':
        with open('%s.pbs' % (smiles), 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            # r410 node
            fp.write("#PBS -q r410\n")
            fp.write('\n')
            fp.write('module load pbspro molpro\n')
            fp.write('\n')
            fp.write('export WORKDIR=$PBS_O_WORKDIR\n')
            fp.write('export TMPDIR=/tmp/$USER/$PBS_JOBID\n')
            fp.write('mkdir -p $TMPDIR\n')
            fp.write('\n')
            fp.write('cd $WORKDIR\n')
            fp.write('\n')
            fp.write('date\n')
            fp.write('hostname\n')
            fp.write('molpro -t 4 ' + str(baseName) + '.com\n')
            fp.write('date\n')
            fp.write('\n')
            fp.write('rm -rf $TMPDIR\n')
            fp.write('\n')



    return

def runjobs(name,number):
    os.chdir(name)
    print(number)
    os.chdir(str(number) + '/')
    os.system('qsub ' + str(number) + '.pbs')
    os.chdir('../')  
    return    

def Main():
    path_to_codeworkspace = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/'
    os.chdir(path_to_codeworkspace)
    os.mkdir('TopDyesEOM')
  
    
    path_to_xyz = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/top10_ds1'
    path_to_EOMCCSD = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/top10_ds1'
    os.chdir(str(path_to_EOMCCSD))
    leftoverdirect = ['3ed_16b_4ea','6ed_16b_1ea','6ed_16b_7ea','6ed_16b_6ea','6ed_16b_10ea','6ed_16b_9ea','3ed_16b_7ea','6ed_16b_11ea', '6ed_16b_2ea','3ed_16b_1ea']
    for smiles in leftoverdirect:
        try:
            os.mkdir(smiles)
            os.chdir(smiles) 
            os.mkdir('EOMCCSD')
        except FileExistsError:
      
            os.chdir(smiles)
         #   os.mkdir('EOMCCSD')
    for l in leftoverdirect:
        os.chdir('EOMCCSD')
        excpbsfilecreator('map','mexc')
        xyzcoords = grabxyz(path_to_xyz+'/'+str(l),'mexc')
        inputcreator(xyzcoords,'mexc')
        runjobs(str(i) + '/' + 'mexc','mexc')


    
    return
Main()


