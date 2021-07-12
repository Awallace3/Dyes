import glob
import os

def acquire_half_results_dir(first=True):
	os.chdir("../results")
	lst = glob.glob('*')
	if first:
		print("monitor_jobs = ", lst[:len(lst)//2])
	else:
		print("monitor_jobs = ", lst[len(lst)//2:])
		

if __name__ == '__main__':
	acquire_half_results_dir(False)