import os
import  numpy as np
import pandas as pd
from MO_Dict import xyzcoords
from gather_results import json_pandas_molecule
from MO_Dict import *
from homo_lumo_boxer_csv import *
import json
#from gather_results import json_pandas_molecule

def SMILES_FINDER(SMILES_csv):
    filename = open(SMILES_csv,'r')
    data = filename.readlines()
    SMILES_Dic = {}
    for line in data[1:]:
        line = line.split(',')
        SMILES_Dic[line[0]]=line[1].replace('\n','')

    return SMILES_Dic
def numericalize(jobs,smile):
    tot = {
    }
    num = 0
    
    for name in jobs:
        atom = {
            'Smiles':'',
            'donor':{},
            'backbone':{},
            'acceptor':{}
        }
     #   print(smile[name])
        atom['Smiles']=smile[name]
        line = smile[name].split('.')
        donor = line[0]
        backbone = line[1]
        acceptor = line[2]
        atom['Name']=name
        dlet = 1
        for let in donor:
            if let.isalpha()==True:
                atom['donor'][dlet]=let
                dlet+=1
       # print(dlet)
        
        blet = dlet
        for let in backbone:
            if let.isalpha()==True:
               # blet+=1
                atom['backbone'][blet]= let
                blet+=1
        tot[name]=atom
        alet = blet
        for let in acceptor:
            if let.isalpha()==True:
                atom['acceptor'][alet]=let
                alet+=1
         
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
def homo_lumo_percents(filename,aa,jobname,
        acceptor=True,
        backbone = False,
        donor = False,
        anchor = False):
        
    atom = xyzcoords(filename)
    num = amountofbasisfunctions(filename)
    atom_let = atom_num_let_dic(filename)
    start_num_h,end_num_h,start_num_l,end_num_l,occ,vir  = lastO(filename,num) 
    homo = homo_dict(filename,start_num_h,end_num_h,occ)
    lumo = lumo_dict(filename,start_num_l,end_num_l,vir)
    final_homo,final_lumo = summer(homo,lumo,atom_let)
    tot_homo,tot_lumo = total_contrib(final_homo,final_lumo,atom_let)
    mol = {
            'donor':{
            'HOMO':'',
            'LUMO':''
        },
        'backbone':{
            'HOMO':'',
            'LUMO':''
        },
        'acceptor':{
            'HOMO':'',
            'LUMO':''
        },

        'anchor':{
            'HOMO':'',
            'LUMO':''
        }
    }

    

    if acceptor == True:
        atom_num_list = []
        for i in aa[jobname]['acceptor'].keys():
            print(i)
            atom_num_list.append(i)
        tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,jobname)

        mol['acceptor']['HOMO']=tot[1]
        mol['acceptor']['LUMO']=tot[2]

    #    print((tot,'acceptor'))
    if backbone == True:
        atom_num_list = []
        for i in aa[jobname]['backbone'].keys():
            atom_num_list.append(i)
        tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,jobname)
     #   print((tot,'backbone'))
        mol['backbone']['HOMO'] = tot[1]
        mol['backbone']['LUMO'] = tot[2]
    if donor == True:
        atom_num_list = []
        for i in aa[jobname]['donor'].keys():
            atom_num_list.append(i)
        tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,jobname)
        mol['donor']['HOMO'] = tot[1]
        mol['donor']['LUMO'] = tot[2]
     #   print((tot,'donor'))
    if anchor==True:
        if '7ea' in jobname:
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
                                            Carboxy = False,
                                            Amide = False,
                                            cyanoacrylic=False,
                                            SI=True)
            tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,jobname)

            mol['anchor']['HOMO']=tot[1]
            mol['anchor']['LUMO']=tot[2]

            pass
        if '2ea' in jobname or '3ea' in jobname or '5ea' in jobname or '11ea' in jobname or '9ea' in jobname or '11ea' in jobname or '6ea' in jobname:
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
                                            cyanoacrylic=False,
                                            SI=False)
            tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,jobname)

            mol['anchor']['HOMO']=tot[1]
            mol['anchor']['LUMO']=tot[2]
        if '1ea' in jobname or '4ea' in jobname or '8ea' in jobname and '12ea' in jobname and '13ea' in jobname:
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
                                            Carboxy = False,
                                            Amide = False,
                                            cyanoacrylic=True,
                                            SI=False)
            tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,jobname)

            mol['anchor']['HOMO']=tot[1]
            mol['anchor']['LUMO']=tot[2]
        if '10ea' in jobname:
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
                                            Carboxy = False,
                                            Amide = True,
                                            cyanoacrylic=False,
                                            SI=False,)
            tot = part_tot_contrib(final_homo,final_lumo,atom_let,tot_homo,tot_lumo,atom_num_list,jobname)

            mol['anchor']['HOMO']=tot[1]
            mol['anchor']['LUMO']=tot[2]

        



        print()

    return mol

