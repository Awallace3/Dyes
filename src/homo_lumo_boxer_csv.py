import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import string
from matplotlib.lines import Line2D


def HOMO_LUMO_dict(file):
    '''
    HOMO is       index 0 or the first two columns of the csv value
    LUMO is       index 1 or the third and fourth columns of the csv 
    Wavelength is index 2 or the last two columns of the csv
    '''
    filename = open(file, 'r')
    data = filename.readlines()
    name_dict = {}
    for line in data[1:]:
        line = line.split(',')
        name_dict[line[0]] = float(line[1])

    #    name_dict[line[2]]=float(line[3])

    # if line[0]==line[2]==line[4]:
    for line in data[1:]:
        line = line.split(',')
        #print(line[2])
        if line[2] in name_dict:
            a = name_dict[line[2]]
            name_dict[line[2]] = [a, float(line[3])]
        #   name_dict[line].update(line[3])
        #   print(name_dict[line[2]])

    for line in data[1:]:
        #print(line)
        line = line.split(',')
        if line[4] in name_dict:
            a = name_dict[line[4]]
            a.append(float(line[5]))
            #print(a)
            name_dict[line[4]] = a
            #print(name_dict)

        #print(line)
       #     print(line)
    
    #print(name_dict)
    

    return name_dict


def optimal_dyes(numbs):
    aa = []
    for name in numbs.keys():
        #print(numbs[name][0])
        if numbs[name][0] <= -4.8 and numbs[name][1] >= -4.0:
            aa.append(name)
    print(aa)
    print(len(aa))

    return


def scatter_plot(file):
    filename = open(file, 'r')
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
        wave.append(str(line[3].replace('\n', ' nm')))
        #print(line)

    df = {'Name': name, 'LUMO': lumo, 'HOMO': homo, 'Wavelength': wave}
    ss = np.array([50])

    x = name
    s = 10
    a = homo
    b = lumo
    plt.scatter(x, a, c='r', s=0, marker='s', label="HOMO")
    plt.rc('font', size=7)

    legend_elements = [
        #plt.plot([0], [0], 'b-.', label=r'TiO_2'),
        #plt.plot([0], [0], 'r--', label=r'Iodine'),
        Line2D([0], [0], color='b', ls='-.', label=r'$Ti_O$'),
        plt.scatter([0], [0], color='b', marker='s', label='LUMO'),
        Line2D([0], [0], c='r', ls="--", label='I'),
        plt.scatter([0], [0], c='r', marker="s", lw=2, label='HOMO'),
    ]
    labels = [r'TiO$_2$', 'LUMO', 'I', "HOMO"]

    plt.legend(legend_elements, labels)
    for v in range(len(a)):
        p2 = a[v]
        rect = matplotlib.patches.Rectangle([v, p2], .5, 0.03, color='red')
        plt.gca().add_patch(rect)
        
        plt.text(v + 0.3,
                 p2 - 0.20,
                 "%s \n " % (homo[v]),
                 va="center",
                 ha="center")
        
        #plt.annotate(v, p2, )

    b = lumo
    mina = min(lumo)
    maxa = max(lumo)
    plt.ylim([-7, -2])

    xs_horiz = []
    ys_tio = []
    ys_io = []
    for v in range(len(name) + 1):
        xs_horiz.append(v)
        ys_tio.append(-4)
        ys_io.append(-4.8)
    plt.plot(xs_horiz, ys_tio, 'b-.', label=r'TiO_2')
    plt.plot(xs_horiz, ys_io, 'r--', label=r'Iodine')
    #plt.xticks(name)
    plt.scatter(x, b, c='b', s=0, marker='s', label="LUMO")
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,  # ticks along the bottom edge are on 
   # bottom=False,  # ticks alone the bottom are off 
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
    plt.ylabel("Energy (eV)")
    plt.xlabel("Theoretical Dyes")

    #plt.xticks(homo)

    for v in range(len(b)):
        p2 = b[v]
        rect = matplotlib.patches.Rectangle([v, p2], 0.5, 0.03, color='blue')
        plt.gca().add_patch(rect)
        
        plt.text(v+0.3, p2-0.20, "%s \n %s" % (name[v], wave[v]), va="center", ha="center")
        
        #plt.annotate(v, p2, )
    plt.savefig('demo-file.pdf')

    df = {'Name': name, 'LUMO': lumo, 'HOMO': homo, 'Wavelength': wave}
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
   # file = '../data_analysis/600_800.csv'
   # file = '../data_analysis/400_600.csv' 
    
    numbs = HOMO_LUMO_dict(file)
    a = 0
    optimal_list = []
