import os



#path = input('what directory is the file in? ')
#path = path + '/'
#path ="/Users/tsantaloci/Desktop/python_projects/electronacceptors"
#dir = os.listdir(path)
#print("Here is a list of files: ")
#print(dir)



filename = input('What webmofile cartesian coordinate file do you want edited ')
text_file = open(filename,"r")
amountofatoms = 0
multiplicity = []
differ = []
charge = []
lol = text_file.readlines()
for x in lol:
    amountofatoms += 1
numberofatoms = amountofatoms - 1
#print(numberofatoms)
#del lol[0]
#print(lol[0])
charge = lol[0]
#print(lol[0])
del lol[0]
#print(charge)
charge = charge.split()
number = charge[0]
#print(number)
strcharge = 'charge='+number+"=\n"
#print(strcharge)
numberofatoms = str(numberofatoms)
strnumberofatoms = numberofatoms + "\n"
#print(strnumberofatoms)
del charge[0]
del charge[0]

numberofatoms = len(lol)
lol.insert(0,strcharge)
lol.insert(0,strnumberofatoms)
#print(lol)
#print(type(lol))
axyz = []
#amountoflines = 0
#amountofatoms = 0
#for linenumber,x in enumerate(text_file):
#    amountoflines += 1
##    amountofatoms = amountoflines - 1
 #   if linenumber == 0:
 #       x = x.split()
 #       multiplicity.append(x[0])
 #       charge.append('charge='+x[1]+'=')
    #    print(x[1])

#print(lol)
#print(charge)
#print(amountofatoms)
#amountofatoms = str(amountofatoms)
strlol = []
for x in lol:
    x = str(x)
    strlol.append(x)
x = str(x)
#print(strlol)
text_file.close()
my_file = open(filename,"w") 
my_file.writelines(strlol)
my_file.close()


    #    charge.append(x[1])
#charge = zero - differ
#print(charge)
    #    charge.split(',')
     #   charge.append('charge='+x+'=')
       



#print(amountofatoms)

