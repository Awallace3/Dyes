import os
import pandas as pd


def grepper(path):
    os.chdir(path)
    cmd = 'grep ' + 'Excited State   1:' + ' */*/*.out ' + ' >> ' + '../bench.csv'
    os.system(cmd)
    
    return

def name_gather(path):
    with open(str(path) + '/'+ 'bench.csv','r') as file:
        data = file.readlines()
        namelist = []
        for i in data:
            i = i.split('/')
            #print(i)
            name = i[0]
            namelist.append(name)
        namelist = list(dict.fromkeys(namelist))
        #print(namelist)
    return namelist

def pbepbe_gather(path,num):
    with open(str(path) + '/'+ 'bench.csv','r') as file:
        data = file.readlines()
        namelist = []
        tot = []
        for i in data:
            i = i.split('/')
           # print(str(i[2][10:28]))
            if i[1] == 'pbe1pbe' and str(i[2][10:28]) ==  'Excited State   1:' and num == 1:
                name = i[0]
                #print(name)
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
               # print(osci)
                exc_num_1 = i
                tot.append((name,' Excited State 1 ', method,float(abs_eV),float(abs_nm),float(osci))) 

            if i[1] == 'pbe1pbe_dichloromethane' and str(i[2][10:28]) ==  'Excited State   1:' and num == 1:
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 1 ', method,float(abs_eV),float(abs_nm),float(osci))) 

                
                
                #print(exc_num_1)
            if i[1] == 'pbe1pbe' and str(i[2][10:28]) ==  'Excited State   2:' and num == 2: 
                exc_num_2 = i
                name = i[0]
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 2 ', method,float(abs_eV),float(abs_nm),float(osci))) 
            if i[1] == 'pbe1pbe_dichloromethane' and str(i[2][10:28]) ==  'Excited State   2:' and num == 2:
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 2 ', method,float(abs_eV),float(abs_nm),float(osci))) 

            if i[1] == 'pbe1pbe' and str(i[2][10:28]) ==  'Excited State   3:' and num == 3:  
                exc_num_3 = i
                name = i[0]
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 3 ', method,float(abs_eV),float(abs_nm),float(osci)))

            if i[1] == 'pbe1pbe_dichloromethane' and str(i[2][10:28]) ==  'Excited State   3:' and num == 3:
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 3 ', method,float(abs_eV),float(abs_nm),float(osci)))  




            if i[1] == 'mexc' and str(i[2][10:28]) ==  'Excited State   1:' and num == 1:
                name = i[0]
                #print(name)
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
               # print(osci)
                exc_num_1 = i
                tot.append((name,' Excited State 1 ', 'CAM-B3LYP ',float(abs_eV),float(abs_nm),float(osci))) 

            if i[1] == 'mexc_dichloromethane' and str(i[2][10:28]) ==  'Excited State   1:' and num == 1:
                #print(i)
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 1 ', 'CAM-B3LYPdichloromethane',float(abs_eV),float(abs_nm),float(osci))) 





            if i[1] == 'mexc' and str(i[2][10:28]) ==  'Excited State   2:' and num == 2:
                name = i[0]
                #print(name)
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
               # print(osci)
                exc_num_1 = i
                tot.append((name,' Excited State 2 ', 'CAM-B3LYP ',float(abs_eV),float(abs_nm),float(osci))) 

            if i[1] == 'mexc_dichloromethane' and str(i[2][10:28]) ==  'Excited State   2:' and num == 2:
                #print(i)
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 2 ', 'CAM-B3LYPdichloromethane',float(abs_eV),float(abs_nm),float(osci))) 
            

            if i[1] == 'mexc' and str(i[2][10:28]) ==  'Excited State   3:' and num == 3:
                name = i[0]
                #print(name)
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
               # print(osci)
                exc_num_1 = i
                tot.append((name,' Excited State 3 ', 'CAM-B3LYP ',float(abs_eV),float(abs_nm),float(osci)))  

            if i[1] == 'mexc_dichloromethane' and str(i[2][10:28]) ==  'Excited State   3:' and num == 3:
                #print(i)
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 3 ', 'CAM-B3LYPdichloromethane',float(abs_eV),float(abs_nm),float(osci))) 


            
            if i[1] == 'bhandhlyp' and str(i[2][10:28]) ==  'Excited State   1:' and num == 1:
                name = i[0]
                #print(name)
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
               # print(osci)
                exc_num_1 = i
                tot.append((name,' Excited State 1 ', method,float(abs_eV),float(abs_nm),float(osci))) 

            if i[1] == 'bhandhlyp_dichloromethane' and str(i[2][10:28]) ==  'Excited State   1:' and num == 1:
                #print(i)
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 1 ', method,float(abs_eV),float(abs_nm),float(osci))) 
                
            if i[1] == 'bhandhlyp' and str(i[2][10:28]) ==  'Excited State   2:' and num == 2:
                name = i[0]
                #print(name)
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
               # print(osci)
                exc_num_1 = i
                tot.append((name,' Excited State 2 ', method,float(abs_eV),float(abs_nm),float(osci))) 

            if i[1] == 'bhandhlyp_dichloromethane' and str(i[2][10:28]) ==  'Excited State   2:' and num == 2:
                #print(i)
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 2 ', method,float(abs_eV),float(abs_nm),float(osci)))




            if i[1] == 'bhandhlyp' and str(i[2][10:28]) ==  'Excited State   3:' and num == 3:
                name = i[0]
                #print(name)
                method = i[1]
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
               # print(osci)
                exc_num_1 = i
                tot.append((name,' Excited State 3 ', method,float(abs_eV),float(abs_nm),float(osci))) 


                #print(i) 
            if i[1] == 'bhandhlyp_dichloromethane' and str(i[2][10:28]) ==  'Excited State   3:' and num == 3:
                #print(i)
                name = i[0]
                #print(name)
                method = i[1]
             #   print(i[1:])
                abs_eV = i[2][48:56] 
                abs_nm = i[2][58:67]
                osci = i[2][73:80] 
                tot.append((name,' Excited State 3 ', method,float(abs_eV),float(abs_nm),float(osci))) 
           # print(i[1])

     #       name = i[0]
     #       namelist.append(name)
     #   namelist = list(dict.fromkeys(namelist))
     #   print(namelist)
    return tot

