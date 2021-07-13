import os
import glob
import error_mexc_dyes_v1

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
		"methods" : ["B3LYP", 'B3LYP', 'M062X', 'M062X', 'BHandHLYP', 'BHandHLYP' ],
		"basis_sets" : ["6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)",  "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)" ],
		"solvents" : ["Dichloromethane", "", 'Dichloromethane', "", 'Dichloromethane', "",  ], 
		"mem_com" : ["1600", "1600", "1600", "1600", "1600", "1600"  ],
		"mem_pbs" : ["10", "10", "10", "10", "10", "10" ],
	}
	path = '../testing_results/test_functionals/AP25/b3lyp/new_geom'
	#path = '../testing_results/test_functionals/XY1/GO'
	
	#specifc_file_gen(path, add_methods, chem_package="Gaussian")

	add_methods = {
		"methods" : [ "CC2" ],
		"basis_sets" : [ "AUG-PVDZ" ],
		"solvents" : [ "" ], 
		"mem_com" : [ "8" ],
		"mem_pbs" : [ "16" ],
	}
	
	specifc_file_gen(path, add_methods, chem_package="CFOUR")

if __name__ == "__main__":
	main()
