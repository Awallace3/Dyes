import os
import glob

from molecule_json import Molecule, Molecule_exc_BM, MoleculeList_exc
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

def convert_Molecule_to_Molecule_BM(path_benchmarks, exp_values, exc_json=False):
	os.chdir(path_benchmarks)
	for i in glob.glob("*"):
		os.chdir(i)
		#print(i)
		if not glob.glob('info.json'):
			if exc_json:
				mol = Molecule_exc_BM()
			else:
				mol = Molecule_BM()
			mol.setName(i)
			mol.setLocalName(i)
			if i in exp_values:
				mol.setExp(exp_values[i])
			mol.sendToFile('info.json')
		else:
			if exc_json:
				mol = Molecule_exc_BM()
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

def clean_solvent(solvent):
	return solvent.replace('-', '').replace(',', '')

def gather_benchmark_excitations(
	path_benchmarks, monitor_jobs, add_methods,
	method_mexc, basis_set_mexc, baseName='mexc',
	results_json='benchmark.json',
	exc_json=False
	):
	if not check_add_methods(add_methods, "gather_excitation_data"):
		return
	os.chdir(path_benchmarks)
	if exc_json:
		mol_lst = MoleculeList_exc()
		print(os.getcwd())
		mol_lst.setData('../%s'%results_json)
	else:
		mol_lst = MoleculeList()
		if os.path.exists('../%s'%results_json):
			mol_lst.setData("../%s"%results_json)
		else:
			print("Creating benchmarks.json\n")

		mol_lst.sendToFile("../%s"%results_json)
	failed = []
	for i in monitor_jobs:
		os.chdir(i)
		# print(i)
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
		if exc_json:
			mol = Molecule_exc_BM()
			mol.setData('info.json')
		else:
			mol = Molecule_BM()
			mol.setData('info.json')
			mol.setHOMO(occVal)
			mol.setLUMO(virtVal)
		excitations = absorpt('mexc/mexc.out', method_mexc, basis_set_mexc, exc_json=exc_json)
		if excitations == []:
			if i not in failed:
				failed.append(i)
				print(i, '\n')
			os.chdir("..")
			continue
		mol.setExictations(excitations)

		methods_len = len(add_methods['methods'])
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

			mol.appendExcitations(absorpt('%s/%s.out' % (method.lower(), baseName), method_name, basis_set, solvent=add_methods['solvent'][j], exc_json=exc_json))
		# except:
		# 	failed.append(i)



		mol.toJSON()
		mol.sendToFile('info.json')
		if not exc_json:
			mol_lst = MoleculeList()
			mol_lst.setData("../../benchmarks.json")
			mol_lst.updateMolecule(mol)
			mol_lst.sendToFile('../../benchmarks.json')
		else:
			mol_lst.updateMolecule(mol, exc_json=exc_json)

		os.chdir("..")
	print("FAILED:", len(failed), failed)
	if exc_json:
		mol_lst.sendToFile("../%s"%results_json)

def main():
	#make_benchmark_json('../Benchmark/results/')


	exp_values = {
		"TH304": 568,
		"C258": 458,
		"BTD-1": 515,
		"NKX-2883": 552,
		"WS-6": 547,
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
		"TPA-T-TTAR-T-A": 413,
        "TPA-T-TTAR-A": 413,
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
		"TTAR-B8": 485,

		"AP11":377,
		"AP14": 399,
		"AP16":384,
		"AP17":379,
		"C218":550,
		"CC3":377,
		"JD21":582,
		"ND1":646,
		"ND2":641,
		"ND3":668,
		"NL12":565,
		"NL13":590,
		"NL3":651,
		"NL5":672,
		"QL4":386,
		"RR9":399,
		"YZ12":543,
		"YZ15":549,
		"YZ7":532
	}
	convert_Molecule_to_Molecule_BM("../Benchmark/results/", exp_values, exc_json=True)

	method_mexc = "CAM-B3LYP"
	basis_set_mexc = "6-311G(d,p)"

	add_methods = {
        "methods" : ["CAM-B3LYP", "PBE1PBE", 'bhandhlyp', "PBE1PBE", 'bhandhlyp', "CAM-B3LYP", "PBE1PBE", 'bhandhlyp', "CAM-B3LYP", "PBE1PBE", 'bhandhlyp', ],
        "basis_set" : ["6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)","6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)","6-311G(d,p)", "6-311G(d,p)", ],
        "mem_com" : ["1600", "1600", "1600", "1600", "1600", "1600", "1600", "1600", "1600","1600", "1600", ],
        "solvent" : ["dichloromethane", 'dichloromethane', 'dichloromethane', '','', 'n,n-dimethylformamide', 'n,n-dimethylformamide','n,n-dimethylformamide', 'tetrahydrofuran', 'tetrahydrofuran', 'tetrahydrofuran', ],
        "mem_pbs" : ["10", "10", "10", "10", "10", "10",  "10", "10", "10", "10", "10", ]
    }
	'''
	add_methods = {
		"methods" : ["CAM-B3LYP","bhandhlyp", "PBE1PBE"],
		"basis_set" : ["6-311G(d,p)","6-311G(d,p)", "6-311G(d,p)"],
		"mem_com" : ["1600","1600", "1600"],
        "solvent" : ["","", ""],
		"mem_pbs" : ["10","10", "10"]
	}
	'''

	monitor_jobs =  ['DQ5', 'S-DAHTDTT', 'NKX-2883', 'S3', 'HKK-BTZ4', 'TPA-T-TTAR-A', 'NL7', 'NL8', 'AP3', 'NL11', 'C271', 'WS-6', 'IQ4', 'WS-55', 'SGT-130', 'FNE52', 'IQ21', 'SGT-136', 'D-DAHTDTT', 'R6', 'TPA-TTAR-A', 'T-DAHTDTT', 'TH304', 'NL4', 'C258', 'TTAR-9', 'SGT-121', 'TTAR-15', 'NL2', 'SGT-129', 'FNE32', 'BTD-1', 'Y123', 'C272', 'FNE34', 'IQ6', 'TP1', 'TTAR-B8', 'R4', 'TPA-T-TTAR-T-A']

	monitor_jobs_bm2 =  ['DQ5', 'S-DAHTDTT', 'NKX-2883', 'S3', 'HKK-BTZ4', 'TPA-T-TTAR-A', 'NL7', 'NL8', 'AP3', 'NL11', 'C271',  'IQ4', 'WS-55', 'SGT-130', 'FNE52', 'IQ21', 'SGT-136', 'D-DAHTDTT', 'R6', 'TPA-TTAR-A', 'T-DAHTDTT', 'TH304', 'NL4', 'C258', 'TTAR-9', 'SGT-121', 'TTAR-15', 'NL2', 'SGT-129', 'FNE32', 'BTD-1', 'Y123', 'C272', 'FNE34', 'IQ6', 'TP1', 'TTAR-B8', 'R4', 'TPA-T-TTAR-T-A','ZL003','WS-6','NL4','NL6','JW1','AP25','AP11','AP14','AP16','AP17','C218','CC3','JD21','ND1','ND2','ND3','NL12','NL13','NL3','NL5','QL4','RR9','YZ12','YZ15','YZ7','D1','D3','XY1']
	print(len(monitor_jobs_bm2))
	print(len(exp_values))


	gather_benchmark_excitations('../Benchmark/results', monitor_jobs_bm2, add_methods, method_mexc, basis_set_mexc, results_json='benchmarks_exc.json', exc_json=True)


if __name__ == "__main__":
	main()
