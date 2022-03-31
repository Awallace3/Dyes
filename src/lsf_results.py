import molecule_json


def conv_energy(val, rounding=3):
    h = 6.626e-34
    c = 2.998e17
    J_over_eV = 1.602e-19
    return round(h * c / (float(val) * J_over_eV), rounding)

def main():
    moleculeList = molecule_json.MoleculeList_exc()
    moleculeList.setData("../json_files/results_exc.json")
    homo_lsf = [-0.36764963, -0.38964081]  # CAM - PBE
    lumo_lsf = [-0.95798195, 0.93317353]  # CAM - PBE
    nm_lsf = [1.24306358, -0.38355558]  # CAM - PBE

    d = moleculeList.getMoleculeList()
    for n, mol in enumerate(d):
        excs = mol.getExcitations()
        # Gather cam and pbe0
        cam = 0
        cam_h = 0
        cam_l = 0
        cam_o = 0
        pbe0 = 0
        pbe0_h = 0
        pbe0_l = 0
        pbe0_o = 0
        nm = 0

        for ex in excs:
            tmp_dict = ex.toDict()
            if (tmp_dict["method_basis_set"] == "CAM-B3LYP/6-311G(d,p)"
                    and tmp_dict["exc"] == 1):
                cam = tmp_dict["nm"]
                cam_h = tmp_dict["HOMO"]
                cam_l = tmp_dict["LUMO"]
                cam_o = tmp_dict["osci"]

            if (tmp_dict["method_basis_set"] == "PBE1PBE/6-311G(d,p)"
                    and tmp_dict["exc"] == 1):
                pbe0 = tmp_dict["nm"]
                pbe0_h = tmp_dict["HOMO"]
                pbe0_l = tmp_dict["LUMO"]
                pbe0_o = tmp_dict["osci"]

        # do coefficient math...
        if cam != 0 and pbe0 != 0:
            homo = homo_lsf[0] * cam_h + homo_lsf[1] * pbe0_h
            lumo = lumo_lsf[0] * cam_l + lumo_lsf[1] * pbe0_l
            nm = nm_lsf[0] * conv_energy(cam) + nm_lsf[1] * conv_energy(pbe0)
            nm = conv_energy(nm)
            osci = nm_lsf[0] * cam_o + nm_lsf[1] * pbe0_o
            if cam > 700:
                print(cam, pbe0, nm)
        else:
            continue

        # create new excitation and update fields
        new_d = {
            "exc":
            1,
            "method_basis_set":
            "LSF",
            "nm":
            nm,
            "osci":
            osci,
            "orbital_Numbers": [
                # put coefficients here as an array of floats
                homo_lsf,
                lumo_lsf,
                nm_lsf
            ],
            "LUMO":
            homo,
            "HOMO":
            lumo,
        }
        new_exc = molecule_json.Excitation_exc()
        new_exc.giveData(new_d)
        mol.appendExcitations([new_exc])
        d[n] = mol
    moleculeList.setMolecules(d)
    moleculeList.sendToFile("../json_files/test.json")


main()
