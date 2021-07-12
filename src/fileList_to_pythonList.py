

filename = open('../a','r')
jobs = []
for i in filename.readlines():
    
    i = str(i).rstrip('\n')
    jobs.append(i)
print(jobs)
print(len(jobs))
    
