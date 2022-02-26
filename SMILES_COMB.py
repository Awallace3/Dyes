def eDonor(smi):
    filename = open("../eDonors/" + smi, "r")
    data = filename.readlines()

    return data[0].replace("\n", "")


def eAcceptor(smi):
    filename = open("../eAcceptors/" + smi, "r")
    data = filename.readlines()

    return data[0].replace("\n", "")


def Backbones(smi):
    filename = open("../backbones/" + smi, "r")
    data = filename.readlines()

    return data[0].replace("\n", "")


def number_gather(smi):
    # print(smi[0])
    num1 = []
    num2 = []
    num3 = []
    for num, i in enumerate(smi[0]):
        if (
            smi[0][num] == "%"
            or smi[0][num - 1] == "%"
            or smi[0][num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(smi[0][num + 1 : num + 3])
                new = str(new)
                edit = edit.replace("*", "%")
                num1.append(int(new))
        #  print(smi[0][num:num+2])
        else:
            if (
                i == "0"
                or i == "1"
                or i == "2"
                or i == "3"
                or i == "4"
                or i == "5"
                or i == "6"
                or i == "7"
                or i == "8"
                or i == "9"
            ):
                num1.append(int(i))

    for num, i in enumerate(smi[1]):
        if (
            smi[1][num] == "%"
            or smi[1][num - 1] == "%"
            or smi[1][num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(smi[1][num + 1 : num + 3])
                new = str(new)
                edit = edit.replace("*", "%")
                num2.append(int(new))
        #  print(smi[0][num:num+2])
        else:
            if (
                i == "0"
                or i == "1"
                or i == "2"
                or i == "3"
                or i == "4"
                or i == "5"
                or i == "6"
                or i == "7"
                or i == "8"
                or i == "9"
            ):
                num2.append(int(i))

    for num, i in enumerate(smi[2]):
        if (
            smi[2][num] == "%"
            or smi[2][num - 1] == "%"
            or smi[2][num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(smi[2][num + 1 : num + 3])
                new = str(new)
                edit = edit.replace("*", "%")
                num3.append(int(new))
        #  print(smi[0][num:num+2])
        else:
            if (
                i == "0"
                or i == "1"
                or i == "2"
                or i == "3"
                or i == "4"
                or i == "5"
                or i == "6"
                or i == "7"
                or i == "8"
                or i == "9"
            ):
                num3.append(int(i))
    a = 0
    b = 0
    c = 0
    if num1 == []:
        a += 0
    else:
        num1.sort()
        a += max(num1)
    if num2 == []:
        b += 0
    else:
        num2.sort()
        b += max(num2) + a
    if num3 == []:
        c += 0
    else:
        num3.sort()
        c = max(num3) + b
    # print((a,b,c))

    return a, b, c


def check(smi, add):
    eDonor = smi[0]
    Backbones = smi[1]
    eAcceptor = smi[2]
    # print((eDonor,Backbones,eAcceptor))
    Backbones_updt = ""
    eAcceptor_updt = ""

    for num, i in enumerate(Backbones):
        if (
            Backbones[num] == "%"
            or Backbones[num - 1] == "%"
            or Backbones[num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(Backbones[num + 1 : num + 3]) + add[1]
                new = str(new)
                edit = edit.replace("*", "%")
                Backbones_updt += edit + new
        else:
            try:
                i = int(i)
                if i + add[1] > 10:
                    i = i + add[1]
                    i = "%" + str(i)
                    Backbones_updt += str(i)
                elif i + add[1] > 100:
                    print(
                        "SMILES string value is greater than 100 and further analysis needed."
                    )
                else:
                    i = int(i) + add[1]
                    Backbones_updt += str(i)

            except ValueError:
                Backbones_updt += i
    for num, i in enumerate(eAcceptor):
        if (
            eAcceptor[num] == "%"
            or eAcceptor[num - 1] == "%"
            or eAcceptor[num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(eAcceptor[num + 1 : num + 3]) + add[2]
                new = str(new)
                edit = edit.replace("*", "%")
                eAcceptor_updt += edit + new
        else:
            try:
                i = int(i)
                if i + add[2] > 10:
                    i = i + add[2]
                    i = "%" + str(i)
                    eAcceptor_updt += str(i)
                elif i + add[1] > 100:
                    print(
                        "SMILES string value is greater than 100 and further analysis needed."
                    )
                else:
                    i = int(i) + add[2]
                    eAcceptor_updt += str(i)

            except ValueError:
                eAcceptor_updt += i

    return (eDonor, Backbones_updt, eAcceptor_updt)


def combine(smi):
    x = smi[0].replace("BBD", "%98").replace("BBA", "%99")
    y = smi[1].replace("BBD", "%98").replace("BBA", "%99")
    z = smi[2].replace("BBA", "%99").replace("BBD", "%98")
    return x + "." + y + "." + z


def SMILES_COMB(smi1, smi2, smi3):
    """

    #smi1_f = ['2ed.smi','5ed.smi']
    smi1_f = ['5ed.smi']
    #smi2_f = ['34b.smi','1b.smi']
    smi2_f = ['1b.smi']
    #smi3_f = ['6ea.smi','9ea.smi']
    smi3_f = ['8ea.smi']
    smi1='COC1=CC=C(N(C2=CC=C(OC)C=C2)C3=CC=C((BBD))C=C3)C=C1'
    smi2='C(C=C1)=CC=C1C(C2=C3SC4=C2SC5=C4C(C6=CC=C(C)C=C6)(C7=CC=C(C)C=C7)C8=C9C5=C(C=CC=C%10)C%10=C((BBA))C9=CC=C8)(C%11=CC=C(C)C=C%11)C%12=CC=CC%13=C((BBD))C%14=C(C=CC=C%14)C3=C%13%12'
    smi3= 'N#C/C(C(O)=O)=C\(BBA)'
    """

    """


    for x in smi3_f:
        smi1 += eAcceptor(x)
        print(smi1)


    for x in smi1_f:
        smi3 += eDonor(x)
        print(smi3)

    for x in smi2_f:
        smi2+=Backbones(x)
        print(smi2)
    """

    # print(("I am the Little Train that could"))
    smi = (smi1, smi2, smi3)
    max1 = number_gather(smi)

    uptsmiles = check(smi, max1)

    return combine(uptsmiles)
# main(smi1,smi2,smi3)

