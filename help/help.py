from asyncore import write
import os
import json
import pandas as pd

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

def list_former(json_file):
	'''
	gathers specific names for published papers
	'''
	names = []
	with open(json_file,'r') as fp:
		data = fp.readlines()
		for name in data:
			name = name.split(',')
			if 'TPA' in name[0]:
				pass
			else:
				print(name)
				names.append(name[0])
	print(len(names))

	return names

def csv_former(filename,names):
	tot = {}
	with open(filename,'r') as fp:
		data = fp.readlines()
		for name in data[1:]:
			name = name.split(',')
			tot[name[0]]=name[1]
	error = []
	for i in names:
		try:
			print(tot[i])
		except KeyError:
			error.append(i)
	print('key error list')
	print(error)
	print(len(error))
	'''
	for names in name:
		print(tot[names])
	'''

	return tot

def csv_editor(tot):
	df = {
		'Name':[],
		'SMILES':[]
	}
	bbb = []
	for name in tot:
		aa = str(tot[name])
		bb = aa.split('..')
		df['Name'].append(name)
		df['SMILES'].append(bb[0])
	df = pd.DataFrame(df)
	df.to_csv('SMILES_for_paper_1.csv',index=False)
	

	#	upt = str(tot[name]).split('..','')
	#	print(upt)
	return df

def json_file_tot(file):
	names = []
	with open(file,'r') as fp:
		data = json.load(fp)
		for line in data['molecules']:
			if 'TPA' in line['name']:
				pass 
			else:
				names.append(line['name'])
			#print(line['name'])
	print(len(names))
	return



def main():
#	file = '../data_analysis/theoreitcal_dyes_600_800_first_paper.tex'
#	file = '../data_analysis/theoreitcal_dyes_800_1000_first_paper.tex' 

#	jobs = file_editor(file)
#	print(jobs)
	
	
	file_csv= '../data_analysis/scoring_B.csv'
#	file_csv = '../data_analysis/scoring_600.csv'
	file_csv = '../data_analysis/scoring_800.csv'
#	file_csv = '../data_analysis/scoring.csv'
	old_csv_file = 'names_for_first_paper.csv'
#	list_former(old_json_file)
#	specifier(jobs,file_csv)
	file_json = '../json_files/ds_all5_out.json'
	file_json = '../json_files/single.json'
	json_file_tot(file_json)
	
	
	
#	benchmark(file_csv)
#	file = '../data_analysis/gensmiles_upt.csv'
#	names = list_former(old_csv_file)
#	tot = csv_former(file,names)
#	csv_editor(tot)
	
	return
main()