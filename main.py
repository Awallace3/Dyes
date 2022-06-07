import json
import src
from src.molecule_json import Molecule_exc_to_db
import pickle
import matplotlib.pyplot as plt
import pandas as pd


def write_pickle(data, fname='mol.pickle'):
    with open(fname, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_pickle(fname='mol.pickle'):
    with open(fname, 'rb') as handle:
        return pickle.load(handle)


# def user(x, y):
#     filename = open(x + "/" + "user", "w+")
#     filename.write(y)
#     filename.close()
#     return
#
#
# def combiner(method, data):
#     three_types = data["generateMolecules"]["three_types"]
#     banned = data["generateMolecules"]["banned"]
#
#     localStructuresDict = collectLocalStructures(three_types, banned)
#     smiles_tuple_list = permutationDict(localStructuresDict)
#     print("smiles_tuple_list", smiles_tuple_list)
#     monitor_jobs = generateMolecules(
#         smiles_tuple_list,
#         data["generateMolecules"]["method_opt"],
#         data["generateMolecules"]["basis_set_opt"],
#         data["generateMolecules"]["mem_com_opt"],
#         data["generateMolecules"]["mem_pbs_opt"],
#         data["generateMolecules"]["cluster"],
#     )
#     jobResubmit_v2(
#         monitor_jobs,
#         data["generateMolecules"]["resubmit_delay_min"],
#         data["generateMolecules"]["resubmit_max_attempts"],
#         data["generateMolecules"]["method_opt"],
#         data["generateMolecules"]["basis_set_opt"],
#         data["generateMolecules"]["mem_com_opt"],
#         data["generateMolecules"]["mem_pbs_opt"],
#         data["excitation"]["method_mexc"],
#         data["excitation"]["basis_set_mexc"],
#         data["excitation"]["mem_com_mexc"],
#         data["excitation"]["mem_pbs_mexc"],
#         data["generateMolecules"]["cluster"],
#         data["path"]["path_to_results"],
#         method,
#         data["generateMolecules"]["max_queue"],
#         data["generateMolecules"]["results_json"],
#     )
#
#     return
#
#
# def pbs(data):
#     for name in data["geomopt"]["dyeoptlist"]:
#         if data["geomopt"]["procedure"] == "opt":
#             gaussianpbsFiles(
#                 data["geomopt"]["method_opt"],
#                 data["geomopt"]["basis_set_opt"],
#                 data["geomopt"]["mem_com_opt"],
#                 data["geomopt"]["mem_pbs_opt"],
#                 data["geomopt"]["cluster"],
#                 name,
#                 baseName="mex",
#                 outName="mexc_o",
#             )
#
#         if data["geomopt"]["procedure"] == "exc":
#             gaussianpbsFiles(
#                 data["geomopt"]["method_opt"],
#                 data["geomopt"]["basis_set_opt"],
#                 data["geomopt"]["mem_com_opt"],
#                 data["geomopt"]["mem_pbs_opt"],
#                 data["geomopt"]["cluster"],
#                 name,
#                 baseName="mexc",
#                 outName="mexc_o",
#             )
#         os.chdir(data["path"]["path_to_results"])
#     return
#
#
# def opt(data):
#     for name in data["geomopt"]["dyeoptlist"]:
#         if data["geomopt"]["procedure"] == "opt":
#             gaussianInputFiles(
#                 data["geomopt"]["method_opt"],
#                 data["geomopt"]["basis_set_opt"],
#                 data["geomopt"]["mem_com_opt"],
#                 data["geomopt"]["mem_pbs_opt"],
#                 data["geomopt"]["cluster"],
#                 baseName="mex",
#                 procedure="OPT",
#                 data="",
#                 dir_name=name,
#                 solvent=data["geomopt"]["solvent"],
#                 outName="mexc_o",
#             )
#         os.chdir(data["path"]["path_to_results"])
#     return
#
#
# def add_methods(data):
#     return data["add_methods"]
#
#
# def resubmit(method, data):
#     jobResubmit_v2(
#         data["excitation"]["dyeList"],
#         data["excitation"]["resubmit_delay_min"],
#         data["excitation"]["resubmit_max_attempts"],
#         data["excitation"]["method_opt"],
#         data["excitation"]["basis_set_opt"],
#         data["excitation"]["mem_com_opt"],
#         data["excitation"]["mem_pbs_opt"],
#         data["excitation"]["method_mexc"],
#         data["excitation"]["basis_set_mexc"],
#         data["excitation"]["mem_com_mexc"],
#         data["excitation"]["mem_pbs_mexc"],
#         data["excitation"]["cluster"],
#         data["path"]["path_to_results"],
#         method,
#         data["excitation"]["max_queue"],
#         data["excitation"]["results_json"],
#     )
#     return
#
#
# def qsuber(data):
#     os.chdir(data["path"]["path_to_results"])
#     for name in data["geomopt"]["dyeoptlist"]:
#         os.chdir(name)
#         os.system("qsub mex.pbs")
#         os.chdir("..")
#     return

# def main():
#     filename = "input.json"
#     with open(str(filename), "r") as read_file:
#         config = json.load(read_file)
#     # user(config["path"]["path_to_final"], config["user"]["user"])
#
#     # if config["generateMolecules"]["enable"]:
#     #     os.chdir(config["path"]["path_to_final"])
#         # add_methods_1 = add_methods(config)
#         # combiner(add_methods_1, config)
#
#     # ans3 = config["geomopt"]["enable"]
#     # ans3 = ans3.lower()
#     # if opt_enabled and not exc_enabled:
#     #     os.chdir(config["path"]["path_to_results"])
#         # pbs(config)
#         # opt(config)
#         # if config["geomopt"]["submit"] == "no":
#         #     qsuber(config)
#
#     opt_enabled = config["qmgr"]["options"]["opt"]
#     exc_enabled = config["qmgr"]["options"]["opt"]
#     if opt_enabled and exc_enabled:
#         src.qmgr(config["qmgr"])
#     return

# def json_to_db():
#     Molecule_exc_to_db('./json_files/test.json',
#                        "./json_files/test2.json")


def method_name_converter(method: str):
    v = ""
    c = ""
    if method == 'lsf':
        v = "LSF"
        c = "green"
    elif method == "CAM_B3LYP_6_311G_d_p":
        v = "CAM-B3LYP/6-311G(d,p)"
        c = "blue"
    elif method == "PBE1PBE_6_311G_d_p":
        v = "PBE1PBE/6-311G(d,p)"
        c = "orange"
    elif method == "bhandhlyp_6_311G_d_p":
        v = "BHandHLYP/6-311G(d,p)"
        c = "red"
    else:
        print("Method not supported ")
    return v, c


def convert_units(v):
    h = 6.626e-34
    c = 3e17
    Joules_to_eV = 1.602e-19
    v = h * c / (v * Joules_to_eV)
    return v


def plot_absoprtion_lambda_max(pickle_path="./pickles/ds_all5.pickle",
                               plot_methods=[
                                   "CAM_B3LYP_6_311G_d_p",
                                   "PBE1PBE_6_311G_d_p",
                                   "bhandhlyp_6_311G_d_p",
                                   "lsf",
                               ],
                               sort_by="lsf",
                               units="nm",
                               output="theory_abs.png",
                               transparent=True):
    """
    Plots the theoretical absorption data with filtering incomplete
    excitation data or egregiously incorrect predictions
    """
    data = read_pickle(pickle_path)
    plot_dict = {}
    for i in plot_methods:
        plot_dict[i] = []
    for k, v in data.items():
        for i in plot_methods:
            if i in v:
                e = -1
                for j in v[i]:
                    if j["exc"] == 1:
                        e = j["nm"]
                        break
                if e != -1:
                    if units == "eV":
                        e = convert_units(e)
                    plot_dict[i].append(e)
                elif i == sort_by:
                    plot_dict[i].append(0)
                else:
                    plot_dict[i].append(None)
            elif i == sort_by:
                plot_dict[i].append(0)
            else:
                plot_dict[i].append(None)
    df = pd.DataFrame(plot_dict)
    df = df.sort_values(sort_by)

    # This filters out dyes with incomplete excitation data
    df = df[df[sort_by] != 0]
    # This filters bad excitations predictions
    df = df[df[sort_by] < 1500]

    df[sort_by].dropna()
    xs = range(len(df[sort_by]))
    print(len(xs))
    for k in plot_methods:
        label, color = method_name_converter(k)
        plt.plot(xs, df[k], color=color, label=label, linewidth=0.5)
    plt.xlabel("Theoretical Dyes")
    plt.ylabel("Excitation Energy (%s)" % units)
    plt.grid(color="grey",
             which="major",
             axis="y",
             linestyle="-",
             linewidth=0.2)
    plt.legend()
    out_path = "data_analysis/%s" % (output)
    plt.savefig(out_path, transparent=transparent)
    plt.show()
    return


def main():
    plot_absoprtion_lambda_max()

    return


if __name__ == "__main__":
    # main()
    # json_to_db()
    main()