#    print(numbs)
    
    
    for name in numbs.keys():
        #print(numbs[name][2])
        if numbs[name][0]>=-3.9 and numbs[name][0]<=-3.5 and numbs[name][2]>620.0:
            optimal_list.append(name)
         #   print(name)
#            print(str(name)+','+str(numbs[name][1])+','+str(numbs[name][0])+','+str(numbs[name][2]))
    print(optimal_list)
    
    '''
    600 to 800 nm MO choices
    test_num = [
'7ed_20b_5ea',
'3ed_1b_5ea',
'1ed_26b_11ea',
'2ed_26b_10ea',
'9ed_1b_7ea',
'6ed_16b_7ea'
        ]
    test_num = [
        '7ed_26b_10ea',
        '10ed_26b_9ea',
        '10ed_26b_10ea',
        '7ed_26b_9ea',
        '9ed_20b_9ea',
        '9ed_16b_7ea'
    ]
    test_num = [
        '11ed_34b_2ea',
        '1ed_32b_10ea',
        '9ed_1b_4ea',
        '5ed_35b_5ea',
        '9ed_35b_3ea',
        '9ed_32b_11ea'
    ]
    '''
    '''

    800 to 1000 nm MO choices

    test_num = [
        '6ed_28b_11ea',
        '7ed_28b_9ea',
        '10ed_29b_6ea',
        '6ed_28b_1ea',
        '6ed_29b_4ea',
        '6ed_28b_3ea'
    ]
    test_num=[
        '6ed_29b_5ea',
        '9ed_29b_7ea',
        '10ed_29b_7ea',
        '7ed_29b_7ea',
        '6ed_28b_7ea',
        '6ed_29b_7ea'
    ]
    test_num=[
        '6ed_16b_5ea',
        '5ed_29b_11ea',
        '7ed_29b_3ea',
        '7ed_29b_6ea',
        '2ed_28b_7ea',
        '10ed_29b_6ea'
    ]
    '''
    '''
    test_num = [
        '5ed_26b_4ea',
        '3ed_26b_4ea',
        '5ed_11b_4ea',
        '3ed_11b_4ea',
    #    '5ed_30b_4ea',
        '3ed_12b_4ea',
    ]
    '''
    '''
    
    
    #800 to 1000 
    test_num = [
'1ed_29b_7ea',
'7ed_29b_10ea',
'10ed_29b_10ea',
'6ed_28b_2ea',
'11ed_29b_7ea'

    #800 to 1000
    test_num = [
        '1ed_29b_7ea', '7ed_29b_10ea', '10ed_29b_10ea', '6ed_28b_2ea',
        '11ed_29b_7ea'
    ]
    '''
    '''
    
    
    test_num = [
'6ed_31b_5ea',
'7ed_16b_11ea',
'7ed_16b_10ea',
'1ed_20b_4ea',
'7ed_16b_3ea'
    ]
    '''
    '''
    
    
    filename = open('test.csv', 'w+')
 #   for i in test_num:
    for i in optimal_list:

        a = str(i) + ',' + str(round(numbs[i][1], 2)) + ',' + str(
            round(numbs[i][0], 2)) + ',' + str(round(numbs[i][2], 2))
        print(a)
        filename.write(str(a) + '\n')
    filename.close()
    '''
    
    

    scatter_plot('test.csv')
    # optimal_dyes(numbs)

    return


main()
