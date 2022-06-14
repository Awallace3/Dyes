import os
import numpy as np
import pandas as pd
from MO_Dict import xyzcoords
from gather_results import json_pandas_molecule
from MO_Dict import *
from homo_lumo_boxer_csv import *
import json
#from gather_results import json_pandas_molecule





def SMILES_FINDER(SMILES_csv):
    filename = open(SMILES_csv, 'r')
    data = filename.readlines()
    SMILES_Dic = {}
    for line in data[1:]:
        line = line.split(',')
        SMILES_Dic[line[0]] = line[1].replace('\n', '')

    return SMILES_Dic


def numericalize(jobs, smile):
    tot = {}
    num = 0

    for name in jobs:
        atom = {'Smiles': '', 'donor': {}, 'backbone': {}, 'acceptor': {}}
        #   print(smile[name])
        atom['Smiles'] = smile[name]
        line = smile[name].split('.')
        donor = line[0]
        backbone = line[1]
        acceptor = line[2]
        atom['Name'] = name
        dlet = 1
        for let in donor:
            if let.isalpha() == True:
                atom['donor'][dlet] = let
                dlet += 1
    # print(dlet)

        blet = dlet
        for let in backbone:
            if let.isalpha() == True:
                # blet+=1
                atom['backbone'][blet] = let
                blet += 1
        tot[name] = atom
        alet = blet
        for let in acceptor:
            if let.isalpha() == True:
                atom['acceptor'][alet] = let
                alet += 1
        '''
        print(backbone)


        print(donor)
        backbone = line[1]
        print(backbone)
        acceptor = line[2]
        print(acceptor)
        for let in smile[name]:
            if let.isalpha()==True:
                num += 1
               # print((num,let))

             #   print(let)
        '''

#   print(tot)

    return tot


