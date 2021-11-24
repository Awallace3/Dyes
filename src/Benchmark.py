import os
from error_mexc_dyes_v2 import gaussianInputFiles

def smilesinput(SMILES,name,path):
    '''
    code needs smiles str from ChemDraw
    the name is also what the directory name is going to be
    '''
    os.chdir(path)
    try:
        error = 0
        os.mkdir(str(name))
        os.chdir(str(name))
        filename = open(str(name + '.smi'),'w')
        filename.write(SMILES)
    except FileExistsError:
        error = 1
        print('This Dye name already exists')
       
    return error

def obabelxyzconverter(name, path):
    cmd = 'obabel ' + str(name) + '.smi ' + '-oxyz --Gen3D -O ../tmp.txt'
    os.system(cmd) 
    return
def coordsexteditor(path):
    #print(path,'AAAAAAAA')
    os.system('ls')
    print(' ')
    print(' ')
    filename = open('../tmp.txt','r')
    data = filename.readlines()
    data.pop(0)
    data.pop(0)
   # print(data)
    filename2 = open('../tmp.txt', 'w+')
    for i in data:
        filename2.write(i)
#    filename2.write('\n')

    return

def xyzadder(path):
    filename = open('../tmp' + '.txt','r')
    data = filename.readlines()
   # print(data)
    filename2 = open('mex.com', 'a')
    for coords in data:
        print(coords)
        filename2.write(coords)
    filename2.write('\n')
    filename.close()
    filename2.close()
    filename3 = open('mex.com', 'r')
    data = filename3.readlines()
   # print(data[6:])
    data.pop(7)
    filename4 = open('mex.com', 'w+')
    for i in data:
        filename4.write(i)

  #  print(data)
    return



def main():

    path_to_benchmark = '../Benchmark/results'
    SMILES = input('What is the SMILES str for Benchmark Dye ')
    name = input('What is the name of Benchmark Dye ')
#    SMILES = 'CCCC'
#    name = 'TESTTTTT'
    error = smilesinput(SMILES,name,path_to_benchmark)
    if error == 1:
        print(path_to_benchmark + '/' + name)
    else:
       
        obabelxyzconverter(name, path_to_benchmark)
        path_to_coords = path_to_benchmark + '/'  + str(name)
        coordsexteditor(path_to_benchmark + '/'  + str(name)) 
        dir_name = name
      #  os.chdir(path_to_benchmark + '/'  + str(name))
        xyzadder(path_to_benchmark + '/'  + str(name))
        os.chdir('..')

        gaussianInputFiles(output_num='0', method_opt='B3LYP', 
                            basis_set_opt='6-311G(d,p)', mem_com_opt='1600', 
                            mem_pbs_opt='10', cluster='map', 
                            baseName='mex', procedure='OPT',
                            data='', dir_name=str(name), solvent='', 
                            outName='mex_o'
                            )
        os.system('rm tmp.txt')
    #    xyzadder(path_to_benchmark + '/'  + str(name))
    return
main()

# Delcamp Dyes: ['D35','NL5','NL3','NL12','NL13']
# Delcamp Dyes: ['NL3','NL5','NL12','NL13','ND1','ND2','ND3','AP11','AP14','AP16','AP17','RR6','YZ7','YZ12','YZ15','JD21','C218']




