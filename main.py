import json
import src
from src.molecule_json import Molecule_exc_to_db

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


def json_to_db():
    Molecule_exc_to_db('./json_files/test.json',
                       "./json_files/test2.json")


if __name__ == "__main__":
    # main()
    json_to_db()
