import os
import glob
import error_mexc_dyes_v1
import subprocess
import pandas
import numpy as np

def gather_excitation_data(path, output_path, add_methods, outName= 'mexc_o', chem_package='Gaussian', moleculeName="", nStates=3):
	add_methods_length = len(add_methods['methods'])
	if add_methods_length != len(add_methods['basis_sets']) and add_methods_length != len(add_methods['mem_com']) and add_methods_length != len(add_methods['mem_pbs']) and add_methods_length != len(add_methods['solvents']):
		print("add_methods must have values that have lists of the same length.\nTerminating jobResubmit before start")
		return
	os.chdir(path)
	data_dict = {}
	df = {
		'Name': ["%s Exc %d" % (moleculeName, i) for i in range(1, nStates+1) ]
	}
	df = pandas.DataFrame(df)
	for i in range(len(add_methods['methods'])):
		if add_methods['solvents'] != '':
			dir_name = ('%s_%s_%s' % (add_methods['methods'][i], add_methods['basis_sets'][i].replace("(", "").replace(")", ""), add_methods['solvents'][i])).lower()
			header_name = ('%s/%s in %s' % (add_methods['methods'][i], add_methods['basis_sets'][i], add_methods['solvents'][i]))
		else:
			dir_name = ('%s_%s' % (add_methods['methods'][i], add_methods['basis_sets'][i].replace("(", "").replace(")", "") )).lower()
			header_name = ('%s/%s' % (add_methods['methods'][i], add_methods['basis_sets'][i] ))
		if not os.path.exists(dir_name):
			print('No directory exists: %s\n moving to next method' % dir_name)
		else:
			


			if chem_package == 'Gaussian':			
				outFile = glob.glob("%s/*.out" % dir_name)
				print()
				print(outFile[-1])
				if len(outFile) > 0:
					cmd = "awk '/Excited State/ {print $5, $9}' %s | tac | tail -n %d | tac | sed s/f=// > tmp.csv" % (outFile[-1], nStates)
					subprocess.call(cmd, shell=True)
					#with open('tmp.csv', 'r') as fp:
						#data = fp.read().split("\n")[:-1]
						#data = [ [float(j[0]), float(j[1])] for j in [i.split(" ") for i in data]]
						#print(data)
					data = np.genfromtxt('tmp.csv', delimiter=" ")
					print(data)
					#data_dict[dir_name] = data
					if len(data) > 0:
						eV = data[:,0]
						osc = data[:,1]
						if add_methods['solvents'][i] != '':
							header_name = ('%s/%s in %s' % (add_methods['methods'][i], add_methods['basis_sets'][i], add_methods['solvents'][i]))
						else:
							header_name = ('%s/%s' % (add_methods['methods'][i], add_methods['basis_sets'][i] ))
						
						header = "%s Excitation Energy (eV)" % (header_name)
						df[header] = eV
						header = "%s Oscillator Strength" % (header_name)
						df[header] = osc
	df.to_csv('%s/tmp.csv' % output_path)
	"""
	Name	M/BS 	M/BS ... 
	xyz		exc1	exc1 ...
	xyz		exc2	exc2 ...
	xyz		exc3	exc3 ...
	"""

	return data_dict

def data_dict_to_pandas(data_dict, ):
	df = {
		"Name" : [],
		"Exc1" : [],
		"Exc2" : [],
		"Exc3" : [],	
	}

				

   	


