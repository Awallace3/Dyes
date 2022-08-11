import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D




def convert_df_nm_to_eV(df, columns_convert=["Exp"]):
    h = 6.626e-34
    c = 3e17
    Joules_to_eV = 1.602e-19

    for i in columns_convert:
        df[i] = df[i].apply(lambda x: h * c / (x * Joules_to_eV))

    return df

def lsf_eqn(cam,pbe):
    camc = 1.31
    pbec = -0.47
    print(cam)
    print(pbe)
#    for i in cam:
#        print(i)

    return camc*cam+pbec*pbe

def json_pandas_molecule(path_results, results_exc=False,):

    error = []
    cam_b3lyp = {}
    pbe = {}
    bh = {}
    with open(path_results,'r') as fp:
        data = json.load(fp)
        for line in data:
            try:
            #print(line)
                name = line['name']
                if 'TPA' in name or '36b' in name:
                    pass
                else:
                    generalSMILES = line['generalSMILES']
                    localName = line['localName'] 
                    cam_b3lyp[name]=line['CAM_B3LYP_6_311G_d_p'][0]['nm']
                    pbe[name] = line['PBE1PBE_6_311G_d_p'][0]['nm']
                    bh[name] = line['bhandhlyp_6_311G_d_p'][0]['nm']
            #  print(cam_b3lyp_1)
    #            print(pbepbe_1)
            except IndexError:
                error.append(line['name'])
    #print(error)
    print(len(error))
    #print(cam_b3lyp)
    cam_b3lyp_new = {}
    print(len(cam_b3lyp))
    print(len(pbe))
    print(len(bh))
    print("_________")

    for name in error:
        if name in cam_b3lyp:
            cam_b3lyp.pop(name)
        if name in pbe:
            pbe.pop(name)
        if name in bh:
            bh.pop(name)

    print(len(cam_b3lyp))
    print(len(pbe))
    df = {
        'Name':[],
        'CAM-B3LYP/6-311G(d,p)':[],
        'bhandhlyp/6-311G(d,p)':[],
        'PBE1PBE/6-311G(d,p)':[],
   #     'LSF':[]
    }
    for name in cam_b3lyp.keys():
        df['Name'].append(name)
        df['CAM-B3LYP/6-311G(d,p)'].append(cam_b3lyp[name])
        df['bhandhlyp/6-311G(d,p)'].append(bh[name])
        df['PBE1PBE/6-311G(d,p)'].append(pbe[name])
    df = pd.DataFrame(df)
    print(df)
    df = convert_df_nm_to_eV(df, columns_convert=["CAM-B3LYP/6-311G(d,p)"])
    df = convert_df_nm_to_eV(df, columns_convert=['bhandhlyp/6-311G(d,p)'])
    df = convert_df_nm_to_eV(df, columns_convert=['PBE1PBE/6-311G(d,p)'])
    df['LSF'] = lsf_eqn(df['CAM-B3LYP/6-311G(d,p)'],df['PBE1PBE/6-311G(d,p)'])
    print(df)
    df = df.sort_values(by = ['LSF'],ascending=False)

    print(df)




    return df

def plot(df, outname,                       
        headers_colors=[
                ["CAM-B3LYP/6-311G(d,p)", "blue"],
                ["BHandHLYP/6-311G(d,p)", "red"],
                ["PBE0/6-311G(d,p)", "orange"],
                ["LSF", "green"]],
                ):
   # x = np.arange(0, len(df['Name']), 500)
    amount=[]
    for num,i in enumerate(df['LSF']):
        amount.append(num)

    plt.plot(amount,df['LSF'],                
                label='LSF',
                color='green',
                linewidth=1,)
    plt.plot(amount,df['CAM-B3LYP/6-311G(d,p)'],
                label='CAM-B3LYP/6-311G(d,p)',
                color='blue',
                linewidth=.07,)
    plt.plot(amount,df['bhandhlyp/6-311G(d,p)'],
                label='BHandHLYP/6-311G(d,p)',
                color='red',
                linewidth=.07,)
    plt.plot(amount,df['PBE1PBE/6-311G(d,p)'],
                label='PBE1PBE/6-311G(d,p)',
                color='orange',
                linewidth=.07,)
    #plt.ylim(min(df['LSF']), max(df['LSF']))
    plt.ylim(1.0, max(df['LSF']))

    

    plt.xlabel("Theoretical Dyes")
    plt.ylabel("Excitation Energy (%s)" % 'eV')
    plt.grid(color="grey",
             which="major",
             axis="y",
             linestyle="-",
             linewidth=1.0)
    legend_elements = [
        Line2D([0], [0], color='b',ls="-",  label='CAM-B3LYP/6-311G(d,p)'),
        Line2D([0], [0], c='r', ls="-", label='BHandHLYP/6-311G(d,p)'),
        Line2D([0], [0], c='#FFA500', ls="-", lw=2, label='PBE1PBE/6-311G(d,p)'),
        Line2D([0], [0], color='g', ls='-', label='LSF'),
    ]

    labels = ['CAM-B3LYP/6-311G(d,p)', 'BHandHLYP/6-311G(d,p)', "PBE1PBE/6-311G(d,p)",'LSF']
    plt.legend(legend_elements,labels)
    # print(outname)
    # print(os.getcwd())
    plt.savefig(outname, transparent=True)
    print("graph name:", outname)
    return




def main():
    filename = '../json_files/ds_all5_out.json'
    outname = '../data_analysis/7000.png'
#    filename ="../json_files/results_exc.json"
    df = json_pandas_molecule(filename, results_exc=True)
    print(df)
    
    
    plot(df, outname,
    headers_colors=[
                ["CAM-B3LYP/6-311G(d,p)", "blue"],
                ["BHandHLYP/6-311G(d,p)", "red"],
                ["PBE0/6-311G(d,p)", "orange"],
                ["LSF", "green"]], )
    
    
                
    return
main()