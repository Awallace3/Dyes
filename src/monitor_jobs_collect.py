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


def acquire_results_dir(path='../results'):
    os.chdir(path)
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

    Delcamp_Dyes = ['NL3','NL5','NL12','NL13','ND1','ND2','ND3','AP11','AP14','AP16','AP17','RR6','YZ7','YZ12','YZ15','JD21','C218']
    delete_calc_grouping('../Benchmark/results', Delcamp_Dyes, 'bhandhlyp')
    delete_calc_grouping('../Benchmark/results', Delcamp_Dyes, 'mexc_nndimethylformamide')

    #results = jobs_list('../results')
    #complete_monitor_jobs(results)
    #acquire_results_dir('../Benchmark/results')
