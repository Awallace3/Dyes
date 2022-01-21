import glob 

def dir_to_list(path):
    ls = glob.glob(path + "/*ed*b*ea")
    for i in range(len(ls)):
        ls[i] = ls[i].split('/')[-1]
    print(ls)
if __name__ == "__main__":
    dir_to_list('../results')
