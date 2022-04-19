import os
import math

def xyzcoords(file):
    filename = open(file,'r')
    data = filename.readlines()
    start = []
    end = []
    for num,line in enumerate(data):
        if 'Standard orientation:' in line:
            start.append(num+5)
        if '---------------------------------------------------------------------' in line:
            end.append(num)
    #print(start)
    #print(end)
    atom_info = {
        'atom_num' : {},
        'atom_let' : {},
        'xcoord' : {},
        'ycoord' : {},
        'zcoord' : {}
    }
    for line in data[start[-1]:end[-1]]:
        line= line.replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
        line = line.split()
        #print(line)
        atom_info['atom_num'][line[0]]=line[0]
        atom_info['atom_let'][line[0]]=line[1]
        atom_info['xcoord'][line[0]]=  float(line[3])
        atom_info['ycoord'][line[0]] = float(line[4])
        atom_info['zcoord'][line[0]] = float(line[5])
   # for x in atom_info['xcoord'].values():
    #    print(x)
    return atom_info
def atom_type_O(atom_dict):
    O_nums = []
    for name in atom_dict['atom_let']:
        lett = atom_dict['atom_let'][name]
        #print(lett)
        if lett == '8':
            O_nums.append(name)
    return O_nums
def atom_type_N(atom_dict):
    N_nums = []
    for name in atom_dict['atom_let']:
        lett = atom_dict['atom_let'][name]
        #print(lett)
        if lett == '7':
            #print(name)
            N_nums.append(name)
    return N_nums
def atom_type_S(atom_dict):
    S_nums = []
    for name in atom_dict['atom_let']:
        lett = atom_dict['atom_let'][name]
        #print(lett)
        if lett == '16':
            #print(name)
            S_nums.append(name)
    return S_nums
def atom_type_H(atom_dict):
    H_nums = []
    for name in atom_dict['atom_let']:
        lett = atom_dict['atom_let'][name]
        #print(lett)
        if lett == '1':
            #print(name)
            H_nums.append(name)
    return H_nums
def atom_type_Si(atom_dict):
    Si_nums = []
    for name in atom_dict['atom_let']:
        lett = atom_dict['atom_let'][name]
        #print(lett)
        if lett == '14':
            #print(name)
            Si_nums.append(name)
    return Si_nums
def atom_type_C(atom_dict):
    C_nums = []
    for name in atom_dict['atom_let']:
        lett = atom_dict['atom_let'][name]
        #print(lett)
        if lett == '6':
            #print(name)
            C_nums.append(name)
    return C_nums

def Bond_lengths_O_C(atomO,atomC,atom):
    '''
    looks for oxygen carbon double bond

    '''
    #print(atomO)
    #print(atomC)
    bond_length = {}
    for o in atomO:
        for c in atomC:
            tot = (atom['xcoord'][o]-atom['xcoord'][c])**2+(atom['ycoord'][o]-atom['ycoord'][c])**2+(atom['zcoord'][o]-atom['zcoord'][c])**2
            dis = tot**.5
            if dis >= 1.2 and dis <= 1.3:
                #print(dis)
                #double.append((o,c))
                bond_length[str(o)+' '+str(c)]=dis
                #print((o,c))
                #double = dis
    return bond_length

def Bond_lengths_H_C(atomH,atomC,atom):
    '''
    looks for hydrogen carbon double bond

    '''
    #print(atomH)
    #print(atomC)
    bondlength= {}
    double = []
    for o in atomH:
        for c in atomC:
            tot = (atom['xcoord'][o]-atom['xcoord'][c])**2+(atom['ycoord'][o]-atom['ycoord'][c])**2+(atom['zcoord'][o]-atom['zcoord'][c])**2
            dis = tot**.5
          #  print(dis)
            if dis >= 1.0 and dis <= 1.15:
                bondlength[str(o)+' ' +str(c)]=dis
                double.append((o,c))
                #print(dis) 
                #print((o,c))
                #double = dis
    #print(len(double))
    return bondlength

