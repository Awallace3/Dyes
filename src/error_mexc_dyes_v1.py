import numpy as np
import os
import math
import random
from numpy import genfromtxt
import numpy as npimport
from numpy import genfromtxt
import pandas as pd
# import re
import glob
import subprocess
from molecule_json import Molecule
from molecule_json import MoleculeList

#CFOUR
"""
ZMAT
CNCN
6     -7.546561    1.280310    2.683097
6     -8.592842    0.800254    1.678459
6     -7.982348    0.250768    0.559527
6     -6.560027    0.312166    0.721275
16     -5.139569   -0.126570   -0.154442
6     -4.110677    0.497597    1.154165
6     -4.886064    1.009111    2.184047
6     -6.267212    0.903068    1.938473
1     -4.434723    1.436566    3.066072
6     -2.664740    0.421969    1.036834
6     -2.033004   -0.180668   -0.038723
6     -0.630861   -0.259925   -0.188264
6      0.271476    0.248550    0.727084
6     -0.325305    0.886039    1.870252
7      0.341718    1.432283    2.889414
16     -0.764611    2.009353    3.945696
7     -2.137532    1.584801    3.156203
6     -1.773595    0.971653    2.029089
6      1.727905    0.129793    0.534743
6      2.627700    1.127090    0.949407
6      3.989468    1.015240    0.716343
6      4.520458   -0.105162    0.056672
6      3.630876   -1.111584   -0.353867
6      2.271351   -0.992571   -0.114460
1      1.618590   -1.799849   -0.426000
1      4.012512   -1.990779   -0.857038
7      5.905965   -0.218076   -0.183178
6      6.541714   -1.490986   -0.162595
6      7.452277   -1.849593   -1.164607
6      8.080003   -3.087880   -1.142777
6      7.814461   -4.022365   -0.129081
6      6.902809   -3.649608    0.871239
6      6.281857   -2.406948    0.863770
1      5.595470   -2.138317    1.657746
1      6.698462   -4.333679    1.687379
6      8.431479   -5.372355   -0.123591
6      7.655440   -6.504999    0.184186
6      8.175336   -7.787662    0.179345
6      9.520917   -7.991698   -0.146516
6     10.322163   -6.890794   -0.449187
6      9.781010   -5.603663   -0.436548
8     10.630860   -4.567494   -0.772508
6     11.174607   -3.854858    0.341958
1     11.768846   -4.521873    0.977035
1     11.818644   -3.079567   -0.072520
1     10.385781   -3.390238    0.941552
1     11.366991   -6.989955   -0.708897
8      9.950727   -9.284025   -0.144623
6     11.303899   -9.547345   -0.489284
1     11.419341  -10.628514   -0.434744
1     11.531966   -9.209206   -1.506079
1     11.997205   -9.073730    0.214791
1      7.557214   -8.648199    0.402949
1      6.602998   -6.368378    0.405019
1      8.776499   -3.344012   -1.929784
1      7.660802   -1.152742   -1.967442
6      6.684190    0.938764   -0.477466
6      7.924033    1.137885    0.141914
6      8.692136    2.255911   -0.153082
6      8.251760    3.224345   -1.068286
6      7.002848    3.017724   -1.673254
6      6.234035    1.894297   -1.394612
1      5.276141    1.759105   -1.882366
1      6.622935    3.753594   -2.372990
6      9.074355    4.404066   -1.438322
6      9.741533    5.204812   -0.488005
6     10.490422    6.320690   -0.879745
6     10.589114    6.656541   -2.233187
6      9.938791    5.878317   -3.191525
6      9.200749    4.778553   -2.783035
1      8.714408    4.166883   -3.534234
1     10.032331    6.144342   -4.236502
8     11.299441    7.720324   -2.704903
6     11.985477    8.550716   -1.780708
1     12.745332    7.991399   -1.222891
1     12.473802    9.319260   -2.377619
1     11.294191    9.027627   -1.076442
1     10.986088    6.922385   -0.134488
8      9.602716    4.840751    0.820595
6     10.183472    5.647349    1.833286
1     11.275635    5.680701    1.748293
1      9.784755    6.667732    1.813423
1      9.912805    5.176009    2.776807
1      9.646101    2.386068    0.339831
1      8.285881    0.405206    0.853395
1      4.654626    1.802552    1.047713
1      2.255914    1.998856    1.468874
1     -0.252500   -0.727024   -1.089395
1     -2.635999   -0.614377   -0.828430
16     -9.123789   -0.305543   -0.605419
6    -10.469575    0.212829    0.424075
6     -9.994005    0.777274    1.599899
1    -10.653402    1.174492    2.359953
6    -11.846087    0.026495    0.002967
6    -12.911052    0.188287    0.914530
6    -14.220700    0.019765    0.513571
6    -14.553611   -0.327482   -0.814183
6    -13.488229   -0.495374   -1.724850
6    -12.178791   -0.320031   -1.325168
1    -11.391855   -0.441040   -2.060468
1    -13.683793   -0.758683   -2.755101
6    -15.951965   -0.484358   -1.128773
6    -16.598111   -0.801101   -2.284978
6    -15.969472   -1.065192   -3.530449
7    -15.544201   -1.294906   -4.583914
6    -18.103574   -0.878389   -2.242749
8    -18.738018   -0.672509   -1.243038
8    -18.723307   -1.195286   -3.399137
1    -18.087752   -1.332222   -4.115879
1    -16.637229   -0.323158   -0.300363
1    -15.018492    0.148074    1.237166
1    -12.704703    0.430789    1.949174
6     -7.637268    2.804247    2.911604
1     -7.558605    3.347206    1.967676
1     -8.589316    3.066421    3.381452
1     -6.831512    3.140233    3.569513
6     -7.660911    0.524229    4.024198
1     -7.602613   -0.555306    3.871714
1     -6.853024    0.819794    4.698782
1     -8.611489    0.752222    4.514437


*CFOUR(CHARGE=0,REFERENCE=RHF,SPHERICAL=ON,BASIS=AUG-PVDZ
LINDEP_TOL=7,LINEQ_CONV=7,SCF_CONV=6,SCF_MAXCYC=250
CALC=CC2,EXCITE=EOMEE,ESTATE_SYM=5
COORDS=CARTESIAN
FROZEN_CORE=ON,ABCDTYPE=AOBASIS
CONVERGENCE=7,MEMORY_SIZE=8,MEM_UNIT=GB)

###########PBS############

#!/bin/csh
#
#PBS -N 1NaphCNC2H0
#PBS -S /bin/csh
#PBS -j oe
#PBS -W umask=022
#PBS -l cput=2400:00:00
#PBS -l mem=9gb
#PBS -l nodes=1:ppn=2
#PBS -q gpu

cd $PBS_O_WORKDIR
setenv NUM $NCPUS
echo "$NUM cores requested in PBS file"
echo " "
source /ddn/home1/r1621/.tschrc
/ddn/home1/r1621/maple/bin/tempQC/bin/c4ext_old.sh 20


"""

