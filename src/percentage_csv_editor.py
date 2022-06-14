import pandas as pd
import json

def csv_names(file):
    name = []
    with open(file,'r') as fp:
        data = fp.readlines()
        for line in data:
            line=line.split(',')
            name.append(line[0])
    return name

def json_reader(json_file):
    red = {}
    with open(json_file,'r') as fp:
        data = json.load(fp)
        for mol in data["molecules"]:
            for exc in mol["lsf"]:
                if exc['exc']==1:
                    red[mol['name']] =  (exc['nm'],exc['HOMO'],exc['LUMO'])
    return red

def df_adder(filename,names,red,output):
    new_dict = {}
    for name in names:
        if name in red.keys():
            new_dict[name]=red[name]
    #print(new_dict)
    df = pd.read_csv(filename)
    #print(df)
    wave=[]
    lumo=[]
    homo = []
    for name in df['Name']:
        wave.append(new_dict[name][0])
        lumo.append(new_dict[name][1])
        homo.append(new_dict[name][2])
    df['LUMO Energy']=lumo
    df['HOMO Energy']=homo
    df['Wave']=wave
    df.to_csv('../data_analysis/%s.csv' % output,index=False)
    
    print(df)
    


    return df



def main():
    filename = '../data_analysis/percentages_800to1000.csv'
    filename = '../data_analysis/percentages.csv'
    #filename = '../data_analysis/fin_800.csv'

    json_file = '../json_files/test2.json'
    output_file = '../data_analysis/800_final_before_scoring'
    output_file = '../data_analysis/600_final_before_scoring'

    names = csv_names(filename)
    red = json_reader(json_file)
    df_adder(filename,names,red,output_file)




 #   dataframe_editor(filename,json_file)

    return
main()
