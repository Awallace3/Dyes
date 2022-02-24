import os
import json


def checker(data):
    ans = {}

    for num, name in enumerate(data["molecules"]):
        test = 0
        if data["molecules"][num]["excitations"] == []:
            test += 0
        else:
            for name in data["molecules"][num]["excitations"]:
                if name["method_basis_set"] == "PBE1PBE/6-311G(d,p)":
                    test += 1
                if name["method_basis_set"] == "CAM-B3LYP/6-311G(d,p)":
                    test += 1
        if test == 6:
            ans[data["molecules"][num]["name"]] = True
        else:
            ans[data["molecules"][num]["name"]] = False
        # print(ans)

    return ans


def camexc(data, num):
    # print(data["molecules"][0]["name"])
    camexc = {}
    if data["molecules"][num]["excitations"] == []:
        #    print((data["molecules"][num]["name"],"CAM Name"))
        camexc[data["molecules"][num]["name"]] = "CAM or PBE is not completed"
    else:
        for name in data["molecules"][num]["excitations"]:
            if name["exc"] == 1:
                if name["method_basis_set"] == "CAM-B3LYP/6-311G(d,p)":
                    camexc[data["molecules"][num]["name"]] = name["nm"]
    return camexc


def pbeexc(data, num):
    pbeex = {}
    if data["molecules"][num]["excitations"] == []:
        print((data["molecules"][num]["name"], "PBE Empty"))
        print(data["molecules"][num]["excitations"])
        # print((data["molecules"][num]["name"],"PBE Name"))
        pbeex[data["molecules"][num]["name"]] = "CAM or PBE is not completed"
    else:
        print((data["molecules"][num]["name"], "PBE Name"))
        print(data["molecules"][num]["excitations"])
        for name in data["molecules"][num]["excitations"]:
            if name["exc"] == 1:
                if name["method_basis_set"] == "PBE1PBE/6-311G(d,p)":
                    pbeex[data["molecules"][num]["name"]] = name["nm"]

    return pbeex


def lsf(cam, pbe, data, contrib1, contrib2, num):
    lsfnm = {}
    lsfev = {}
    molname = data["molecules"][num]["name"]
    print(molname)
    # print(pbe[molname])
    if (
        cam[molname] == "CAM or PBE is not completed"
        or pbe[molname] == "CAM or PBE is not completed"
    ):
        print(molname)
        #  print('Cam or pbe are not done')
        lsfnm[molname] = "Cam or pbe are not done"
        lsfev[molname] = "Cam or pbe are not done"
    else:
        camev = 1240 / cam[molname]
        pbeev = 1240 / pbe[molname]
        tot = camev * contrib1 + pbeev * contrib2
        totnm = 1240 / tot
        lsfnm[molname] = totnm
        lsfev[molname] = tot
    return [lsfnm, lsfev]


def jsoncreator(cam, pbe, lsf, data, num):
    # lsfconver = json.dumps(lsf,indent=3)

    data["molecules"][num]["STATS"] = {
        "nm": lsf[0][data["molecules"][num]["name"]],
        "eV": lsf[1][data["molecules"][num]["name"]],
    }
    # print(data["molecules"][num])
    with open("json_test.json", "w+") as outfile:
        aaa = json.dumps(data, indent=1)
        # aaa=json.dumps(i,indent=2)
        outfile.write(str(aaa))
    return


def main():
    filename = open("results_exc.json")
    data = json.load(filename)
    test = checker(data)
    for num, name in enumerate(data["molecules"]):
        #   print(test[data["molecules"][num]["name"]])
        if test[data["molecules"][num]["name"]] == True:
            cam = camexc(data, num)
            pbe = pbeexc(data, num)
            lsfcamcontib = 1.255
            lsfpbecontrib = -0.408
            lsf2 = lsf(cam, pbe, data, lsfcamcontib, lsfpbecontrib, num)
            jsoncreator(cam, pbe, lsf2, data, num)
        else:
            print("PBE or CAM are not finished")

    return


main()
