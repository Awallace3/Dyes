import os
import glob

#path = '/ddn/home6/r2532/chem/dyemolcata/inputs/*'

#a = os.chdir(glob.glob('*/mex.pbs/')

a = glob.glob('*') 
#b = os.chdir(str(a)+'mex.pbs')
#c = os.chdir('..')
#print(b)

'''

Geometry Optimization job submit 


for i in a:
	try:
		os.chdir(str(i)+'/')
		os.system('qsub '+   'mex.pbs')
		os.chdir('..')
	except NotADirectoryError:
		pass
	
#	print(i)
#	os.system('qsub '+   i)

'''
'''
absorption, Emission and MO orbital submit script

''' 
for i in a:
#	print(i)
	try:
		print(i)
		os.chdir(str(i)+'/')
		print(i)
		os.chdir('ES/')
		os.system('qsub ' + 'ES.pbs')
		os.chdir('../')
		os.chdir('MO/')
		os.system('qsub ' + 'MO.pbs')
		os.chdir('../')
		os.chdir('ESGO/')
		os.system('qsub ' + 'ESGO.pbs')
		os.chdir('../../')
		print(i)
	except FileNotFoundError:
		os.chdir('../')
		pass
	except NotADirectoryError:
		pass
	