def homo_lumo_percents(filename,
                       aa,
                       jobname,
                       acceptor=True,
                       backbone=False,
                       donor=False,
                       anchor=False):

    atom = xyzcoords(filename)
    num = amountofbasisfunctions(filename)
    atom_let = atom_num_let_dic(filename)
    start_num_h, end_num_h, start_num_l, end_num_l, occ, vir = lastO(
        filename, num)
    homo = homo_dict(filename, start_num_h, end_num_h, occ)
    lumo = lumo_dict(filename, start_num_l, end_num_l, vir)
    final_homo, final_lumo = summer(homo, lumo, atom_let)
    tot_homo, tot_lumo = total_contrib(final_homo, final_lumo, atom_let)
    mol = {
        'donor': {
            'HOMO': '',
            'LUMO': ''
        },
        'backbone': {
            'HOMO': '',
            'LUMO': ''
        },
        'acceptor': {
            'HOMO': '',
            'LUMO': ''
        },
        'anchor': {
            'HOMO': '',
            'LUMO': ''
        }
    }

    if acceptor == True:
        atom_num_list = []
        for i in aa[jobname]['acceptor'].keys():
            print(i)
            atom_num_list.append(i)
        tot = part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo,
                               tot_lumo, atom_num_list, jobname)

        mol['acceptor']['HOMO'] = tot[1]
        mol['acceptor']['LUMO'] = tot[2]

    #    print((tot,'acceptor'))
    if backbone == True:
        atom_num_list = []
        for i in aa[jobname]['backbone'].keys():
            atom_num_list.append(i)
        tot = part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo,
                               tot_lumo, atom_num_list, jobname)
        #   print((tot,'backbone'))
        mol['backbone']['HOMO'] = tot[1]
        mol['backbone']['LUMO'] = tot[2]
    if donor == True:
        atom_num_list = []
        for i in aa[jobname]['donor'].keys():
            atom_num_list.append(i)
        tot = part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo,
                               tot_lumo, atom_num_list, jobname)
        mol['donor']['HOMO'] = tot[1]
        mol['donor']['LUMO'] = tot[2]
    #   print((tot,'donor'))
    if anchor == True:
        if '7ea' in jobname:
            O = atom_type_O(atom)
            N = atom_type_N(atom)
            S = atom_type_S(atom)
            H = atom_type_H(atom)
            Si = atom_type_Si(atom)
            C = atom_type_C(atom)
            Od = Bond_lengths_O_C(O, C, atom)
            ch = Bond_lengths_H_C(H, C, atom)
            Os = Bond_lengths_H_O(H, O, atom)
            Co = Bond_lengths_O_C(O, C, atom)
            No = Bond_lengths_O_N(O, N, atom)
            tot = Bond_length(atom)
            ang = Bond_angles(atom, tot)
            carboxy = Bond_angle_H_O_C(O, C, atom, tot, ang)
            #print(carboxy)
            amide = Bond_angle_H_O_N(O, C, N, atom, tot, ang)
            atom_num_list = bondistancecheck(amide, tot)
            atom_num_list = bondistancecheck(carboxy, tot)
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
                                            Carboxy=False,
                                            Amide=False,
                                            cyanoacrylic=False,
                                            SI=True)
            tot = part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo,
                                   tot_lumo, atom_num_list, jobname)

            mol['anchor']['HOMO'] = tot[1]
            mol['anchor']['LUMO'] = tot[2]

            pass
        if '2ea' in jobname or '3ea' in jobname or '5ea' in jobname or '11ea' in jobname or '9ea' in jobname or '11ea' in jobname or '6ea' in jobname:
            O = atom_type_O(atom)
            N = atom_type_N(atom)
            S = atom_type_S(atom)
            H = atom_type_H(atom)
            Si = atom_type_Si(atom)
            C = atom_type_C(atom)
            Od = Bond_lengths_O_C(O, C, atom)
            ch = Bond_lengths_H_C(H, C, atom)
            Os = Bond_lengths_H_O(H, O, atom)
            Co = Bond_lengths_O_C(O, C, atom)
            No = Bond_lengths_O_N(O, N, atom)
            tot = Bond_length(atom)
            ang = Bond_angles(atom, tot)
            carboxy = Bond_angle_H_O_C(O, C, atom, tot, ang)
            #print(carboxy)
            amide = Bond_angle_H_O_N(O, C, N, atom, tot, ang)
            atom_num_list = bondistancecheck(amide, tot)
            atom_num_list = bondistancecheck(carboxy, tot)
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
                                            Carboxy=True,
                                            Amide=False,
                                            cyanoacrylic=False,
                                            SI=False)
            tot = part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo,
                                   tot_lumo, atom_num_list, jobname)

            mol['anchor']['HOMO'] = tot[1]
            mol['anchor']['LUMO'] = tot[2]
        if '1ea' in jobname or '4ea' in jobname or '8ea' in jobname:
            O = atom_type_O(atom)
            N = atom_type_N(atom)
            S = atom_type_S(atom)
            H = atom_type_H(atom)
            Si = atom_type_Si(atom)
            C = atom_type_C(atom)
            Od = Bond_lengths_O_C(O, C, atom)
            ch = Bond_lengths_H_C(H, C, atom)
            Os = Bond_lengths_H_O(H, O, atom)
            Co = Bond_lengths_O_C(O, C, atom)
            No = Bond_lengths_O_N(O, N, atom)
            tot = Bond_length(atom)
            ang = Bond_angles(atom, tot)
            carboxy = Bond_angle_H_O_C(O, C, atom, tot, ang)
            #print(carboxy)
            amide = Bond_angle_H_O_N(O, C, N, atom, tot, ang)
            atom_num_list = bondistancecheck(amide, tot)
            atom_num_list = bondistancecheck(carboxy, tot)
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
                                            Carboxy=False,
                                            Amide=False,
                                            cyanoacrylic=True,
                                            SI=False)
            tot = part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo,
                                   tot_lumo, atom_num_list, jobname)

            mol['anchor']['HOMO'] = tot[1]
            mol['anchor']['LUMO'] = tot[2]
        if '10ea' in jobname:
            O = atom_type_O(atom)
            N = atom_type_N(atom)
            S = atom_type_S(atom)
            H = atom_type_H(atom)
            Si = atom_type_Si(atom)
            C = atom_type_C(atom)
            Od = Bond_lengths_O_C(O, C, atom)
            ch = Bond_lengths_H_C(H, C, atom)
            Os = Bond_lengths_H_O(H, O, atom)
            Co = Bond_lengths_O_C(O, C, atom)
            No = Bond_lengths_O_N(O, N, atom)
            tot = Bond_length(atom)
            ang = Bond_angles(atom, tot)
            carboxy = Bond_angle_H_O_C(O, C, atom, tot, ang)
            #print(carboxy)
            amide = Bond_angle_H_O_N(O, C, N, atom, tot, ang)
            atom_num_list = bondistancecheck(amide, tot)
            atom_num_list = bondistancecheck(carboxy, tot)
            # print(atom_num_list)
            atom_num_list = atomnearchecker(
                atom_num_list,
                H,
                O,
                N,
                Si,
                C,
                tot,
                atom,
                ang,
                Carboxy=False,
                Amide=True,
                cyanoacrylic=False,
                SI=False,
            )
            tot = part_tot_contrib(final_homo, final_lumo, atom_let, tot_homo,
                                   tot_lumo, atom_num_list, jobname)

            mol['anchor']['HOMO'] = tot[1]
            mol['anchor']['LUMO'] = tot[2]

        print()

    return mol

def file_reader(path):
        jobs = []
        os.chdir(path)
        for i in os.listdir():
            print(i)
            jobs.append(i)
        os.chdir('../src')

        '''
        with open(file,'r') as fp:
                data = fp.readlines()
                for line in data:
                        jobs.append(line.replace('\n',''))
        '''
        return jobs
