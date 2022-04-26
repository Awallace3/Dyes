import os
import pandas as pd
from MO_func_find import *
from homo_lumo_boxer_csv import HOMO_LUMO_dict
from Part_atom_finder import *
from MO_Dict import xyzcoords





def amountofbasisfunctions(file):
    filename = open(file, 'r')
    data = filename.readlines()
    aa = 0
    for num, line in enumerate(data):
        if 'basis functions,' in line:
            line = line.split(',')
            line = line[0].replace('basis functions', '')
            aa += int(line)
    return aa


def orbital_sym(file):
    filename = open(file, 'r')
    data = filename.readlines()
    for num, line in enumerate(data):
        if 'Orbital symmetries:' in line:
            print()

    return


def atom_num_let_dic(file):
    filename = open(file, 'r')
    data = filename.readlines()
    coord = {}
    first_num = []
    last_num = []
    for num, i in enumerate(data):
        if 'Standard orientation:' in i:
            first_num.append(num + 5)
        # print(data[num+5])
        if ' ---------------------------------------------------------------------' in i:
            last_num.append(num)
    for line in data[int(first_num[0]):int(last_num[-1])]:
        line = line.strip().replace("  ", " ").replace("  ", " ").replace(
            "  ", " ").replace("  ", " ").replace("  ", " ")
        line = line.split(" ")
        if line[1] == '7':
            let = 'N'
            coord[line[0]] = let
        if line[1] == '6':
            let = 'C'
            coord[line[0]] = let
        if line[1] == '1':
            let = 'H'
            coord[line[0]] = let
        if line[1] == '8':
            let = 'O'
            coord[line[0]] = let
        if line[1] == '16':
            let = 'S'
            coord[line[0]] = let
        if line[1] == '9':
            let = 'F'
            coord[line[0]] = let
        if line[1] == '14':
            let = 'Si'
            coord[line[0]] = let
    #print(coord)
    return coord


def lastO(file, basis):
    filename = open(file, 'r')
    data = filename.readlines()

    number = []
    for num, line in enumerate(data):
        if 'Molecular Orbital Coefficients:' in line:
            number.append(num)

        if '     Density Matrix:' in line:
            number.append(num)
    #print(data[number[0]:number[1]])
    #print(number)

    last_num = 0
    for num, line in enumerate(data[number[0]:number[1]]):
        #print(line)
        line = line.replace('\n', '')
        #print(line)
        if '        O        ' in line:
            #    line = line.strip(' ')
            #    line=line.split('         ')
            # print(num)
            if 'V' in line:

                line = line.strip().replace("  ", " ").replace(
                    "  ", " ").replace("  ",
                                       " ").replace("  ",
                                                    " ").replace("  ", " ")
                line = line.split(" ")
                occ = -1
                print((occ, 'start'))

                #if line[i][-1] == "V":

                vir = 0

                for i in range(-1, -len(line), -1):
                    if line[0] == "O" and line[1] == "O" and line[
                            2] == "O" and line[3] == "O" and line[4] == "V":
                        vir = -1
                        occ = -1 - 1
                    if line[0] == "O" and line[1] == "O" and line[
                            2] == "O" and line[3] == "V" and line[4] == "V":
                        vir = -2
                        occ = -3
                    if line[0] == "O" and line[1] == "O" and line[
                            2] == "V" and line[3] == "V" and line[4] == "V":
                        vir = -3
                        occ = -4
                    if line[0] == "O" and line[1] == "V" and line[
                            2] == "V" and line[3] == "V" and line[4] == "V":
                        vir = -4
                        occ = -5

            # print((occ,'done'))
            #vir = occ + 1
            # print(occ, vir)
                last_num = num + number[0] + 1
                start_homo = last_num + 1
                end_homo = last_num + basis + 1
                start_lumo = last_num + 1
                end_lumo = last_num + basis + 1
                print(line)
                for i in line:
                    i
            else:
                #print(line)
                #print(num+number[0])
                start_homo = num + number[0] + 1
                #print((start_homo,'Start HOMO'))
                end_homo = start_homo + last_num + basis + 1
                #print((end_homo,'End HOMO'))
                start_lumo = start_homo + last_num + basis + 3
                #  print((start_lumo,'Start LUMO'))
                end_lumo = start_lumo + last_num + basis + 1
                #  print((end_lumo,'End LUMO'))
                # print("virtual in next block")
                occ = -1
                vir = -5
    return start_homo, end_homo, start_lumo, end_lumo, occ, vir


