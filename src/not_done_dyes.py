

def Notdone(name):
    filename = open(name,'r')
    data = filename.readlines()
    not_done = []
    for line in data[1:]:
        line = line.split(',')
        name = line[0]
        if len(line)!=4:
            #print(line)
            if line[2] == '"bhandhlyp/6-311G(d':
                not_done.append(str(name)+"/bhandhlyp/")
            if line[3] == '"PBE1PBE/6-311G(d' or line[4]=='"PBE1PBE/6-311G(d' :
                not_done.append(str(name)+"/pbe1pbe/")
            
          #  not_done.append(name)
   # print(len(not_done))
    print(not_done)
        
        


    return not_done

def main():
    csv_file = '../data_analysis/Absorption_nm.csv'
    Notdone(csv_file)


    return
main()