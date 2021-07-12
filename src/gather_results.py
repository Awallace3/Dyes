import os
import glob
import subprocess
from numpy import testing
import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.function_base import average
from numpy.lib.shape_base import split
import pandas as pd
import json
import io

# Genetic algorithm in the future?

"""
json_pandas_molecules dataframe

    'name', 'exc', 'nm','osci', 'method_basis_set', 'orbital_Numbers', 'HOMO','LUMO', 'generalSMILES', 'localName', 'parts',  'SMILES' 

"""

def json_pandas_molecule():
    dat = pd.read_json('results.json')

    FIELDS = ["name", "localName", "generalSMILES"]
    df = pd.json_normalize(dat["molecules"])
    df[FIELDS]
    #['A', 'B', 'C'] <-this is your columns order
    df = df[[
            'name', 'parts',
            'generalSMILES','localName',
            'SMILES', 'excitations',
            'HOMO', 'LUMO',
            ]]
    df = pd.json_normalize(data=dat['molecules'], record_path='excitations', 
                            meta=['name', 'HOMO','LUMO', 'SMILES', 'generalSMILES','localName', 'parts' ])
    df = df [[
    'name', 'exc', 'nm','osci', 'method_basis_set', 'orbital_Numbers', 'HOMO','LUMO', 'generalSMILES', 'localName', 'parts',  'SMILES' 
    ]]
    return df

"""
Excitation pandas:::

    LocalName   generalSMILES   Excitation1 Excitation2 Excitation3 

"""

def nm_osci_df (df):
    nm_osci = df[["nm", 'osci', 'generalSMILES']]
    nm_osci = nm_osci.sort_values(['nm', 'osci'], ascending=(False, False))
    #print(nm_osci.head(10))
    return nm_osci

def name_nm_df (df):
    name_nm = df[["name", 'nm']]
    return name_nm

def name_nm_osci_LUMO_df (df):
    df = df[["name", 'nm', 'osci', 'LUMO']]
    return df

def name_nm_osci_LUMO_exc_df (df):
    df = df[["name", 'nm', 'osci', 'LUMO', 'exc']]
    return df

def gen_allowed_dict (df):
    # add logic for filtering through df to determine if flagged or not
    allowed_dict = {}
    for index, row in df.iterrows():
        names = row["name"].split('_')
        a, b, d = names[0], names[1], names[2]
        for i in names:
            allowed_dict[i] = True
    return allowed_dict


def acquire_averages(df, piece_dict, allowed_dict ):
    for key, val in  piece_dict.items():
        data = {
            'nm': [],
            'osci': [],
            'LUMO': []
            }
        for index, row in df.iterrows():
            d, b, a = row['name'].split("_")
            #print(row)
            if key in row['name'] and allowed_dict[d] and allowed_dict[b] and allowed_dict[a] and row['exc']==1:
                data['nm'].append(row['nm'])
                data['osci'].append(row['osci'])
                data['LUMO'].append(row['LUMO'])
        
        #std_nm = np.std(np.array(data['nm']))

        avg_nm = sum(data['nm']) / len(data['nm'])
        #print(avg_nm)
        avg_osci = sum(data['osci']) / len(data['osci'])
        avg_LUMO = sum(data['LUMO']) / len(data['LUMO'])
        piece_dict[key] = [avg_nm, avg_osci, avg_LUMO]
    print(piece_dict)
    for key, value in piece_dict.items():
        #print(key, value[0])
        print("KEY: %s, nm: %.1f" % (key, value[0]))
    print()
    
    return piece_dict

def evalAllowed(piece_dict, allowed_dict):
    for key, val in piece_dict.items():
        if val[0] < 430:
            allowed_dict[key] = False
        if val[1] < 0.1:
            allowed_dict[key] = False
        if val[2] > -0.9:
            allowed_dict[key] = False
    
    return allowed_dict
        
       

