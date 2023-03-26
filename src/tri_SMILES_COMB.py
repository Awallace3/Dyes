def eDonor_1(smi):
    filename = open("../eDonors/" + smi, "r")
    data = filename.readlines()

    return data[0].replace("\n", "")
def eDonor_2(smi):
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
    num4 = []
    num5 = []


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

    for num, i in enumerate(smi[3]):
        if (
            smi[3][num] == "%"
            or smi[3][num - 1] == "%"
            or smi[3][num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(smi[2][num + 1 : num + 3])
                new = str(new)
                edit = edit.replace("*", "%")
                num4.append(int(new))
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
                num4.append(int(i))

    for num, i in enumerate(smi[4]):
        if (
            smi[4][num] == "%"
            or smi[4][num - 1] == "%"
            or smi[4][num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(smi[2][num + 1 : num + 3])
                new = str(new)
                edit = edit.replace("*", "%")
                num5.append(int(new))
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
                num5.append(int(i))


    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
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
    if num4 == []:
        d += 0
    else:
        num4.sort()
        d = max(num4) + c
    if num5 == []:
        e += 0
    else:
        num5.sort()
        e = max(num5) + d
    # print((a,b,c))

    return a, b, c, d, e


def check(smi, add):
    eDonor = smi[0]
    eDonor_2 = smi[1]
    eDonor_3 = smi[2]
    Backbones = smi[3]
    eAcceptor = smi[4]
    eDonor_updt = ""
    eDonor_2_updt = ""
    eDonor_3_updt = ""

    Backbones_updt = ""
    eAcceptor_updt = ""
    for num, i in enumerate(eDonor):
        #print(i)
        if (
            eDonor[num] == "%"
            or eDonor[num - 1] == "%"
            or eDonor[num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(eDonor[num + 1 : num + 3]) + add[2]
                new = str(new)
                edit = edit.replace("*", "%")
                eDonor_updt += edit + new
        else:
            try:
                i = int(i)
                if i + add[2] > 10:
                    i = i + add[2]
                    i = "%" + str(i)
                    eDonor_updt += str(i)
                elif i + add[1] > 100:
                    print(
                        "SMILES string value is greater than 100 and further analysis needed."
                    )
                else:
                    i = int(i) + add[2]
                    eDonor_updt += str(i)

            except ValueError:
                #print('Value error edonor 1')
                eDonor_updt+= i



    for num, i in enumerate(eDonor_2):
        if (
            eDonor_2[num] == "%"
            or eDonor_2[num - 1] == "%"
            or eDonor_2[num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(eDonor_2[num + 1 : num + 3]) + add[2]
                new = str(new)
                edit = edit.replace("*", "%")
                eDonor_2_updt += edit + new
        else:
            try:
                i = int(i)
                if i + add[2] > 10:
                    i = i + add[2]
                    i = "%" + str(i)
                    eDonor_2_updt += str(i)
                elif i + add[1] > 100:
                    print(
                        "SMILES string value is greater than 100 and further analysis needed."
                    )
                else:
                    i = int(i) + add[2]
                    eDonor_2_updt += str(i)

            except ValueError:
                #print('Value error edonor_2')
                
                eDonor_2_updt+= i

    for num, i in enumerate(eDonor_3):
        if (
            eDonor_3[num] == "%"
            or eDonor_3[num - 1] == "%"
            or eDonor_3[num - 2] == "%"
        ):
            edit = str(i).replace("%", "*")
            if "*" in edit:
                new = int(eDonor_3[num + 1 : num + 3]) + add[2]
                new = str(new)
                edit = edit.replace("*", "%")
                eDonor_3_updt += edit + new
        else:
            try:
                i = int(i)
                if i + add[2] > 10:
                    i = i + add[2]
                    i = "%" + str(i)
                    eDonor_3_updt += str(i)
                    #print(i)
                elif i + add[1] > 100:
                    print(
                        "SMILES string value is greater than 100 and further analysis needed."
                    )
                else:
                    i = int(i) + add[2]
                    #print(i)

                    eDonor_3_updt += str(i)

            except ValueError:
                '''
                gathers all the letters of the SMILES string
                '''
                #print('Value error edonor_3')
                #print(i)
                eDonor_3_updt+= i


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
                #print('Value Error acceptor')
                eAcceptor_updt += i

    return (eDonor_updt,eDonor_2_updt,eDonor_3_updt,Backbones_updt, eAcceptor_updt)


def combine(smi):
    #print(smi)
    x = smi[0].replace("BBD", "%98").replace("BBA", "%99")
    y = smi[1].replace("BBD", "%97").replace("BBA", "%99")
    j = smi[2].replace("BBD", "%96").replace("BBA", "%99")
   


    z = smi[3].replace("BBA", "%99")
    z = z.split('BBD')
    z = z[0]+'%98'+z[1]+'%97'+z[2]+'%96'+z[3] 



    k = smi[4].replace("BBD", "%98").replace("BBA", "%99")
    return x + "." + y + "." + j + "." + z + "." + k


def SMILES_COMB(smi1, smi2, smi3, smi4, smi5):
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
    """
    smi1 = 'COC1=CC=C(N(C2=CC=C(OC)C=C2)C3=CC=C((BBD))C=C3)C=C1'
    smi2 = 'COC1=CC=C(N(C2=CC=C(OC)C=C2)C3=CC=C((BBD))C=C3)C=C1' 
    smi3 = 'COC1=CC=C(N(C2=CC=C(OC)C=C2)C3=CC=C((BBD))C=C3)C=C1'
    smi4 = 'C(BBA)1=C2C=C((BBD))C((BBD))=CC2=C((BBD))S1'
    smi5 = 'N#C/C(C(O)=O)=C\(BBA)'
    """


    
    # print(("I am the Little Train that could"))
    smi = (smi1, smi2, smi3, smi4, smi5)
    print('smi1 =  '+ "'" +str(smi1)+"'")
    print('smi2 =  '+ "'" +str(smi2)+"'")
    print('smi3 =  '+ "'" +str(smi3)+"'")
    print('smi4 =  '+ "'" +str(smi4)+"'")
    print('smi5 =  '+ "'" +str(smi5)+"'")
    print('If there is a index error more and likely it is SMILES_COMB.\n The above smi variables and can be copied and pasted and will help figure out what is wrong')
    max1 = number_gather(smi)

    uptsmiles = check(smi, max1)
    
    

    return combine(uptsmiles)
'''
comment everything below if running for trifinal.py
'''
"""

smi1 =  'CN1C(C)(C)CC(C)C2=C1C=CC((BBD))=C2'
smi2 =  'CN1C(C)(C)CC(C)C2=C1C=CC((BBD))=C2'
smi3 =  'CN1C(C)(C)CC(C)C2=C1C=CC((BBD))=C2'
smi4 =  'C(BBA)1=C2C=C((BBD))C((BBD))=CC2=C((BBD))S1'
smi5 =  'C(BBA)1=C(C=CS2)C2=C(/C=C(C(O)=O)\C#N)S1'
#main(smi1,smi2,smi3)
SMILES_COMB(smi1, smi2, smi3, smi4, smi5)
"""



