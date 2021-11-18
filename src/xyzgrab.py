
import os 


def xyzgrabber(name,path):
    print(path)
    with open(path,'r') as file:
        data =file.readlines()
        #print(data)

        #print(ycoord)
        total2 = []
        startgeom = []
        endgeom = []
        for num,line in enumerate(data):
            zcoord = data[num][33:]
            #print(zcoord)
            if 'Standard orientation' in line:
                startgeom.append(num)
            if '---------------------------------------------------------------------' in line:
                endgeom.append(num)

        xyzcoords = data[startgeom[-1]+5:endgeom[-1]]
    #    for i in a:
    #        print(i)
     #   atomnum = int(amountofatoms)
     #   print(atomnum)
        
        #xyzcoords = data[standnum[-1]+5:standnum[-1]+atomnum+5]        
        for i in xyzcoords:
            a = i.replace('  0  ',' ')
            atom = a[10:20]
            xcoord = a[30:45]
            ycoord = a[43:56]
            zcoord = a[57:67]
            
        #    zcoord = 0.000
            total = atom + '   ' +  str(xcoord) +'   ' +  str(ycoord) + '   ' + str(zcoord)
            print(total)
            total2.append(total)

    
    return 



def Main():

    path = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/testing_results/1ed_1b_1ea/mex.out'
    path = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark/ZL003/mex.out'
    path_2 = path.split('/')
    os.chdir('/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark/results')
  #  for i in os.listdir():
  #      xyzgrabber(name,str(i))
  #      print(i)
    #print(path_2)
    name = ''
    for i in path_2:
        if 'ed' in i and 'b' in i and 'ea' in i:
            name = i
    for i in os.listdir():
        xyzgrabber(str(i),str(i) + '/' + 'mex.out')
        print(i)
    #print(name)
   # xyzgrabber(name,str(path))
    return
Main()
  #  xyzgrabber()