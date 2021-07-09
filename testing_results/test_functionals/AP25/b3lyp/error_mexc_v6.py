import numpy as np
import os
import math
import random
from numpy import genfromtxt
import numpy as npimport 
from numpy import genfromtxt
import pandas as pd
#import re
import glob


def Convert(string): 
        li = list(string.split(" "))
        return li 

def conv_num(string): 
    li = list(string.split(" ")) 
    return li 

def clean_many_txt():

    """ This will replace the numerical forms of the elements as their letters numbered in order """

    f = open('tmp.txt','r')
    a = ['6.0 ', '8.0 ', '1.0 ','7.0 ']
    table = {
        '6.0 ': 'C', '8.0 ' : 'O', '1.0 ': 'H', '7.0 ':'N'
    }

    lst = []
    cnt2 = 0
    for line in f:
        cnt2 += 1
        for word in a: 
            if word in line:
                convert_wrd = table[word]
                line = line.replace(word, convert_wrd + str(cnt2) + " ")
                print(line[:-2])
                
        lst.append(line)
    f.close()
    f = open('tmp.txt','w')
    for line in lst:
        f.write(line)
    f.close()

def freq_hf_zero(lines):
    frequency = "Frequencies --"
    freqs = []
    HF = "HF="
    HFs = []
    zero_point = " Zero-point correction="
    zeros = []
    freq_start = 0
    with open(filename) as search:
        for num, line in enumerate(search,1):

            if frequency in line:
                freqs.append(line)
                if len(freqs) == 1:
                    freq_start = num + 5

            if HF in line:
                start = 'HF='
                #end = '\RMSD='
                #a = re.search(r'\b(HF=)\b', line)
                index = line.index(start)

                

                HFs.append(line[index:])
            

            if zero_point in line:
                zeros.append(line)
    imag_freq = [False, False, False]
    if len(freqs) >= 1:
        vals = (freqs[0][15:])
        vals = vals.strip()
        for i in range(4):
            vals = vals.replace('  ', ' ')
        vals = vals.split()
        for num, i in enumerate(vals):
            vals[num] = float(i)
        #print(vals)
        
        for i in range(len(vals)):
            if vals[i] < 0:
                imag_freq[i] = True
        if vals[0] < 0:

            print('\n', imag_freq)


    if len(HFs) == 1:
         return freqs[0], HFs[0],0, zeros[0] , imag_freq, freq_start
    else:
         return freqs[0], HFs[0], HFs[1], zeros[0], imag_freq, freq_start


def find_geom(lines, imag_freq=[False], freq_start=0, error=False):

    if error==True:
        pop_2 = "Population analysis using the SCF Density."
        pops = []
        pop_2_test = False
        with open(filename) as search:
            for  line in search:
                if pop_2 in line:
                    pops.append(1)
                if len(pops) == 2:
                    pop_2_test = True
        if pop_2_test == True:

            with open(filename) as search:
                for num, line in enumerate(search,1):
                    if geom_start in line:
                        standards.append(num + 5)


            geom_end_pops = " Rotational constants (GHZ):"
            with open(filename) as search:
                for num, line in enumerate(search,1):
                    if geom_end_pops in line:
                        orientation.append(num - 1)
        else:

            with open(filename) as search:
                for num, line in enumerate(search,1):
                    if geom_start in line:
                        standards.append(num + 5)


            

            with open(filename) as search:
                for num, line in enumerate(search,1):
                    if geom_end in line:
                        orientation.append(num - 2)

    else:

        with open(filename) as search:
            for num, line in enumerate(search,1):
                if geom_start in line:
                    standards.append(num + 5)


        

        with open(filename) as search:
            for num, line in enumerate(search,1):
                if geom_end in line:
                    orientation.append(num - 2)
    
    
    length = orientation[-1] - standards[-1]

    freqs = lines[:]
    

    del lines[standards[-1] -1 + length:]
    del lines[:standards[-1] - 1]

    for i in range(1, 10, 1):
        k = "  " * i
        lines = [item.replace(k, " ") for item in lines]

    

    
    start_ls = []
    for i in lines:
        #i = i.strip()
        i = i.rstrip()
        k = Convert(i)
        start_ls.append(k)


    start_array = np.array(start_ls)
    new_geom = np.zeros(((int(len(start_array[:,3]))), 4))
    
    del freqs[freq_start + length -1:]
    del freqs[:freq_start -1]
    #print(freq_start, 'yes')
    #print(freqs)
    new_geom[:, 0] = start_array[:, 5]
    new_geom[:, 1] = start_array[:, 9]
    new_geom[:, 2] = start_array[:, 11]
    new_geom[:, 3] = start_array[:, 13]

    if imag_freq[0] == True:
        freqs_lst = []
        for n, i in enumerate(freqs):
            i = i.rstrip()
            for j in range(4):
                for l in i:
                    i = i.replace('  ', ' ')
            k = Convert(i)

            freqs_lst.append(k[1:])
        freqs_lst = [[float(y) for y in x] for x in freqs_lst]
        freqs_lst = np.array(freqs_lst)




        for num, imaginary in enumerate(imag_freq):
            if imaginary == True:
                tmp_array = freqs_lst[:,2+3*num:5+3*num]
                b = np.zeros((length, 1))
                tmp_array = np.hstack((b,tmp_array))
                final_geom = np.add(new_geom, tmp_array)

        final_geom = np.around(final_geom, decimals=8)
    else:
        final_geom = new_geom

    out_file = "tmp.txt"

    np.savetxt(out_file, final_geom,
    fmt="%s")

    clean_many_txt()
    