def pandadataframe(path,num):
    print(num[0:6])
    ll = {'AP25':[],'DQ5':[],'NKX-2883':[],'S3':[],'HKK-BTZ4':[],'TPA-T-TTAR-A':[],'NL7':[],'NL8':[],'AP3':[], 'NL11':[], 'C271':[], 'WS-8':[], 'IQ4':[], 'WS-55':[], 'SGT-130':[], 'FNE52':[], 'IQ21':[], 'SGT-136':[], 'D-DAHTDTT':[], 'R6':[], 'TPA-TTAR-A':[], 'T-DAHTDTT':[], 'TH304':[], 'NL4':[], 'C258':[], 'TTAR-9':[], 'SGT-121':[], 'TTAR-15':[], 'NL2':[], 'SGT-129':[], 'FNE32':[], 'BTD-1':[], 'Y123':[], 'C272':[], 'FNE34':[], 'IQ6':[], 'TP1':[], 'TTAR-B8':[], 'R4':[], 'TPA-T-TTAR-T-A':[],'ZL003':[],'WS-6':[],'NL4':[],'NL6':[],'JW1':[],'AP25':[],'D1':[],'D3':[],'S-DAHTDTT':[],'XY1':[]}

    exp_values = {
        "TH304": 568,
        "C258": 458,
        "BTD-1": 515,
		"NKX-2883": 552,
		"WS-8": 547,
		"HKK-BTZ4": 540,
		"WS-55": 558,
		"IQ4": 529,
		"FNE52": 526,
		"DQ5": 547,
		"R4": 613,
		"R6": 631,
		"IQ6": 543,
		"IQ21": 557,
		"S3": 628,
		"NL11": 570,
		"FNE32": 596,
		"FNE34": 625,
		"AP3": 650,
		"TP1": 581,
		"TPA-TTAR-A": 498,
		"TTAR-15": 498,
		"S-DAHTDTT": 441,
		"TPA-T-TTAR-A": 413,
		"TTAR-9": 519,
		"D-DAHTDTT": 439,
		"SGT-121": 470.5,
		"SGT-129": 426,
		"SGT-130": 514.5,
		"SGT-136": 531,
		"Y123": 506,
		"NL2": 621,
		"NL4": 657,
		"NL7": 589,
		"NL8": 628,
		"C272": 512,
		"C271": 508,
		"T-DAHTDTT": 434,
		"AP25": 660,
		"D1": 570,
		"D3": 562,
		"XY1": 552,
		"NL6": 605,
		"ZL003": 519,
		"JW1": 590,
	}
    camb3lyp= []
    camb3lypsolv = []
    pbe1pbe = []
    pbe1pbesolv = []


    for i in num:
        #print(i)
        if 'CAM-B3LYP' in i[2] and not 'CAM-B3LYPdichloromethane' in i[2]:
            camb3lyp.append((i[0],i[4],i[5]))
        if 'CAM-B3LYPdichloromethane' in i[2]:
            print(i[2])
            camb3lypsolv.append((i[0],i[4]))

        if 'pbe1pbe' in i[2] and not 'pbe1pbe_dichloromethane' in i[2]:
            pbe1pbe.append((i[0],i[4]))
        
        if 'pbe1pbe_dichloromethane' in i[2]: 
            pbe1pbesolv.append((i[0],i[4]))


        ll[i[0]].append([i[1],i[2],i[3],i[4],i[5]])
  #      df = pd.DataFrame(i[2],columns=['method'])
   # df = pd.DataFrame(df['name'].to_list(),columns = ['name','state','method','abs_eV','abs_nm','osci'])
  #      df.to_csv('../energy.csv',index=False) 

   # for num in exp_values.keys():
   #     ll[num].append(exp_values[num])

   # print(ll['JW1'])
        #print(i)
       # if i[0] == 'AP25':
          
 #       name = i[0]
 #       state = i[1]
 #       method = i[2]
 #       abs_eV = i[3]
 #       abs_nm = i[4]
 #       osci = i[5]
        

   # d = {'name': num}
    #print(ll.items())
    df =  pd.DataFrame(ll,columns=['method']) 
    df = pd.DataFrame(df['method'].to_list(),columns=['name','state','method','abs_eV','abs_nm','osci'])
    #print(num[0])
    print(len(camb3lyp))
    print(len(camb3lypsolv))

    print(len(pbe1pbe))
    print(len(pbe1pbesolv))
  #  df = pd.DataFrame(camb3lypsolv,columns = ['name', 'solvecam_abs_nm'])
    
    df.to_csv('../energy.csv',index=False)
 

    return 


    

def main():
    path_to_benchmarks = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark/results'
    grepper(path_to_benchmarks)
    path_to_bench = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark'
    name_gather(path_to_bench)
    num = pbepbe_gather(path_to_bench,1)

    pandadataframe(path_to_bench,num)

    return
main()
path_to_bench = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark'
os.chdir(path_to_bench)
#os.system('cat ' + 'bench.csv')
os.remove('bench.csv')
    