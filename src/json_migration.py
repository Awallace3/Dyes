from molecule_json import *
import json

def molecule_list_json_to_exc(path_results_json='../results.json', path_out_json='../results_exc.json', exp=False):
    with open(path_results_json) as json_file:
        og_json = json.load(json_file)
    added = []
    # print(og_json)
    mol_lst = MoleculeList()

    for molecule in og_json['molecules']:
        if molecule["name"] not in added:
            added.append(molecule['name'])
            molecule.pop("HOMO")
            molecule.pop("LUMO")
            if exp:
                new_mol = Molecule_exc_BM()
            else:
                new_mol = Molecule_exc()
            cp_mol = molecule.copy()
            cp_mol["excitations"] = []
            new_mol.giveData(cp_mol)

            local_excitations = []
            for exc in molecule['excitations']:
                new_exc = Excitation_exc()
                if exc:
                    new_exc.giveOldData(exc)
                else:
                    print('else', exc)
                # print('new exc', new_exc)
                local_excitations.append(new_exc)

            new_mol.appendExcitations(local_excitations)
            mol_lst.addMolecule(new_mol)
    mol_lst.sendToFile(path_out_json)
    # print(json_obj)


def main():
    # molecule_list_json_to_exc('../Benchmark/benchmarks.json', '../Benchmark/benchmarks_exc.json', exp=True)
    molecule_list_json_to_exc('../results.json', '../results_exc.json', exp=False)

if __name__ == "__main__":
    main()
