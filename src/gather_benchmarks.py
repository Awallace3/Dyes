import os
import glob

from molecule_json import Molecule
from molecule_json import MoleculeList
from molecule_json import Molecule_BM
from absorpt import absorpt
import ES_extraction

def make_benchmark_json(path_benchmarks):
	os.chdir(path_benchmarks)
	for i in glob.glob("*"):
		os.chdir(i)
		#print(i)
		if not glob.glob('info.json'):
			mol = Molecule()
			#mol.setData('info.json')
			mol.setName(i)
			mol.setLocalName(i)
			mol.sendToFile('info.json')
		else:
			mol = Molecule()
			mol.setData('info.json')
			mol.setName(i)
			mol.sendToFile('info.json')

		os.chdir("..")
	os.chdir("../../src")

def convert_Molecule_to_Molecule_BM(path_benchmarks, exp_values):
	os.chdir(path_benchmarks)
	for i in glob.glob("*"):
		os.chdir(i)
		#print(i)
		if not glob.glob('info.json'):
			mol = Molecule_BM()
			mol.setName(i)
			mol.setLocalName(i)
			if i in exp_values:
				mol.setExp(exp_values[i])
			mol.sendToFile('info.json')
		else:
			mol = Molecule_BM()
			mol.setData('info.json')
			if i in exp_values:
				mol.setExp(exp_values[i])
			mol.setName(i)
			mol.sendToFile('info.json')

		os.chdir("..")
	os.chdir("../../src")


def check_add_methods(add_methods, funct_name):
    ln = len(add_methods['methods'])
    if ln == len(add_methods['basis_set']) and ln == len(add_methods['mem_com']) and ln == len(add_methods['mem_pbs']):
        return True 
    else:
        print("\nadd_methods must have values that have lists of the same length.\nTerminating %s before start\n" % funct_name)
        return False 

<<<<<<< HEAD
=======
def clean_solvent(solvent):
	return solvent.replace('-', '').replace(',', '')

>>>>>>> 1b9d1a5ba670a9d1789df84a5543d8fba8b80c8b
def gather_benchmark_excitations(path_benchmarks, monitor_jobs, add_methods, 
	method_mexc, basis_set_mexc, baseName='mexc'):
	if not check_add_methods(add_methods, "gather_excitation_data"):
		return 

	os.chdir(path_benchmarks)
	mol_lst = MoleculeList()
	if os.path.exists('../benchmarks.json'):
		mol_lst.setData("../benchmarks.json")
	else:
		print("Creating benchmarks.json\n")
		mol_lst.sendToFile("../benchmarks.json")
	failed = []
	for i in monitor_jobs:
		os.chdir(i)
		print(i)
		if not os.path.exists('mexc/mexc.out'):
			print(i, 'does not have mexc/mexc.out')
			os.chdir("..")
			continue
		occVal, virtVal = ES_extraction.ES_extraction('mexc/mexc.out')
		if occVal == virtVal and occVal == 0:
			print(i, "no data found in mexc/mexc.out\n")
			failed.append(i)
			os.chdir("..")
			continue
		mol = Molecule_BM()
		mol.setData('info.json')
		mol.setHOMO(occVal)
		mol.setLUMO(virtVal)
		excitations = absorpt('mexc/mexc.out', method_mexc, basis_set_mexc)
		if excitations == []:
			if i not in failed:
				failed.append(i)
				print(i, '\n')
			os.chdir("..")
			continue
		mol.setExictations(excitations)
		
		methods_len = len(add_methods['methods'])
<<<<<<< HEAD
		try:
			for j in range(methods_len):
				method = add_methods['methods'][j]
				basis_set = add_methods['basis_set'][j]
				
				mol.appendExcitations(absorpt('%s/%s.out' % (method.lower(), baseName), method, basis_set))
		except:
			failed.append(i)
=======
		# try:
		for j in range(methods_len):
			method = add_methods['methods'][j]
			if method.lower() == 'cam-b3lyp':
				method_name = method
				method = 'mexc'
			else:
				method_name = method
			
			basis_set = add_methods['basis_set'][j]
			if add_methods['solvent'][j] != '':
				
				method += '_%s'% clean_solvent(add_methods['solvent'][j])
				#method_name += '_%s'% clean_solvent(add_methods['solvent'][j])
			
			if 'mexc' in method_name:
				method_name.replace('mexc', 'CAM-B3LYP')

			mol.appendExcitations(absorpt('%s/%s.out' % (method.lower(), baseName), method_name, basis_set, solvent=add_methods['solvent'][j]))
		# except:
		# 	failed.append(i)