def CFOUR_input_files(
    method, basis_set, 
    mem_ZMAT, mem_pbs, data, dir_name, cluster='map',
    baseName='mexc', 
 ):
    if cluster == 'map':
        with open('%s/ZMAT' % (dir_name), 'w') as fp:
            fp.write("%s\n" % (dir_name))
            fp.write(data)
            fp.write('\n\n')
            fp.write("*CFOUR(CHARGE=0,REFERENCE=RHF,SPHERICAL=ON,BASIS=%s\n" % basis_set)
            fp.write("LINDEP_TOL=7,LINEQ_CONV=7,SCF_CONV=6,SCF_MAXCYC=250\n")
            fp.write("CALC=%s,EXCITE=EOMEE,ESTATE_SYM=5\nCOORDS=CARTESIAN\n" % method) 
            fp.write("FROZEN_CORE=ON,ABCDTYPE=AOBASIS\nCONVERGENCE=7,MEMORY_SIZE=%s,MEM_UNIT=GB\n" % mem_ZMAT)
        with open('%s/%s.pbs' % (dir_name, baseName), 'w') as fp:
            fp.write("#!/bin/csh\n#\n#PBS -N %s\n" % baseName)
            fp.write("#PBS -S /bin/csh\n#PBS -j oe\n#PBS -W umask=022\n#PBS -l cput=2400:00:00\n#PBS -l mem=%sgb\n#PBS -l nodes=1:ppn=2\n#PBS -q gpu" % mem_pbs)
            fp.write('\n\ncd $PBS_O_WORKDIR\nsetenv NUM $NCPUS\necho "$NUM cores requested in PBS file"\necho " "\nsource /ddn/home1/r1621/.tschrc\n/ddn/home1/r1621/maple/bin/tempQC/bin/c4ext_old.sh 20')
    return

