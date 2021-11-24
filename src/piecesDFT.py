import os

def eAcceptor(path):
    os.chdir(path)
    for i in os.listdir():
        if '.smi' in i:
            filename= open(i,'r')
            data = filename.readlines()
            print(str(data[0]).replace('(BBA)',''))
            cmd = 'obabel -:' + str(data[0]).replace('(BBA)','') +  
            
            #for i in data[0]:
               # print(i)
        #    print(i)



    return



def main():
    path_to_acceptor = '../eAcceptors/'
    eAcceptor(path_to_acceptor)
    #print('LLL')



    return
main()
