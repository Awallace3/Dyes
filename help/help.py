from asyncore import write
import os

def file_editor(file):
	jobs = []

	with open(file,'r') as fp:
		data = fp.readlines()
		for line in data:
			line = line.split(',')
			name = line[0].replace("\\",'')
			jobs.append(name)

	print(jobs)

	return jobs

def specifier(jobs,file):
	test = []
	with open(file,'r') as fp:
		data = fp.readlines()
		first = data[0].replace('\n','').split(',')
		test.append(first)
		for line in data:

			line = line.replace('\n','').split(',')
			print(line)
			
			for name in jobs:
				if line[0]==name:
					test.append(line)
	print(len(test))
	for i in test:
		print(i)
	'''		
	with open('test.csv','w+') as fp:
		for line in test:
			print(line)
			for num,a in enumerate(line):
				#print(num)
				if num == 0 or num==4 or num==5 or num==6 or num==7 or num==8 or num==9: 
					#print(num)
					fp.write(str(a).replace('_','\_')+' & ')
				elif num == 10:
					fp.write(str(a).replace('FAIL','0'))
			fp.write('   \\\\ \n' )
	'''

			
	return

def benchmark(file):
	test = []
	with open(file,'r') as fp:
		data = fp.readlines()
		for line in data:

			line = line.replace('\n','').split(',')
			test.append(line)
	with open('test.csv','w+') as fp:
		for line in test:
			for num,a in enumerate(line):
				#print(num)
				if num == 0 or num==1 or num==2 or num==3 or num==4 or num==5 or num==6 or num==7 or num==8 or num==9: 

					#print(num)
					fp.write(str(a).replace('_','\_')+' & ')
				elif num == 10:
					fp.write(str(a).replace('FAIL','0'))
			fp.write('   \\\\ \n' )
	

	return


def main():
	file = '../data_analysis/theoreitcal_dyes_600_800_first_paper.tex'
#	file = '../data_analysis/theoreitcal_dyes_800_1000_first_paper.tex' 

	jobs = file_editor(file)
	print(jobs)
	'''
	
	file_csv= '../data_analysis/scoring_B.csv'
	file_csv = '../data_analysis/scoring_600.csv'
	specifier(jobs,file_csv)
	'''
	
	
#	benchmark(file_csv)
	
	return
main()