def homo_dict(file, start_num, end_num, occ):
    filename = open(file, 'r')
    data = filename.readlines()
    tot_homo = {}
    for num, i in enumerate(data[start_num:end_num]):
        #print(i)
        if 'Eigenvalues' in i:
            i
        else:
            #print(i[occ])
            i = i.replace("  ",
                          " ").replace("  ", " ").replace("  ", " ").replace(
                              "  ", " ").replace("  ", " ").replace("  ", " ")
            i = i.split(" ")[1:]
            #print(i)
            # atom = {}
            if len(i) == 9:
                #print(i, len(i),num+last_num)
                #print(i[1])
                #atom['type'.update(i[1])
                type1 = i[1]
                #atom['type'].update(type1)
                '''
                atom['occ_coef'].update(float(i[occ]))
                occup={'occ_coef':float(i[occ]}

                atom['vir_coef'].update(float(i[vir])**2)
                atom['line_num'].update(num +last_num)
                '''

                atom = {
                    'type': i[1],
                    'occ_coef': [float(i[occ])**2],
                    #      'vir_coef': [float(i[vir])**2],
                    #      'line_num': num+last_num
                }
                #print(atom['line_num'])
            else:
                atom['occ_coef'].append(float(i[occ])**2)
               # atom['vir_coef'].append(float(i[vir])**2)
                tot_homo[atom['type']]=atom['occ_coef']
               # tot_lumo[atom['type']]=atom['vir_coef']
    #print(tot_homo['1'])

    return tot_homo


def lumo_dict(file, start_num, end_num, vir):
    filename = open(file, 'r')
    data = filename.readlines()
    tot_lumo = {}
    for num, i in enumerate(data[start_num:end_num]):
        #print(i)
        if 'Eigenvalues' in i:
            i
        else:
            #print(i[occ])
            i = i.replace("  ",
                          " ").replace("  ", " ").replace("  ", " ").replace(
                              "  ", " ").replace("  ", " ").replace("  ", " ")
            i = i.split(" ")[1:]
            #print(i)
            # atom = {}
            if len(i) == 9:
                #print(i, len(i),num+last_num)
                #print(i[1])
                #atom['type'.update(i[1])
                type1 = i[1]
                #atom['type'].update(type1)
                '''
                atom['occ_coef'].update(float(i[occ]))
                occup={'occ_coef':float(i[occ]}

                atom['vir_coef'].update(float(i[vir])**2)
                atom['line_num'].update(num +last_num)
                '''

                atom = {
                    'type': i[1],
                    'vir_coef': [float(i[vir])**2],
                }
            else:
                atom['vir_coef'].append(float(i[vir])**2)
                tot_lumo[atom['type']]=atom['vir_coef']
    #print(tot_lumo['1'])

    return tot_lumo


