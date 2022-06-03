from fileinput import filename
from operator import index
from collections import Counter
import pandas as pd
import os

def csvtolatex(name,csvfile):
    file = open(str(csvfile),'r')
    data = file.readlines()
    tab = []
    for line in data:
        line = line.replace(',',' & ').replace('\\\\',' ').replace('\n','').replace('_','\\_').replace('nm','')
        print(line)
        tab.append(line)
    

    filename = open(str(name),'w+')
    filename.write("\\begin{longtabu} to \\textwidth{p{0.15\\linewidth}p{0.15\\linewidth}p{0.15\\linewidth}p{0.15\\linewidth}}         \n")
    filename.write("    \\caption{The data for the " + str(csvfile).replace('.csv','').replace('_','\_') + " scatter plot}\n")
 #   filename.write("    \\begin{tabular}{cccc}\n")
    filename.write("    \hline\n")
    for line in tab:
        filename.write(line +" \\\\ "+"\n")
#    filename.write("    \\end{tabular}\n")
    filename.write("\\end{longtabu}\n")

    filename.close()
    file.close()
   

    
   


    return

def subfinderboxer(filename):
    df = pd.read_csv(filename)
    print(df.keys())
    name = []
    cam=[]
    for i in df['Name']:
        name.append(i)
    for x in df['CAM-B3LYP']:
        cam.append(x)
    test = {}

    for num,i in enumerate(name):
        test[i]=cam[num]
    commonea = []
    commonb = []
    commoned = []
    countb={}
    howmany = 0
    for keys in test.keys():
       # if test[keys]<=2.06 and test[keys]>1.84:
        if test[keys]<=1.96:
            print(keys)
            howmany += 1
            name = keys.split('_')
            commonea.append(name[0])
            commonb.append(name[1])
            commoned.append(name[2])
            countb[name[1]]=0
    for i in commonb:
        if i in countb.keys():
            countb[i] += 1
    #print(commonb)
    print(countb)
    print('hom many ')
    print(howmany)
          #  print(keys)



   # print(test['6ed_28b_4ea'])
    return
def percentchange(file):
    df = pd.read_csv(file)
    print(df.keys())
    name = []
    cam=[]
    bhand=[]
    total = {}
    per = []
    for i in df['Name']:
        name.append(i)
    for x in df['CAM-B3LYP']:
        cam.append(x)
    for x in df['PBE1PBE']:
        bhand.append(x)
    for num,name in enumerate(name):
        tot = (bhand[num]-cam[num])/cam[num]
        total[name]=tot*100
        per.append(tot*100)
    print(str(max(per))+' Maximum')
    print(str(min(per))+' Minimum')
    absper = []
    for i in per:
        absper.append(abs(round(i,0)))
#        if abs(i) > 20.0:
#            print(i)
    tot = sum(absper)/len(per)

    print(str(max(absper))+' Maximum')
    print(str(min(absper))+' Minimum')
    print(str(Counter(absper)))

    print(str(tot)+' Average')



    return

def main():
    csvfile = 'g_400_600.csv' 
    csvfile = 'benchscatter.csv'
    name = 's_400_600.tex'
    name='benchscatter.tex'
    csvfile_data = 'Absorption_final.csv'
  #  csvtolatex(name,csvfile)
    subfinderboxer(csvfile_data)
  #  percentchange(csvfile_data)
    return

main()