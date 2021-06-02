import os
import glob


differ = 460545 - 460474
a = 460474
out = []
'''
for i in range(differ):
	os.system('qstat ' + str(a)+ ' -H' )
	a += 1
'''
	
a = glob.glob('*')
for i in a:
	try:
		os.chdir(str(i)+'/')
		filename = open('mex.out','r')
		for x in filename:
			if 'Normal termination' in x:
				print((str(i),'Done'))
				os.chdir('..')
			else:
				print(str(i))
				os.chdir('..')
	except NotADirectoryError:
		pass


'''
creates ES and MO input files and pbs script if jobs have normal termination
a = glob.glob('*')
for i in a:
	try:
		os.chdir(str(i) +'/')
		print(i)
		filename = open('mex.out','r')
		editfile = []
		for i in filename:
			if 'Normal termination' in i:
				print('Done')
				filename2 = open('mex.out','r')
				for x in filename2:
					editfile.append(x)
			elif 'Error termination' in i:
				print('Error'+  str(i))
				pass

		#print(editfile[9126])
		x = 0
		for i in range(len(editfile)):
			if 'Pop' in editfile[i]:
				x += 1
				if x == 2:
					num,atomnum,unoc,x,y,z = editfile[i-6].split()
					os.mkdir('ES')
		#			os.mkdir('MO')
		#			os.mkdir('ESGO')
					os.chdir('ES/')
					filename3 = open('ES.com','w+')
					filename3.write('%mem=8gb'+'\n')
					filename3.write('#N TD(NStates=10) B3lYP/6-311G(d,p)' +'\n')
					filename3.write(' \n')
					filename3.write('Name' + '\n')
					filename3.write(' \n')
					filename3.write('0' + ' 1' + '\n') 
		#			os.chdir('..')
		#			os.chdir('MO/')
		#			filename4 = open('MO.com','w+')
		#			filename4.write('')
		#			os.chdir('..')
					
						
			#		print(editfile[i-5-int(num)])
					for l in range(int(num)):
		#				os.chdir('ES/')
						num2,atomnum,unoc,x,y,z = editfile[i-6-l].split()
					#	print((atomnum,x,y,z))
						filename3.write( str(atomnum) + ' ' + str(x) + ' ' + str(y) + ' '  + str(z) + '\n')
					filename3.write('\n')
					filename3.close()
		try:		
			os.chdir('../ES/')
			file = open("ES.pbs","w+")
			file.write('#!/bin/sh' + '\n')
			file.write('#PBS -N ' + 'mex_o' + "\n")
			file.write("#PBS -S /bin/sh" + '\n')
			file.write("#PBS -j oe" + '\n')
			file.write("#PBS -m abe" + '\n')
			file.write("#PBS -l cput=4000:00:00" +  '\n')
			file.write("#PBS -l mem=10gb" + '\n')
			file.write("#PBS -l nodes=1:ppn=1" + '\n')
			file.write("#PBS -l file=100gb" + '\n')
			file.write("" + '\n')
			file.write("export g09root=/usr/local/apps/" + '\n')
			file.write(". $g09root/g09/bsd/g09.profile" + '\n')
			file.write("" + '\n')
			file.write("scrdir=/tmp/bnp.$PBS_JOBID" + '\n')
			file.write("mkdir -p $scrdir" + '\n')
			file.write("export GAUSS_SCRDIR=$scrdir" + '\n')
			file.write("export OMP_NUM_THREADS=1" + '\n')
			file.write("" + '\n')
			file.write("printf 'exec_host = '" + '\n')
			file.write("head -n 1 $PBS_NODEFILE" + '\n')
			file.write("" + '\n')
			file.write("cd $PBS_O_WORKDIR" + '\n')
			file.write("/usr/local/apps/bin/g09setup ES.com ES.out" + '\n')
			file.close()
			os.chdir('..')
			os.mkdir('MO')
			os.chdir('MO/')
			file = open("MO.pbs","w+")
			file.write('#!/bin/sh' + '\n')
			file.write('#PBS -N ' + 'mex_o' + "\n")
			file.write("#PBS -S /bin/sh" + '\n')
			file.write("#PBS -j oe" + '\n')
			file.write("#PBS -m abe" + '\n')
			file.write("#PBS -l cput=4000:00:00" +  '\n')
			file.write("#PBS -l mem=10gb" + '\n')
			file.write("#PBS -l nodes=1:ppn=1" + '\n')
			file.write("#PBS -l file=100gb" + '\n')
			file.write("" + '\n')
			file.write("export g09root=/usr/local/apps/" + '\n')
			file.write(". $g09root/g09/bsd/g09.profile" + '\n')
			file.write("" + '\n')
			file.write("scrdir=/tmp/bnp.$PBS_JOBID" + '\n')
			file.write("mkdir -p $scrdir" + '\n')
			file.write("export GAUSS_SCRDIR=$scrdir" + '\n')
			file.write("export OMP_NUM_THREADS=1" + '\n')
			file.write("" + '\n')
			file.write("printf 'exec_host = '" + '\n')
			file.write("head -n 1 $PBS_NODEFILE" + '\n')
			file.write("" + '\n')
			file.write("cd $PBS_O_WORKDIR" + '\n')
			file.write("/usr/local/apps/bin/g09setup MO.com MO.out" + '\n')
			file.close()
			mo = open('MO.com','w+')
			mo.write('%mem=8gb' + '\n')
			mo.write('#N TD(NStates=1,root=1) B3lYP/6-311G(d,p) OPT Guess=Sparse' + '\n')
			mo.write('  ' + '\n')
			mo.write('name' + '\n')
			mo.write('  ' + '\n')
			mo.write('0 1' + '\n')
			os.chdir('../ES/')
			esr = open('ES.com','r')
			l = 0
			f = []
			for i in esr:
				l += 1
				f.append(i)
			for i in range(int(l)):
				try:
					mo.write(str(f[i+6]))
				except IndexError:
					pass
			os.chdir('..')
			os.mkdir('ESGO')
			os.chdir('ESGO/')
			file = open("ESGO.pbs","w+")
			file.write('#!/bin/sh' + '\n')
			file.write('#PBS -N ' + 'mex_o' + "\n")
			file.write("#PBS -S /bin/sh" + '\n')
			file.write("#PBS -j oe" + '\n')
			file.write("#PBS -m abe" + '\n')
			file.write("#PBS -l cput=4000:00:00" +  '\n')
			file.write("#PBS -l mem=10gb" + '\n')
			file.write("#PBS -l nodes=1:ppn=1" + '\n')
			file.write("#PBS -l file=100gb" + '\n')
			file.write("" + '\n')
			file.write("export g09root=/usr/local/apps/" + '\n')
			file.write(". $g09root/g09/bsd/g09.profile" + '\n')
			file.write("" + '\n')
			file.write("scrdir=/tmp/bnp.$PBS_JOBID" + '\n')
			file.write("mkdir -p $scrdir" + '\n')
			file.write("export GAUSS_SCRDIR=$scrdir" + '\n')
			file.write("export OMP_NUM_THREADS=1" + '\n')
			file.write("" + '\n')
			file.write("printf 'exec_host = '" + '\n')
			file.write("head -n 1 $PBS_NODEFILE" + '\n')
			file.write("" + '\n')
			file.write("cd $PBS_O_WORKDIR" + '\n')
			file.write("/usr/local/apps/bin/g09setup ESGO.com ESGO.out" + '\n')
			file.close()
			mo = open('ESGO.com','w+')
			mo.write('%mem=8gb' + '\n')
			mo.write('#N B3LYP/6-311G(d,p) SP GFINPUT POP=FULL' + '\n')
			mo.write('  ' + '\n')
			mo.write('name' + '\n')
			mo.write('  ' + '\n')
			mo.write('0 1' + '\n')
			os.chdir('../ES/')
			esr = open('ES.com','r')
			l = 0
			f = []
			for i in esr:
				l += 1
				f.append(i)
			for i in range(int(l)):
				try:
					mo.write(str(f[i+6]))
				except IndexError:
					pass
			os.chdir('../../')

		except FileNotFoundError:
			os.chdir('..')
			pass


				
	except NotADirectoryError:
		pass


#		num2,atomnum,unoc,x,y,z = f.split()
#	print((atomnum,x,y,z))
#	mo.write( str(atomnum) + ' ' + str(x) + ' ' + str(y) + ' '  + str(z) + '\n')




		#	print(editfile[i-(int(num)+5)]	
	#	editfile[i-6]
#		print(editfile[i-6])  


'''