def Bond_lengths_H_O(atomH,atomO,atom):
    '''
    looks for oxygen hydrogen single bond

    '''
   # print(atomH)
   # print(atomO)
    double = []
    bondlength = {}
    for o in atomH:
        for c in atomO:
            tot = (atom['xcoord'][o]-atom['xcoord'][c])**2+(atom['ycoord'][o]-atom['ycoord'][c])**2+(atom['zcoord'][o]-atom['zcoord'][c])**2
            dis = tot**.5
           # print(dis)
            if dis >= .96 and dis <= .98:
                #print(o,c)
                bondlength[str(o)+' '+str(c)]=dis
                double.append((o,c))
      #          print(dis) 
      #          print((o,c))
                #double = dis
    #print(len(double))
    return bondlength

def Bond_lengths_O_C(atomO,atomC,atom):
    '''
    looks for hydrogen carbon double bond

    '''
    #print(atomO)
    #print(atomC)
    bondlength= {}
    double = []
    for o in atomO:
        for c in atomC:
            tot = (atom['xcoord'][o]-atom['xcoord'][c])**2+(atom['ycoord'][o]-atom['ycoord'][c])**2+(atom['zcoord'][o]-atom['zcoord'][c])**2
            dis = tot**.5
            #print(dis)
            if dis >= 1.2 and dis <= 1.35:
                #print(o,c)
                bondlength[str(o)+' ' +str(c)]=dis
                double.append((o,c))
                #print(dis) 
                #print((o,c))
                #double = dis
    #print(len(double))
    return bondlength

def Bond_lengths_O_N(atomO,atomC,atom):
    '''
    looks for hydrogen carbon double bond

    '''
    #print(atomO)
    #print(atomC)
    bondlength= {}
    double = []
    for o in atomO:
        for c in atomC:
            tot = (atom['xcoord'][o]-atom['xcoord'][c])**2+(atom['ycoord'][o]-atom['ycoord'][c])**2+(atom['zcoord'][o]-atom['zcoord'][c])**2
            dis = tot**.5
            #print(dis)
            if dis >= 1.2 and dis <= 1.6:
                bondlength[str(o)+' ' +str(c)]=dis
                double.append((o,c))
                #print(dis) 
                #print((o,c))
                #double = dis
    #print(len(double))
    return bondlength


def Bond_lengths_C_C(atomO,atomC,atom):
    '''
    looks for hydrogen carbon double bond

    '''
    #print(atomO)
    #print(atomC)
    bondlength= {}
    double = []
    for o in atomO:
        for c in atomC:
            tot = (atom['xcoord'][o]-atom['xcoord'][c])**2+(atom['ycoord'][o]-atom['ycoord'][c])**2+(atom['zcoord'][o]-atom['zcoord'][c])**2
            dis = tot**.5
            #print(dis)
            if dis >= 1.2 and dis <= 1.6:
                bondlength[str(o)+' ' +str(c)]=dis
                double.append((o,c))
                #print(dis) 
                #print((o,c))
                #double = dis
    #print(len(double))
    return bondlength









def Bond_length(atom):
    Bond_length = {

    }
    for x in atom['atom_num']:
        for y in atom['atom_num']:
           
            #print(x)
                tot = (atom['xcoord'][x]-atom['xcoord'][y])**2+(atom['ycoord'][x]-atom['ycoord'][y])**2+(atom['zcoord'][x]-atom['zcoord'][y])**2
                dis = tot**.5
                #print(x,y,'keys')
                
            
                Bond_length[str(x)+' '+str(y)]=dis
                #print((x,y,dis))

    return Bond_length

