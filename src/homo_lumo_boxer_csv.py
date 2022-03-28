import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import string
from matplotlib.lines import Line2D

def HOMO_LUMO_dict(file):
    '''
    HOMO is       index 0
    LUMO is       index 1
    Wavelength is index 2
    '''
    filename = open(file,'r')
    data = filename.readlines()
    name_dict = {}
    for line in data[1:]:
        line = line.split(',')
        name_dict[line[0]]=float(line[1])

    #    name_dict[line[2]]=float(line[3])

       # if line[0]==line[2]==line[4]:
    for line in data[1:]:
        line = line.split(',')
        #print(line[2])
        if line[2] in name_dict:
            a = name_dict[line[2]]
            name_dict[line[2]]=[a,float(line[3])]
         #   name_dict[line].update(line[3]) 
         #   print(name_dict[line[2]])

    for line in data[1:]:
        #print(line)
        line = line.split(',')
        if line[4] in name_dict:
            a = name_dict[line[4]]
            a.append(float(line[5]))
            #print(a)
            name_dict[line[4]]=a
            #print(name_dict)
            
        #print(line)
       #     print(line)
    
  #  print(name_dict)

    return name_dict
def optimal_dyes(numbs):
    aa = []
    for name in numbs.keys():
        #print(numbs[name][0])
        if numbs[name][0]<=-4.8 and numbs[name][1]>=-4.0:
            aa.append(name) 
    print(aa)
    print(len(aa))
        



    return



def scatter_plot(file):
    filename = open(file,'r')
    data = filename.readlines()
    name = []
    lumo = []
    homo = []
    wave = []
    for line in data:
        line = line.split(',')
        name.append(line[0])
        lumo.append(float(line[1]))
        homo.append(float(line[2]))
        wave.append(str(line[3].replace('\n',' nm')))
        #print(line)
    
    df = {'Name':name,'LUMO':lumo,'HOMO':homo,'Wavelength':wave}
    ss = np.array([50])

    x = name
    s = 10
    a = homo
    plt.scatter(x, a, c='r', s=0, marker='s', label="HOMO")
    plt.rc('font', size=8)

    legend_elements = [
         #plt.plot([0], [0], 'b-.', label=r'TiO_2'),
        #plt.plot([0], [0], 'r--', label=r'Iodine'),
        Line2D([0], [0], color='b', ls='-.', label=r'$Ti_O$'),
        plt.scatter([0], [0], color='b', marker='s', label='LUMO'),
        Line2D([0], [0], c='r', ls="--", label='I'),
        plt.scatter([0], [0], c='r', marker="s",lw=2, label='HOMO'),
                   ]
    labels = [
        r'TiO$_2$',
        'LUMO',
        'I',
        "HOMO" 
    ]

    plt.legend(legend_elements, labels)
    for v in range(len(a)):
        p2 = a[v]
        rect = matplotlib.patches.Rectangle([ v, p2 ], .5, 0.03, color='red')
        plt.gca().add_patch(rect)
        plt.text(v+0.3, p2-0.15, "%s \n %s" % (wave[v],name[v]), va="center", ha="center")
        #plt.annotate(v, p2, )

    b = lumo
    plt.ylim([-5.5, -3])
    
    xs_horiz = []
    ys_tio = []
    ys_io = []
    for v in range(len(name)+1):
        xs_horiz.append(v)
        ys_tio.append(-4)
        ys_io.append(-4.8)
    plt.plot(xs_horiz, ys_tio, 'b-.', label=r'TiO_2')
    plt.plot(xs_horiz, ys_io, 'r--', label=r'Iodine')
    #plt.xticks(name)
    plt.scatter(x,b, c='b', s=0, marker='s', label="LUMO")
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
    plt.ylabel("Energy (eV)")
    plt.xlabel("Dye")
    
    
   
    #plt.xticks(homo)
    
    for v in range(len(b)):
        p2 = b[v]
        rect = matplotlib.patches.Rectangle([ v, p2 ], 0.5, 0.03,color='blue' )
        plt.gca().add_patch(rect)
        '''
        plt.text(v+0.3, p2-0.15, "%s \n %s" % (name[v], wave[v]), va="center", ha="center")
        '''
        #plt.annotate(v, p2, )
    plt.savefig('demo-file.pdf')


    df = {'Name':name,'LUMO':lumo,'HOMO':homo,'Wavelength':wave}
    df = pd.DataFrame(df)
   # plt = df.scatter(x='Name',y='LUMO')

   # plt.scatter(x='Name',y='LUMO',c='blue')
   # plt.show()
  #  ax = df.plot.scatter(x='Name',y='LUMO',c='HOMO',colormap='viridis')
    #ax = df.plot.scatter(x='Name',y='HOMO')

  #  plt.figure.savefig('demo-file.pdf')
 
    

   
  
    #print(df)


    return

def main():
    file = '../data_analysis/800_1000.csv'
    #file = '../data_analysis/600_800.csv'
    #file = '../data_analysis/400_600.csv' 
    
    numbs = HOMO_LUMO_dict(file)
    '''
    for name in numbs.keys():
        #print(i)
        if numbs[name][1]>=-3.4 and numbs[name][1]<=-3.2  and numbs[name][0]<=-4.6 and numbs[name][0]>=-5.2:
            print(str(name)+','+str(numbs[name][1])+','+str(numbs[name][0]))
    '''
            
    
    test_num = [
'6ed_29b_5ea',
'9ed_29b_7ea',
'10ed_29b_7ea',
'7ed_29b_7ea',
'6ed_28b_7ea',
'6ed_29b_7ea'
        ]
    filename = open('test.csv','w+')
    for i in test_num:
        
        a = str(i)+','+str(numbs[i][1])+','+str(numbs[i][0])+','+str(numbs[i][2]) 
        filename.write(str(a)+'\n')
    filename.close()


    scatter_plot('test.csv')

    


      #  print(str(i).replace(' ',''),',',str(numbs[i][1]).replace(' ','')+','+str(numbs[i][0]).replace(' ','')+','+str(numbs[i][2]).replace(' ',''))
    

   # optimal_dyes(numbs)



    return
main()