def gaussianInputFiles(output_num, method_opt, 
                    basis_set_opt, mem_com_opt, 
                    mem_pbs_opt, cluster, 
                    baseName='mexc', procedure='OPT',
                    data='', dir_name='', solvent='', 
                    outName='mexc_o'
                    ):
    # baseName = baseName.com / baseName.pbs / baseName.out
    # dir_name = directory name 
    output_num = str(output_num)
    if output_num == '0':
        output_num = ''

    if dir_name=='':
        dir_name=baseName
    
    if data == '':
        with open('tmp.txt') as fp:
            data = fp.read()

    # Reading data from file2
    charges = "0 1"

    if cluster == "map":
        with open('%s/%s.com' % (dir_name, baseName), 'w') as fp:
            fp.write("%mem={0}mb\n".format(mem_com_opt))
            fp.write("%nprocs=4\n")
            if solvent == '':
                #print('no solvent')
                fp.write("#N %s/%s %s" % (method_opt, basis_set_opt, procedure))
            else:
                #print(solvent, 'exists')
                fp.write("#N %s/%s %s %s" % (method_opt, basis_set_opt, procedure, solvent))

            fp.write("\n\n")
            fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open('%s/%s.pbs' % (dir_name, baseName), 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            # r410 node
            fp.write("#PBS -q r410\n")
            fp.write("#PBS -W umask=022\n")
            fp.write(
                "#PBS -l nodes=1:ppn=1\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
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
    elif cluster == 'seq':
        with open('%s/%s.com' % (dir_name, baseName), 'w') as fp:
            fp.write('%mem=8gb\n')
            if solvent == '':
                #print('no solvent')
                fp.write("#N %s/%s %s" % (method_opt, basis_set_opt, procedure))
            else:
                #print(solvent, 'exists')
                fp.write("#N %s/%s %s %s" % (method_opt, basis_set_opt, procedure, solvent))

            fp.write("\n\n")
            fp.write("Name \n")
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open('%s/%s.pbs' % (dir_name, baseName), 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -W umask=022\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l " % outName)
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
            fp.write("export g09root=/usr/local/apps/\n. $g09root/g09/bsd/g09.profile\n\n")
            fp.write("scrdir=/tmp/bnp.$PBS_JOBID\n\nmkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
            fp.write("printf 'exec_host = '\nhead -n 1 $PBS_NODEFILE\n\ncd $PBS_O_WORKDIR\n\n")
            fp.write("/usr/local/apps/bin/g09setup %s.com %s.out%s" % (baseName, baseName, output_num))



# from ice_analogs, but modified input files
def Convert(string):
    li = list(string.split(" "))
    return li

def cleanLine(line):
    aList = []
    cropped_line = line.rstrip()
    for i in range(2,10):
        k = ' ' * i
        cropped_line = cropped_line.replace(k, " ")
    cropped_line = cropped_line.split(" ")
    for i in cropped_line:
        if i == '':
            continue
        else: 
            aList.append(float(i))
    return aList

def conv_num(string):
    li = list(string.split(" "))
    return li


def clean_many_txt(geomDirName, xyzSmiles=True, numbered=True):
    """ This will replace the numerical forms of the elements as their letters numbered in order """

    f = open('tmp.txt', 'r')
    a = ['14.0 ','30.0 ' ,
            '16.0 ', '6.0 ', 
            '8.0 ', '1.0 ', 
            '7.0 ' 
        ]
    table = {
        '6.0 ': 'C', '8.0 ': 'O', 
        '1.0 ': 'H', '7.0 ': 'N', 
        '16.0 ': 'S', '30.0 ': 'Zn', 
        '14.0 ': 'Si'
    }

    xyzToMolLst = []
    lst = []
    cnt2 = 0
    for line in f:
        cnt2 += 1
        for word in a:
            if word in line:
                convert_wrd = table[word]
                line2 = line.replace(word, convert_wrd + " ")
                if numbered:
                    line = line.replace(word, convert_wrd + str(cnt2) + " ")
                else:
                    line = line.replace(word, convert_wrd + " ")

                

        lst.append(line)
        xyzToMolLst.append(line2)
    f.close()
    f = open('tmp.txt', 'w')
    length = 0
    for line in lst:
        f.write(line)
        length += 1
    f.close()
    if xyzSmiles:
        xyzToSmiles(length, xyzToMolLst, geomDirName)



def i_freq_check(filename):
    imaginary = False
    frequency = "Frequencies --"
    dif = 0
    freq_lst_len = []
    with open(filename) as search:

        freq_clean = []
        for num, line in enumerate(search):
            if frequency in line:
                freq_lst_len.append(num)
                freq_line = line[16:].split(" ")
                for k in freq_line:
                    k = k.rstrip()
                    try:
                        k = float(k)
                        # print(k)
                        if k < 0:
                            imaginary = True
                        freq_clean.append(k)
                    except:
                        pass
            if len(freq_lst_len) > 1:
                break
    try:
        freq_lst_len = [freq_lst_len[0]+5, freq_lst_len[1]-2]
    except:
        pass

    return imaginary, freq_clean, freq_lst_len


def add_imaginary(freq_clean, freq_lst_len, filename, geomDirName):
    # print(freq_clean)
    cnt = 0
    for k in freq_clean:
        if k < 0:
            cnt += 1
            if cnt > 2:
                break

    f = open(filename)
    lines = f.readlines()
    f.close()
    imag_values = lines[freq_lst_len[0]: freq_lst_len[1]]
    for num, i in enumerate(imag_values):
        i = i.replace("  ", " ")
        i = i.replace("  ", " ")
        i = i.replace("  ", " ")
        i = i.replace("\n", "")
        i = (i.split(" "))[3:3+cnt*3]
        for k in range(len(i)):
            i[k] = float(i[k])
        imag_values[num] = i
    # print(imag_values)
    carts = genfromtxt('tmp.txt')
    carts_no_atom = carts[:, 1:4]
    imag_values = np.array(imag_values)

    for i in range(len(imag_values[0, :]) // 3):
        carts_no_atom = np.add(carts_no_atom, imag_values[:, i: i+4])
    # print(carts_no_atom)
    carts[:, 1:4] = carts_no_atom

    carts = np.around(carts, 6)
    """    carts = carts.astype(str)
        carts = carts.tolist() """
    np.savetxt("tmp.txt", carts,
               fmt="%s")

    clean_many_txt(geomDirName)

def freq_hf_zero(lines, filename):
    frequency = "Frequencies --"
    freqs = []
    HF = "HF="
    HFs = []
    zero_point = " Zero-point correction="
    zeros = []

    with open(filename) as search:
        for num, line in enumerate(search, 1):

            if frequency in line:
                freqs.append(line)

            if HF in line:
                start = 'HF='
                index = line.index(start)
                HFs.append(line[index:])

            if zero_point in line:
                zeros.append(line)
    print("hf", HFs, 'freqs', freqs, 'zeros', zeros)
    if len(freqs) == 0 and len(zeros) == 0:
        freqs.append("0")
        zeros.append(" (Hartree/Particle)0")
    if len(HFs) == 1:
        return freqs[0], HFs[0], 0, zeros[0]
    else:
        return freqs[0], HFs[0], HFs[1], zeros[0]


def find_geom(lines, error, filename, imaginary, geomDirName,
    xyzSmiles=True, numberedClean=True
):
    print("Opening..." + filename)
    found = False
    geom_size = 0
    geom_list = []
    with open(filename) as search:
        for num, line in enumerate(search, 1):
            if " Charge =  0 Multiplicity = 1" in line:
                geom_size = num + 1
                found = True
            elif found == True and num < geom_size + 200:
                #print(line, end="")
                geom_list.append(line)
            elif found == True and line == ' \n':
                #geom_size = num - geom_size
                break
    clean_geom_size = []
    for i in geom_list:
        if not " \n" == i:
            clean_geom_size.append(i)
        elif i == ' \n':
            break
    geom_size = len(clean_geom_size)
    if error == True:
        print("Error == True")
        pop_2 = "Population analysis using the SCF Density."
        pops = []
        pop_2_test = False
        with open(filename) as search:
            for line in search:
                if pop_2 in line:
                    pops.append(1)
                if len(pops) == 2:
                    pop_2_test = True
        if pop_2_test == True:
            print(pop_2_test, "occuring")
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)

            geom_end_pops = " Rotational constants (GHZ):"
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end_pops in line:
                        orientation.append(num - 1)
            print("if")
        else:
            print('else')
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)
                        
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end in line:
                        orientation.append(num - 2)
    else:
        print("No error")

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if geom_start in line:
                    standards.append(num + 5)

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if geom_end in line:
                    orientation.append(num - 2)
    if len(orientation) < 6:
        orien = len(orientation)
    else:
        orien = 5
    if len(standards) < 6:
        stand = len(standards)
    else:
        stand = 5
    for i in range(-1, -orien, -1):
        for j in range(-1, -stand, -1):
            length = orientation[i] - standards[j]
            if length == geom_size:
                orien = i
                stand = j
                break
    if stand == 5:
        stand = -1
    del lines[standards[stand] - 1 + length:]
    del lines[:standards[stand] - 1]

    cleaned_lines = []
    for i in range(len(lines)):
        clean = cleanLine(lines[i])
        cleaned_lines.append(clean)

    start_array = np.array(cleaned_lines)
    new_geom = np.zeros(((int(len(start_array[:, 3]))), 4))
    new_geom[:, 0] = start_array[:, 1]
    new_geom[:, 1] = start_array[:, 3]
    new_geom[:, 2] = start_array[:, 4]
    new_geom[:, 3] = start_array[:, 5]

    out_file = "tmp.txt"
    np.savetxt(out_file, new_geom,
               fmt="%s")
    
    if not imaginary:
        clean_many_txt(geomDirName, xyzSmiles, numberedClean)
    elif error:
        clean_many_txt(geomDirName, xyzSmiles, numberedClean)
    
def xyzToSmiles(length, xyz, geomDirName):
    with open('molecule.xyz', 'w') as fp:
        fp.write('%s\ncharge=0=\n' % length)
        for n, i in enumerate(xyz):
            if n == len(xyz) -1:
                fp.write(i[:-2])
            else:
                fp.write(i)

    """
    cmd = 'python3 ../../src/xyz2mol.py ./molecule.xyz'

    val = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    os.remove('molecule.xyz')
    """
    print("\n\n")
    cmd = 'obabel -ixyz molecule.xyz -osmi -molecule.smi'
    err = subprocess.call(cmd, shell=True)
    with open('molecule.smi', 'r') as fp:
        val = fp.readlines()[0]
        val = val.split("charge")
        val = val[0].rstrip()
    print(val)

    mol = Molecule()
    if os.path.exists('info.json'):
        mol.setData('info.json')
        mol.setGeneralSMILES(val.rstrip())
        mol.sendToFile('info.json')
        mol_lst = MoleculeList()
        mol_lst.setData("../../results.json")
        mol_lst.updateMolecule(mol)
        #print(mol_lst)
        mol_lst.sendToFile('../../results.json')
    else:

        mol.setLocalName(geomDirName)
        mol.setGeneralSMILES(val.rstrip())
        mol.sendToFile('info.json')



def make_input_files_no_constraints(output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt, cluster):
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """
    data = ""
    with open('tmp.txt') as fp:
        data = fp.read()
    charges = "0 1"

    if cluster == "map":
        with open('mex.com', 'w') as fp:
            fp.write("%mem={0}mb\n".format(mem_com_opt))
            fp.write("%nprocs=4\n")
            fp.write("#N {0}".format(method_opt) +
                    "/{0} OPT\n".format(basis_set_opt))
            fp.write("\n")
            fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open('mex.pbs', 'w') as fp:
            fp.write("#!/bin/sh\n")
            fp.write("#PBS -N mex_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
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
            fp.write("cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out" +
                    str(output_num) + "\n\nrm -r $scrdir\n")
    elif cluster == 'seq':
        gaussianInputFiles(output_num, method_opt, 
                    basis_set_opt, mem_com_opt, 
                    mem_pbs_opt, cluster, 
                    baseName='mex', procedure='OPT' 
                    )

def qsub(path='.'):
    resetDirNum = len(path.split("/"))
    #print(resetDirNum)
    os.chdir(path)
    pbs_file = glob.glob("*.pbs")[0]
    cmd = 'qsub %s' % pbs_file
    print(os.getcwd(), "cmd", cmd)
    failure = subprocess.call(cmd, shell=True)
    if path != '.':
        for i in range(resetDirNum):
            #print('dir changed')
            os.chdir("..")


def make_exc_mo_freq(method_mexc, basis_set_mexc, 
                mem_com_mexc, mem_pbs_mexc, cluster,
                geomDirName
                ):
    
    #baseName = 'cam-b3lyp'
    if method_mexc == 'CAM-B3LYP':
        baseName = 'mexc'
        dir_name = 'mexc'
    else:
        baseName = 'mexc'
        dir_name = method_mexc.lower()
    if os.path.exists(dir_name):
        print('\n%s directory already exists\n' % (dir_name))
        return 
    os.mkdir(dir_name)
    procedure = 'TD(NStates=10)'
    output_num = 0
    #basis_set_mexc='CAM-B3LYP'

    #solvent = 'SCRF=(Solvent=Dichloromethane)'
    solvent=''
    outName = geomDirName 
    gaussianInputFiles(output_num, method_mexc, 
                    basis_set_mexc, mem_com_mexc, 
                    mem_pbs_mexc, cluster,
                    baseName=baseName, procedure=procedure,
                    data='', dir_name=dir_name, solvent='', 
                    outName=outName
                    )
    path = '%s' % dir_name
    qsub(path)
    """
    gaussianInputFiles(output_num, method_opt, 
                    basis_set_opt, mem_com_opt, 
                    mem_pbs_opt, cluster, 
                    baseName='mexc', procedure='OPT',
                    data='', dir_name='', solvent='', 
                    outName='mexc_o'
                    ):
    """
    
    """
    baseName = 'mexc'
    os.mkdir(baseName)
    procedure = 'TD(NStates=10)'
    output_num = 0
    gaussianInputFiles(output_num, method_mexc, 
                    basis_set_mexc, mem_com_mexc, 
                    mem_pbs_mexc, cluster,
                    baseName, procedure
                    )
    path = '%s' % baseName
    qsub(path)
    """
    """
    baseName = 'mo'
    os.mkdir(baseName)
    procedure = 'SP GFINPUT POP=FULL'
    output_num = 0
    gaussianInputFiles(output_num, method_mexc, 
                    basis_set_mexc, mem_com_mexc, 
                    mem_pbs_mexc, cluster,
                    baseName, procedure
                    )
    path = '%s' % baseName
    qsub(path)
    """
    """
    baseName = 'freq'
    os.mkdir(baseName)
    procedure = 'FREQ'
    output_num = 0
    gaussianInputFiles(output_num, method_mexc, 
                    basis_set_mexc, mem_com_mexc, 
                    mem_pbs_mexc, cluster,
                    baseName, procedure
                    )
    path = '%s' % baseName
    qsub(path)
    """

    
def clean_energies(hf_1, hf_2, zero_point):
    zero_point = zero_point[30:].replace(" (Hartree/Particle)", "")
    for i in range(10):
        zero_point = zero_point.replace("  ", " ")
    zero_point = float(zero_point)
    hf_1 = (hf_1[3:].replace("\n", "").split('\\'))

    if hf_2 != 0:
        hf_2 = (hf_2[3:].replace("\n", "").split('\\'))

        if hf_1[0] > hf_2[0]:
            return float(hf_1[0]) + zero_point
        else:
            return float(hf_2[0]) + zero_point
    else:
        return float(hf_1[0]) + zero_point


word_error = "Error"
geom_start = "Standard orientation:"

geom_end = " Standard basis:"
standards = []
orientation = []


def main(index,
         method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
         method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
         resubmissions, delay,
         cluster, geomDirName
         ):

    out_files = glob.glob("*.out*")
    out_completion = glob.glob("mex_o.*")
    print(out_files)
    if len(out_files) > 0:

        filename = out_files[-1]

        output_num = list(filename)
        output_num = output_num[-1]

        if output_num == "t":
            output_num = 2

        else:
            output_num = int(output_num[-1]) + 1
            if delay == 0:
                resubmissions[index] = output_num
        if len(out_completion) != len(out_files):
            print("Not finished yet")
            return True, resubmissions
        if resubmissions[index] > output_num:
            print("Awaiting queue")
            return True, resubmissions

        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        error = False

        imaginary, freq_clean, freq_lst_len = i_freq_check(filename)

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                if word_error in line:
                    error = True
        cmd = "qsub mex.pbs"
        if error == True:
            find_geom(lines, error=True, filename=filename,
                        imaginary=imaginary, geomDirName=geomDirName)
            make_input_files_no_constraints(
                output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt, cluster)
            os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            resubmissions[index] += 1
            return False, resubmissions

        elif imaginary == True:
            find_geom(lines, error=False, filename=filename,
                        imaginary=imaginary, geomDirName=geomDirName)
            add_imaginary(freq_clean, freq_lst_len, filename, geomDirName=geomDirName)

            make_input_files_no_constraints(
                output_num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt, cluster)
            os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            print('imaginary frequency handling...')
            resubmissions[index] += 1
            return False, resubmissions
        else:
            cmd = "qsub mexc.pbs"
            find_geom(lines, error=False, filename=filename,
                        imaginary=imaginary, geomDirName=geomDirName)
            '''
            freq, hf_1, hf_2, zero_point = freq_hf_zero(
                lines, filename=filename)
            '''
            print("entering make_exc_mo_freq")
            make_exc_mo_freq(method_mexc, basis_set_mexc, 
                            mem_com_mexc, mem_pbs_mexc, cluster,
                            geomDirName
                            )
            
            os.remove("tmp.txt")
            
            return False, resubmissions
        print('Calculation still running')
        return True, resubmissions
    else:
        print('No output files detected for geom%d' % (index+1))
        return True, resubmissions

# main()