def make_input_files_no_constraints(output_num):
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """

    data = "" 
    
    with open('tmp.txt') as fp: 
        data = fp.read() 
    
    # Reading data from file2 
    charges = "0 1"

    
    with open ('mex.com', 'w') as fp: 
        fp.write("%mem=1600mb\n")
        fp.write("%nprocs=4\n")
        fp.write("#N wB97XD/6-31G(d) OPT FREQ\n")
        fp.write("\n")
        fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data) 
        fp.write("\n")

    with open ('mex.pbs', 'w') as fp: 
        fp.write("#!/bin/sh\n")
        fp.write("#PBS -N mex\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
        fp.write("mem=15gb\n")
        fp.write("#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
        fp.write("mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
        fp.write("""echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
        fp.write("then\n")
        fp.write("  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
        fp.write("""  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
        fp.write("    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
        fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
        fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write("cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out" + str(output_num) + "\n\nrm -r $scrdir\n")


def make_mexc():
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """

    data = "" 
    
    with open('tmp.txt') as fp: 
        data = fp.read() 
    
    # Reading data from file2 
    charges = "0 1"

    new_dir = "mexc"
    os.mkdir(new_dir)

    with open (new_dir + '/mexc.com', 'w') as fp: 
        fp.write("%mem=1600mb\n")
        fp.write("%nprocs=4\n")
        fp.write("#N TD(NStates=25) B3lYP/6-311G(d,p)\n")
        fp.write("\n")
        fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)
        fp.write("\n") 

    with open (new_dir + '/mexc.pbs', 'w') as fp: 
        fp.write("#!/bin/sh\n")
        fp.write("#PBS -N mexc\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
        fp.write("mem=15gb\n")
        fp.write("#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
        fp.write("mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
        fp.write("""echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
        fp.write("then\n")
        fp.write("  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
        fp.write("""  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
        fp.write("    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
        fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
        fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write("cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mexc.com mexc.out\n\nrm -r $scrdir\n")



out_files = glob.glob("*.out*")



filename = out_files[-1]

output_num = list(filename)
output_num = output_num[-1]

if output_num == "t":
    output_num = 2
else:
    output_num = int(output_num[-1]) + 1


print("Input file: " + filename)
f=open(filename,'r')
lines = f.readlines()
f.close() 



word_error = "Error"
geom_start = "Standard orientation:"

geom_end = " Standard basis:"

error = False


standards = []
orientation = []

with open(filename) as search:
    for num, line in enumerate(search,1):
        if word_error in line:
            error = True

if error == True:
    find_geom(lines, error=True)
    make_input_files_no_constraints(output_num)
    os.system("qsub mex.pbs")
    
else:
    freq, hf_1, hf_2, zero_point, imag_freq, freq_start = freq_hf_zero(lines)
    find_geom(lines, imag_freq, freq_start)

    if imag_freq[0] == True:
        make_input_files_no_constraints(output_num)
        os.system("qsub mex.pbs")
    else:

        print("\n")
        print(freq)
        print(imag_freq)
        print(hf_1)
        print(hf_2)
        print(zero_point)
        make_mexc()
        os.chdir("mexc")
        os.system("qsub mexc.pbs")
        os.chdir("..")

os.remove("tmp.txt")