>>>>>>> 1b9d1a5ba670a9d1789df84a5543d8fba8b80c8b



		mol.toJSON()
		mol.sendToFile('info.json')
		mol_lst = MoleculeList()
		mol_lst.setData("../../benchmarks.json")
		
		mol_lst.updateMolecule(mol)
		mol_lst.sendToFile('../../benchmarks.json')
		

		os.chdir("..")
<<<<<<< HEAD
		print("FAILED:", failed)

def main():
	make_benchmark_json('../Benchmark/results/')
=======
	print("FAILED:", len(failed), failed)

def main():
	#make_benchmark_json('../Benchmark/results/')
>>>>>>> 1b9d1a5ba670a9d1789df84a5543d8fba8b80c8b


	exp_values = {
		"TH304": 568,
		"C258": 458,
		"BTD-1": 515,
		"NKX-2883": 552,
<<<<<<< HEAD
		"WS-8": 547,
=======
		"WS-6": 547,
>>>>>>> 1b9d1a5ba670a9d1789df84a5543d8fba8b80c8b
		"HKK-BTZ4": 540,
		"WS-55": 558,
		"IQ4": 529,
		"FNE52": 526,
		"DQ5": 547,
		"R4": 613,
		"R6": 631,
		"IQ6": 543,
		"IQ21": 557,
		"S3": 628,
		"NL11": 570,
		"FNE32": 596,
		"FNE34": 625,
		"AP3": 650,
		"TP1": 581,
		"TPA-TTAR-A": 498,
		"TTAR-15": 498,
		"S-DAHTDTT": 441,
<<<<<<< HEAD
		"TPA-T-TTAR-A": 413,
=======
		"TPA-T-TTAR-T-A": 413,
>>>>>>> 1b9d1a5ba670a9d1789df84a5543d8fba8b80c8b
		"TTAR-9": 519,
		"D-DAHTDTT": 439,
		"SGT-121": 470.5,
		"SGT-129": 426,
		"SGT-130": 514.5,
		"SGT-136": 531,
		"Y123": 506,
		"NL2": 621,
		"NL4": 657,
		"NL7": 589,
		"NL8": 628,
		"C272": 512,
		"C271": 508,
		"T-DAHTDTT": 434,
		"AP25": 660,
		"D1": 570,
		"D3": 562,
		"XY1": 552,
		"NL6": 605,
		"ZL003": 519,
		"JW1": 590,
<<<<<<< HEAD
		"TPA-T-TTAR-T-A":413,
=======
>>>>>>> 1b9d1a5ba670a9d1789df84a5543d8fba8b80c8b
		"TTAR-B8": 485,
	}
	convert_Molecule_to_Molecule_BM("../Benchmark/results/", exp_values)

	method_mexc = "CAM-B3LYP"
	basis_set_mexc = "6-311G(d,p)"
	add_methods = {
<<<<<<< HEAD
		"methods" : ["bhandhlyp", "PBE1PBE","pbe1pbe_dichloromethane","mexc_dichloromethane","bhandhlyp_dichloromethane","mexc_nndimethylformamide","pbe1pbe_nndimethylformamide","bhandhlyp_nndimethylformamide",'mexc_tetrahydrofuran','bhandhlyp_tetrahydrofuran','pbe1pbe_tetrahydrofuran'],
		"basis_set" : ["6-311G(d,p)", "6-311G(d,p)","6-311G(d,p)","6-311G(d,p)","6-311G(d,p)","6-311G(d,p)","6-311G(d,p)","6-311G(d,p)","6-311G(d,p)","6-311G(d,p)","6-311G(d,p)"],
		"mem_com" : ["1600", "1600","1600","1600","1600","1600","1600","1600","1600","1600","1600"],
		"mem_pbs" : ["10", "10","10", "10","10","10","10","10", "10","10","10"]
	}
	monitor_jobs =  ['DQ5', 'S-DAHTDTT', 'NKX-2883', 'S3', 'HKK-BTZ4', 'TPA-T-TTAR-A', 'NL7', 'NL8', 'AP3', 'NL11', 'C271', 'WS-8', 'IQ4', 'WS-55', 'SGT-130', 'FNE52', 'IQ21', 'SGT-136', 'D-DAHTDTT', 'R6', 'TPA-TTAR-A', 'T-DAHTDTT', 'TH304', 'NL4', 'C258', 'TTAR-9', 'SGT-121', 'TTAR-15', 'NL2', 'SGT-129', 'FNE32', 'BTD-1', 'Y123', 'C272', 'FNE34', 'IQ6', 'TP1', 'TTAR-B8', 'R4', 'TPA-T-TTAR-T-A']

	##### FULLL LISTTT OF BENCHMARKS #####
	monitor_jobs = ['AP25','C272','FNE32','IQ4','NL2','R4','SGT-129','TP1','TTAR-9','XY1','AP3','D-DAHTDTT','FNE34','IQ6','NL4','R6','SGT-130','TPA-T-TTAR-A','TTAR-B8','Y123','BTD-1','D1','FNE52','JW1','NL6','S-DAHTDTT','SGT-136','TPA-T-TTAR-T-A','WS-55','ZL003','C258','D3','HKK-BTZ4','NKX-2883','NL7','S3','T-DAHTDTT','TPA-TTAR-A','C271','DQ5','IQ21','NL11','NL8','SGT-121','TH304','TTAR-15']
   # monitor_jo
	monitor_jobs = ['AP25','C272','FNE32','IQ4','NL2','SGT-129','TTAR-9','XY1','AP3','D-DAHTDTT','FNE34','IQ6','NL4','R6','SGT-130','TPA-T-TTAR-A','TTAR-B8','Y123','BTD-1','D1','FNE52','NL6','S-DAHTDTT','SGT-136','TPA-T-TTAR-T-A','WS-55','ZL003','C258','D3','HKK-BTZ4','NKX-2883','NL7','T-DAHTDTT','TPA-TTAR-A','C271','DQ5','IQ21','NL11','NL8','SGT-121','TH304','TTAR-15']
 

