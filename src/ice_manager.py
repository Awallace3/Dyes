import matplotlib.pyplot as plt
from src import ice_build_geoms
#from src import error_mexc_v9
from src import error_mexc_v10
from src import gather_energies
from src import vibrational_frequencies
import time
import glob
import os
import sys
import subprocess
import numpy as np
import scipy.signal
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
            print(j)
            delay = i
            if method_mexc == 'PBE0':
                mexc_check = glob.glob("pbe0")
                path_mexc = 'pbe0'
            
            elif method_mexc == 'wB97XD':
                mexc_check = glob.glob("wb97xd")
                path_mexc = 'wb97xd'
            
            elif method_mexc == 'B3LYP':
                mexc_check = glob.glob("mexc")
                path_mexc = 'mexc'
            
            elif method_mexc == 'B3LYPD3':
                mexc_check = glob.glob("b3lypd3")
                path_mexc = 'b3lypd3'
            
            elif method_mexc == 'CAM-B3LYP':
                mexc_check = glob.glob("cam-b3lyp")
                path_mexc = 'cam-b3lyp'
            
            elif method_mexc == 'B97D3':
                mexc_check = glob.glob('b97d3')
                path_mexc = 'b97d3'
            else:
                print("This method is not supported for TD-DFT yet.")

            print(mexc_check)
            if len(mexc_check) > 0:
                print('{0} entered mexc checkpoint 1'.format(num+1))
                complete[num] = 1

                #mexc_check_out = glob.glob("mexc/mexc.o*")
                #mexc_check_out_complete = glob.glob("mexc_o/mexc.o*")
                mexc_check_out = glob.glob("%s/mexc.o*" % path_mexc)
                mexc_check_out_complete = glob.glob("%s/mexc_o.o*" % path_mexc)

                #if complete[num] != 2 and len(mexc_check_out) > 1:
                if complete[num] != 2 and len(mexc_check_out) > 0 and len(mexc_check_out_complete) > 0:
                    print('{0} entered mexc checkpoint 2'.format(num+1))
                    complete[num] = 2
            if complete[num] < 1:
                action, resubmissions = error_mexc_v10.main(
                    num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                    method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                    resubmissions, delay
                )
                print(resubmissions)
           
            mexc_check = []
            os.chdir('../..')
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            if stage == len(complete)*2:
                calculations_complete = True

        if calculations_complete == True:
            print(complete)
            print('\nCalculations are complete.')
            print('Took %.2f hours' % (i*min_delay / 60))
            return complete
        print('Completion List\n', complete, '\n')
        print('delay %d' % (i))
        time.sleep(min_delay)
    return complete


def boltzmannAnalysisSetup(complete, method_mexc='B3LYP'):

    analysis_ready = []
    if "results" not in glob.glob("results"):
        os.mkdir("results")
    os.chdir("results")
    if "mexc_values" not in glob.glob("mexc_values"):
        os.mkdir("mexc_values")
        os.chdir("..")
    else:
        os.chdir("..")
    if method_mexc == 'PBE0':
        path_mexc = 'pbe0'
    
    elif method_mexc == 'wB97XD':
        path_mexc = 'wb97xd'
    
    elif method_mexc == 'B3LYP':
        path_mexc = 'mexc'
    
    elif method_mexc == 'B3LYPD3':
        path_mexc = 'b3lypd3'
    
    elif method_mexc == 'CAM-B3LYP':
        path_mexc = 'cam-b3lyp'
    
    elif method_mexc == 'B97D3':
        path_mexc = 'b97d3'
    
    else:
        print("This method is not supported for TD-DFT yet.")
    for i in range(len(complete)):
        if complete[i] == 2:
            analysis_ready.append(i)
        else:
            #print('geom%d/mexc %d is not finished with TD-DFT' % (i+1, i+1))
            print('geom%d/%s %d is not finished with TD-DFT' % (i+1, path_mexc, i+1))
    os.chdir("calc_zone")
    for i in analysis_ready:
        
        #cmd = '''awk '/Excited State/ {print $7, $9}' geom%d/mexc/mexc.out | sed 's/f=//g' > ../results/mexc_values/mexc_out%d.csv''' % (
        #    i+1, i+1)
        cmd = '''awk '/Excited State/ {print $7, $9}' geom%d/%s/mexc.out | sed 's/f=//g' > ../results/mexc_values/mexc_out%d.csv''' % (
            i+1, method_mexc, i+1)
        failure = subprocess.call(cmd, shell=True)
    os.chdir("..")
    print('\nBoltzmann Analysis Setup Complete.\n')
    return