def specifc_file_gen(path, add_methods, cluster='seq', outName='mexc_o', baseName='mexc', chem_package='Gaussian'):
	add_methods_length = len(add_methods['methods'])
	if add_methods_length != len(add_methods['basis_sets']) and add_methods_length != len(add_methods['mem_com']) and add_methods_length != len(add_methods['mem_pbs']) and add_methods_length != len(add_methods['solvents']):
		print("add_methods must have values that have lists of the same length.\nTerminating jobResubmit before start")
		return

	os.chdir(path)
	out_files = glob.glob("*.out*")
	
	if len(out_files) == 0:
		print("NO OUT FILE")
		return

	last_out = out_files[0]
	highest = 1
	for i in range(len(out_files)):
		t = out_files[i][-1]
		if t =='t':
			t = 1
		else:
			t = int(t)
		if t > highest:
			t = highest
			last_out = out_files[i]
	with open(last_out, 'r') as fp:
		lines = fp.readlines()
	if chem_package == 'Gaussian':
		numberedClean = True
	else:
		numberedClean = False
	error_mexc_dyes_v1.find_geom(lines, error=False, filename=last_out,
								imaginary=False, geomDirName=i, xyzSmiles=False,
								numberedClean=numberedClean
	)
	with open('tmp.txt', 'r') as fp:
		xyz_carts = fp.read()
	for i in range(len(add_methods['methods'])):
		if add_methods['solvents'] != '':
			dir_name = ('%s_%s_%s' % (add_methods['methods'][i], add_methods['basis_sets'][i].replace("(", "").replace(")", ""), add_methods['solvents'][i])).lower()
		else:
			dir_name = ('%s_%s' % (add_methods['methods'][i], add_methods['basis_sets'][i].replace("(", "").replace(")", "") )).lower()
		if os.path.exists(dir_name):
			print('Directory already exists for %s... moving to next method' % dir_name)
		else:
			os.mkdir(dir_name)
			print(dir_name)
			if add_methods['solvents'][i] != '':
				solvent = 'SCRF=(Solvent=%s)' % (add_methods['solvents'][i])
			else:
				solvent = ''
			if chem_package == "Gaussian":
				error_mexc_dyes_v1.gaussianInputFiles(
					'0', add_methods['methods'][i], add_methods['basis_sets'][i],
					add_methods['mem_com'][i], add_methods['mem_pbs'][i],
					cluster, baseName, 'TD(NStates=10)', xyz_carts, dir_name, 
					solvent, outName
				)
			elif chem_package == "CFOUR":
				print("Here")
				error_mexc_dyes_v1.CFOUR_input_files(
					add_methods['methods'][i], add_methods['basis_sets'][i], 
					add_methods['mem_com'][i], add_methods['mem_pbs'][i], xyz_carts, dir_name, cluster='map',
					baseName='mexc', 
				)	
			error_mexc_dyes_v1.qsub(dir_name)

	return

def main():
	add_methods = {
		"methods" : ["B3LYP", 'B3LYP', 'M062X', 'M062X', 'BHandHLYP', 'BHandHLYP', 'VSXC', "VSXC", "N12", "N12" ],
		"basis_sets" : ["6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)",  "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)" , "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)"],
		"solvents" : ["Dichloromethane", "", 'Dichloromethane', "", 'Dichloromethane', "", 'Dichloromethane', "", 'Dichloromethane', "", ], 
		"mem_com" : ["1600", "1600", "1600", "1600", "1600", "1600" ,"1600", "1600","1600", "1600"   ],
		"mem_pbs" : ["10", "10", "10", "10", "10", "10" , "10", "10", "10", "10" ],
	}
	path = '../testing_results/test_functionals/AP25/b3lyp/new_geom'
	path = '../testing_results/test_functionals/XY1/GO'
	
	#specifc_file_gen(path, add_methods, chem_package="Gaussian")
	output_path = '~/research/Dyes/testing_results/'
	gather_excitation_data(path, output_path, add_methods, moleculeName="XY1")

	add_methods = {
		"methods" : [ "CC2" ],
		"basis_sets" : [ "AUG-PVDZ" ],
		"solvents" : [ "" ], 
		"mem_com" : [ "8" ],
		"mem_pbs" : [ "16" ],
	}
	
	#specifc_file_gen(path, add_methods, chem_package="CFOUR")

if __name__ == "__main__":
	main()
