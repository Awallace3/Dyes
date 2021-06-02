import os
import glob

a = glob.glob('*')
for i in a:
	try:
		os.chdir(str(i) +'/')
		print(i)
		os.system('rm -r' +' ES' + ' ESGO' + ' MO')
		os.chdir('..')
	except NotADirectoryError:
		pass