def summer(dict_homo,dict_lumo,num):
    #print(num)
    final_homo = {}
    final_lumo = {}

    for atom_num in num.keys():
        #print(dict_homo[atom_num])
        homo_tot = {'atom_lett': {}, 'total': {}}
        tot_homo = sum(dict_homo[atom_num])
        homo_tot['atom_lett'] = num[atom_num]
        homo_tot['total'] = tot_homo
        # final.update(homo_tot)
        final_homo[atom_num] = homo_tot

        lumo_tot = {'atom_lett': {}, 'total': {}}
        tot_lumo = sum(dict_lumo[atom_num])
        lumo_tot['atom_lett'] = num[atom_num]
        lumo_tot['total'] = tot_lumo
        # final.update(homo_tot)
        final_lumo[atom_num] = lumo_tot

    # print(homo_tot)
    '''
    print(final_homo)

    print(final_homo['1']['atom_lett'])
    print(final_homo['1']['total'])
    print(final_lumo['1']['atom_lett'])
    print(final_lumo)
    '''

    #dict_homo

    return final_homo, final_lumo


def total_contrib(dict_homo, dict_lumo, num):
    tot_homo = 0
    tot_lumo = 0
    for atom_num in num.keys():
        #print(atom_num)
        tot_homo += dict_homo[atom_num]['total']
        tot_lumo += dict_lumo[atom_num]['total']
    #print(tot_homo)
    #print(tot_lumo)
    
    return tot_homo,tot_lumo

def part_tot_contrib(dict_homo,dict_lumo,num,tot_homo,tot_lumo,atom_num_list,name):
    par_homo = 0
    par_lumo = 0
    #atom_num_list=[1,2,3,4,5,6,20,21,22,30,31,32] 
  #  atom_num_list = [1, 2, 3, 4, 5, 6, 20, 21, 22, 32, 33, 34]
    '''
    atom_num_list = [7,8,9,10,11,12,13,14,15,16,17,18,19]
    atom_num_list = [1,2,3,4,5,6,20,21,22,50,51,52]
    atom_num_list = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
    atom_num_list = [1,2,3,4,5,6,20,21,22,49,48,50,51,52]
    '''
    #atom_num_list = [7,8,9,10,11,12,13,14,15,16,17,18,19]

   # for atom_num in range(21,31):
    '''
    atom_num_list = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
    atom_num_list = [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78]
    atom_num_list = ['1', '2', '3', '4', '5', '6', '48', '49', '50', '51', '52', '53', '54', '80', '81', '82', '83', '84', '85', '86', '87']
    '''
    #atom_num_list = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43]
    #satom_num_list = [1,2,3,4,5,6]
   # atom_num_list= ['13', '14', '15', '16', '17', '18', '19', '48'] #anchor
    
    for atom_num in atom_num_list:
        #print(atom_num)
        
        par_homo += dict_homo[str(atom_num)]['total']
        par_lumo += dict_lumo[str(atom_num)]['total']

    #print(tot_homo)

    per_homo = par_homo / tot_homo * 100
    per_lumo = par_lumo / tot_lumo * 100
    #print(per_homo)
    #print()

    print('The percentage of HOMO ' + str(per_homo))
    print('The percentage of LUMO ' + str(per_lumo))
    '''
    df = {"Name":name,
          "HOMO":str(round(per_homo,2))+' %',
          "LUMO":str(round(per_lumo,2))+' %'}
    print(df)
    '''
    '''
    
    filename = open('HOMO_LUMO_Per.tex','a')
    filename.write(name+'\n')
    filename.write('HOMO '+' '+'LUMO\n')
    filename.write(str(round(per_homo,2))+' '+str(round(per_lumo,2))+'\n')
    '''
    

    #print(tot_lumo)


    return name,round(per_homo,2),round(per_lumo,2)