=======
		"methods" : ["bhandhlyp", "PBE1PBE"],
		"basis_set" : ["6-311G(d,p)", "6-311G(d,p)"],
		"mem_com" : ["1600", "1600"],
		"mem_pbs" : ["10", "10"]
	}

	add_methods = {
        "methods" : ["CAM-B3LYP", "PBE1PBE", 'bhandhlyp', "PBE1PBE", 'bhandhlyp', "CAM-B3LYP", "PBE1PBE", 'bhandhlyp', "CAM-B3LYP", "PBE1PBE", 'bhandhlyp', ],
        "basis_set" : ["6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)","6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)","6-311G(d,p)", "6-311G(d,p)", ],
        "mem_com" : ["1600", "1600", "1600", "1600", "1600", "1600", "1600", "1600", "1600","1600", "1600", ],
        "solvent" : ["dichloromethane", 'dichloromethane', 'dichloromethane', '','', 'n,n-dimethylformamide', 'n,n-dimethylformamide','n,n-dimethylformamide', 'tetrahydrofuran', 'tetrahydrofuran', 'tetrahydrofuran', ],
        "mem_pbs" : ["10", "10", "10", "10", "10", "10",  "10", "10", "10", "10", "10", ]
    }
	monitor_jobs =  ['DQ5', 'S-DAHTDTT', 'NKX-2883', 'S3', 'HKK-BTZ4', 'TPA-T-TTAR-A', 'NL7', 'NL8', 'AP3', 'NL11', 'C271', 'WS-6', 'IQ4', 'WS-55', 'SGT-130', 'FNE52', 'IQ21', 'SGT-136', 'D-DAHTDTT', 'R6', 'TPA-TTAR-A', 'T-DAHTDTT', 'TH304', 'NL4', 'C258', 'TTAR-9', 'SGT-121', 'TTAR-15', 'NL2', 'SGT-129', 'FNE32', 'BTD-1', 'Y123', 'C272', 'FNE34', 'IQ6', 'TP1', 'TTAR-B8', 'R4', 'TPA-T-TTAR-T-A']
>>>>>>> 1b9d1a5ba670a9d1789df84a5543d8fba8b80c8b

	gather_benchmark_excitations('../Benchmark/results', monitor_jobs, add_methods, method_mexc, basis_set_mexc)


if __name__ == "__main__":
	main()
