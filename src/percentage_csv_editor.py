from hashlib import new
import pandas as pd
import json

def csv_names(file):
    name = []
    with open(file,'r') as fp:
        data = fp.readlines()
        for line in data[1:]:
            line=line.split(',')
            name.append(line[0])
    return name

def json_reader(json_file):
    red = {}
    with open(json_file,'r') as fp:
        data = json.load(fp)
        for mol in data:
            #print(mol['nam'])
           # print(mol['lsf'])
            for exc in mol['lsf']:
                if exc['exc']==1:
                    #print(exc)
                    red[mol['name']] =  (exc['nm'],exc['HOMO'],exc['LUMO'])
   # print(red)
   # print(red)
                #print(exc)
        #    for exc in mol['name']:
        #        print(exc['lsf'])

        #    print(mol['name']['lsf'])
     #   for mol in data["molecules"]:
     #       for exc in mol["lsf"]:
     #           if exc['exc']==1:
        #    red[mol['name']] =  (exc['nm'],exc['HOMO'],exc['LUMO'])
    return red

def df_adder(filename,names,red,output):
    new_dict = {}
    for name in names:
        if name in red.keys():
            #print(name)
            new_dict[name]=red[name]
    #print(new_dict)
    df_2 = pd.read_csv(filename)
  #  print(df_2)
    
    
    

   
              #  print(df_2['HOMO Donor'])


     #   print((line,'HELPP'))
    
    df = {
    'name':[],
    'HOMO Donor':[],
    'LUMO Donor':[],
   
    'HOMO Backbone':[],
    'LUMO Backbone':[],
    'HOMO Acceptor':[],
    'LUMO Acceptor':[],
    'HOMO Anchor':[],
    'LUMO Anchor':[],
    

    'homo': [],
    'lumo':[],
    'wave': []
    }
    '''
    
    for name in names:
    #print(df_2[0])
        ll = df_2.loc[df_2['Name'] == name]
        a = ll['HOMO Donor'].to_string()
        a = str(a[4:])
        df['HOMO Donor'].append(a)

        b = ll['LUMO Donor'].to_string() 
        b = str(b[4:])
        df['LUMO Donor'].append(b)
        

        c = ll['HOMO Backbone'].to_string() 
        c = str(c[4:])
        df['HOMO Backbone'].append(c)
        

        d = ll['LUMO Backbone'].to_string() 
        d = str(d[4:])
        df['LUMO Backbone'].append(d)
        

        e = ll['HOMO Acceptor'].to_string() 
        e = str(e[4:])
        df['HOMO Acceptor'].append(e)
        

        h = ll['LUMO Acceptor'].to_string() 
        print(h)
        h = str(h[4:])
        df['LUMO Acceptor'].append(h)
        

        i = ll['HOMO Anchor'].to_string() 
        i = str(i[4:])
        df['HOMO Anchor'].append(i)
        

        k = ll['LUMO Anchor'].to_string() 
        k = str(k[4:])
        df['LUMO Anchor'].append(k)
    '''
        








    error = []
   # ignore = ['2ed_29b_7ea', '2ed_29b_5ea', '2ed_29b_11ea', '2ed_29b_10ea', '2ed_29b_9ea', '2ed_29b_6ea', '2ed_29b_2ea', '2ed_29b_3ea', '2ed_29b_1ea', '2ed_29b_4ea', '9ed_29b_1ea', '2ed_29b_8ea', '9ed_30b_7ea', '9ed_33b_11ea', '9ed_29b_8ea', '2ed_30b_5ea', '9ed_30b_11ea', '9ed_30b_2ea', '2ed_30b_1ea', '2ed_36b_5ea', '2ed_30b_4ea', '2ed_30b_8ea']
