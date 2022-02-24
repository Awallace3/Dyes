import os


def monitor():
    filename = open("monitor.txt")
    data = filename.readlines()
    data_2 = []
    for i in data:
        i = i.replace("\n", "")
        data_2.append(i)
    #  print(len(data))
    return data_2


def results(path):
    os.chdir(path)
    directory = []

    for i in os.listdir():
        if "smiles_input" in i:
            i
        else:
            directory.append(i)
    # print(len(directory))
    return directory


def tmp():
    filename = open("tmp.dat")
    data = filename.readlines()
    data_3 = []
    for i in data:
        i = i.replace("\n", "")
        data_3.append(i)
    #  print(len(data))
    return data_3


def deleter(path):

    return


def main():
    path_to_results = "results/"
    monitor()
    # results(path_to_results)
    directory = results(path_to_results)
    os.chdir("..")
    data = monitor()
    # data_3 = set(data)-set(directory)
    # different ones that are in monitor tex
    data_3 = set(directory) - set(data)
    data_3 = list(data_3)
    print(data_3)
    for i in data_3:
        i
    print(len(data_3))

    return


main()
