import numpy as np
import os
import glob
import subprocess
# from molecule_json import Molecule
# from molecule_json import MoleculeList
from .molecule_json import Molecule
from .molecule_json import MoleculeList


def gaussianpbsFiles(
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    cluster,
    dir_name,
    baseName="mexc",
    outName="mexc_o",
):
    # baseName = baseName.com / baseName.pbs / baseName.out
    # dir_name = directory name
    if cluster == "map":
        with open("%s/%s.pbs" % (dir_name, baseName), "w") as fp:
            fp.write("#!/bin/sh\n")
            fp.write(
                "#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l "
                % outName.replace("-", "").replace(",", "_"))
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            # r410 node
            fp.write("#PBS -q r410\n")
            # fp.write("#PBS -q gpu\n")
            fp.write("#PBS -W umask=022\n")
            # fp.write("#PBS -l nodes=1:ppn=1\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
            fp.write(
                "#PBS -l nodes=1:ppn=1\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
            fp.write(
                "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
            )
            fp.write(
                """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n"""
            )
            fp.write("then\n")
            fp.write(
                "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n"
            )
            fp.write(
                """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n"""
            )
            fp.write(
                "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n"
            )
            fp.write(
                """  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n"""
            )
            fp.write(
                """    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n"""
            )
            fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
            fp.write(
                "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 {0}.com {0}.out"
                .format(baseName, baseName) + "\n\nrm -r $scrdir\n")

    elif cluster == "seq":
        with open("%s/%s.pbs" % (dir_name, baseName), "w") as fp:
            fp.write("#!/bin/sh\n")
            fp.write(
                "#PBS -N %s_o\n#PBS -S /bin/bash\n#PBS -W umask=022\n#PBS -j oe\n#PBS -m abe\n#PBS -l cput=1000:00:00\n#PBS -l "
                % outName.replace("-", "").replace(",", "_"))
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write("#PBS -l nodes=1:ppn=2\n#PBS -l file=100gb\n\n")
            fp.write(
                "export g09root=/usr/local/apps/\n. $g09root/g09/bsd/g09.profile\n\n"
            )
            fp.write(
                "scrdir=/tmp/bnp.$PBS_JOBID\n\nmkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
            )
            fp.write(
                "printf 'exec_host = '\nhead -n 1 $PBS_NODEFILE\n\ncd $PBS_O_WORKDIR\n\n"
            )
            fp.write("/usr/local/apps/bin/g09setup %s.com %s.out" %
                     (baseName, baseName))


def gaussianInputFiles(
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    cluster,
    baseName="mexc",
    procedure="OPT",
    data="",
    dir_name="",
    solvent="",
    outName="mexc_o",
):
    # baseName = baseName.com / baseName.pbs / baseName.out
    # dir_name = directory name
    if dir_name == "":
        dir_name = baseName

    if solvent != "":
        # dir_name += '_%s'%solve:qnt
        print(dir_name)
        solvent_line = "SCRF=(Solvent=%s)" % solvent
        print(dir_name)

    # Reading data from file2
    charges = "0 1"
    filename = open("%s/%s.com" % (dir_name, baseName), "r")
    read = filename.readlines()
    read[0] = "%mem={0}mb\n".format(mem_com_opt)
    read[1] = "%nprocs=4\n"
    if solvent == "":
        read[2] = ("#N %s/%s %s" % (method_opt, basis_set_opt, procedure) +
                   "\n")
    else:
        read[2] = ("#N %s/%s %s %s" %
                   (method_opt, basis_set_opt, procedure, solvent_line) + "\n")
    filename.close()
    filename = open("%s/%s.com" % (dir_name, baseName), "w")
    for i in read:
        filename.write(str(i))

    # with open('%s/%s.com' % (dir_name, baseName), 'w+') as fp:
    #    fp.wr
    #    fp.write("%mem={0}mb\n".format(mem_com_opt))
    #    fp.write("%nprocs=4\n")
    #    if solvent == '':
    #        fp.write("#N %s/%s %s" % (method_opt, basis_set_opt, procedure))
    #    else:
    #        fp.write("#N %s/%s %s %s" % (method_opt, basis_set_opt, procedure, solvent_line ))

    #    fp.write("\n\n")
    #    fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
    #    fp.write("\n")
    #    fp.write(charges + "\n")
    #  fp.write(data)
    #    fp.write("\n")


# from ice_analogs, but modified input files
def Convert(string):
    li = list(string.split(" "))
    return li


def cleanLine(line):
    aList = []
    cropped_line = line.rstrip()
    for i in range(2, 10):
        k = " " * i
        cropped_line = cropped_line.replace(k, " ")
    cropped_line = cropped_line.split(" ")
    for i in cropped_line:
        if i == "":
            continue
        else:
            aList.append(float(i))
    return aList


def conv_num(string):
    li = list(string.split(" "))
    return li


def clean_many_txt(geomDirName, xyzSmiles=True, numbered=True):
    """This will replace the numerical forms of the elements as their letters numbered in order"""

    f = open("tmp.txt", "r")
    """
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
    """
    a = [
        "14.000000 ",
        "30.000000 ",
        "16.000000 ",
        "6.000000 ",
        "8.000000 ",
        "1.000000 ",
        "7.000000 ",
        "35.000000",
    ]
    table = {
        "6.000000 ": "C",
        "8.000000 ": "O",
        "1.000000 ": "H",
        "7.000000 ": "N",
        "16.000000 ": "S",
        "30.000000 ": "Zn",
        "14.000000 ": "Si",
        "35.000000": "F",
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
    f = open("tmp.txt", "w")
    length = 0
    for line in lst:
        f.write(line)
        length += 1
    f.close()
    if xyzSmiles:
        xyzToSmiles(length, xyzToMolLst, geomDirName)


def find_geom(
    lines,
    error,
    filename,
    imaginary,
    geomDirName,
    xyzSmiles=True,
    numberedClean=True,
):
    found = False
    geom_size = 0
    geom_list = []
    with open(filename) as search:
        for num, line in enumerate(search, 1):
            if " Charge =  0 Multiplicity = 1" in line:
                geom_size = num + 1
                found = True
            elif found == True and num < geom_size + 200:
                geom_list.append(line)
            elif found == True and line == " \n":
                # geom_size = num - geom_size
                break
    clean_geom_size = []
    for i in geom_list:
        if not " \n" == i:
            clean_geom_size.append(i)
        elif i == " \n":
            break
    geom_size = len(clean_geom_size)
    if error == True:
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
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)

            geom_end_pops = " Rotational constants (GHZ):"
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end_pops in line:
                        orientation.append(num - 1)
        else:
            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_start in line:
                        standards.append(num + 5)

            with open(filename) as search:
                for num, line in enumerate(search, 1):
                    if geom_end in line:
                        orientation.append(num - 2)
    else:

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
    np.savetxt(out_file, new_geom, fmt="%f")

    if not imaginary:
        clean_many_txt(geomDirName, xyzSmiles, numberedClean)
    elif error:
        clean_many_txt(geomDirName, xyzSmiles, numberedClean)


def xyzToSmiles(length, xyz, geomDirName):
    with open("molecule.xyz", "w") as fp:
        fp.write("%s\ncharge=0=\n" % length)
        for n, i in enumerate(xyz):
            if n == len(xyz) - 1:
                fp.write(i[:-2])
            else:
                fp.write(i)
    """
    cmd = 'python3 ../../src/xyz2mol.py ./molecule.xyz'

    val = subprocess.check_output(cmd, shell=True).decode("utf-8")

    os.remove('molecule.xyz')
    """
    cmd = "obabel -ixyz molecule.xyz -osmi -molecule.smi"
    err = subprocess.call(cmd, shell=True)
    with open("molecule.smi", "r") as fp:
        val = fp.readlines()[0]
        val = val.split("charge")
        val = val[0].rstrip()

    mol = Molecule()
    if os.path.exists("info.json"):
        mol.setData("info.json")
        mol.setGeneralSMILES(val.rstrip())
        mol.sendToFile("info.json")
        mol_lst = MoleculeList()
        mol_lst.setData("../../results.json")
        mol_lst.updateMolecule(mol)
        mol_lst.sendToFile("../../results.json")
    else:

        mol.setLocalName(geomDirName)
        mol.setGeneralSMILES(val.rstrip())
        mol.sendToFile("info.json")


def make_input_files_no_constraints(output_num, method_opt, basis_set_opt,
                                    mem_com_opt, mem_pbs_opt, cluster):
    """Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory"""
    data = ""
    with open("tmp.txt") as fp:
        data = fp.read()
    charges = "0 1"

    if cluster == "map":
        with open("mex.com", "w") as fp:
            fp.write("%mem={0}mb\n".format(mem_com_opt))
            fp.write("%nprocs=4\n")
            fp.write("#N {0}".format(method_opt) +
                     "/{0} OPT\n".format(basis_set_opt))
            fp.write("\n")
            fp.write(
                "Name ModRedundant - Minimalist working constrained optimisation\n"
            )
            fp.write("\n")
            fp.write(charges + "\n")
            fp.write(data)
            fp.write("\n")

        with open("mex.pbs", "w") as fp:
            fp.write("#!/bin/sh\n")
            fp.write(
                "#PBS -N mex_o\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l"
            )
            fp.write("mem={0}gb\n".format(mem_pbs_opt))
            fp.write(
                "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n"
            )
            fp.write(
                "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n"
            )
            fp.write(
                """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n"""
            )
            fp.write("then\n")
            fp.write(
                "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n"
            )
            fp.write(
                """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n"""
            )
            fp.write(
                "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n"
            )
            fp.write(
                """  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n"""
            )
            fp.write(
                """    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n"""
            )
            fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
            fp.write(
                "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mex.com mex.out"
                + str(output_num) + "\n\nrm -r $scrdir\n")
    elif cluster == "seq":
        gaussianInputFiles(
            output_num,
            method_opt,
            basis_set_opt,
            mem_com_opt,
            mem_pbs_opt,
            cluster,
            baseName="./",
            procedure="OPT",
        )

        # qsub()


def clean_name(name):
    return name.replace("-", "_").replace(",", "")


def clean_input_name(method, basis_set, solvent):
    clean = method
    if basis_set != "6-311G(d,p)":
        clean += basis_set.replace("(", "").replace(")", "").replace(",", "_")
    if solvent != "":
        clean += "_%s" % (clean_name(solvent))
    return solvent


def qsub(path="."):
    resetDirNum = len(path.split("/"))
    if path != ".":
        os.chdir(path)
    pbs_file = glob.glob("*.pbs")[0]
    cmd = "qsub %s" % pbs_file
    print(os.getcwd(), "cmd", cmd)
    failure = subprocess.call(cmd, shell=True)
    if path != ".":
        for i in range(resetDirNum):
            os.chdir("..")


def clean_dir_name(dir_name):
    return dir_name.replace("-", "").replace(",", "")


def make_exc(
    method_mexc,
    basis_set_mexc,
    mem_com_mexc,
    mem_pbs_mexc,
    cluster,
    geomDirName,
    solvent="",
):

    # baseName = 'cam-b3lyp'
    if method_mexc == "CAM-B3LYP":
        baseName = "mexc"
        dir_name = "mexc"
    else:
        baseName = "mexc"
        dir_name = method_mexc.lower()
    if solvent != "":
        dir_name += "_%s" % solvent
    if os.path.exists(dir_name):
        print("\n%s directory already exists\n" % (dir_name))
        return

    dir_name = clean_dir_name(dir_name)
    os.mkdir(dir_name)
    procedure = "TD(NStates=10)"
    output_num = 0
    # basis_set_mexc='CAM-B3LYP'

    # solvent = 'SCRF=(Solvent=dichloromethane)'

    outName = geomDirName + "_%s_%s" % (baseName, solvent)
    gaussianInputFiles(
        output_num,
        method_mexc,
        basis_set_mexc,
        mem_com_mexc,
        mem_pbs_mexc,
        cluster,
        baseName=baseName,
        procedure=procedure,
        data="",
        dir_name=dir_name,
        solvent=solvent,
        outName=outName,
    )
    path = "%s" % dir_name
    # qsub(path)


def clean_energies(hf_1, hf_2, zero_point):
    zero_point = zero_point[30:].replace(" (Hartree/Particle)", "")
    for i in range(10):
        zero_point = zero_point.replace("  ", " ")
    zero_point = float(zero_point)
    hf_1 = hf_1[3:].replace("\n", "").split("\\")

    if hf_2 != 0:
        hf_2 = hf_2[3:].replace("\n", "").split("\\")

        if hf_1[0] > hf_2[0]:
            return float(hf_1[0]) + zero_point
        else:
            return float(hf_2[0]) + zero_point
    else:
        return float(hf_1[0]) + zero_point


def make_exc_mo_freq(method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                     cluster, geomDirName):

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
    outName = geomDirName
    gaussianInputFiles(output_num,
                       method_mexc,
                       basis_set_mexc,
                       mem_com_mexc,
                       mem_pbs_mexc,
                       cluster,
                       baseName=baseName,
                       procedure=procedure,
                       data='',
                       dir_name=dir_name,
                       solvent='',
                       outName=outName)
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


word_error = "Error"
geom_start = "Standard orientation:"

geom_end = " Standard basis:"
standards = []
orientation = []


def main(
    index,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    method_mexc,
    basis_set_mexc,
    mem_com_mexc,
    mem_pbs_mexc,
    resubmissions,
    delay,
    cluster,
    geomDirName,
    xyzSmiles=True,
    solvent="",
):

    out_files = glob.glob("*.out*")
    out_completion = glob.glob("*_o.*")
    if method_mexc == "CAM-B3LYP":
        qsub_dir = "mexc"
    else:
        qsub_dir = method_mexc
    if solvent != "":
        qsub_dir += "_%s" % solvent

    qsub_dir = clean_dir_name(qsub_dir)

    print("v2 %s %s" % (solvent, qsub_dir))

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
            return True, resubmissions, "None"
        if resubmissions[index] > output_num:
            return True, resubmissions, "None"

        f = open(filename, "r")
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

            print("ERROR == TRUE")
            find_geom(
                lines,
                error=True,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            make_input_files_no_constraints(
                output_num,
                method_opt,
                basis_set_opt,
                mem_com_opt,
                mem_pbs_opt,
                cluster,
            )
            # os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            resubmissions[index] += 1
            qsub_dir = "./"
            return False, resubmissions, qsub_dir

        elif imaginary == True:
            find_geom(
                lines,
                error=False,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
            )
            add_imaginary(freq_clean,
                          freq_lst_len,
                          filename,
                          geomDirName=geomDirName)

            make_input_files_no_constraints(
                output_num,
                method_opt,
                basis_set_opt,
                mem_com_opt,
                mem_pbs_opt,
                cluster,
            )
            # os.system("qsub mex.pbs")
            failure = subprocess.call(cmd, shell=True)
            print("imaginary frequency handling...")
            resubmissions[index] += 1
            qsub_dir = "./"
            return False, resubmissions, qsub_dir
        else:
            print("ELSE")
            cmd = "qsub mexc.pbs"
            find_geom(
                lines,
                error=False,
                filename=filename,
                imaginary=imaginary,
                geomDirName=geomDirName,
                xyzSmiles=xyzSmiles,
            )
            """
            freq, hf_1, hf_2, zero_point = freq_hf_zero(
                lines, filename=filename)
            """
            print("entering make_exc")
            make_exc(
                method_mexc,
                basis_set_mexc,
                mem_com_mexc,
                mem_pbs_mexc,
                cluster,
                geomDirName,
                solvent,
            )

            os.remove("tmp.txt")

            return False, resubmissions, qsub_dir

    else:
        print("No output files detected for geom%d" % (index + 1))
        return True, resubmissions, "None"


# main()
