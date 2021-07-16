import glob
import os
import subprocess

def acquire_half_results_dir(first=True):
	os.chdir("../results")
	lst = glob.glob('*')
	if first:
		print("monitor_jobs = ", lst[:len(lst)//2])
	else:
		print("monitor_jobs = ", lst[len(lst)//2:])
			

def acquire_results_dir():
	os.chdir("../results")
	lst = glob.glob('*')
	print("monitor_jobs = ", lst[:len(lst)])
			

def acquire_directories(path):
	if path =='tmp.txt':
		return ''
	os.chdir(path)

	cmd = 'ls -d */ > ../tmp.txt' 
	subprocess.call(cmd, shell=True)
	
	with open('../tmp.txt', 'r') as fp:
		line = fp.read()
	os.chdir('..')
	return line

def jobs_list(path_to_results):
	results = []
	os.chdir(path_to_results)
	for i in glob.glob("*"):
		line = acquire_directories(i)
		results.append([i, line])
	#print(results)
	os.remove('tmp.txt')
	os.chdir('..')
	return results

def complete_monitor_jobs(jobs_list_results):
	final = []
	for i in jobs_list_results:
		#print(i[1].split('/\\'))
		first = i[1].split("/")
		print(first)
		for j in range(len(first)-1, -1, -1):
			print(first[j])
			if "GO" in first[j]:
				del first[j]
			elif "ES" in first[j]:
				del first[j]
			elif "ESGO" in first[j]:
				del first[j]
			elif "MO" in first[j]:
				del first[j] 

		if len(first) > 3:
			
			final.append(i[0])
		else:
			print(i, 'is not done', )
	with open('monitor_jobs.txt', 'w') as fp:
		fp.write('monitor_jobs = [')
		for i in final:
			fp.write(' "%s",' % i )
		fp.write("]")

def delete_calc_grouping(path, monitor_jobs, target):
	os.chdir(path)
	for i in monitor_jobs:
		if i =='tmp.txt':
			continue
		os.chdir(i)
		os.remove(target)
		#cmd = 'rm -r %s' % target
		#subprocess.call(cmd, shell=True)
		os.chdir('..')

if __name__ == '__main__':
	#acquire_half_results_dir(False)
	
	#monitor_jobs =  ['3ed_12b_1ea', '3ed_8b_1ea', '2ed_8b_1ea', '6ed_14b_2ea', '1ed_1b_1ea', '1ed_9b_3ea', '1ed_13b_2ea', '5ed_16b_2ea', '2ed_11b_2ea', 'TPA2_6b_1ea', '5ed_5b_2ea', '6ed_16b_3ea', '2ed_2b_2ea', 'TPA2_14b_1ea', '3ed_2b_2ea', '1ed_11b_3ea', '5ed_14b_3ea', '2ed_13b_3ea', '5ed_7b_3ea', '7ed_6b_1ea', '7ed_14b_1ea', '6ed_6b_1ea', '3ed_11b_1ea', '2ed_4b_1ea', 'TPA2_12b_2ea', '3ed_4b_1ea', '1ed_5b_3ea', '7ed_12b_2ea', '5ed_9b_2ea', 'TPA2_2b_3ea', '1ed_15b_1ea', '1ed_7b_2ea', '6ed_12b_1ea', 'TPA2_10b_3ea', '5ed_10b_1ea', '5ed_3b_1ea', '7ed_2b_3ea', '7ed_10b_3ea', '6ed_2b_3ea', '3ed_15b_3ea', '3ed_14b_3ea', 'TPA2_1b_2ea', '5ed_2b_1ea', '7ed_3b_3ea', '7ed_11b_3ea', '6ed_3b_3ea', '5ed_11b_1ea', '2ed_16b_1ea', '1ed_6b_2ea', '6ed_13b_1ea', 'TPA2_11b_3ea', '1ed_14b_1ea', '3ed_16b_2ea', 'TPA2_3b_3ea', '7ed_1b_2ea', '6ed_1b_2ea', '7ed_13b_2ea', '5ed_8b_2ea', '2ed_5b_1ea', 'TPA2_13b_2ea', '3ed_5b_1ea', '1ed_4b_3ea', '3ed_10b_1ea', '5ed_6b_3ea', '7ed_7b_1ea', '7ed_15b_1ea', '6ed_7b_1ea', '2ed_12b_3ea', '5ed_15b_3ea', '1ed_10b_3ea', '2ed_3b_2ea', 'TPA2_15b_1ea', '3ed_3b_2ea', '5ed_4b_2ea', 'TPA2_7b_1ea', '2ed_10b_2ea', '1ed_12b_2ea', '3ed_9b_1ea', '2ed_1b_3ea', '3ed_1b_3ea', '2ed_9b_1ea', '6ed_15b_2ea', '1ed_8b_3ea', '3ed_2b_1ea', 'TPA2_14b_2ea', '2ed_2b_1ea', '1ed_3b_3ea', '6ed_6b_2ea', '7ed_14b_2ea', '7ed_6b_2ea', 'TPA2_4b_3ea', '3ed_11b_2ea', '1ed_13b_1ea', '1ed_1b_2ea', '6ed_14b_1ea', '2ed_8b_2ea', 'TPA2_16b_3ea', '3ed_8b_2ea', '2ed_11b_1ea', '5ed_16b_1ea', '5ed_5b_1ea', '7ed_16b_3ea', '6ed_4b_3ea', '7ed_4b_3ea', 'TPA2_6b_2ea', '3ed_13b_3ea', '3ed_6b_3ea', '2ed_6b_3ea', '6ed_12b_2ea', '1ed_7b_1ea', '1ed_15b_2ea', '5ed_10b_2ea', 'TPA2_8b_3ea', '5ed_3b_2ea', '6ed_10b_3ea', '3ed_4b_2ea', 'TPA2_12b_1ea', '2ed_4b_2ea', '5ed_12b_3ea', '2ed_15b_3ea', '5ed_1b_3ea', '5ed_9b_1ea', '7ed_12b_1ea', '7ed_8b_3ea', '6ed_8b_3ea', '3ed_16b_1ea', '5ed_8b_1ea', '7ed_13b_1ea', '6ed_1b_1ea', '7ed_9b_3ea', '6ed_9b_3ea', '7ed_1b_1ea', '2ed_14b_3ea', '5ed_13b_3ea', '1ed_16b_3ea', '6ed_11b_3ea', '3ed_5b_2ea', 'TPA2_13b_1ea', '2ed_5b_2ea', '5ed_2b_2ea', 'TPA2_9b_3ea', 'TPA2_1b_1ea', '2ed_16b_2ea', 'tin_results', '5ed_11b_2ea', '1ed_14b_2ea', '3ed_7b_3ea', '2ed_7b_3ea', '6ed_13b_2ea', '1ed_6b_1ea', '3ed_12b_3ea', 'TPA2_7b_2ea', '5ed_4b_1ea', '6ed_5b_3ea', '7ed_5b_3ea', '2ed_10b_1ea', '6ed_15b_1ea', '2ed_9b_2ea', '3ed_9b_2ea', '1ed_12b_1ea', '3ed_10b_2ea', 'TPA2_5b_3ea', '6ed_7b_2ea', '7ed_15b_2ea', '7ed_7b_2ea', '3ed_3b_1ea', 'TPA2_15b_2ea', '2ed_3b_1ea', '1ed_2b_3ea']
	#delete_calc_grouping('../results', monitor_jobs, 'bhandhlyp')
	
	#results = jobs_list('../results')
	#complete_monitor_jobs(results)
	acquire_results_dir()
	