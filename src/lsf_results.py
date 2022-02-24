import molecule_json


def main():
    moleculeList = molecule_json.MoleculeList_exc()
    moleculeList.setData("../json_files/results_exc.json")
    d = moleculeList.getMoleculeList()
    for n, mol in enumerate(d):
        excs = mol.getExcitations()
        # Gather cam and pbe0
        for ex in excs:
            tmp_dict = ex.toDict()
            # print(tmp_dict["method_basis_set"])
            # print(tmp_dict["nm"])
            # print(tmp_dict["HOMO"])
            # print(tmp_dict["LUMO"])

        # do coefficient math...

        # create new excitation and update fields
        new_d = {
            "exc": "1",
            "method_basis_set": "LSF",
            "nm": 0,
            "osci": 0,
            "orbital_Numbers": [
                # put coefficients here as an array of floats
            ],
            "LUMO": 0,
            "HOMO": 0,
        }
        new_exc = molecule_json.Excitation_exc()
        new_exc.giveData(new_d)
        mol.appendExcitations([new_exc])
        d[n] = mol
    moleculeList.setMolecules(d)
    moleculeList.sendToFile("../json_files/test.json")


main()