def Bond_angles(atom,dis):
    bond_angle = {}
    ex = {}
    ey = {}
    ez = {}
    num = []
    for x in atom['atom_num']:
        for y in atom['atom_num']:
            if x != y:
                ex[str(x)+' '+str(y)] = -(atom['xcoord'][x]-atom['xcoord'][y])/dis[str(x)+' '+str(y)]
                ey[str(x)+' '+str(y)] = -(atom['ycoord'][x]-atom['ycoord'][y])/dis[str(x)+' '+str(y)]
                ez[str(x)+' '+str(y)] = -(atom['zcoord'][x]-atom['zcoord'][y])/dis[str(x)+' '+str(y)]
    for x in atom['atom_num']:
        for y in atom['atom_num']:
            for k in atom['atom_num']:
                if x!=y and x!=k and y!=k: 
                   # print(x,y)
                   # print(x,k)
                   # print(y,k)
               
    
                    tot = ex[x+' '+y]*ex[x+' '+k]+ey[x+' '+y]*ey[x+' '+k]+ez[x+' '+y]*ez[x+' '+k]
                    ang = math.acos(tot)
                    result = math.degrees(ang)
                    bond_angle[str(x)+ '-'+ str(y) + '-' + str(k)]= result
                   # print(result,int(x),int(y),int(k))
    return bond_angle

def Bond_angle_H_O_C(O,C,atom,tot,ang):
    '''
    finds carboxylic functional groups
    '''
    oangl = []
    cangl=[]


    for o in O:
        for c in C:
        
           #print(c)
           #print(o,c)
           #print(c,h)
           test = tot[o+' '+c]
           
           #print(test_H,'test')
           if test < 2.11:
               oangl.append(o)
               cangl.append(c)

    final = {}
    for c in cangl:
        for o in oangl:
            for ot in oangl:
                if c!=o and c!=ot and o!=ot:
                   tot = ang[str(c)+'-'+str(o)+'-'+str(ot)]
                   if tot >= 115 and tot <= 135:
                       rep = sorted((int(c),int(o),int(ot)))
                       rep = str(rep[0])+'-'+str(rep[1])+'-'+str(rep[2])
                   

                       final[rep]=tot

    
    return final


def Bond_angle_H_O_N(O,C,N,atom,tot,ang):
    '''
    finds amide functional groups
    O= oxygen
    C=Carbon
    N=Nitrogen
    '''
    oangl = []
    cangl=[]
    nangl = []

    for o in O:
        for c in C:
            for n in N:
                test_o_c = tot[o+' '+c]
                test_n_c = tot[n+' '+c]
                if test_o_c < 2.11:
                    #print(test_o_c,o,c)
                    oangl.append(o)
                    cangl.append(c)
                if test_n_c<2.11:
                    #print(test_n_c,n,c)

                    nangl.append(n)
    final = {}
    for c in cangl:
        for o in oangl:
            for ot in nangl:
                if c!=o and c!=ot and o!=ot:
                   tot = ang[str(c)+'-'+str(o)+'-'+str(ot)]
                   #print(tot)
                   if tot >= 115 and tot <= 135:
                       rep = sorted((int(c),int(o),int(ot)))
                       rep = str(rep[0])+'-'+str(rep[1])+'-'+str(rep[2])

                   

                       final[rep]=tot

    
    return final

def bondistancecheck(fin,dis):
    '''
    checks the distances of the angles to make sure atoms are next to each other
    '''
    final = []
    for i in fin:
        i = i.split('-')
        #print(i)
        a = dis[i[0]+' '+i[1]]
        b = dis[i[0]+' '+i[2]]
        c =dis[i[1]+' '+i[2]]
        if a < 4 and b<4 and c<4:
            i = [str(i[0]),str(i[1]),str(i[2])]
            #print(i)

            for x in i:
                final.append(x)
         #   print(i)
       # print(a,b,c)
    return final