def boltzmannAnalysis(T, energy_levels='electronic'):
    if energy_levels == 'electronic':
        os.chdir('results/mexc_values')
        csv_name = 'mexc_out'
        cmd = "perl ../../../src/specsim.pl"
    elif energy_levels == 'vibrational':
        os.chdir('results/vibrational_values')
        csv_name = 'vib'
        cmd = "perl ../../../src/specsim_xrange.pl 50 3600"
    print(os.getcwd())
    mexc_out_names = glob.glob("*.csv")
    #print(mexc_out_names)
    mexc_dict = {}
    print(mexc_out_names)
    for i in mexc_out_names:
        val = i[:-4]
        #print("val")
        print(val)
        #print(np.genfromtxt(i, delimiter=" "))
        mexc_dict['{0}'.format(val)] = np.genfromtxt(i, delimiter=" ")
    os.chdir('../energies')
    energy_all = np.genfromtxt('energy_all.csv', delimiter=",")
    energy_all = energy_all[np.argsort(energy_all[:, 0])]
    lowest_energy = np.amin(energy_all[:, 1])
    lowest_energy_ind = (np.where(energy_all[:, 1] == lowest_energy))[0][0]
    lowest_energy = lowest_energy * 4.3597E-18  # convert hartrees to joules
    kb = 1.380649E-23
    
    #combining_mexc = mexc_dict['mexc_out{0}'.format(lowest_energy_ind+1)]
    combining_mexc = mexc_dict['{0}'.format(csv_name + str(lowest_energy_ind+1))]

    # print(combining_mexc)
    #print("energy_all:\n", energy_all)
    for key, value in mexc_dict.items():
        if key == 'mexc_out{0}'.format(lowest_energy_ind+1):
            continue
        print(key) # crashes if not all mexc_out*.csv accounted for
        # remember energy_all array index starts at zero
        if energy_levels == 'electronic':
            current_energy_ind = int(key[8:]) - 1
        elif energy_levels == 'vibrational':
            current_energy_ind = int(key[3:]) - 1
        #print(current_energy_ind)
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
    #cmd = "perl ../../../src/specsim.pl"
    subprocess.call(cmd, shell=True)
    # if multiple, mv "spec" to new name

    os.chdir("../../../")
    return


def generateGraph(spec_name, T, title, filename, x_range=[100,300], x_units='nm', peaks=False):
    #print(os.getcwd())
    fig, ax1 = plt.subplots()

    data = np.genfromtxt("results/final/data/" + spec_name, delimiter=" ")
    data = data.tolist()
    # print(data)
    x = []
    y = []
    highest_y = 0
    for i in data:
        #print(i)
        x.append(i[0])
        y.append(i[1])
        if i[1] > highest_y:
            highest_y = i[1]
    
    for i in range(len(y)):
        y[i] /= highest_y
    if x_units == 'eV' or x_units=='ev':
        h = 6.626E-34
        c = 3E17
        ev_to_joules = 1.60218E-19
        x = [ h*c/(i*ev_to_joules) for i in x ]
        x.reverse()
        y.reverse()
    elif x_units == 'cm-1':
        x.reverse()
        y.reverse()
        #maxima = scipy.signal.argrelextrema(y, np.greater)
        
    # print(x)
    #print('\n', y)
    ax1.plot(x, y, "k-", label="T = {0} K".format(T))
    #ax1.set_xlim([x[0], x[-1]])
    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.2)

    plt.title(title)
    if x_units == 'ev' or x_units=='eV':
        print(x)
        plt.xlabel("Electronvolts (eV)")
        ax1.legend(shadow=True, fancybox=True)
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                print(round(x[i],2), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i], 2)
                if height > 0.02:
                    plt.text(frequency - 0.08, arr_y[i]+0.05, '%.2f' % frequency )

    elif x_units == 'cm-1':
        plt.xlabel(r"Wavenumbers cm$^{-1}$")
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                print(round(x[i]), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i])
                if height > 0.02:
                    plt.text(frequency+100, arr_y[i]+0.1, '%d' % frequency )
    else:
        plt.xlabel("Wavelength (nm)")
        ax1.legend(shadow=True, fancybox=True)

    plt.ylabel("Oscillator Strength")
    plt.grid(b=None, which='major', axis='y', linewidth=1)
    plt.grid(b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(filename)
    os.chdir("../../..")

    return

def generateMultiGraph(methods_lst, spec_name, T, title, filename, x_range=[100,300], x_units='nm', peaks=False):
    #print(os.getcwd())
    fig, ax1 = plt.subplots()

    data = np.genfromtxt("results/final/data/" + spec_name, delimiter=" ")
    data = data.tolist()
    # print(data)
    x = []
    y = []
    highest_y = 0
    for i in data:
        #print(i)
        x.append(i[0])
        y.append(i[1])
        if i[1] > highest_y:
            highest_y = i[1]
    
    for i in range(len(y)):
        y[i] /= highest_y
    if x_units == 'eV' or x_units=='ev':
        h = 6.626E-34
        c = 3E17
        ev_to_joules = 1.60218E-19
        x = [ h*c/(i*ev_to_joules) for i in x ]
        x.reverse()
        y.reverse()
    elif x_units == 'cm-1':
        x.reverse()
        y.reverse()
        #maxima = scipy.signal.argrelextrema(y, np.greater)
        
    # print(x)
    #print('\n', y)
    ax1.plot(x, y, "k-", label="T = {0} K".format(T))
    #ax1.set_xlim([x[0], x[-1]])
    ax1.set_xlim(x_range)
    ax1.set_ylim(0, 1.2)

    plt.title(title)
    if x_units == 'ev' or x_units=='eV':
        print(x)
        plt.xlabel("Electronvolts (eV)")
        ax1.legend(shadow=True, fancybox=True)
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                print(round(x[i],2), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i], 2)
                if height > 0.02:
                    plt.text(frequency - 0.08, arr_y[i]+0.05, '%.2f' % frequency )

    elif x_units == 'cm-1':
        plt.xlabel(r"Wavenumbers cm$^{-1}$")
        if peaks:
            arr_y = np.array(y)
            print("local maxima")
            peaks, _ = scipy.signal.find_peaks(arr_y, height=0)
            for i in peaks:
                print(round(x[i]), arr_y[i])
                height = arr_y[i]
                frequency = round(x[i])
                if height > 0.02:
                    plt.text(frequency+100, arr_y[i]+0.1, '%d' % frequency )
    else:
        plt.xlabel("Wavelength (nm)")
        ax1.legend(shadow=True, fancybox=True)

    plt.ylabel("Oscillator Strength")
    plt.grid(b=None, which='major', axis='y', linewidth=1)
    plt.grid(b=None, which='major', axis='x', linewidth=1)
    # os.chdir("results/final/graphs")
    os.chdir("results/final")
    if "graphs" not in glob.glob("graphs"):
        os.mkdir("graphs")
    os.chdir("graphs")
    plt.savefig(filename)
    os.chdir("../../..")

    return


