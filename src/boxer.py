import os
import json

def box0(x):
    red = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        #print(data["molecules"][1])
        for mol in data["molecules"]:
            #print(mol['name'])
            cam,pbe= 0,0
            camhomo,camlumo = 0,0
            pbehomo,pbelumo = 0,0
            for exc in mol["excitations"]:
                if exc['exc'] == 1:
                    if exc["method_basis_set"]=='CAM-B3LYP/6-311G(d,p)':
                        cam += exc['nm']
                        camhomo += exc['HOMO']
                        camlumo += exc['LUMO']

                    if exc["method_basis_set"]=='PBE1PBE/6-311G(d,p)':
                        pbe += exc['nm']
                        pbehomo += exc['HOMO']
                        pbelumo += exc['LUMO'] 

            try:
                lsf =  1239.84/cam * 1.25471048 + 1239.84/pbe * -0.4079027  # nm
                lsfhomo = -abs((camhomo+4.5)*-0.36764963) +-abs((pbehomo+4.5)*-0.38964081) # NHE
                lsflumo = -abs((camlumo+4.5)*-0.95798195) +-abs((pbelumo+4.5)*0.93317353) # NHE 

                #print(lsf)
                lsf = 1239.84/lsf
                #print(lsf)
                if lsf >=800 and lsf <= 1000:
                    red.append((mol['name'],'cam: '+ str(cam),'pbe: ' + str(pbe),'lsf: '+ str(round(lsf,2)),'HOMO: '+str(lsfhomo),'LUMO: '+str(lsflumo)))
            except ZeroDivisionError:
               # pass
                print((mol['name'],'Excited states is zero in .json '))
        for i in red:
            i
                        

    return red


def box1(x):
    red = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        #print(data["molecules"][1])
        for mol in data["molecules"]:
            #print(mol['name'])
            cam,pbe= 0,0
            camhomo,camlumo = 0,0
            pbehomo,pbelumo = 0,0
            for exc in mol["excitations"]:
                if exc['exc'] == 1:
                    if exc["method_basis_set"]=='CAM-B3LYP/6-311G(d,p)':
                        cam += exc['nm']
                        camhomo += exc['HOMO']
                        camlumo += exc['LUMO']

                    if exc["method_basis_set"]=='PBE1PBE/6-311G(d,p)':
                        pbe += exc['nm']
                        pbehomo += exc['HOMO']
                        pbelumo += exc['LUMO'] 

            try:
                lsf =  1239.84/cam * 1.25471048 + 1239.84/pbe * -0.4079027  # nm
                lsfhomo = -abs((camhomo+4.5)*-0.36764963) +-abs((pbehomo+4.5)*-0.38964081) # NHE
                lsflumo = -abs((camlumo+4.5)*-0.95798195) +-abs((pbelumo+4.5)*0.93317353) # NHE 

                #print(lsf)
                lsf = 1239.84/lsf
                #print(lsf)
                if lsf >=600 and lsf < 800:
                    red.append((mol['name'],'cam: '+ str(cam),'pbe: ' + str(pbe),'lsf: '+ str(round(lsf,2)),'HOMO: '+str(lsfhomo),'LUMO: '+str(lsflumo)))
            except ZeroDivisionError:
               # pass
                print((mol['name'],'Excited states is zero in .json '))
        for i in red:
            i
                        

    return red

def box2(x):
    orange = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        #print(data["molecules"][1])
        for mol in data["molecules"]:
            #print(mol['name'])
            cam,pbe= 0,0
            camhomo,camlumo = 0,0
            pbehomo,pbelumo = 0,0
            for exc in mol["excitations"]:
                if exc['exc'] == 1:
                    if exc["method_basis_set"]=='CAM-B3LYP/6-311G(d,p)':
                        cam += exc['nm']
                        camhomo += exc['HOMO']
                        camlumo += exc['LUMO']

                    if exc["method_basis_set"]=='PBE1PBE/6-311G(d,p)':
                        pbe += exc['nm']
                        pbehomo += exc['HOMO']
                        pbelumo += exc['LUMO'] 

            try:
                lsf =  1239.84/cam * 1.25471048 + 1239.84/pbe * -0.4079027  # nm
                lsfhomo = -abs((camhomo+4.5)*-0.36764963) +-abs((pbehomo+4.5)*-0.38964081) # NHE
                lsflumo = -abs((camlumo+4.5)*-0.95798195) +-abs((pbelumo+4.5)*0.93317353) # NHE 

                #print(lsf)
                lsf = 1239.84/lsf
                #print(lsf)
                if lsf >=400 and lsf < 600:
                    orange.append((mol['name'],'cam: '+ str(cam),'pbe: ' + str(pbe),'lsf: '+ str(round(lsf,2)),'HOMO: '+str(lsfhomo),'LUMO: '+str(lsflumo)))
            except ZeroDivisionError:
               # pass
                print((mol['name'],'Excited states is zero in .json '))
        for i in orange:
            i

    return orange






def main():
    os.chdir('../')
    filename = 'results_exc.json'
    print('800-1000')
    print(' ')
    print(' ')
    print(box0(filename))
    print(' ')
    print(' ')
    print(box1(filename))
    print(' ')
    print('600-800')
    print(' ')
    print(box2(filename))
    print(' ')
    print('400-600')
    print(' ')
    return
main()