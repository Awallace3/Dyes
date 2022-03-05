import os


def timegrabber(path,method,name):
    #time is in minutes

        #print(name)
    
   # try:
    times = {}
    filename = open(str(name) + '/' + str(method) + '/mexc.out','r')
    data = filename.readlines()
    #print(direct)
    for i in data:
                #print(i)
        if 'Job cpu time:' in i :
            days = str(i.replace('days',':'))
            time = i.replace('days',':').replace('hours',':').replace('minutes',':')
            time_2 = time.replace('seconds.','').replace('Job cpu time:','')
            time_3 = time_2.split(':')
           # print((name,time_3))
            days = float(time_3[0])*1440
            hours = float(time_3[1])*60
            minutes = float(time_3[2])
            seconds = float(time_3[3])/60
            times[name]=days+hours+minutes+seconds

  #  except FileNotFoundError:
  #      print('No File')
  #      continue
    #print(Camb3lyp)

    return times[name]

def average(dict,length,method):
    total = 0
    #print(dict)
    for i in dict.keys():
        print(dict[i])
        total += dict[i]
   # print(total/length)


    return (method,total/int(length))

#filename = open(UnsolvB3LYPCPUtimes.

def main():
    path_to_benchmarks = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark/results'
    os.chdir(path_to_benchmarks)
   # method = ['mexc','mexc_dichloromethane','mexc_nndimethylformamide','mexc_tetrahydrofuran','pbe1pbe','pbe1pbe_dichloromethane','pbe1pbe_nndimethylformamide','pbe1pbe_tetrahydrofuran','bhandhlyp','bhandhlyp_dichloromethane','bhandhlyp_nndimethylformamide','bhandhlyp_tetrahydrofuran']
    method = ['mexc_tetrahydrofuran']
    timedict = {}
    for name in os.listdir(path_to_benchmarks):
        for x in method:
            value = timegrabber(path_to_benchmarks,x,name)
            #print(value)
            timedict[name] = value
    print(timedict)

    #print(timedict)
    print(average(timedict,len(timedict),x))
    
       #     print(name)
       #     print(i)
       #     print(name)

 #   method = 'mexc'
 #   method = 'pbe1pbe'
 #   method = 'bhandhlyp'
 #   method = 'bhandhlyp_dichloromethane'
 #   method = 'bhandhlyp_nndimethylformamide'
 #   method = 'bhandhlyp_tetrahydrofuran'
 #   method = 'mexc_dichloromethane'
 #   method = 'mexc_nndimethylformamide'
 #   method = 'mexc_tetrahydrofuran'
 #   method = 'pbe1pbe_dichloromethane'
 #   method = 'pbe1pbe_nndimethylformamide'
 #   method = 'pbe1pbe_tetrahydrofuran'



    #    timedict = timegrabber(path_to_benchmarks,x)
    #print(len(timedict))
    #    print(average(timedict,len(timedict),x))
    


    return
main()