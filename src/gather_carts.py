from glob import glob
import pickle
import os


def write_pickle(data, fname='mol.pickle'):
    with open(fname, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_pickle(fname='mol.pickle'):
    with open(fname, 'rb') as handle:
        return pickle.load(handle)


def read_carts_com(fn: str):
    if not os.path.exists(fn):
        return None
    with open(fn) as f:
        data = f.read()
    data = data.split("\n0 1\n")[1].replace("\n\n", "\n").replace(
        "\n\n", "\n").replace("  ", " ").replace("  ", " ")
    xyz = data.split("\n")[:-1]
    order = []
    new_xyz = []
    for n, i in enumerate(xyz):
        s = i.split(" ")
        coords = []
        for j, k in enumerate(s):
            if j == 0:
                k = "".join([i for i in k if i.isalpha()])
                order.append(k)
            else:
                coords.append(float(k))
        new_xyz.append(coords)
    xyz = {"order": order, "xyz": new_xyz}
    return xyz


def create_mol_dict(path_results: str, exc_fp="/mexc/mexc.com"):
    mol_dict = {}
    data = glob(path_results)
    print(len(data))
    for i in data:
        xyz = read_carts_com(i + exc_fp)
        if xyz is None:
            continue
        name = i.split("/")[-1]
        mol_dict[name] = xyz
    return mol_dict


def main():
    mol_dict = create_mol_dict("../results_cp/ds_all5/*")
    write_pickle(mol_dict, 'dyes_xyz.pickle')
    return


if __name__ == "__main__":
    main()
