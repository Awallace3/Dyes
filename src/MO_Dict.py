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
    

    #print(tot_lumo)


    return name,round(per_homo,2),round(per_lumo,2)


def main():
    jobs = ['6ed_16b_10ea']
    jobs = ['16ed_35b_8ea']
    jobs = ['13ed_18b_12ea', '6ed_41b_12ea','7ed_1b_13ea','7ed_3b_13ea','9ed_18b_12ea']
    jobs = ['7ed_1b_13ea']
    json_file = '../json_files/test2.json'



    for name in jobs:

        filename = '../MO_start/' + str(name) + '/mo/'+ str(name)+'.out'

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
                                        Amide = True,
                                        cyanoacrylic=True,
                                        SI=False)
       # print(atom_num_list)
        
          

        kkk = {}
       
        for i in atom_num_list:
            for x in atom['atom_num']:
    #for i in range(1,50):
 #           for i in atom['atom_num']:
                dis = tot[str(i)+' '+str(x)]
                
        #        print(dis)
                if dis <= 1:
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
        total[name]=[tot[0],tot[1],tot[2]]
        print(total)
       # total['HOMO']=tot[1]
       # total['LUMO']=tot[2]
  #  file = '../data_analysis/600_800.csv'
    
#    file = '../data_analysis/800_1000.csv'
    
#    numbs = HOMO_LUMO_dict(file)
    
            

    
            
    
   
        

          

    name1 = []
    homo = []
    lumo = []
    wave = []
    for name in total.keys():
        with open(json_file,"r") as read_file:
            data = json.load(read_file)
            for mol in data["molecules"]:
                if mol['name']== name:
                    for exc in mol["lsf"]:
                        if exc['exc']==1:
                            homo.append(exc['HOMO'])
                            lumo.append(exc['LUMO'])
                            wave.append(exc['nm'])
        name1.append(name)


    df= {"Name":name1,
        "HOMO":homo,
        "LUMO":lumo,
        "Wave":wave
        }
    df = pd.DataFrame(df)

    df.to_csv('lll.csv',index=False)
    
    print(df)


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
 
