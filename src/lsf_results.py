from . import molecule_json


class lsfExcGather():
    """ docstring for lsfExcGather."""
    def __init__(self, v_abs, v_homo, v_lumo, v_osci):
        self.v_abs = v_abs
        self.v_homo = v_homo
        self.v_lumo = v_lumo
        self.v_osci = v_osci

    def getDict(self):
        return {
            "v_abs": self.v_abs,
            "v_homo": self.v_homo,
            "v_lumo": self.v_lumo,
            "v_osci": self.v_osci,
        }


def conv_energy(val, rounding=3):
    h = 6.626e-34
    c = 2.998e17
    J_over_eV = 1.602e-19
    return round(h * c / (float(val) * J_over_eV), rounding)


def generate_lsf_exc(results_json="../json_files/benchmarks_exc.json", output_json="../json_files/test.json"):
    moleculeList = molecule_json.MoleculeList_exc()
    moleculeList.setData(results_json)
    homo_lsf = [1.0423105, -0.20338681]  # CAM - PBE
    lumo_lsf = [-0.01785889, 1.22883249]  # CAM - PBE
    nm_lsf = [1.24306358, -0.38355558]  # CAM - PBE

    d = moleculeList.getMoleculeList()
    for n, mol in enumerate(d):
        excs = mol.getExcitations()
        # Gather cam and pbe0
        cam = {}
        pbe0 = {}

        for ex in excs:
            tmp_dict = ex.toDict()
            v_abs = tmp_dict["nm"]
            v_homo = tmp_dict["HOMO"]
            v_lumo = tmp_dict["LUMO"]
            v_osci = tmp_dict["osci"]
            p = tmp_dict["exc"]
            if (tmp_dict["method_basis_set"] == "CAM-B3LYP/6-311G(d,p)"):
                cam["exc%d" % p] = lsfExcGather(v_abs, v_homo, v_lumo, v_osci)

            if (tmp_dict["method_basis_set"] == "PBE1PBE/6-311G(d,p)"):
                pbe0["exc%d" % p] = lsfExcGather(v_abs, v_homo, v_lumo, v_osci)

                # do coefficient math...
        for e in cam.keys():
            if e in pbe0:
                c_d = cam[e].getDict()
                cam_h = c_d["v_homo"]
                cam_l = c_d["v_lumo"]
                cam_o = c_d["v_osci"]
                cam_nm = c_d['v_abs']
                p_d = cam[e].getDict()
                pbe0_h = p_d["v_homo"]
                pbe0_l = p_d["v_lumo"]
                pbe0_o = c_d["v_osci"]
                pbe0_nm = p_d['v_abs']
                homo = homo_lsf[0] * cam_h + homo_lsf[1] * pbe0_h
                lumo = lumo_lsf[0] * cam_l + lumo_lsf[1] * pbe0_l
                nm = nm_lsf[0] * conv_energy(cam_nm) + nm_lsf[1] * conv_energy(
                    pbe0_nm)
                nm = conv_energy(nm)
                osci = nm_lsf[0] * cam_o + nm_lsf[1] * pbe0_o
                new_d = {
                    "exc":
                    int(e[-1]),
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
    moleculeList.sendToFile(output_json)
    return


def main():
    moleculeList = molecule_json.MoleculeList_exc()
    moleculeList.setData("../json_files/results_ds5.json")
    homo_lsf = [1.0423105, -0.20338681]  # CAM - PBE
   # lumo_lsf = [-0.01785889, 1.22883249]  # CAM - PBE
    lumo_lsf = [0.76, 0.67]
  #  nm_lsf = [1.24306358, -0.38355558]  # CAM - PBE
    nm_lsf = [1.31, -0.47]

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
            lumo,
            "HOMO":
            homo,
        }
        new_exc = molecule_json.Excitation_exc()
        new_exc.giveData(new_d)
        mol.appendExcitations([new_exc])
        d[n] = mol
    moleculeList.setMolecules(d)
    moleculeList.sendToFile("../json_files/test.json")


# main()
if __name__ == "__main__":
    generate_lsf_exc("../json_files/results_ds5.json")