def score_pieces (df):
    # split name by _ 
    # for each unique eAccptor, eDonor, backbone -> tally score with weighted targets
    # Could a system of equations be employed to solve for "average" contribution from each piece?
    
    allowed_dict = gen_allowed_dict(df)

    eA_dict = {}
    eD_dict = {}
    bb_dict = {}
    for i in df['name']:
        name = i.split('_')
        eA, eD, bb = name[0], name[2], name[1]
        eA_dict[eA] = [0, 0, 0] # nm_avg, osci_avg, 
        eD_dict[eD] = [0, 0, 0]
        bb_dict[bb] = [0, 0, 0]
    '''
    Need to update to 
    if LUMO < -0.9:
        0.5*lambda/650 + 0.3*f + 0.2*LUMO/-0.1.3
    '''
    #bb_dict = acquire_averages(df, bb_dict, allowed_dict)
    #eA_dict = acquire_averages(df, eA_dict, allowed_dict)
    #eD_dict = acquire_averages(df, eD_dict, allowed_dict)

    #allowed_dict = evalAllowed(bb_dict, allowed_dict)
    #allowed_dict = evalAllowed(eA_dict, allowed_dict)
    #allowed_dict = evalAllowed(eD_dict, allowed_dict)
    

    #print(allowed_dict)

    return 

'''
col = df.loc[: , "salary_1":"salary_3"]
where "salary_1" is the start column name and "salary_3" is the end column name

df['salary_mean'] = col.mean(axis=1)
'''

def score_structures(df):
    """
    score_col = []
    for index, row in df.iterrows():
        if row["exc"] == 1:
            nm = row["nm"]
            f = row["osci"]
            LUMO = row["LUMO"]
            if LUMO > -0.9:
                score = NaN
            else:
                score = 0.7*nm/650 + 0.2*f + 0.1*LUMO/-1.3
            print(score)
            score_col.append(score)
    """
    df["score"] = 0.85*df["nm"]/650 + 0.10*df['osci'] + 0.05*df['LUMO']/-1.3
    print(df['score'])
    return df

def score_piece(df):
    df = score_structures(df)
    allowed_dict = gen_allowed_dict(df)
    print(allowed_dict)
    pieces = {'ea': [],
        'bb': [],
        'ed': []
    }
    pos = -1
    for key, allowed in allowed_dict.items():
        score_lst = []
        for index, row in df.iterrows():
            if row['exc'] == 1 and allowed and key in row['name'] :
                name_split = row['name'].split("_")
                for n, i in enumerate(name_split):
                    if i == key:
                        pos = n
                        
                
                nm = row["nm"]
                f = row['osci']
                LUMO = row["LUMO"]
                score = row['score']
                score_lst.append(score)
        if pos == 0:
            pos = 'ea'
        elif pos == 1:
            pos = 'bb'
        elif pos == 2:
            pos = 'ed'
        score_avg = sum(score_lst)/len(score_lst)
        pieces[pos].append([key, score_avg])

    for key, value in pieces.items():
        grouping = sorted(value, key=lambda x:x[1], reverse=True)
        length = len(grouping)
        #grouping = grouping[:length//2]
        #print(grouping)
        for n, i in enumerate(grouping):
            if n > length//2:
                allowed_dict[i[0]] = False
    print(allowed_dict)
    

def main():
    
    location = os.getcwd().split('/')[-1]
    if location == 'src':
        os.chdir("..")
    elif location == 'results':
        os.chdir("..")
    else:
        print("need to be in src, results or Dyes directory")
    # need to add a 
    df_molecules = json_pandas_molecule()
    
    
    #name_nm = name_nm_df (df_molecules)
    #df = name_nm_osci_LUMO_df(df_molecules)
    df = name_nm_osci_LUMO_exc_df(df_molecules)

    #score_pieces(df)
    """
    df_molecules = score_structures(df_molecules)
    df_molecules = df_molecules.sort_values(['nm'], ascending=False)
    df_molecules.to_csv('out2.csv')
    """
    score_piece(df_molecules)


# criteria
# nm : greatest          ::: Higher
# osci : LUMO : second   ::: osci > 0.1 ::: LUMO > -0.9 eg. -0.8 is better
if __name__ == "__main__":
    main()