#    ignore = ['9ed_32b_8ea', '10ed_35b_5ea', '2ed_35b_3ea', '10ed_33b_4ea', '2ed_8b_4ea', '2ed_30b_6ea', '2ed_35b_8ea', '2ed_35b_11ea', '2ed_34b_8ea', '9ed_1b_3ea', '2ed_35b_10ea', '2ed_34b_7ea', '2ed_35b_7ea', '10ed_16b_2ea', '9ed_34b_2ea', '2ed_35b_5ea', '2ed_35b_1ea', '9ed_33b_4ea', '2ed_34b_5ea', '2ed_31b_7ea', '2ed_30b_7ea', '11ed_10b_9ea', '2ed_34b_6ea', '2ed_31b_1ea', '9ed_31b_1ea', '2ed_31b_9ea', '2ed_35b_9ea', '9ed_33b_1ea', '9ed_35b_10ea', '2ed_34b_2ea', '2ed_35b_4ea', '9ed_34b_11ea', '2ed_31b_10ea', '1ed_8b_9ea', '2ed_34b_3ea', '2ed_34b_11ea']
    ignore = ['9ed_32b_8ea', '10ed_35b_5ea', '2ed_35b_3ea', '10ed_33b_4ea', '2ed_8b_4ea', '2ed_30b_6ea', '2ed_35b_8ea', '2ed_35b_11ea', '2ed_34b_8ea', '9ed_1b_3ea', '2ed_35b_10ea', '2ed_34b_7ea', '2ed_35b_7ea', '10ed_16b_2ea', '9ed_34b_2ea', '2ed_35b_5ea', '2ed_35b_1ea', '9ed_33b_4ea', '2ed_34b_5ea', '2ed_31b_7ea', '2ed_30b_7ea', '11ed_10b_9ea', '2ed_34b_6ea', '2ed_31b_1ea', '9ed_31b_1ea', '2ed_31b_9ea', '2ed_35b_9ea', '9ed_33b_1ea', '9ed_35b_10ea', '2ed_34b_2ea', '2ed_35b_4ea', '9ed_34b_11ea', '2ed_31b_10ea', '1ed_8b_9ea', '2ed_34b_3ea', '2ed_34b_11ea']
    names_2 = []
    for name in names:
        if name in ignore:
            print(name)
        else:
            names_2.append(name)
    
    
    for name in names_2:
        try:
            
            ll = df_2.loc[df_2['Name'] == name]
          #  print(ll)
            a = ll['HOMO Donor'].to_string()
         #   print(a)
            a = str(a[4:])
            df['HOMO Donor'].append(a)

            b = ll['LUMO Donor'].to_string() 
            b = str(b[4:])
            df['LUMO Donor'].append(b)
            

            c = ll['HOMO Backbone'].to_string() 
            c = str(c[4:])
            df['HOMO Backbone'].append(c)
            

            d = ll['LUMO Backbone'].to_string() 
            d = str(d[4:])
            df['LUMO Backbone'].append(d)
            

            e = ll['HOMO Acceptor'].to_string() 
            e = str(e[4:])
            df['HOMO Acceptor'].append(e)
            

            h = ll['LUMO Acceptor'].to_string() 
            print(h)
            h = str(h[4:])
            df['LUMO Acceptor'].append(h)
            

            i = ll['HOMO Anchor'].to_string() 
            i = str(i[4:])
            df['HOMO Anchor'].append(i)
            

            k = ll['LUMO Anchor'].to_string() 
            k = str(k[4:])
            df['LUMO Anchor'].append(k)
            

            
            df['name'].append(name)
            df['wave'].append(new_dict[name][0])
            df['lumo'].append(new_dict[name][1])
           # df['lumo'].append(new_dict[name][2])
            df['homo'].append(new_dict[name][2])
           # df['homo'].append(new_dict[name][1])
        except KeyError:
            df['name'].append(name)
            df['HOMO Donor'].append('Key Error')
            df['LUMO Donor'].append('Key Error')
            df['HOMO Backbone'].append('Key Error')
            df['LUMO Backbone'].append('Key Error')
            df['HOMO Acceptor'].append('Key Error')
            df['LUMO Acceptor'].append('Key Error')
            df['HOMO Anchor'].append('Key Error')
            df['LUMO Anchor'].append('Key Error')
            df['wave'].append('Key Error')
            df['lumo'].append('Key Error')
            df['homo'].append('Key Error')
            error.append(name)
    print('Dyes with key error')
    print(error)
    print(len(error))
    df = pd.DataFrame(df)
    print(df)
    #    print(name)
        
    #    wave.append(new_dict[name][0])
    #    lumo.append(new_dict[name][1])
    #    homo.append(new_dict[name][2])
    
        
    #df['LUMO Energy']=lumo
    #df['HOMO Energy']=homo
    #df['Wave']=wave
    df.to_csv('../data_analysis/%s.csv' % output,index=False)
    
   # print(df)
   
    
    


    return df



def main():
 #   filename = '../data_analysis/percentages_800to1000.csv'
 #   namer = '../data_analysis/names_for_paper_800_to_1000.csv'
 #   filename = '../data_analysis/names_for_paper_600_to_800.csv'
    namer = '../data_analysis/names_for_paper_600_to_800.csv'
    namer = '../data_analysis/600_final_before_scoring.csv'
 #   filename = '../data_analysis/fin_800.csv'
    filename = '../data_analysis/percentages.csv'
#    filename = '../data_analysis/test.csv'

    json_file = '../json_files/ds_all5_out.json'
#    output_file = '../data_analysis/800_final_before_scoring'
    output_file = '../data_analysis/600_all_before_scoring'

    names = csv_names(filename)
  #  names = csv_names(namer)
    print(len(names))
    red = json_reader(json_file)
    print(red)
    df_adder(filename,names,red,output_file)




 #   dataframe_editor(filename,json_file)

    return
main()
