import matplotlib.pyplot as plt
from src import ice_build_geoms
from src import error_mexc_v8
import time
import glob
import os
import sys
import subprocess
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
# print(sys.path)

# NEED TO CHECK IF Q SUBMITTED BEFORE RESUBMITTING


def jobResubmit(min_delay, number_delays,
                method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc):

    min_delay = min_delay * 60
    cluster_list = glob.glob("calc_zone/geom*")
    print(cluster_list)
    complete = []
    resubmissions = []
    for i in range(len(cluster_list)):
        complete.append(0)
        resubmissions.append(2)
    calculations_complete = False

    for i in range(number_delays):
        # time.sleep(min_delay)
        for num, j in enumerate(cluster_list):
            os.chdir(j)
            delay = i
            if complete[num] < 1:
                action, resubmissions = error_mexc_v8.main(
                    num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                    method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                    resubmissions, delay
                )
                print(resubmissions)
            mexc_check = glob.glob("mexc")
            # print(mexc_check)
            if len(mexc_check) > 0:
                print('{0} entered mexc checkpoint 1'.format(num+1))
                complete[num] = 1
                mexc_check_out = glob.glob("mexc/mexc.o*")

                if complete[num] != 2 and len(mexc_check_out) > 1:
                    print('{0} entered mexc checkpoint 2'.format(num+1))
                    complete[num] = 2
            mexc_check = []
            os.chdir('../..')
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            if stage == len(complete)*2:
                calculations_complete = True

        if calculations_complete == True:
            print(complete)
            print('\nCalculatinos are complete.')
            print('Took %.2f hours' % (i*min_delay / 60))
            return complete
        print('Completion List\n', complete, '\n')
        print('delay %d' % (i))
        time.sleep(min_delay)
    return complete


def boltzmannAnalysisSetup(complete):

    analysis_ready = []
    if "results" not in glob.glob("results"):
        os.mkdir("results")
    os.chdir("results")
    if "mexc_values" not in glob.glob("mexc_values"):
        os.mkdir("mexc_values")
        os.chdir("..")
    else:
        os.chdir("..")

    for i in range(len(complete)):
        if complete[i] == 2:
            analysis_ready.append(i)
        else:
            print('geom%d/mexc %d is not finished with TD-DFT' % (i+1, i+1))
    os.chdir("calc_zone")
    for i in analysis_ready:

        cmd = '''awk '/Excited State/ {print $7, $9}' geom%d/mexc/mexc.out | sed 's/f=//g' > ../results/mexc_values/mexc_out%d.csv''' % (
            i+1, i+1)
        failure = subprocess.call(cmd, shell=True)
    os.chdir("..")
    print('\nBoltzmann Analysis Setup Complete.\n')
    return


def boltzmannAnalysis(T):

    os.chdir('results/mexc_values')
    mexc_out_names = glob.glob("*.csv")

    mexc_dict = {}
    for i in mexc_out_names:
        mexc_dict['{0}'.format(i[0:9])] = np.genfromtxt(i, delimiter=" ")
    os.chdir('../energies')
    energy_all = np.genfromtxt('energy_all.csv', delimiter=",")
    energy_all = energy_all[np.argsort(energy_all[:, 0])]
    lowest_energy = np.amin(energy_all[:, 1])
    lowest_energy_ind = (np.where(energy_all[:, 1] == lowest_energy))[0][0]
    lowest_energy = lowest_energy * 4.3597E-18  # convert hartrees to joules
    #print(lowest_energy, lowest_energy_ind+1)

    kb = 1.380649E-23
    combining_mexc = mexc_dict['mexc_out{0}'.format(lowest_energy_ind+1)]
    # print(combining_mexc)
    #print("energy_all:\n", energy_all)
    for key, value in mexc_dict.items():
        if key == 'mexc_out{0}'.format(lowest_energy_ind+1):
            continue
        # remember energy_all array index starts at zero
        current_energy_ind = int(key[8:]) - 1
        # find current energy and convert hartrees to joules
        current_energy = ((energy_all[current_energy_ind, :])[1]) * 4.3597E-18

        print(lowest_energy)

        print(current_energy)

        ni_nj = math.exp((lowest_energy - current_energy) / (T * kb))
        print("n%d / n%d = %.10f" %
              (lowest_energy_ind+1, current_energy_ind + 1, ni_nj))
        for i in range(len(value)):

            value[i][1] = value[i][1] * ni_nj
            # print(value[i][1])
            # print(value[i])
        # if want only certain number randomly, modify here
        combining_mexc = np.concatenate((combining_mexc, value), axis=0)
    # print(combining_mexc)

    # os.chdir("../final/data")
    os.chdir("..")
    if "final" not in glob.glob("final"):
        os.mkdir("final")
    os.chdir("final")
    if "data" not in glob.glob("data"):
        os.mkdir("data")
    os.chdir("data")

    np.savetxt("data", combining_mexc, fmt="%s")
    print("\ndata file made for specsim.pl\n")
    cmd = "perl ../../../src/specsim.pl"
    subprocess.call(cmd, shell=True)
    # if multiple, mv "spec" to new name

    os.chdir("../../../")
    return