def json_reader(json_file,jobs):
    smiles = {}
    with open(json_file,'r') as fp:
        data = json.load(fp)
        for name in jobs:


            smiles[name]=data[name]
    '''
    df = {'Name': name, 'SMILES': smiles}
    df = pd.DataFrame(df)
    print(df)
    
    #  df2 = {'Name':data['name'],"Exc":data['exc'],"method":data[]]}
    df = pd.DataFrame(df)
    print(df)
    df.to_csv('../data_analysis/SMILES_DICT.csv', index=False)
    SMILES_csv = '../data_analysis/SMILES_DICT.csv'
    smile = SMILES_FINDER(SMILES_csv)
    '''

    return smiles


def main():

  #  data = json_pandas_molecule('../json_files/test2.json',
  #                              results_exc=True)
    json_file = '../json_files/smiles.json'
    #print(df['name'])
    #  print(df['SMILES']['1ed_1b_1ea'])

    # print(smile)

    jobs = ['6ed_41b_12ea']
    path_to_MO = '../ds5batchMO_600_800/'  
    jobs = file_reader(path_to_MO)
    jobs = ['9ed_28b_8ea']
    smile = json_reader(json_file,jobs)
    numbs = HOMO_LUMO_dict('../data_analysis/600_800.csv')
    #numbs = HOMO_LUMO_dict('../data_analysis/800_1000.csv')
    print(smile)
    final = {}
    for x in jobs:
       
        #filename = '../MO_start/' + str(x) + '/mo/'+ str(x)+'.out'

        try:
            filename = '../ds5batchMO_600_800/' + str(x) + '/mo/' + str(x) + '.out'
            atom = xyzcoords(filename)
            aa = numericalize(jobs, smile)
            jobname = x
            mol = homo_lumo_percents(filename,
                                     aa,
                                     jobname,
                                     acceptor=True,
                                     backbone=True,
                                     donor=True,
                                     anchor=True)
            final[x] = mol
        except FileNotFoundError:
            print('File Not Found:%s '%filename)
            pass
    df = {
        'Name': [],
        'HOMO Donor': [],
        'LUMO Donor': [],
        'HOMO Backbone': [],
        'LUMO Backbone': [],
        'HOMO Acceptor': [],
        'LUMO Acceptor': [],
        'HOMO Anchor': [],
        'LUMO Anchor': [],
        'LUMO': [],
        'HOMO': [],
        'Wave': [],
    }
    # numbs = HOMO_LUMO_dict('../data_analysis/600_800.csv')
    #numbs = HOMO_LUMO_dict('../data_analysis/800_1000.csv')
 
    for name in final.keys():
        '''

        df['Name']=[name]
        df['HOMO Donor']= [final[name]['donor']['HOMO']]
        df['LUMO Donor']= [final[name]['donor']['LUMO']]
        df['HOMO Backbone']= [final[name]['backbone']['HOMO']]
        df['LUMO Backbone']= [final[name]['backbone']['LUMO']]
        df['HOMO Acceptor']= [final[name]['acceptor']['HOMO']]
        df['LUMO Acceptor']= [final[name]['acceptor']['LUMO']]
        df['HOMO Anchor']= [final[name]['anchor']['HOMO']]
        df['LUMO Anchor']= [final[name]['anchor']['LUMO']]
        '''

        df['Name'].append(name)
        df['HOMO Donor'].append(final[name]['donor']['HOMO'])
        df['LUMO Donor'].append(final[name]['donor']['LUMO'])
        df['HOMO Backbone'].append(final[name]['backbone']['HOMO'])
        df['LUMO Backbone'].append(final[name]['backbone']['LUMO'])
        df['HOMO Acceptor'].append(final[name]['acceptor']['HOMO'])
        df['LUMO Acceptor'].append(final[name]['acceptor']['LUMO'])
        df['HOMO Anchor'].append(final[name]['anchor']['HOMO'])
        df['LUMO Anchor'].append(final[name]['anchor']['LUMO'])

 
        
        df['HOMO'].append(round(float(numbs[name][1]),2))
        df['LUMO'].append(round(float(numbs[name][0]),2))
        df['Wave'].append(round(float(numbs[name][2]),2))
        

    #  print(final[name]['donor']['HOMO'])
    # df['Donor']=final[name]['donor'][1]

#  df = {'Name':final.keys(), 'Donor': final['donor']}

    df = pd.DataFrame(df)
    print(df)
    df.to_csv('../data_analysis/fin.csv', index=False)
    '''
    for key in final.keys():
        print(key)
    '''
    # print(final)

    #  print('Next Molecule\n')
    

    return
if __name__ == '__main__':
    main()
