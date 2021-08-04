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
import matplotlib.pyplot as plt


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
    #print(piece_dict)
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
    #print(df['score'])
    return df

def total_allowed_dict(allowed_dict):
    total = 0
    for val in allowed_dict.values():
        if val:
            total += 1
    #print("TOTAL =", total)
    return total

def acquire_allowed(allowed_dict):
    allowed = []
    banned = []
    for key, val in allowed_dict.items():
        if val:
            allowed.append(key)
        else:
            banned.append(key)
    return allowed, banned

def score_piece(df, banned_lst=[], structures=['bb'], col_name='CAM-B3LYP/6-311G(d,p)', score_type='nm', above_score=460):
    """
    Score structures by each piece (EA, ED, or BB)
    score_type can either be 'nm' or 'score'
    above_score sets bar for score to exceed for the average of the piece
        e.g. if the average 'nm' for 1bb < above_score, then it is banned from competing again
    """
    df = score_structures(df)
    allowed_dict = gen_allowed_dict(df)
    pieces = {'ea': [],
        'bb': [],
        'ed': []
    }
    total_allowed_dict(allowed_dict)    
    pos = -1
    for key, allowed in allowed_dict.items():
        score_lst = []
        for index, row in df.iterrows():
            if row['exc'] == 1 and allowed and key in row['name'] and row['method_basis_set'] == col_name:
                name_split = row['name'].split("_")
                for n, i in enumerate(name_split):
                    if i == key:
                        pos = n
                           
                nm = row["nm"]
                f = row['osci']
                LUMO = row["LUMO"]
                score = row['score']
                if score_type == 'score':
                    score_lst.append(score)
                elif score_type == 'nm':
                    score_lst.append(nm)
        if pos == 0:
            pos = 'ea'
        elif pos == 1:
            pos = 'bb'
        elif pos == 2:
            pos = 'ed'        
        score_avg = sum(score_lst)/len(score_lst)
        pieces[pos].append([key, score_avg])
    for key, value in pieces.items():
        if key in structures:
            if key in structures:
                grouping = sorted(value, key=lambda x:x[1], reverse=True)
                length = len(grouping)
                for n, i in enumerate(grouping):
                    #print(i)
                    if i[1] < above_score:
                        allowed_dict[i[0]] = False                    
    total_allowed_dict(allowed_dict)    
    allowed, banned = acquire_allowed(allowed_dict)
    for i in banned:
        banned_lst.append(i)
    #print(allowed, banned_lst, sep='\n')
    return allowed, banned_lst
    
def df_molecules_to_df_method_basisset(df_molecules, method_basis_set=[]):
    df = {
        "Name": [],
    }
    for i in method_basis_set:
        df[i] = []
    df = pd.DataFrame(df)
    #print(df)
    for i1, r1 in df_molecules.iterrows():
        #print(r1['name'])
        #print(df.Name)
        #print(r1['name'] in df.Name)
        """
        method_basis_set_lst = ['-' for i in method_basis_set]
        method_basis_set_lst.insert(0, r1['name'])
        df.loc[len(df)] = method_basis_set_lst
        Names = pd.Series(df['Name'])
        print(df)
        print(r1['name'])
        print(df['Name'])
        print()
        
        break
        """
        Names = [str(i) for i in df['Name'].values]
        if str(r1['name']) not in Names:
            method_basis_set_lst = [i for i in method_basis_set]
            
            for n, j in enumerate(method_basis_set_lst):
                #print(j, r1['method_basis_set'])
                if str(j) == str(r1['method_basis_set']):
                    method_basis_set_lst[n] = r1['nm']
            
            method_basis_set_lst.insert(0, r1['name'])
            #if r1['name'] == "1ed_16b_1ea":
            #    print(method_basis_set_lst)
            df.loc[len(df)] = method_basis_set_lst
        else:
            #df.ix[df['id'] == 12, ['uid','gid']] = ['IN','IN-1']
            for j in method_basis_set:                    
                if str(j) == r1['method_basis_set']:
                    if r1['exc'] == 1:                        
                        df.loc[df['Name'] == r1['name'], [j]] = [r1['nm']]  
    #nm = df.sort_values([method_basis_set[0]], ascending=(False))
    return df

def plot_methods(df, 
        weighted_avg=['CAM-B3LYP/6-311G(d,p)','PBE1PBE/6-311G(d,p)'], 
        headers_colors=[['CAM-B3LYP/6-311G(d,p)', 'blue'], ['BHandHLYP/6-311G(d,p)', 'purple'], ['PBE0/6-311G(d,p)', 'red'], ['Weighted Average', 'green'] ]
    ):
    # 72 hours for calculation for each Dye vs. $10k and 3mnths
    """
    df must be df_method_basisset
    """
    df = df.drop(['Name'], axis=1)
    df = df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
    
    df['Weighted Avg.'] = df[['CAM-B3LYP/6-311G(d,p)','PBE1PBE/6-311G(d,p)']].mean(axis=1)
    df = df.sort_values(['Weighted Avg.'], ascending=False)
    fig = plt.figure(dpi=400)
    dye_cnt = range(len(df['Weighted Avg.']))
    for ind, col in enumerate(df[::-1]):
        print(ind)
        print(headers_colors[ind][0])
        
        plt.plot(
            dye_cnt, list(df[col]),
            label=headers_colors[ind][0],
            color=headers_colors[ind][1], 
            linewidth=1
        )
    plt.title('Methods on Theoretical Dyes')
    plt.xlabel("Theoretical Dyes Sorted by the Weighted Average Excitation Energy")
    plt.ylabel("Excitation Energy (nm)")
    plt.grid(color='grey', which='major',
    axis='y',
    linestyle='-', linewidth=0.2)
    plt.legend()
    plt.savefig("dyes_theor_methods.png")