def generateGraph(spec_name, T, title):
    print(os.getcwd())
    fig, ax1 = plt.subplots()

    data = np.genfromtxt("results/final/data/" + spec_name, delimiter=" ")
    data = data.tolist()
    # print(data)
    x = []
    y = []

    for i in data:
        print(i)
        x.append(i[0])
        y.append(i[1])
    # print(x)
    #print('\n', y)
    ax1.plot(x, y, "k-", label="T = {0} K".format(T))
    ax1.set_xlim([x[0], x[-1]])
    ax1.set_ylim(0, 1.2)

    plt.title(title)

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Oscillator Strength")
    plt.grid(b=None, which='major', axis='y', linewidth=1)
    plt.grid(b=None, which='major', axis='x', linewidth=1)
    ax1.legend(shadow=True, fancybox=True)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(title + '.png')

    return


def main():
    mol_xyz1 = "mon_h2o.xyz"
    mol_xyz2 = "mon_h2o.xyz"
    #mol_xyz2 = "mon_methanol.xyz"
    number_clusters = 70
    # enter the number of molecules of each geometry in the respective index
    molecules_in_cluster = [32, 0]
    box_length = 9                   # in angstroms
    minium_distance_between_molecules = 2.0

    resubmit_delay_min = 0.01
    resubmit_max_attempts = 40
    T = 9260  # Kelvin (K)

    # geometry optimization options
    method_opt = "wB97XD"
    basis_set_opt = "6-31G(d)"
    mem_com_opt = "1600"  # mb
    mem_pbs_opt = "15"  # gb

    # TD-DFT options
    method_mexc = "B3lYP"
    basis_set_mexc = "6-311G(d,p)"
    mem_com_mexc = "1600"  # mb
    mem_pbs_mexc = "15"  # gb"

    # ice_build_geoms.main(molecules_in_cluster, number_clusters, box_length, minium_distance_between_molecules,
    #                     mol_xyz1, mol_xyz2, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt)

    complete = jobResubmit(resubmit_delay_min, resubmit_max_attempts,
                           method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                           method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc)  # delay_min, num_delays
    for i in complete:
        if i != 2:
            print(
                "\nNot all calculations are complete with given time limits. Exiting program now...\n")
            return
    boltzmannAnalysisSetup(complete)

    boltzmannAnalysis(T)
    generateGraph("spec", T, "Title")

    # ps ax | grep test.py
    # nohup python3 test.py > output.log &
    # command & disown -h
    # brent way
    # ps aux | grep test.py
    # kill <pid> -9

    # ps axo user,comm,pid,time


    # ts or tsp // look into for off supercomputer
    # command below for background and updating .log file as it goes
    # python3 -u ./ice_manager.py > output.log & disown -h
main()