def main():
    mol_xyz1 = "mon_nh3.xyz"
    mol_xyz2 = "mon_nh3.xyz"
    #mol_xyz2 = "mon_methanol.xyz"
    number_clusters = 30
    # enter the number of molecules of each geometry in the respective index
    molecules_in_cluster = [8, 0]
    box_length = 9                   # in angstroms
    minium_distance_between_molecules = 3.0

    resubmit_delay_min = 0.01
    resubmit_max_attempts = 1


    # geometry optimization options
    method_opt = "wB97XD"
    basis_set_opt = "6-31G(d)"
    mem_com_opt = "1600"  # mb
    mem_pbs_opt = "15"  # gb

    methods_lst = ["B3LYP", "PBE0", "wB97XD", "CAM-B3LYP", "B3LYPD3", "B97D3"]
    # TD-DFT options
    #method_mexc = "B3LYP"
    #method_mexc = "PBE0"
    #method_mexc = "wB97XD"
    #method_mexc = "CAM-B3LYP"
    #method_mexc = "B3LYPD3"
    method_mexc = "B97D3"
    basis_set_mexc = "6-311G(d,p)"
    mem_com_mexc = "1600"  # mb
    mem_pbs_mexc = "15"  # gb"

    T = 1000  # Kelvin (K)
    title = r"30 Randomized Clusters of 8 CO$_2$ Molecules"
    filename = "30_8_rand_co2_%s.png" % method_mexc
    #ice_build_geoms.main(molecules_in_cluster, number_clusters, box_length, minium_distance_between_molecules,
     #                   mol_xyz1, mol_xyz2, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt)

    complete = jobResubmit(resubmit_delay_min, resubmit_max_attempts,
                           method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                           method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc)  # delay_min, num_delays
    """
    #for i in complete:
    #    if i != 2:
    #        print(
    #            "\nNot all calculations are complete with given time limits. Exiting program now...\n")
    #        return
    """

    boltzmannAnalysisSetup(complete, method_mexc)
    gather_energies.main()

    boltzmannAnalysis(T)
    generateGraph("spec", T, title, filename, x_range=[5,11], x_units='ev', peaks=True)


    T = 1000  # Kelvin (K)
    title = r"30 Randomized Clusters of 8 CO$_2$ Molecules: Vibrational"
    filename = "30_8_rand_co2_vib_wB97XD.png"

    #vibrational frequency
    #vibrational_frequencies.main()
    #boltzmannAnalysis(T, energy_levels='vibrational')
    #generateGraph("spec", T, title, filename, x_range=[3600, 50], x_units='cm-1', peaks=True)

    # ps aux | grep test.py
    # kill <pid> -9

    # python3 -u ./ice_manager.py > output.log & disown -h
main()