def plot_methods_exp(
    exp_data={
        "dyes": ['AP25', 'D1', 'D3', 'XY1', 'ZL003'],
        "CAM": [-127.31, -39.04, -22.85, -34.71, -20.29],
        "PBE": [-13.80, 141.99, 238.93, 125.85, 91.99],
        "Weighted": [-89.85, 20.70, 63.54, 18.28, 16.76], 
    }
):
    fig = plt.figure(dpi=400)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.plot(
        exp_data["dyes"], exp_data['CAM'],
        label="CAM-B3LYP/6-311G(d,p)", color='blue',
    )
    plt.plot(
        exp_data["dyes"], exp_data['PBE'],
        label="PBE0/6-311G(d,p)", color='red',
    )
    plt.plot(
        exp_data["dyes"], exp_data['Weighted'],
        label="Weighted Average", color='green',
    )
    zeros = [0 for i in range(len(exp_data['dyes']))]
    plt.plot(
        exp_data["dyes"], zeros,
        '.',
        label="Experiment", color='black',
    )
    plt.grid(color='grey', which='major',
        axis='y',
      linestyle='-', linewidth=0.2)
    plt.title('Methods Compared with Experimental Dyes\n')
    plt.ylim([-150, 300])
    plt.xlabel("Experimental Dyes")
    plt.ylabel("Experimental Difference (nm)")
    plt.legend()
    plt.savefig("dyes_exp_methods.png")


def df_conv_energy(df, min_num=300):
    """
    Converts from nm to eV or eV to nm
    """
    h = 6.626E-34
    c = 2.998E17
    J_over_eV = 1.602E-19
    for col in df:
        if col != 'Name':
            df = df[pd.to_numeric(df[col], errors='coerce').notnull()]
            df[col]= df[col].mask( df[col] > min_num, h*c/(df[col]*J_over_eV) )
    return df
    
def df_diff_std(df, col_names=['CAM-B3LYP/6-311G(d,p)', 'PBE1PBE/6-311G(d,p)']):
    """
    Calculates the difference between two method energies and calculates the std of the differences
    """
    dif_col = "%s - %s" % (col_names[0], col_names[1])
    df[dif_col] = df[col_names[0]] - df[col_names[1]]
    dif_std_col = "std(%s)" % dif_col
    std_val = df[dif_col].std(axis=0)
    mean_val = df[dif_col].mean(axis=0)
    # z_score = x - mu / sig
    df[dif_std_col] = (df[dif_col] -mean_val) / std_val
    df = df.sort_values([dif_std_col], ascending=True )
    datatypes = df.dtypes()
    print(datatypes)
    #df.hist(column=dif_col)
    #plt.show()
    """
    val = pd.qcut(df[dif_col], q=4)
    print(val)
    # print(df[dif_col].describe()) 
    
    bin_labels_5 = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
    results, bin_edges = pd.qcut(df[dif_col],
                            q=[0, .2, .4, .6, .8, 1],
                            labels=bin_labels_5,
                            retbins=True)

    results_table = pd.DataFrame(zip(bin_edges, bin_labels_5),
                                columns=['Threshold', 'Tier'])

    print(results_table)
    """
    #df_hist = df.filter(['Name', dif_std_col], axis=1)
    #print(df_hist)
    
    
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

    
    
        


    # df_method_baisset set 3 lines below
    methods_basissets = ['CAM-B3LYP/6-311G(d,p)', 'bhandhlyp/6-311G(d,p)', 'PBE1PBE/6-311G(d,p)']
    df = df_molecules_to_df_method_basisset(df_molecules, methods_basissets)
    #df.to_csv("out3.csv", index=False)
    #plot_methods(df)
    #plot_methods_exp()
    #df = df_conv_energy(df, 0)
    #df = df_diff_std(df)
    
    """
    """ 
    """
    #name_nm = name_nm_df (df_molecules)
    #df = name_nm_osci_LUMO_df(df_molecules)
    df = name_nm_osci_LUMO_exc_df(df_molecules)
    """
    #df_molecules = score_structures(df_molecules)
    #df_molecules = df_molecules.sort_values(['nm'], ascending=False)
    #print(df_molecules)
    #df_molecules.to_csv('out2.csv')
    allowed, banned = score_piece(df_molecules)
    print("banned = ", banned )


# criteria
# nm : greatest          ::: Higher
# osci : LUMO : second   ::: osci > 0.1 ::: LUMO > -0.9 eg. -0.8 is better
if __name__ == "__main__":
    main()