def atomnearchecker(atom_num_list,H,O,N,Si,C,tot,atom,ang,Carboxy=False,Amide=False,cyanoacrylic=False,SI=False):
    atom_num_dict = {}
    print(atom_num_list)
    if Amide == True:
        for h in H:
            for o in O:
                dis2 = tot[o+' '+h]
                if dis2 < 1.1:
                    for x in atom['atom_num']:
                        #print(x,o)
                        dis = tot[h+' '+x]
                        if dis < 3.4:
                            atom_num_dict[x]=x

    if Carboxy == True:
        
        for h in H:
            for o in O:
                dis2 = tot[o+' '+h]
                if dis2 < 1.1:
                    for x in atom['atom_num']:
                        #print(x,o)
                        dis = tot[h+' '+x]
                        if dis < 3.2:
                            atom_num_dict[x]=x
        '''
        
        if len(atom_num_dict.keys())!= 5:

            print('help')
        '''

    if cyanoacrylic == True:
        for h in H:
            for o in O:
                for n in N:
                    for c in C:
                        dis2 = tot[o+' '+h]
                        if dis2 < 1.1:
                            for x in atom['atom_num']:
                                #print(x,o)
                                dis = tot[h+' '+x]
                                dis2 = tot[n+' '+x]
                                if dis2 < 1.3:
                                    l = tot[n+' '+c]
                                    #print(l)
                                    if l < 1.3:
                                        atom_num_dict[x]=x
                                if dis < 4.11:
                                    atom_num_dict[x]=x

                                
                        
                                '''

                                if dis < 1.5 or dis2 < 1.3 or dis3<4.11 and dis4<5.0:
                                    atom_num_dict[x]=x
                                '''
    if SI ==True:
        for si in Si:
            for o in O:
                dis2 = tot[o+' '+si]

                if dis2 < 2.1:
                    for x in atom['atom_num']:
                        #print(x,o)
                        dis = tot[si+' '+x]
                        #print(dis4)
                        if dis < 2.7:
                            atom_num_dict[x]=x




                  #      dis_2 = tot['42',' ','1']
                        #if dis <4.11:
                        #    atom_num_dict[x]=x
                 #   print(o,h)
                           # print(dis)




              #  print(x,y)
              #  print(dis)
    #print(atom_num_dict)




    return atom_num_dict






def main():
    '''
    cartesians are in Angstroms
    '''
    #filename = '../MO_start/10ed_29b_10ea/mo/10ed_29b_10ea.out'
   # filename = '../MO_start/3ed_15b_3ea/mo/3ed_15b_3ea.out'
    #filename = '../MO_start/3ed_12b_4ea/mo/3ed_12b_4ea.out'
    #filename = '../MO_start/5ed_30b_4ea/mo/5ed_30b_4ea.out'
   # filename = '../MO_start/3ed_15b_3ea/mo/test.out'
    """
    atom = xyzcoords(filename)
    O = atom_type_O(atom)
    N = atom_type_N(atom)
    #print(N)
    S = atom_type_S(atom)
    H = atom_type_H(atom)
    Si= atom_type_Si(atom)
    C = atom_type_C(atom)
    Od = Bond_lengths_O_C(O,C,atom)
    '''
    for i in Od:
        print(i)
    '''
    
    ch = Bond_lengths_H_C(H,C,atom)
    Os = Bond_lengths_H_O(H,O,atom)
    Co = Bond_lengths_O_C(O,C,atom) 
    No = Bond_lengths_O_N(O,N,atom) 
    #print(No)
    
    tot = Bond_length(atom)
    ang = Bond_angles(atom,tot)
    #for i in Co:
    #    print(i)
    
    '''
    
    for i in Os:
        print(Os)
    '''
    
  
    carboxy = Bond_angle_H_O_C(O,C,atom,tot,ang) 
    amide = Bond_angle_H_O_N(O,C,N,atom,tot,ang)
    
    print(amide)
    
    atom_num_list = bondistancecheck(amide,tot)
    """
    
    
    
    
    
if __name__=="__main__": 
    main()
