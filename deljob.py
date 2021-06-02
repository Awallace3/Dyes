import os

a = 463658
differ = 463753 - a
out = []

for i in range(differ):
#        os.system('qstat ' + str(a)+ ' -H' )
	os.system('qdel ' + str(a))
	a += 1