def main():
#    filename = '../MO_start/6ed_28b_4ea/mo/6ed_28b_4ea.out'
#    filename = '../MO_start/3ed_7b_2ea/mo/3ed_7b_2ea.out'
  #  filename = '../MO_start/11ed_28b_8ea/mo/11ed_28b_8ea.out'
  #  filename = '../MO_start/3ed_26b_4ea/mo/3ed_26b_4ea.out'
  #  filename = '../MO_start/11ed_8b_8ea/mo/test/mani.out'
   # filename = '../MO_start/11ed_8b_8ea/mo/11ed_8b_8ea.out' # has two carboxy
    #Smiles = '../MO_start/11ed_8b_8ea/mo/test.smi'
    #input_file = '../MO_start/3ed_7b_2ea/mo/3ed_7b_2ea.com'
  #  filename = '../MO_start/1ed_20b_4ea/mo/1ed_20b_4ea.out'
   # filename = '../MO_start/10ed_29b_10ea/mo/10ed_29b_10ea.out'
   # filename = '../MO_start/3ed_15b_3ea/mo/3ed_15b_3ea.out'
  #  filename = '../MO_start/11ed_28b_8ea/mo/11ed_28b_8ea.out'
  #  filename = '../MO_start/11ed_30b_8ea/mo/11ed_30b_8ea.out'
   # jobs = ['11ed_28b_8ea','6ed_28b_4ea','11ed_30b_8ea','3ed_26b_4ea']
  #  jobs = ['2ed_32b_11ea','1ed_16b_2ea']
   # jobs = ['1ed_16b_2ea','1ed_33b_3ea','3ed_1b_5ea']
   # jobs = ['6ed_16b_5ea','6ed_29b_6ea','6ed_29b_2ea','6ed_29b_11ea']
    """
    jobs = ['7ed_29b_10ea','6ed_29b_10ea','10ed_29b_10ea','5ed_29b_10ea','6ed_28b_10ea']
    jobs = ['6ed_29b_5ea','7ed_29b_2ea','7ed_29b_6ea','7ed_29b_5ea','6ed_28b_2ea','7ed_29b_11ea','6ed_28b_5ea']
    jobs =['5ed_29b_11ea','10ed_29b_5ea','10ed_29b_6ea','6ed_28b_6ea','10ed_29b_11ea']
    jobs = ['6ed_29b_1ea','6ed_16b_5ea','10ed_29b_5ea','6ed_28b_5ea','6ed_29b_5ea']
    jobs = ['6ed_16b_10ea','6ed_16b_3ea','6ed_16b_11ea','6ed_16b_6ea','6ed_31b_2ea']
    jobs = ['6ed_16b_3ea','6ed_31b_2ea']
    '''
    filename = open('/Users/tsantaloci/Desktop/python_projects/austin/Dyes/data_analysis/ori_800_1000.csv')
    data = filename.readlines()
    '''
    '''
    jobs = []
    for line in data:
        line = line.split(',')
        if '1ea' in line[0]:
            jobs.append(line[0])
    '''
    names =['6ed_16b_4ea', '2ed_28b_6ea', '1ed_29b_3ea', '6ed_16b_5ea', '2ed_28b_10ea', '1ed_29b_6ea', '1ed_29b_11ea', '10ed_28b_2ea', '5ed_28b_6ea', '1ed_28b_7ea', '7ed_28b_3ea', '10ed_29b_3ea', '1ed_29b_2ea', '10ed_28b_11ea', '2ed_28b_9ea', '6ed_29b_8ea', '7ed_28b_11ea', '1ed_29b_10ea', '10ed_28b_6ea', '7ed_28b_6ea', '11ed_29b_6ea', '5ed_28b_9ea', '2ed_28b_5ea', '1ed_29b_5ea', '6ed_28b_3ea', '11ed_29b_11ea', '5ed_28b_2ea', '5ed_28b_10ea', '2ed_28b_7ea', '10ed_28b_10ea', '11ed_29b_2ea', '11ed_29b_10ea', '7ed_28b_10ea', '9ed_16b_5ea', '7ed_28b_2ea', '11ed_29b_5ea', '10ed_29b_2ea', '9ed_16b_9ea', '7ed_29b_1ea', '10ed_29b_1ea', '5ed_29b_11ea', '5ed_29b_3ea', '7ed_29b_3ea', '10ed_28b_9ea', '1ed_29b_9ea', '11ed_28b_7ea', '9ed_28b_6ea', '6ed_29b_3ea', '10ed_28b_5ea', '5ed_29b_6ea', '9ed_29b_3ea', '9ed_28b_2ea', '6ed_28b_11ea', '7ed_28b_9ea', '10ed_29b_6ea', '6ed_28b_1ea', '6ed_29b_4ea', '7ed_29b_11ea', '1ed_29b_7ea', '7ed_29b_6ea', '11ed_29b_9ea', '9ed_29b_6ea', '10ed_29b_11ea', '5ed_29b_10ea', '5ed_28b_7ea', '5ed_29b_2ea', '7ed_28b_5ea', '5ed_29b_5ea', '9ed_29b_11ea', '6ed_28b_6ea', '7ed_29b_2ea', '10ed_28b_7ea', '6ed_28b_10ea', '9ed_29b_10ea', '10ed_29b_10ea', '7ed_28b_7ea', '7ed_29b_10ea', '6ed_29b_1ea', '6ed_28b_9ea', '9ed_29b_2ea', '9ed_29b_5ea', '5ed_29b_9ea', '10ed_29b_9ea', '10ed_29b_5ea', '9ed_28b_5ea', '6ed_28b_2ea', '7ed_29b_5ea', '11ed_29b_7ea', '9ed_28b_7ea', '6ed_29b_9ea', '6ed_29b_6ea', '9ed_29b_9ea']


    names = ['10ed_34b_9ea', '7ed_32b_6ea', '2ed_32b_10ea', '3ed_16b_2ea', '10ed_32b_2ea', '2ed_32b_5ea', '5ed_32b_6ea', '2ed_16b_6ea', '7ed_32b_1ea', '11ed_32b_6ea', '10ed_32b_3ea', '1ed_20b_4ea', '10ed_1b_1ea', '6ed_16b_11ea', '7ed_1b_1ea', '7ed_1b_4ea', '6ed_1b_1ea', '7ed_16b_3ea', '1ed_32b_6ea', '6ed_31b_2ea', '2ed_32b_9ea', '3ed_16b_10ea', '7ed_16b_2ea', '1ed_33b_6ea', '2ed_32b_11ea', '1ed_31b_2ea', '2ed_16b_7ea', '7ed_16b_1ea', '2ed_16b_3ea', '1ed_16b_11ea', '6ed_16b_6ea', '1ed_32b_5ea', '6ed_16b_10ea', '3ed_16b_6ea', '10ed_20b_4ea', '2ed_32b_6ea', '10ed_35b_9ea', '2ed_16b_9ea', '5ed_32b_9ea', '5ed_32b_11ea', '2ed_32b_7ea', '1ed_32b_2ea', '1ed_32b_10ea', '10ed_34b_6ea', '2ed_16b_10ea', '1ed_31b_5ea', '1ed_33b_2ea', '10ed_32b_7ea', '3ed_1b_4ea', '1ed_1b_4ea', '5ed_1b_4ea', '10ed_32b_10ea', '2ed_16b_5ea', '6ed_1b_4ea', '3ed_1b_5ea', '1ed_31b_9ea', '3ed_16b_3ea', '10ed_32b_9ea', '1ed_33b_10ea', '1ed_32b_7ea', '5ed_32b_3ea', '3ed_16b_9ea', '1ed_33b_3ea', '10ed_16b_3ea', '2ed_16b_2ea', '10ed_32b_6ea', '7ed_32b_3ea', '3ed_16b_11ea', '10ed_32b_11ea', '2ed_32b_2ea', '1ed_32b_9ea', '2ed_16b_11ea', '7ed_16b_10ea', '1ed_16b_2ea', '2ed_32b_3ea', '3ed_20b_4ea', '10ed_1b_4ea', '1ed_16b_10ea', '2ed_1b_4ea', '1ed_35b_2ea', '7ed_32b_10ea', '10ed_32b_5ea', '10ed_34b_3ea', '6ed_16b_8ea', '1ed_33b_5ea', '10ed_35b_3ea', '10ed_34b_11ea', '1ed_31b_10ea', '6ed_16b_3ea', '7ed_32b_11ea', '10ed_35b_6ea', '2ed_1b_5ea', '6ed_20b_1ea', '2ed_20b_4ea', '1ed_16b_6ea', '10ed_32b_1ea', '1ed_31b_6ea', '10ed_31b_1ea', '1ed_33b_9ea', '1ed_34b_7ea']
    names = ['']

    

    jobs = []
    for name in names:
        if '2ea' in name or '3ea' in name or '5ea' in name or '9ea' in name or '6ea' in name or '8ea' in name:
            jobs.append(name)
    
  #  jobs = ['6ed_16b_3ea','6ed_31b_2ea','6ed_16b_11ea','6ed_16b_6ea','6ed_31b_2ea','6ed_16b_10ea']
   """

        
  #  jobs = ['6ed_29b_2ea']
  #  jobs = ['NL6']
  #  jobs = ['5ed_16b_7ea', '6ed_16b_9ea', '10ed_26b_8ea', '9ed_1b_6ea', '7ed_31b_7ea', '6ed_16b_10ea', '6ed_31b_7ea', '9ed_1b_9ea', '9ed_1b_5ea', '9ed_1b_11ea', '7ed_32b_7ea', '6ed_16b_3ea', '2ed_16b_7ea', '11ed_1b_10ea', '6ed_16b_11ea', '6ed_16b_6ea', '7ed_16b_2ea', '9ed_26b_8ea', '1ed_26b_8ea', '10ed_31b_7ea', '7ed_16b_9ea', '3ed_20b_4ea', '6ed_31b_2ea', '5ed_20b_4ea', '10ed_20b_4ea', '10ed_32b_7ea', '6ed_32b_2ea', '11ed_1b_9ea', '5ed_16b_2ea', '7ed_16b_6ea', '9ed_16b_7ea', '11ed_26b_8ea', '6ed_1b_4ea', '9ed_20b_1ea', '3ed_16b_2ea', '2ed_16b_2ea', '1ed_16b_7ea', '7ed_33b_7ea', '7ed_31b_2ea', '11ed_1b_5ea', '7ed_1b_4ea', '11ed_1b_11ea', '5ed_31b_7ea', '7ed_34b_7ea', '2ed_32b_7ea', '10ed_16b_9ea', '10ed_33b_7ea', '10ed_16b_10ea', '6ed_31b_6ea', '6ed_31b_5ea', '7ed_16b_11ea', '7ed_16b_10ea', '6ed_31b_9ea']
  #  jobs = ['5ed_16b_7ea']

    for x in jobs:
        filename = '../MO_start_B/' + str(x) + '/mo/'+ str(x)+'.out'

   

        num = amountofbasisfunctions(filename)
        atom_let = atom_num_let_dic(filename)



        #homo,lumo = lastO(filename,num)
        start_num_h,end_num_h,start_num_l,end_num_l,occ,vir  = lastO(filename,num) 
        
        homo = homo_dict(filename,start_num_h,end_num_h,occ)
        lumo = lumo_dict(filename,start_num_l,end_num_l,vir)
        
        
        #print(homo.keys())
        atom = xyzcoords(filename)
        




        #print(atom)
        O = atom_type_O(atom)
        N = atom_type_N(atom)
        S = atom_type_S(atom)
        H = atom_type_H(atom)
        Si= atom_type_Si(atom)
        C = atom_type_C(atom)
        Od = Bond_lengths_O_C(O,C,atom)
        ch = Bond_lengths_H_C(H,C,atom)
        Os = Bond_lengths_H_O(H,O,atom)
        Co = Bond_lengths_O_C(O,C,atom) 
        No = Bond_lengths_O_N(O,N,atom) 
        CC = Bond_lengths_O_C(C,C,atom)  
        tot = Bond_length(atom)
        ang = Bond_angles(atom,tot)
        carboxy = Bond_angle_H_O_C(O,C,atom,tot,ang) 
        #print(carboxy)
        amide = Bond_angle_H_O_N(O,C,N,atom,tot,ang)
        atom_num_list = bondistancecheck(amide,tot)
        atom_num_list = bondistancecheck(carboxy,tot)
    # print(atom_num_list)
        atom_num_list = atomnearchecker(atom_num_list,
                                        H,
                                        O,
                                        N,
                                        Si,
                                        C,
                                        tot,
                                        atom,
                                        ang,
                                        Carboxy = True,
                                        Amide = False,
                                        cyanoacrylic=True,
                                        SI=False)
       # print(atom_num_list)
        
          

        kkk = {}
        '''
        atom_num_list=[1,2,3,4,5,6,20,21,22,50,51,52]
        atom_num_list = [7,8,9,10,11,12,13,14,15,16,17,18,19]
        atom_num_list = [1,2,3,4,5,6,20,21,22,49,48,50,51,52]
        '''
      #  atom_num_list = [7,8,9,10,11,12,13,14,15,16,17,18,19]
        '''
        for x in atom_num_list:
            for y in atom_num_list:
                dis = tot[str(x)+' '+str(y)]
                if dis >= 4.79:
                    print((dis,(x,y)))
        '''
       
       # for i in atom_num_list.keys():
      #  for i in atom_num_list: 22:50

      #  atom_num_list =  [7,8,9,10,11,12,13,14,15,16,17,18,19]
    #    atom_num_list = ['57','70', '71', '72', '73', '75', '76', '77', '78', '79', '74']
    #    aaa = ['1', '2', '3', '4', '5', '6', '48', '49', '50', '51', '52', '53', '54','80','81','82','83','84','85','86','87']
       # atom_num_list = [1,2,3,4,5,6,7,8,13,14,15,16,17,18,19]
       # atom_num_list = [9,10,11,12,20,21,22,23,24,25,26,35,36,37,38]
      #  atom_num_list = [26,27,28,29,30,31,32,33,34]
       # atom_num_list = [9, 10, 11, 12, 20, 21, 22, 23, 24, 25, 26,34,35,36,37,38]
      #  atom_num_list =  [39,40,41,42,43,44,45,46,47,48,49,57,58,59]
      #  atom_num_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
      #  atom_num_list =[50,51,52,53,54,55,56,30,31,32,33]
      #  atom_num_list = [ '38', '50', '51','60','61', '22', '35', '36', '37']
      #  atom_num_list = ['150']
      #  atom_num_list = ['23', '55', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '88', '89', '97', '114', '115', '116', '117', '118', '122', '127', '133', '150', '151']
        #atom_num_list = ['15','16','17','18','19','20','21', '22', '23', '24', '25', '26', '27', '84']
        #atom_num_list = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28] # ND acceptor
       # atom_num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 29, 30, 31, 32, 51]
        #atom_num_list = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
      #  atom_num_list = [7,8,9,10,11, 12, 13, 14, 15, 16, 17,18,19, 58]
        #atom_num_list = [3, 4, 5, 6, 20, 21, 45, 46, 47]
       # atom_num_list = [22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44]
        #atom_num_list = [47,48,49,50,51, 52, 53, 54, 55, 56, 57,58,59,100]
    #    atom_num_list = [60,61,62,63,46,45,43,42,41,40]
    #    atom_num_list = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44]
    #    atom_num_list = [1, 2, 3, 4, 5, 45, 46,  60, 61,62]
       # atom_num_list = [27,28,29,30,31, 32, 33, 34, 35, 36, 37,38,39,68]# acceptor
       # atom_num_list = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
       # atom_num_list = [1,2,3,4,5,25,26,40,41,42,43]
       # atom_num_list = [6,7,8,9,10, 11, 12, 13, 14, 15, 16,17,53] # acceptor
       # atom_num_list = [1,2,3,4,5,18,19,43,44,45,46] # Backbone
       # atom_num_list = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42] # Donor
     #   atom_num_list = [1, 2, 3, 4, 5, 45, 46,  60, 61,62]
     #   atom_num_list = [46,47,48,49,50, 51, 52, 53, 54, 55, 56,57, 94] # acceptor
     #   atom_num_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,59,60]
     #   atom_num_list = [22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,58]
       # atom_num_list = [60,61,62,63,64, 65, 66, 67, 68, 69, 70,71, 124]
        '''
        atom_num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,  72, 74, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113]
        atom_num_list = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 119, 120]
        atom_num_list = [1, 2, 3, 4,5, 58, 59,72, 73, 74, 75]
        '''
       # atom_num_list = [71]
     #   atom_num_list = [46, 47, 48, 49, 50, 51, 52, 53, 54, 88, 89, 90] #acceptor
     #   atom_num_list =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 70, 71, 72, 73, 92, 93]
     #   atom_num_list = [23,24,25,26,27,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,55]
        atom_num_list = [42, 55, 58, 65, 87, 88, 89, 90, 91]
        atom_num_list = [7, 13, 14, 15, 16, 17, 26, 31, 33, 86]
        atom_num_list = [68]
        atom_num_list =[ 18, 23, 28, 68, 69, 70, 86]
        atom_num_list = [3,4,5, 6, 9, 10,  68, 69, 70]
        atom_num_list = [71]
        

        for i in atom_num_list:
            for x in atom['atom_num']:
    #for i in range(1,50):
 #           for i in atom['atom_num']:
                dis = tot[str(i)+' '+str(x)]
                
        #        print(dis)
                if dis <= 5:
                    kkk[int(x)]=x


            
        atom_num_list = kkk
        aa = sorted(list(kkk.keys()))
        print(aa)
        for x in kkk.keys():
            print(str(atom['atom_let'][str(x)])+' ' +str(atom['xcoord'][str(x)])+' '+str(atom['ycoord'][str(x)])+' '+ str(atom['zcoord'][str(x)]))

        # print(i)
        
        
        

        total = {}
        final_homo,final_lumo = summer(homo,lumo,atom_let)
        tot_homo,tot_lumo = total_contrib(final_homo,final_lumo,atom_let)
        tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,x)
        total[tot[0]]=[tot[0],tot[1],tot[2]]
       # total['HOMO']=tot[1]
       # total['LUMO']=tot[2]
  #  file = '../data_analysis/600_800.csv'
   # file = '../data_analysis/800_1000.csv'
    
   # numbs = HOMO_LUMO_dict(file)
        

  #  print(total)

    name1 = []
    homo = []
    lumo = []
    
    wave = []

    for name in total.keys():
        name1.append(name)
        homo.append(total[name][1])
        lumo.append(total[name][2] )
     #   wave.append(round(numbs[name][2],2))
    df= {"Name":name1,
        "HOMO":homo,
        "LUMO":lumo,
     #   "Wave":wave
        }
    df = pd.DataFrame(df)

    df.to_csv('lll.csv',index=False)
    
    #print(df)


    '''    
    df = {"Name":total[tot[0][],
          "HOMO":total[tot[0]][1],
          "LUMO":total[tot[0]][2]
          }
    print(df)
    '''
    
    
    
    
    
    
    

    final_homo, final_lumo = summer(homo, lumo, atom_let)
    tot_homo, tot_lumo = total_contrib(final_homo, final_lumo, atom_let)
    part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo, tot_lumo)


  #  for line in lastO(filename,num):
  #      line 
    

#main()
if __name__ == '__main__':
    main()
 