def smiles_reader(file):
    a = open(file)
    data = json.load(a)
    df ={
        'Name':[],
        'SMILES':[]
    }

    for i in data:
        df['Name'].append(i)
        df['SMILES'].append(data[i])
    
    return df

def main():
    
  #  data = json_pandas_molecule('../json_files/results_ds5.json',results_exc=True)
    df = smiles_reader('../json_files/smiles.json')
   # print(data)
    #print(df['name'])
  #  print(df['SMILES']['1ed_1b_1ea'])
  #  df = {'Name':data['name'],'SMILES':data['SMILES']}
  #  df2 = {'Name':data['name'],"Exc":data['exc'],"method":data[]]}
    df = pd.DataFrame(df)
    print(df)
    df.to_csv('../data_analysis/SMILES_DICT.csv',index=False)
    SMILES_csv = '../data_analysis/SMILES_DICT.csv' 
    smile = SMILES_FINDER(SMILES_csv)
   # print(smile)
    
    jobs = ['7ed_29b_10ea','6ed_29b_2ea','10ed_28b_7ea']
    jobs = ['6ed_16b_4ea', '2ed_28b_6ea', '1ed_29b_3ea', '6ed_16b_5ea', '2ed_28b_10ea', '1ed_29b_6ea', '1ed_29b_11ea', '10ed_28b_2ea', '5ed_28b_6ea', '1ed_28b_7ea', '7ed_28b_3ea', '10ed_29b_3ea', '1ed_29b_2ea', '10ed_28b_11ea', '2ed_28b_9ea', '6ed_29b_8ea', '7ed_28b_11ea', '1ed_29b_10ea', '10ed_28b_6ea', '7ed_28b_6ea', '11ed_29b_6ea', '5ed_28b_9ea', '2ed_28b_5ea', '1ed_29b_5ea', '6ed_28b_3ea', '11ed_29b_11ea', '5ed_28b_2ea', '5ed_28b_10ea', '2ed_28b_7ea', '10ed_28b_10ea', '11ed_29b_2ea', '11ed_29b_10ea', '7ed_28b_10ea', '9ed_16b_5ea', '7ed_28b_2ea', '11ed_29b_5ea', '10ed_29b_2ea', '9ed_16b_9ea', '7ed_29b_1ea', '10ed_29b_1ea', '5ed_29b_11ea', '5ed_29b_3ea', '7ed_29b_3ea', '10ed_28b_9ea', '1ed_29b_9ea', '11ed_28b_7ea', '9ed_28b_6ea', '6ed_29b_3ea', '10ed_28b_5ea', '5ed_29b_6ea', '9ed_29b_3ea', '9ed_28b_2ea', '6ed_28b_11ea', '7ed_28b_9ea', '10ed_29b_6ea', '6ed_28b_1ea', '6ed_29b_4ea', '7ed_29b_11ea', '1ed_29b_7ea', '7ed_29b_6ea', '11ed_29b_9ea', '9ed_29b_6ea', '10ed_29b_11ea', '5ed_29b_10ea', '5ed_28b_7ea', '5ed_29b_2ea', '7ed_28b_5ea', '5ed_29b_5ea', '9ed_29b_11ea', '6ed_28b_6ea', '7ed_29b_2ea', '10ed_28b_7ea', '6ed_28b_10ea', '9ed_29b_10ea', '10ed_29b_10ea', '7ed_28b_7ea', '7ed_29b_10ea', '6ed_29b_1ea', '6ed_28b_9ea', '9ed_29b_2ea', '9ed_29b_5ea', '5ed_29b_9ea', '10ed_29b_9ea', '10ed_29b_5ea', '9ed_28b_5ea', '6ed_28b_2ea', '7ed_29b_5ea', '11ed_29b_7ea', '9ed_28b_7ea', '6ed_29b_9ea', '6ed_29b_6ea', '9ed_29b_9ea']
    jobs = ['10ed_29b_7ea', '6ed_28b_7ea', '6ed_29b_10ea', '5ed_29b_7ea', '6ed_16b_5ea', '6ed_29b_9ea', '6ed_29b_6ea', '6ed_29b_2ea', '6ed_29b_11ea', '7ed_28b_7ea', '6ed_29b_5ea', '10ed_28b_7ea', '9ed_29b_7ea', '7ed_29b_9ea', '7ed_29b_10ea']
    jobs = ['5ed_16b_7ea', '6ed_16b_9ea', '7ed_31b_7ea', '6ed_16b_10ea', '6ed_31b_7ea', '6ed_16b_3ea', '2ed_16b_7ea', '6ed_16b_11ea', '6ed_16b_6ea', '7ed_16b_2ea', '10ed_31b_7ea', '7ed_16b_9ea', '6ed_31b_2ea', '7ed_16b_6ea', '9ed_16b_7ea', '3ed_16b_2ea', '2ed_16b_2ea', '1ed_16b_7ea', '7ed_33b_7ea', '7ed_31b_2ea', '7ed_34b_7ea', '10ed_16b_9ea', '10ed_33b_7ea', '10ed_16b_10ea', '6ed_31b_6ea', '6ed_31b_5ea', '7ed_16b_11ea', '7ed_16b_10ea', '6ed_31b_9ea']
    jobs = [ '6ed_16b_3ea', '2ed_16b_7ea', '6ed_16b_11ea', '6ed_16b_6ea', '7ed_16b_2ea', '6ed_31b_2ea',   '3ed_16b_2ea', '2ed_16b_2ea',   ]
    jobs = ['5ed_16b_7ea', '6ed_16b_9ea', '10ed_26b_8ea', '9ed_1b_6ea', '7ed_31b_7ea', '7ed_1b_1ea', '6ed_16b_10ea', '6ed_31b_7ea', '9ed_1b_9ea', '9ed_1b_5ea', '11ed_1b_2ea', '9ed_1b_11ea', '7ed_26b_8ea', '7ed_32b_7ea', '2ed_26b_8ea', '6ed_16b_3ea', '2ed_16b_7ea', '11ed_1b_10ea', '6ed_16b_11ea', '3ed_26b_8ea', '6ed_16b_6ea', '7ed_16b_2ea', '6ed_26b_8ea', '9ed_26b_8ea', '1ed_26b_8ea', '10ed_31b_7ea', '7ed_16b_9ea', '3ed_20b_4ea', '6ed_31b_2ea', '5ed_20b_4ea', '10ed_20b_4ea', '10ed_32b_7ea', '6ed_32b_2ea', '11ed_1b_9ea', '5ed_16b_2ea', '7ed_16b_6ea', '9ed_16b_7ea', '11ed_26b_8ea', '6ed_1b_4ea', '9ed_20b_1ea', '3ed_16b_2ea', '2ed_16b_2ea', '1ed_16b_7ea', '9ed_9b_4ea', '7ed_33b_7ea', '7ed_31b_2ea', '11ed_1b_5ea', '2ed_20b_4ea', '7ed_1b_4ea', '10ed_1b_1ea', '11ed_1b_11ea', '5ed_31b_7ea', '7ed_34b_7ea', '2ed_32b_7ea', '10ed_16b_9ea', '10ed_33b_7ea', '10ed_16b_10ea', '1ed_20b_4ea', '6ed_31b_6ea', '6ed_31b_5ea', '7ed_16b_11ea', '7ed_16b_10ea', '6ed_31b_9ea']
    jobs = ['5ed_16b_7ea', '6ed_16b_9ea', '10ed_26b_8ea', '9ed_1b_6ea', '7ed_31b_7ea', '6ed_16b_10ea', '6ed_31b_7ea', '9ed_1b_9ea', '9ed_1b_5ea', '9ed_1b_11ea', '7ed_32b_7ea', '6ed_16b_3ea', '2ed_16b_7ea', '11ed_1b_10ea', '6ed_16b_11ea', '6ed_16b_6ea', '7ed_16b_2ea', '9ed_26b_8ea', '1ed_26b_8ea', '10ed_31b_7ea', '7ed_16b_9ea', '3ed_20b_4ea', '6ed_31b_2ea', '5ed_20b_4ea', '10ed_20b_4ea', '10ed_32b_7ea', '6ed_32b_2ea', '11ed_1b_9ea', '5ed_16b_2ea', '7ed_16b_6ea', '9ed_16b_7ea', '11ed_26b_8ea', '6ed_1b_4ea', '9ed_20b_1ea', '3ed_16b_2ea', '2ed_16b_2ea', '1ed_16b_7ea', '7ed_33b_7ea', '7ed_31b_2ea', '11ed_1b_5ea', '7ed_1b_4ea', '11ed_1b_11ea', '5ed_31b_7ea', '7ed_34b_7ea', '2ed_32b_7ea', '10ed_16b_9ea', '10ed_33b_7ea', '10ed_16b_10ea', '6ed_31b_6ea', '6ed_31b_5ea', '7ed_16b_11ea', '7ed_16b_10ea', '6ed_31b_9ea']
    jobs = ['5ed_16b_7ea']
  #  jobs = ['7ed_29b_10ea']
    jobs = ['5ed_16b_7ea', '6ed_16b_9ea', '10ed_26b_8ea', '9ed_1b_6ea', '7ed_31b_7ea', '6ed_16b_10ea', '6ed_31b_7ea', '9ed_1b_9ea', '9ed_1b_5ea', '9ed_1b_11ea', '7ed_32b_7ea', '6ed_16b_3ea', '2ed_16b_7ea', '11ed_1b_10ea', '6ed_16b_11ea', '6ed_16b_6ea', '7ed_16b_2ea', '9ed_26b_8ea', '1ed_26b_8ea', '10ed_31b_7ea', '7ed_16b_9ea', '3ed_20b_4ea', '6ed_31b_2ea', '5ed_20b_4ea', '10ed_20b_4ea', '10ed_32b_7ea', '6ed_32b_2ea', '11ed_1b_9ea', '5ed_16b_2ea', '7ed_16b_6ea', '9ed_16b_7ea', '11ed_26b_8ea', '6ed_1b_4ea', '9ed_20b_1ea', '3ed_16b_2ea', '2ed_16b_2ea', '1ed_16b_7ea', '7ed_33b_7ea', '7ed_31b_2ea', '11ed_1b_5ea', '7ed_1b_4ea', '11ed_1b_11ea', '5ed_31b_7ea', '7ed_34b_7ea', '2ed_32b_7ea', '10ed_16b_9ea', '10ed_33b_7ea', '10ed_16b_10ea', '6ed_31b_6ea', '6ed_31b_5ea', '7ed_16b_11ea', '7ed_16b_10ea', '6ed_31b_9ea', '7ed_16b_3ea', '7ed_31b_6ea', '9ed_31b_7ea', '7ed_31b_5ea', '7ed_32b_2ea', '6ed_32b_6ea', '6ed_31b_10ea', '5ed_33b_7ea', '3ed_16b_10ea', '10ed_16b_5ea', '2ed_33b_7ea', '6ed_31b_3ea', '11ed_1b_3ea', '5ed_16b_10ea', '10ed_16b_6ea', '7ed_31b_10ea', '1ed_32b_7ea', '6ed_35b_7ea', '7ed_32b_6ea', '7ed_33b_2ea', '3ed_16b_9ea']
    jobs = ['10ed_29b_7ea', '6ed_28b_7ea', '6ed_29b_10ea', '5ed_29b_7ea', '6ed_16b_5ea', '6ed_29b_9ea', '6ed_29b_6ea', '6ed_29b_2ea', '6ed_29b_11ea', '7ed_28b_7ea', '6ed_29b_5ea', '10ed_28b_7ea', '9ed_29b_7ea', '7ed_29b_9ea', '7ed_29b_10ea', '7ed_29b_2ea', '1ed_29b_7ea', '7ed_29b_6ea', '5ed_28b_7ea', '11ed_29b_7ea', '7ed_29b_5ea', '6ed_28b_2ea', '10ed_29b_9ea', '7ed_29b_11ea', '10ed_29b_10ea']
    jobs = ['5ed_16b_7ea', '6ed_16b_9ea', '10ed_26b_8ea', '9ed_1b_6ea', '7ed_31b_7ea', '6ed_16b_10ea', '6ed_31b_7ea', '9ed_1b_9ea', '9ed_1b_5ea', '9ed_1b_11ea', '7ed_32b_7ea', '6ed_16b_3ea', '2ed_16b_7ea', '11ed_1b_10ea', '6ed_16b_11ea', '6ed_16b_6ea', '7ed_16b_2ea', '9ed_26b_8ea', '1ed_26b_8ea', '10ed_31b_7ea', '7ed_16b_9ea', '3ed_20b_4ea', '6ed_31b_2ea', '5ed_20b_4ea', '10ed_20b_4ea', '10ed_32b_7ea', '6ed_32b_2ea', '11ed_1b_9ea', '5ed_16b_2ea', '7ed_16b_6ea', '9ed_16b_7ea', '11ed_26b_8ea', '6ed_1b_4ea', '9ed_20b_1ea', '3ed_16b_2ea', '2ed_16b_2ea', '1ed_16b_7ea', '7ed_33b_7ea', '7ed_31b_2ea', '11ed_1b_5ea', '7ed_1b_4ea', '11ed_1b_11ea', '5ed_31b_7ea', '7ed_34b_7ea', '2ed_32b_7ea', '10ed_16b_9ea', '10ed_33b_7ea', '10ed_16b_10ea', '6ed_31b_6ea', '6ed_31b_5ea', '7ed_16b_11ea', '7ed_16b_10ea', '6ed_31b_9ea', '7ed_16b_3ea', '7ed_31b_6ea', '9ed_31b_7ea', '7ed_31b_5ea', '7ed_32b_2ea', '6ed_32b_6ea', '6ed_31b_10ea', '5ed_33b_7ea', '3ed_16b_10ea', '10ed_16b_5ea', '2ed_33b_7ea', '6ed_31b_3ea', '11ed_1b_3ea', '5ed_16b_10ea', '10ed_16b_6ea', '7ed_31b_10ea', '1ed_32b_7ea', '6ed_35b_7ea', '7ed_32b_6ea', '7ed_33b_2ea', '3ed_16b_9ea']
    jobs = ['10ed_29b_7ea', '6ed_28b_7ea', '6ed_29b_10ea', '5ed_29b_7ea', '6ed_16b_5ea', '6ed_29b_9ea', '6ed_29b_6ea', '6ed_29b_2ea', '6ed_29b_11ea', '7ed_28b_7ea', '6ed_29b_5ea', '10ed_28b_7ea', '9ed_29b_7ea', '7ed_29b_9ea', '7ed_29b_10ea', '7ed_29b_2ea', '1ed_29b_7ea', '7ed_29b_6ea', '5ed_28b_7ea', '11ed_29b_7ea', '7ed_29b_5ea', '6ed_28b_2ea', '10ed_29b_9ea', '7ed_29b_11ea', '10ed_29b_10ea', '6ed_28b_5ea', '2ed_28b_7ea', '10ed_29b_5ea', '10ed_29b_6ea', '6ed_28b_10ea', '6ed_28b_6ea', '10ed_29b_11ea', '5ed_29b_2ea', '5ed_29b_10ea', '9ed_28b_7ea', '6ed_28b_9ea', '5ed_29b_11ea', '7ed_29b_3ea', '5ed_29b_9ea', '6ed_29b_1ea', '5ed_29b_6ea', '7ed_28b_2ea', '6ed_29b_3ea', '6ed_28b_11ea', '1ed_28b_7ea', '7ed_28b_5ea', '9ed_29b_9ea', '5ed_29b_5ea', '10ed_28b_9ea', '7ed_28b_6ea', '9ed_29b_2ea', '10ed_29b_2ea', '7ed_28b_9ea', '7ed_28b_10ea', '5ed_29b_3ea', '9ed_29b_10ea', '11ed_28b_7ea', '10ed_28b_6ea', '10ed_28b_5ea', '1ed_29b_9ea', '9ed_16b_9ea', '9ed_29b_6ea', '9ed_29b_5ea', '10ed_28b_10ea', '1ed_29b_10ea', '1ed_29b_2ea', '9ed_29b_11ea']
    jobs = ['5ed_10b_4ea', '11ed_8b_9ea', '10ed_9b_4ea', '3ed_9b_4ea', '11ed_6b_1ea', '5ed_9b_4ea', '9ed_22b_11ea', '6ed_22b_4ea', '3ed_10b_4ea', '2ed_21b_4ea', '1ed_1b_5ea', '5ed_13b_1ea', '5ed_22b_1ea', '3ed_13b_1ea', '7ed_15b_3ea', '11ed_8b_3ea', '11ed_14b_1ea', '9ed_7b_8ea', '5ed_2b_8ea', '5ed_6b_4ea', '1ed_7b_1ea', '11ed_21b_1ea', '1ed_9b_1ea', '7ed_13b_4ea', '2ed_20b_1ea', '2ed_10b_4ea', '5ed_7b_4ea', '2ed_2b_8ea', '5ed_21b_4ea', '6ed_8b_1ea', '6ed_3b_8ea', '5ed_2b_1ea', '7ed_8b_8ea', '9ed_9b_1ea', '2ed_7b_4ea', '3ed_6b_4ea', '9ed_10b_4ea', '3ed_7b_4ea', '5ed_14b_4ea', '2ed_13b_1ea', '2ed_9b_1ea', '1ed_17b_4ea', '9ed_17b_4ea', '6ed_2b_4ea', '1ed_1b_11ea', '6ed_3b_1ea', '1ed_8b_3ea', '11ed_22b_5ea', '11ed_22b_10ea', '6ed_15b_1ea', '2ed_6b_4ea', '1ed_9b_8ea', '3ed_4b_3ea', '9ed_6b_4ea', '11ed_22b_9ea', '2ed_4b_3ea', '5ed_20b_1ea', '2ed_2b_1ea', '10ed_3b_1ea', '5ed_24b_8ea', '9ed_14b_8ea', '3ed_4b_1ea', '1ed_10b_4ea', '3ed_2b_1ea', '10ed_20b_8ea', '5ed_2b_4ea', '7ed_3b_1ea', '1ed_7b_4ea', '10ed_13b_4ea', '1ed_13b_1ea', '10ed_24b_1ea', '5ed_32b_7ea', '9ed_13b_8ea', '1ed_1b_3ea', '10ed_24b_8ea', '1ed_6b_4ea', '11ed_22b_3ea', '7ed_2b_4ea', '9ed_21b_8ea', '7ed_15b_1ea', '5ed_24b_1ea', '1ed_22b_1ea', '6ed_8b_4ea', '1ed_2b_1ea', '7ed_3b_8ea', '7ed_22b_8ea', '9ed_22b_1ea', '5ed_4b_3ea', '6ed_24b_1ea', '9ed_14b_4ea', '9ed_21b_4ea', '11ed_9b_1ea', '2ed_4b_1ea', '2ed_22b_4ea', '1ed_15b_2ea', '10ed_25b_1ea', '5ed_25b_1ea', '7ed_8b_1ea', '6ed_25b_1ea', '6ed_24b_8ea', '11ed_22b_11ea', '10ed_8b_1ea', '10ed_3b_8ea', '10ed_2b_4ea', '5ed_3b_1ea', '11ed_13b_1ea', '3ed_3b_1ea', '2ed_15b_3ea', '5ed_4b_1ea', '10ed_22b_4ea', '2ed_9b_4ea', '9ed_2b_8ea', '7ed_22b_4ea', '11ed_6b_4ea', '2ed_3b_1ea', '1ed_24b_1ea', '3ed_13b_4ea', '1ed_3b_1ea', '9ed_25b_1ea', '1ed_2b_8ea', '2ed_22b_8ea', '2ed_8b_8ea', '2ed_25b_1ea', '2ed_24b_1ea', '5ed_3b_8ea', '1ed_14b_4ea', '11ed_17b_4ea', '3ed_1b_1ea', '3ed_15b_3ea', '11ed_3b_1ea', '2ed_13b_4ea', '1ed_21b_4ea', '11ed_7b_8ea', '11ed_24b_1ea', '3ed_22b_4ea', '1ed_25b_1ea', '11ed_25b_1ea', '1ed_20b_1ea', '5ed_8b_1ea', '1ed_9b_4ea', '7ed_25b_1ea', '7ed_24b_1ea', '5ed_20b_8ea', '10ed_8b_8ea', '9ed_9b_8ea', '10ed_22b_8ea', '10ed_25b_8ea', '5ed_25b_8ea', '3ed_24b_1ea', '3ed_25b_1ea', '6ed_25b_8ea', '2ed_2b_4ea', '3ed_3b_8ea', '5ed_22b_4ea', '1ed_24b_8ea', '7ed_1b_8ea', '9ed_13b_4ea', '7ed_3b_4ea', '11ed_13b_8ea', '1ed_13b_4ea', '2ed_24b_8ea', '3ed_2b_4ea', '2ed_3b_8ea', '3ed_8b_8ea', '1ed_21b_8ea', '11ed_21b_4ea', '9ed_2b_4ea', '9ed_3b_8ea', '3ed_22b_8ea', '11ed_24b_8ea', '10ed_24b_4ea', '7ed_24b_8ea', '11ed_14b_4ea', '3ed_15b_1ea', '2ed_15b_1ea', '11ed_22b_1ea', '5ed_22b_8ea', '10ed_8b_4ea', '7ed_8b_4ea', '5ed_24b_4ea', '7ed_25b_8ea', '1ed_4b_1ea', '11ed_7b_4ea', '2ed_8b_1ea', '11ed_2b_8ea', '2ed_25b_8ea', '6ed_25b_4ea', '2ed_1b_1ea', '1ed_4b_3ea', '1ed_3b_8ea', '11ed_25b_8ea', '5ed_15b_3ea', '9ed_3b_4ea', '6ed_24b_4ea', '3ed_3b_4ea', '10ed_25b_4ea', '1ed_25b_8ea', '3ed_8b_1ea', '5ed_1b_1ea', '9ed_24b_4ea', '3ed_24b_8ea']
    
   
   # print(smile)
    jobs = ['16ed_2b_13ea']
    jobs = ['10ed_29b_12ea']
    final = {}

    for x in jobs:
        filename = '../MO_start/' + str(x) + '/mo/'+ str(x)+'.out'

        try:
            atom = xyzcoords(filename)
            aa = numericalize(jobs,smile)
            jobname = x
            mol = homo_lumo_percents(filename,
            aa,   
            jobname,   
            acceptor=True,
            backbone = True,
            donor = True,
            anchor = True)
            final[x]=mol
        except FileNotFoundError:
            print('File Not Found:%s '%filename)
            pass
    df = {
        'Name':[],
        'HOMO Donor':[],
        'LUMO Donor':[],
        'HOMO Backbone':[],
        'LUMO Backbone':[],
        'HOMO Acceptor':[],
        'LUMO Acceptor':[],
        'HOMO Anchor':[],
        'LUMO Anchor':[],
        'HOMO':[],
        'LUMO':[],
        'Wave':[],
    }
   # numbs = HOMO_LUMO_dict('../data_analysis/600_800.csv')
    numbs = HOMO_LUMO_dict('../data_analysis/800_1000.csv')



    
    
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
    df.to_csv('fin.csv',index=False)
    
    '''
    for key in final.keys():
        print(key)
    '''
   # print(final)
        
    
        







        

      #  print('Next Molecule\n')
        










    

    return
if __name__ == '__main__':
    main()
