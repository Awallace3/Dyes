import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#from homo_lumo import *
# Genetic algorithm in the future?
"""
json_pandas_molecules dataframe

    'name', 'exc', 'nm','osci', 'method_basis_set', 'orbital_Numbers', 'HOMO','LUMO', 'generalSMILES', 'localName', 'parts',  'SMILES'

"""


def json_pandas_molecule(path_results, results_exc=False):
    print(os.getcwd(), path_results)
    dat = pd.read_json(path_results)
    # print('dat', dat)

    FIELDS = ["name", "localName", "generalSMILES"]
    df = pd.json_normalize(dat["molecules"])
    df[FIELDS]
    # ['A', 'B', 'C'] <-this is your columns order
    if results_exc:
        df = df[[
            "name",
            "parts",
            "generalSMILES",
            "localName",
            "SMILES",
            "excitations",
        ]]
        df = pd.json_normalize(
            data=dat["molecules"],
            record_path="excitations",
            meta=["name", "SMILES", "generalSMILES", "localName", "parts"],
        )
        df = df[[
            "name",
            "exc",
            "nm",
            "osci",
            "method_basis_set",
            "orbital_Numbers",
            "HOMO",
            "LUMO",
            "generalSMILES",
            "localName",
            "parts",
            "SMILES",
        ]]

    else:
        df = df[[
            "name",
            "parts",
            "generalSMILES",
            "localName",
            "SMILES",
            "excitations",
            "HOMO",
            "LUMO",
        ]]
        df = pd.json_normalize(
            data=dat["molecules"],
            record_path="excitations",
            meta=[
                "name",
                "HOMO",
                "LUMO",
                "SMILES",
                "generalSMILES",
                "localName",
                "parts",
            ],
        )
        df = df[[
            "name",
            "exc",
            "nm",
            "osci",
            "method_basis_set",
            "orbital_Numbers",
            "HOMO",
            "LUMO",
            "generalSMILES",
            "localName",
            "parts",
            "SMILES",
        ]]

    return df



def json_pandas_molecule_BM(path_results, exc_json=False):
    dat = pd.read_json(path_results)
    # print(path_results)

    FIELDS = ["name", "localName", "generalSMILES"]
    df = pd.json_normalize(dat["molecules"])
    df[FIELDS]
    for x in dat["molecules"]:
        print(x["name"])
        print(x["exp"])
    # ['A', 'B', 'C'] <-this is your columns order
    if exc_json:
        df = df[[
            "name",
            "parts",
            "generalSMILES",
            "localName",
            "SMILES",
            "excitations",
            "exp",
        ]]
        df = pd.json_normalize(
            data=dat["molecules"],
            record_path="excitations",
            meta=[
                "name",
                "SMILES",
                "generalSMILES",
                "localName",
                "parts",
                "exp",
            ],
        )
        df = df[[
            "name",
            "exc",
            "nm",
            "osci",
            "method_basis_set",
            "orbital_Numbers",
            "HOMO",
            "LUMO",
            "generalSMILES",
            "localName",
            "parts",
            "SMILES",
            "exp",
        ]]

    else:
        df = df[[
            "name",
            "parts",
            "generalSMILES",
            "localName",
            "SMILES",
            "excitations",
            "HOMO",
            "LUMO",
            "exp",
        ]]
        df = pd.json_normalize(
            data=dat["molecules"],
            record_path="excitations",
            meta=[
                "name",
                "HOMO",
                "LUMO",
                "SMILES",
                "generalSMILES",
                "localName",
                "parts",
                "exp",
            ],
        )
        df = df[[
            "name",
            "exc",
            "nm",
            "osci",
            "method_basis_set",
            "orbital_Numbers",
            "HOMO",
            "LUMO",
            "generalSMILES",
            "localName",
            "parts",
            "SMILES",
            "exp",
        ]]
    # print((df,'AAAAAAAAAAAAAAAA'))
    return df


"""
def json_pandas_molecule_BM(path_results):
    # print(path_results)
    # print(os.getcwd())
    dat = pd.read_json(path_results)

    # print(dat)
    FIELDS = ["name", "localName", "generalSMILES"]
    df = pd.json_normalize(dat["molecules"])
    df[FIELDS]
    #['A', 'B', 'C'] <-this is your columns order
    df = df[[
            'name', 'parts',
            'generalSMILES','localName',
            'SMILES', 'excitations',
            'HOMO', 'LUMO', 'exp'
            ]]
    df = pd.json_normalize(data=dat['molecules'], record_path='excitations',
                            meta=['name', 'HOMO','LUMO', 'SMILES', 'generalSMILES','localName', 'parts', 'exp' ])
    df = df [[
    'name', 'exc', 'nm','osci', 'method_basis_set', 'orbital_Numbers', 'HOMO','LUMO', 'generalSMILES', 'localName', 'parts',  'SMILES', 'exp'
    ]]
    return df
"""
"""
Excitation pandas:::

    LocalName   generalSMILES   Excitation1 Excitation2 Excitation3

"""


def nm_osci_df(df):
    nm_osci = df[["nm", "osci", "generalSMILES"]]
    nm_osci = nm_osci.sort_values(["nm", "osci"], ascending=(False, False))
    # print(nm_osci.head(10))
    return nm_osci


def name_nm_df(df):
    name_nm = df[["name", "nm"]]
    return name_nm


def name_nm_osci_LUMO_df(df):
    df = df[["name", "nm", "osci", "LUMO"]]
    return df


def name_nm_osci_LUMO_exc_df(df):
    df = df[["name", "nm", "osci", "LUMO", "exc"]]
    return df


def gen_allowed_dict(df):
    # add logic for filtering through df to determine if flagged or not
    allowed_dict = {}
    for index, row in df.iterrows():
        names = row["name"].split("_")
        a, b, d = names[0], names[1], names[2]
        for i in names:
            allowed_dict[i] = True
    return allowed_dict


def acquire_averages(df, piece_dict, allowed_dict):
    for key, val in piece_dict.items():
        # print((key,val))
        data = {"nm": [], "osci": [], "LUMO": []}
        for index, row in df.iterrows():
            d, b, a = row["name"].split("_")
            # print(row)
            if (key in row["name"] and allowed_dict[d] and allowed_dict[b]
                    and allowed_dict[a] and row["exc"] == 1):
                data["nm"].append(row["nm"])
                data["osci"].append(row["osci"])
                data["LUMO"].append(row["LUMO"])

        # std_nm = np.std(np.array(data['nm']))

        avg_nm = sum(data["nm"]) / len(data["nm"])
        # print(avg_nm)
        avg_osci = sum(data["osci"]) / len(data["osci"])
        avg_LUMO = sum(data["LUMO"]) / len(data["LUMO"])
        piece_dict[key] = [avg_nm, avg_osci, avg_LUMO]
    # print(piece_dict)
    for key, value in piece_dict.items():
        # print(key, value[0])
        print("KEY: %s, nm: %.1f" % (key, value[0]))
    print()

    return piece_dict


def evalAllowed(piece_dict, allowed_dict):
    for key, val in piece_dict.items():
        if val[0] < 430:
            allowed_dict[key] = False
        if val[1] < 0.1:
            allowed_dict[key] = False
        if val[2] > -0.9:
            allowed_dict[key] = False

    return allowed_dict


def score_pieces(df):
    # split name by _
    # for each unique eAccptor, eDonor, backbone -> tally score with weighted targets
    # Could a system of equations be employed to solve for "average" contribution from each piece?

    allowed_dict = gen_allowed_dict(df)

    eA_dict = {}
    eD_dict = {}
    bb_dict = {}
    for i in df["name"]:
        name = i.split("_")
        eA, eD, bb = name[0], name[2], name[1]
        eA_dict[eA] = [0, 0, 0]  # nm_avg, osci_avg,
        eD_dict[eD] = [0, 0, 0]
        bb_dict[bb] = [0, 0, 0]
    """
    Need to update to
    if LUMO < -0.9:
        0.5*lambda/650 + 0.3*f + 0.2*LUMO/-0.1.3
    """
    # bb_dict = acquire_averages(df, bb_dict, allowed_dict)
    # eA_dict = acquire_averages(df, eA_dict, allowed_dict)
    # eD_dict = acquire_averages(df, eD_dict, allowed_dict)

    # allowed_dict = evalAllowed(bb_dict, allowed_dict)
    # allowed_dict = evalAllowed(eA_dict, allowed_dict)
    # allowed_dict = evalAllowed(eD_dict, allowed_dict)

    # print(allowed_dict)

    return


"""
col = df.loc[: , "salary_1":"salary_3"]
where "salary_1" is the start column name and "salary_3" is the end column name

df['salary_mean'] = col.mean(axis=1)
"""


def score_structures(df):
    """
    score_col = []
    for index, row in df.iterrows():
        if row["exc"] == 1:
            nm = row["nm"]
            f = row["osci"]
            LUMO = row["LUMO"]
            if LUMO > -0.9:
                score = NaN
            else:
                score = 0.7*nm/650 + 0.2*f + 0.1*LUMO/-1.3
            print(score)
            score_col.append(score)
    """
    df["score"] = (0.85 * df["nm"] / 650 + 0.10 * df["osci"] +
                   0.05 * df["LUMO"] / -1.3)
    # print(df['score'])
    return df


def total_allowed_dict(allowed_dict):
    total = 0
    for val in allowed_dict.values():
        if val:
            total += 1
    # print("TOTAL =", total)
    return total


def acquire_allowed(allowed_dict):
    allowed = []
    banned = []
    for key, val in allowed_dict.items():
        if val:
            allowed.append(key)
        else:
            banned.append(key)
    return allowed, banned


def score_piece(
    df,
    banned_lst=[],
    structures=["bb"],
    col_name="CAM-B3LYP/6-311G(d,p)",
    score_type="nm",
    above_score=460,
):
    """
    Score structures by each piece (EA, ED, or BB)
    score_type can either be 'nm' or 'score'
    above_score sets bar for score to exceed for the average of the piece
        e.g. if the average 'nm' for 1bb < above_score, then it is banned from competing again
    """
    df = score_structures(df)
    allowed_dict = gen_allowed_dict(df)
    pieces = {"ea": [], "bb": [], "ed": []}
    total_allowed_dict(allowed_dict)
    pos = -1
    for key, allowed in allowed_dict.items():
        score_lst = []
        for index, row in df.iterrows():
            if (row["exc"] == 1 and allowed and key in row["name"]
                    and row["method_basis_set"] == col_name):
                name_split = row["name"].split("_")
                for n, i in enumerate(name_split):
                    if i == key:
                        pos = n

                nm = row["nm"]
                f = row["osci"]
                LUMO = row["LUMO"]
                score = row["score"]
                if score_type == "score":
                    score_lst.append(score)
                elif score_type == "nm":
                    score_lst.append(nm)
        if pos == 0:
            pos = "ea"
        elif pos == 1:
            pos = "bb"
        elif pos == 2:
            pos = "ed"
        score_avg = sum(score_lst) / len(score_lst)
        pieces[pos].append([key, score_avg])
    for key, value in pieces.items():
        if key in structures:
            if key in structures:
                grouping = sorted(value, key=lambda x: x[1], reverse=True)
                length = len(grouping)
                for n, i in enumerate(grouping):
                    # print(i)
                    if i[1] < above_score:
                        allowed_dict[i[0]] = False
    total_allowed_dict(allowed_dict)
    allowed, banned = acquire_allowed(allowed_dict)
    for i in banned:
        banned_lst.append(i)
    # print(allowed, banned_lst, sep='\n')
    return allowed, banned_lst


def df_molecules_to_df_method_basisset(df_molecules, method_basis_set=[]):

    df = {
        "Name": [],
    }
    for i in method_basis_set:
        df[i] = []
    df = pd.DataFrame(df)
    # print(df)
    for i1, r1 in df_molecules.iterrows():
        # print(r1['name'])
        # print(df.Name)
        # print(r1['name'] in df.Name)
        """
        method_basis_set_lst = ['-' for i in method_basis_set]
        method_basis_set_lst.insert(0, r1['name'])
        df.loc[len(df)] = method_basis_set_lst
        Names = pd.Series(df['Name'])
        print(df)
        print(r1['name'])
        print(df['Name'])
        print()

        break
        """
        Names = [str(i) for i in df["Name"].values]
        if str(r1["name"]) not in Names:
            method_basis_set_lst = [i for i in method_basis_set]

            for n, j in enumerate(method_basis_set_lst):
                # print(j, r1['method_basis_set'])
                if str(j) == str(r1["method_basis_set"]):
                    method_basis_set_lst[n] = r1["nm"]

            method_basis_set_lst.insert(0, r1["name"])
            # if r1['name'] == "1ed_16b_1ea":
            #    print(method_basis_set_lst)
            df.loc[len(df)] = method_basis_set_lst
        else:
            # df.ix[df['id'] == 12, ['uid','gid']] = ['IN','IN-1']
            for j in method_basis_set:
                if str(j) == r1["method_basis_set"]:
                    if r1["exc"] == 1:
                        df.loc[df["Name"] == r1["name"], [j]] = [r1["nm"]]
    # nm = df.sort_values([method_basis_set[0]], ascending=(False))

    return df


def conv_energy(val, rounding=3):
    h = 6.626e-34
    c = 2.998e17
    J_over_eV = 1.602e-19
    return round(h * c / (float(val) * J_over_eV), rounding)


def df_molecules_to_df_method_basisset_exc(df_molecules,
                                           method_basis_set=[],
                                           exp=False,
                                           band_gap=False):

    df = {
        "Name": [],
    }
    for i in method_basis_set:
        df[i] = []
        df["HOMO %s" % i] = []
        df["LUMO %s" % i] = []
        if band_gap:
            df["Band Gap %s" % i] = []

    if exp:
        df["Exp"] = []
    df = pd.DataFrame(df)
    # print(df)
    for i1, r1 in df_molecules.iterrows():
        # print(r1['name'])
        # print(df.Name)
        # print(r1['name'] in df.Name)
        """
        method_basis_set_lst = ['-' for i in method_basis_set]
        method_basis_set_lst.insert(0, r1['name'])
        df.loc[len(df)] = method_basis_set_lst
        Names = pd.Series(df['Name'])
        print(df)
        print(r1['name'])
        print(df['Name'])
        print()

        break
        """
        Names = [str(i) for i in df["Name"].values]
        if str(r1["name"]) not in Names:
            # method_basis_set_lst = [i for i in method_basis_set]
            method_basis_set_lst = []
            for i in method_basis_set:
                method_basis_set_lst.append(i)
                method_basis_set_lst.append("HOMO %s" % i)
                method_basis_set_lst.append("LUMO %s" % i)
                if band_gap:
                    method_basis_set_lst.append("Band Gap %s" % i)

            for n, j in enumerate(method_basis_set_lst):
                # print(j, r1['method_basis_set'])
                if str(j) == str(r1["method_basis_set"]):
                    method_basis_set_lst[n] = conv_energy(r1["nm"])
                if str(r1["method_basis_set"]) in j and "HOMO" in j:
                    method_basis_set_lst[n] = round(r1["HOMO"], 3)
                if str(r1["method_basis_set"]) in j and "LUMO" in j:
                    method_basis_set_lst[n] = round(r1["LUMO"], 3)
                if band_gap:
                    if str(r1["method_basis_set"]) in j and "Band Gap" in j:
                        method_basis_set_lst[n] = round(
                            r1["HOMO"] - r1["LUMO"], 3)

            method_basis_set_lst.insert(0, r1["name"])
            if exp:
                method_basis_set_lst.append(r1["exp"])
            # if r1['name'] == "1ed_16b_1ea":
            #    print(method_basis_set_lst)
            df.loc[len(df)] = method_basis_set_lst
        else:
            # df.ix[df['id'] == 12, ['uid','gid']] = ['IN','IN-1']
            for j in method_basis_set:
                if str(j) == r1["method_basis_set"]:
                    if r1["exc"] == 1:
                        if exp:
                            df.loc[df["Name"] == r1["name"], [j, "Exp"]] = [
                                conv_energy(r1["nm"]),
                                conv_energy(r1["exp"]),
                            ]
                        else:
                            df.loc[df["Name"] == r1["name"],
                                   [j]] = [conv_energy(r1["nm"])]
                        df.loc[df["Name"] == r1["name"],
                               ["HOMO %s" % j]] = round(r1["HOMO"], 3)
                        df.loc[df["Name"] == r1["name"],
                               ["LUMO %s" % j]] = round(r1["LUMO"], 3)
                        if band_gap:
                            df.loc[df["Name"] == r1["name"],
                                   ["Band Gap %s" % j]] = round(
                                       r1["HOMO"] - r1["LUMO"], 3)

    # nm = df.sort_values([method_basis_set[0]], ascending=(False))
    for i in method_basis_set:
        df = df[df[i] != i]
    # print(df)
    # print(method_basis_set)
    # print(df)
    return df


def df_molecules_BM_to_df_method_basisset(df_molecules, method_basis_set=[]):
    df = {
        "Name": [],
    }
    for i in method_basis_set:
        df[i] = []
    df["Exp"] = []
    df = pd.DataFrame(df)
    # print(df)
    for i1, r1 in df_molecules.iterrows():
        # print(r1['name'])
        # print(df.Name)
        # print(r1['name'] in df.Name)
        """
        method_basis_set_lst = ['-' for i in method_basis_set]
        method_basis_set_lst.insert(0, r1['name'])
        df.loc[len(df)] = method_basis_set_lst
        Names = pd.Series(df['Name'])
        print(df)
        print(r1['name'])
        print(df['Name'])
        print()

        break
        """
        Names = [str(i) for i in df["Name"].values]
        if str(r1["name"]) not in Names:
            method_basis_set_lst = [i for i in method_basis_set]

            for n, j in enumerate(method_basis_set_lst):
                # print(j, r1['method_basis_set'])
                if str(j) == str(r1["method_basis_set"]):
                    method_basis_set_lst[n] = r1["nm"]

            method_basis_set_lst.insert(0, r1["name"])
            method_basis_set_lst.append(r1["exp"])
            # if r1['name'] == "1ed_16b_1ea":
            #    print(method_basis_set_lst)

            df.loc[len(df)] = method_basis_set_lst

        else:
            # df.ix[df['id'] == 12, ['uid','gid']] = ['IN','IN-1']
            for j in method_basis_set:
                if str(j) == r1["method_basis_set"]:
                    if r1["exc"] == 1:
                        # df.loc[df['Name'] == r1['name'], [j]] = [r1['nm']]
                        df.loc[df["Name"] == r1["name"], [j, "Exp"]] = [
                            r1["nm"],
                            r1["exp"],
                        ]
    # nm = df.sort_values([method_basis_set[0]], ascending=(False))

    return df


def convert_df_nm_to_eV(df, columns_convert=["Exp"]):
    h = 6.626e-34
    c = 3e17
    Joules_to_eV = 1.602e-19

    for i in columns_convert:
        df[i] = df[i].apply(lambda x: h * c / (x * Joules_to_eV))

    return df


def convert_df_eV_to_nm(df, columns_convert=["Exp"]):
    h = 6.626e-34
    c = 3e17
    Joules_to_eV = 1.602e-19

    for i in columns_convert:
        df[i] = df[i].apply(lambda x: h * c / (x * Joules_to_eV))
    return df


def plot_methods(
    df,
    weighted_avg=["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
    headers_colors=[
        ["CAM-B3LYP/6-311G(d,p)", "blue"],
        ["BHandHLYP/6-311G(d,p)", "red"],
        ["PBE0/6-311G(d,p)", "orange"],
        ["LSF", "green"],
    ],
    outname="dye_plot_weighted.png",
    exp=False,
    weights=[0.6594543456, 0.3405456544],
    units="eV",
    sort_by="Weighted Avg.",
    transparent=False,
    LSF=False,
):
    # 72 hours for calculation for each Dye vs. $10k and 3mnths
    """
    df must be df_method_basisset
    """
    df = df.drop(["Name"], axis=1)
    df = df.apply(lambda x: pd.to_numeric(x, errors="coerce")).dropna()

    if LSF:
        co, residuals, lsf = least_squares(df, weighted_avg)
        print("Coefficients = ", co, "\nresidual = ", residuals)
        # df['Weighted Avg.'] = df['CAM-B3LYP/6-311G(d,p)']*co[0] + df['PBE1PBE/6-311G(d,p)']*co[1]
        df["LSF"] = lsf
        print("lsf:", df["LSF"])
        # df['LSF'] = df['CAM-B3LYP/6-311G(d,p)']*co[0] + df['PBE1PBE/6-311G(d,p)']*co[1]
        # df = df.drop('Weighted Avg.', 1)
        if exp:
            # df = df.sort_values(['Exp'], ascending=False)
            df = df.sort_values(["Exp"], ascending=False)
            dif = (df["LSF"] - df["Exp"]).abs().mean()
            a, b = above_below(df[weighted_avg[0]], df["Exp"])
            print(weighted_avg[0], a / (a + b), b / (a + b))

            a, b = above_below(df[weighted_avg[1]], df["Exp"])
            print(weighted_avg[1], a / (a + b), b / (a + b))

            print("average difference", dif)
            headers_colors.insert(3, ["Experiment", "black"])

        else:
            df = df.sort_values([sort_by], ascending=False)
    else:
        df["Weighted Avg."] = (df["CAM-B3LYP/6-311G(d,p)"] * weights[0] +
                               df["PBE1PBE/6-311G(d,p)"] * weights[1])
        if exp:
            # df = df.sort_values(['Exp'], ascending=False)
            df = df.sort_values(["Weighted Avg."], ascending=False)
            dif = (df["Weighted Avg."] - df["Exp"]).abs().mean()
            print("average difference", dif)
            headers_colors.insert(3, ["Experiment", "black"])
            df = df.sort_values(sort_by, ascending=False)

        else:
            df = df.sort_values([sort_by], ascending=False)

    fig = plt.figure(dpi=400)
    if LSF:
        dye_cnt = range(len(df["LSF"]))
    else:
        dye_cnt = range(len(df["Weighted Avg."]))
    print(df)

    for ind, col in enumerate(df[::-1]):
        try:
            plt.plot(
                dye_cnt,
                list(df[col]),
                label=headers_colors[ind][0],
                color=headers_colors[ind][1],
                linewidth=0.2,
            )
        except:
            print(
                "Error in color and label.\nNo label or specific color assigned\n\n"
            )
            # plt.plot(dye_cnt, list(df[col]), linewidth=2)
    # plt.title('Methods on Theoretical Dyes')
    if exp:
        plt.xlabel("Benchmark Dyes")
    else:
        plt.xlabel("Theoretical Dyes")
    plt.ylabel("Excitation Energy (%s)" % units)
    plt.grid(color="grey",
             which="major",
             axis="y",
             linestyle="-",
             linewidth=0.2)
    plt.legend()
    # print(outname)
    # print(os.getcwd())
    plt.savefig(outname, transparent=transparent)
    print("graph name:", outname)


def plot_solvents(
    df,
    outname,
    units="eV",
    exp=True,
    transparent=True,
    solvents=["Dichloromethane", "N,N-Dimethylformamide", "Tetrahydrofuran"],
    functionals=[
        "CAM-B3LYP",
        "PBE1PBE",
        "bhandhlyp",
    ],
):

    df = df.drop(["Name"], axis=1)
    df = df.apply(lambda x: pd.to_numeric(x, errors="coerce")).dropna()
    headers_colors = []
    clean_solv = []
    for solv in solvents:
        clean_solv.append(clean_solvent(solv).lower())
    if exp:
        # df = df.sort_values(['Exp'], ascending=False)
        # df = df.sort_values(['Weighted Avg.'], ascending=False)
        # dif = (df['Weighted Avg.'] - df['Exp']).abs().mean()
        # print("average difference", dif)
        headers_colors.append(["Exp.", "black"])
        # df = df.sort_values(sort_by, ascending=False)

    # else:
    # df = df.sort_values([sort_by], ascending=False)

    for k in functionals:
        fig = plt.figure(dpi=400)
        # dye_cnt = range(len(df['Weighted Avg.']))
        dye_cnt = range(df.shape[0])

        for ind, col in enumerate(df[::-1]):
            if k in col:
                label = ""
                for ind, solv in enumerate(clean_solv):
                    if solv in col:
                        label = solvents[ind]
                if label == "":
                    label = "Vacuum"
                # try:
                plt.plot(
                    dye_cnt,
                    list(df[col]),
                    label=label,
                    # color=headers_colors[ind][1],
                    linewidth=1,
                )

                # except:
                #     print("Error in color and label.\nNo label or specific color assigned\n\n")
                #     plt.plot(
                #         dye_cnt, list(df[col]),
                #         linewidth=1
                #     )
        # plt.title('Methods on Theoretical Dyes')
        plt.xlabel("Benchmark Dyes")
        plt.ylabel("Excitation Energy (%s)" % units)
        plt.grid(
            color="grey",
            which="major",
            axis="y",
            linestyle="-",
            linewidth=0.2,
        )
        plt.legend()
        # print(col)
        # print(os.getcwd(), k)
        plt.savefig("%s.png" % (k), transparent=transparent)


def plot_methods_og(
    df,
    weighted_avg=["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
    headers_colors=[
        ["CAM-B3LYP/6-311G(d,p)", "blue"],
        ["BHandHLYP/6-311G(d,p)", "purple"],
        ["PBE0/6-311G(d,p)", "red"],
        ["Weighted Average", "green"],
    ],
):
    # 72 hours for calculation for each Dye vs. $10k and 3mnths
    """
    df must be df_method_basisset
    """
    df = df.drop(["Name"], axis=1)
    df = df.apply(lambda x: pd.to_numeric(x, errors="coerce")).dropna()

    df["Weighted Avg."] = df[["CAM-B3LYP/6-311G(d,p)",
                              "PBE1PBE/6-311G(d,p)"]].mean(axis=1)
    df = df.sort_values(["Weighted Avg."], ascending=False)
    fig = plt.figure(dpi=400)
    dye_cnt = range(len(df["Weighted Avg."]))
    for ind, col in enumerate(df[::-1]):
        print(ind)
        print(headers_colors[ind][0])

        plt.plot(
            dye_cnt,
            list(df[col]),
            label=headers_colors[ind][0],
            color=headers_colors[ind][1],
            linewidth=1,
        )
    plt.title("Methods on Theoretical Dyes")
    plt.xlabel(
        "Theoretical Dyes Sorted by the Weighted Average Excitation Energy")
    plt.ylabel("Excitation Energy (nm)")
    plt.grid(color="grey",
             which="major",
             axis="y",
             linestyle="-",
             linewidth=0.2)
    plt.legend()
    plt.savefig("dyes_theor_methods.png")


def plot_methods_BM(df, ):
    """
    exp_data={
        "dyes": ['AP25', 'D1', 'D3', 'XY1', 'ZL003'],
        "CAM": [-127.31, -39.04, -22.85, -34.71, -20.29],
        "PBE": [-13.80, 141.99, 238.93, 125.85, 91.99],
        "Weighted": [-89.85, 20.70, 63.54, 18.28, 16.76],
    }
    """
    fig = plt.figure(dpi=400)
    plt.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    plt.plot(
        exp_data["dyes"],
        exp_data["CAM"],
        label="CAM-B3LYP/6-311G(d,p)",
        color="blue",
    )
    plt.plot(
        exp_data["dyes"],
        exp_data["PBE"],
        label="PBE0/6-311G(d,p)",
        color="red",
    )
    plt.plot(
        exp_data["dyes"],
        exp_data["Weighted"],
        label="Weighted Average",
        color="green",
    )
    zeros = [0 for i in range(len(exp_data["dyes"]))]
    plt.plot(
        exp_data["dyes"],
        zeros,
        ".",
        label="Experiment",
        color="black",
    )
    plt.grid(color="grey",
             which="major",
             axis="y",
             linestyle="-",
             linewidth=0.2)
    plt.title("Methods Compared with Experimental Dyes\n")
    plt.ylim([-150, 300])
    plt.xlabel("Experimental Dyes")
    plt.ylabel("Experimental Difference (nm)")
    plt.legend()
    plt.savefig("dyes_exp_methods.png")


def plot_methods_exp(
    exp_data={
        "dyes": ["AP25", "D1", "D3", "XY1", "ZL003"],
        "CAM": [-127.31, -39.04, -22.85, -34.71, -20.29],
        "PBE": [-13.80, 141.99, 238.93, 125.85, 91.99],
        "Weighted": [-89.85, 20.70, 63.54, 18.28, 16.76],
    }):
    fig = plt.figure(dpi=400)
    plt.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    plt.plot(
        exp_data["dyes"],
        exp_data["CAM"],
        label="CAM-B3LYP/6-311G(d,p)",
        color="blue",
    )
    plt.plot(
        exp_data["dyes"],
        exp_data["PBE"],
        label="PBE0/6-311G(d,p)",
        color="red",
    )
    plt.plot(
        exp_data["dyes"],
        exp_data["Weighted"],
        label="Weighted Average",
        color="green",
    )
    zeros = [0 for i in range(len(exp_data["dyes"]))]
    plt.plot(
        exp_data["dyes"],
        zeros,
        ".",
        label="Experiment",
        color="black",
    )
    plt.grid(color="grey",
             which="major",
             axis="y",
             linestyle="-",
             linewidth=0.2)
    plt.title("Methods Compared with Experimental Dyes\n")
    plt.ylim([-150, 300])
    plt.xlabel("Experimental Dyes")
    plt.ylabel("Experimental Difference (nm)")
    plt.legend()
    plt.savefig("dyes_exp_methods.png")


def df_conv_energy(df, min_num=200):
    """
    Converts from nm to eV or eV to nm
    """
    h = 6.626e-34
    c = 2.998e17
    J_over_eV = 1.602e-19
    for col in df:
        if col != "Name":
            df = df[pd.to_numeric(df[col], errors="coerce").notnull()]
            df[col] = df[col].mask(df[col] > min_num,
                                   h * c / (df[col] * J_over_eV))
    return df


def df_diff_std(df,
                col_names=["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"]):
    """
    Calculates the difference between two method energies and calculates the std of the differences
    """
    dif_col = "%s - %s" % (col_names[0], col_names[1])
    df[dif_col] = df[col_names[0]] - df[col_names[1]]
    dif_std_col = "std(%s)" % dif_col
    std_val = df[dif_col].std(axis=0)
    mean_val = df[dif_col].mean(axis=0)
    # z_score = x - mu / sig
    df[dif_std_col] = (df[dif_col] - mean_val) / std_val
    df = df.sort_values([dif_std_col], ascending=True)
    datatypes = df.dtypes()
    print(datatypes)
    # df.hist(column=dif_col)
    # plt.show()
    """
    val = pd.qcut(df[dif_col], q=4)
    print(val)
    # print(df[dif_col].describe())

    bin_labels_5 = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
    results, bin_edges = pd.qcut(df[dif_col],
                            q=[0, .2, .4, .6, .8, 1],
                            labels=bin_labels_5,
                            retbins=True)

    results_table = pd.DataFrame(zip(bin_edges, bin_labels_5),
                                columns=['Threshold', 'Tier'])

    print(results_table)
    """
    # df_hist = df.filter(['Name', dif_std_col], axis=1)
    # print(df_hist)


def mean_abs_error_weighted(
    df,
    methods=["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
    weights=[0.6594543456, 0.3405456544],
):

    df["Weighted Avg."] = (df[methods[0]] * weights[0] +
                           df[methods[1]] * weights[1])
    return (df["Weighted Avg."] - df["Exp"]).abs().mean()


def mean_abs_error(df, method="Dif. CAM-B3LYP/6-311G(d,p)"):
    return df[method].abs().mean()


def weighted_avg_df(
    df,
    methods=["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
    weights=[0.6594543456, 0.3405456544],
):

    df["Weighted Avg."] = (df[methods[0]] * weights[0] +
                           df[methods[1]] * weights[1])
    return df


def benchmarkFlow(path_benchmark="Benchmark/benchmarks.json"):
    df_molecules = json_pandas_molecule_BM(path_benchmark)
    methods_basissets = [
        "CAM-B3LYP/6-311G(d,p)",
        "bhandhlyp/6-311G(d,p)",
        "PBE1PBE/6-311G(d,p)",
    ]
    df = df_molecules_BM_to_df_method_basisset(df_molecules, methods_basissets)
    convert_lst = methods_basissets.copy()
    convert_lst.append("Exp")
    print(df)
    df = convert_df_nm_to_eV(df, convert_lst)
    unlucky = {
        "AP25": [2.329644, 2.295717, 1.920780, 1.9342315],
        # "AP25": [2.329644,2.295717,1.920780,1.880036],
        "D1": [2.337250, 2.285609, 1.742975, 2.176884],
        "D3": [2.301722, 2.209749, 1.549403, 2.207872],
        "XY1": [2.398999, 2.314932, 1.839675, 2.247870],
        "NL6": [2.250481, 2.239272, 1.383166, 2.050367],
        "ZL003": [2.488369, 2.437129, 2.031108, 2.390798],
        "JW1": [2.320036, 2.302322, 1.910812, 2.103091],
    }
    for key, val in unlucky.items():
        row = {
            "Name": key,
            methods_basissets[0]: val[0],
            methods_basissets[1]: val[1],
            methods_basissets[2]: val[2],
            "Exp": val[3],
        }
        df = df.append(row, ignore_index=True)
    df = convert_df_nm_to_eV(df, convert_lst)
    plot_methods(df, exp=True)
    df = convert_df_nm_to_eV(df, convert_lst)
    df_dif = df_differences_exp(df, methods_basissets)
    df_dif = weighted_avg_df(df, convert_lst)
    print(df_dif)
    df_dif.to_csv("benchmarks.csv", index=False)
    print(mean_abs_error_weighted(df))
    print(mean_abs_error(df_dif, "Dif. PBE1PBE/6-311G(d,p)"))


def benchamrkPredictPCE(
    path_benchmark="Benchmark/benchmarks.json",
    path_ipce="src/ipce.csv",
    extra_values={
        # "AP25": [2.329644,2.295717,1.920780,1.880036],
        "AP25": [2.329644, 2.295717, 1.920780, 1.9342315],
        "D1": [2.337250, 2.285609, 1.742975, 2.176884],
        "D3": [2.301722, 2.209749, 1.549403, 2.207872],
        "XY1": [2.398999, 2.314932, 1.839675, 2.247870],
        "NL6": [2.250481, 2.239272, 1.383166, 2.050367],
        "ZL003": [2.488369, 2.437129, 2.031108, 2.390798],
        "JW1": [2.320036, 2.302322, 1.910812, 2.103091],
    },
):

    df_molecules = json_pandas_molecule_BM(path_benchmark)
    methods_basissets = [
        "CAM-B3LYP/6-311G(d,p)",
        "bhandhlyp/6-311G(d,p)",
        "PBE1PBE/6-311G(d,p)",
    ]
    df = df_molecules_BM_to_df_method_basisset(df_molecules, methods_basissets)
    convert_lst = methods_basissets.copy()
    convert_lst.append("Exp")

    df = convert_df_nm_to_eV(df, convert_lst)
    unlucky = {
        # "AP25": [2.329644,2.295717,1.920780,1.880036],
        "AP25": [2.329644, 2.295717, 1.920780, 1.9342315],
        "D1": [2.337250, 2.285609, 1.742975, 2.176884],
        "D3": [2.301722, 2.209749, 1.549403, 2.207872],
        "XY1": [2.398999, 2.314932, 1.839675, 2.247870],
        "NL6": [2.250481, 2.239272, 1.383166, 2.050367],
        "ZL003": [2.488369, 2.437129, 2.031108, 2.390798],
        "JW1": [2.320036, 2.302322, 1.910812, 2.103091],
    }
    for key, val in unlucky.items():
        row = {
            "Name": key,
            methods_basissets[0]: val[0],
            methods_basissets[1]: val[1],
            methods_basissets[2]: val[2],
            "Exp": val[3],
        }
        df = df.append(row, ignore_index=True)
    # df = convert_df_nm_to_eV(df, convert_lst)
    # df_dif = df_differences_exp(df, methods_basissets)
    df = weighted_avg_df(df, convert_lst)

    print(df)

    ipce = pd.read_csv(path_ipce)
    ipce["IPCE"] = ipce["IPCE"].astype(float)
    ipce["Abs. Max"] = ipce["Abs. Max"].astype(float)
    ipce = convert_df_nm_to_eV(ipce, ["IPCE", "Abs. Max"])
    ipce = ipce.sort_values(["Name"], axis=0).reset_index(drop=True)
    del ipce["Name"]
    df = df.sort_values(["Name"], axis=0).reset_index(drop=True)

    df2 = pd.concat([df, ipce], axis=1).reindex(ipce.index)

    # print(ipce['Name'])
    # print(df['Name'])
    avg_ipce_from_abs_max = (df2["Abs. Max"] - df2["IPCE"]).mean()
    print("avg:", avg_ipce_from_abs_max)
    df2["Comp. IPCE"] = df2["Weighted Avg."] - avg_ipce_from_abs_max
    h = 6.626e-34
    c = 3e17
    J_to_eV = 1.602e-19
    del df2["CAM-B3LYP/6-311G(d,p)"]
    del df2["bhandhlyp/6-311G(d,p)"]
    del df2["PBE1PBE/6-311G(d,p)"]
    del df2["Exp"]

    FF_h = 0.75
    FF_l = 0.60
    I_o = 1
    energy_cut_off = 400
    # energy_cut_off = h*c/(energy_cut_off*J_to_eV)

    df2["Comp. Jsc"] = (((h * c /
                          (df2["Comp. IPCE"] * J_to_eV)) - energy_cut_off) /
                        100 * 7.5)
    df2["Comp. Voc_h"] = df2["Weighted Avg."] - 0.4
    df2["Comp. Voc_l"] = df2["Weighted Avg."] - 0.6

    df2["Comp. PCE Voc_l FF_l"] = (df2["Comp. Jsc"] * df2["Comp. Voc_l"] *
                                   FF_l / I_o)
    df2["Comp. PCE Voc_l FF_h"] = (df2["Comp. Jsc"] * df2["Comp. Voc_l"] *
                                   FF_h / I_o)
    df2["Comp. PCE Voc_h FF_l"] = (df2["Comp. Jsc"] * df2["Comp. Voc_h"] *
                                   FF_l / I_o)
    df2["Comp. PCE Voc_h FF_h"] = (df2["Comp. Jsc"] * df2["Comp. Voc_h"] *
                                   FF_h / I_o)

    df2["Exp. PCE Voc_l FF_l"] = (((
        (h * c) / (df2["IPCE"] * J_to_eV) - energy_cut_off) / 100 * 7.5) *
                                  (df2["Abs. Max"] - 0.6) * FF_l)
    df2["Exp. PCE Voc_l FF_h"] = (((
        (h * c) / (df2["IPCE"] * J_to_eV) - energy_cut_off) / 100 * 7.5) *
                                  (df2["Abs. Max"] - 0.6) * FF_h)
    df2["Exp. PCE Voc_h FF_l"] = (((
        (h * c) / (df2["IPCE"] * J_to_eV) - energy_cut_off) / 100 * 7.5) *
                                  (df2["Abs. Max"] - 0.4) * FF_l)
    df2["Exp. PCE Voc_h FF_h"] = (((
        (h * c) / (df2["IPCE"] * J_to_eV) - energy_cut_off) / 100 * 7.5) *
                                  (df2["Abs. Max"] - 0.4) * FF_h)
    """
    df2['Comp. Jsc'] = h*c/((df2['Comp. IPCE'] + energy_cut_off)*J_to_eV) /100*7.5
    df2['Comp. Voc_h'] = (df2['Weighted Avg.'] - 0.4)
    df2['Comp. Voc_l'] = (df2['Weighted Avg.'] - 0.6)

    df2['Comp. PCE Voc_l FF_l'] = df2['Comp. Jsc'] * df2['Comp. Voc_l'] * FF_l / I_o
    df2['Comp. PCE Voc_l FF_h'] = df2['Comp. Jsc'] * df2['Comp. Voc_l'] * FF_h / I_o
    df2['Comp. PCE Voc_h FF_l'] = df2['Comp. Jsc'] * df2['Comp. Voc_h'] * FF_l / I_o
    df2['Comp. PCE Voc_h FF_h'] = df2['Comp. Jsc'] * df2['Comp. Voc_h'] * FF_h / I_o

    df2['Exp. PCE Voc_l FF_l'] = ((df2['IPCE'] + energy_cut_off) / 100*7.5) * (df2['Abs. Max'] - 0.6) * FF_l
    df2['Exp. PCE Voc_l FF_h'] = ((df2['IPCE'] + energy_cut_off) / 100*7.5) * (df2['Abs. Max'] - 0.6) * FF_h
    df2['Exp. PCE Voc_h FF_l'] = ((df2['IPCE'] + energy_cut_off) / 100*7.5) * (df2['Abs. Max'] - 0.4) * FF_l
    df2['Exp. PCE Voc_h FF_h'] = ((df2['IPCE'] + energy_cut_off) / 100*7.5) * (df2['Abs. Max'] - 0.4) * FF_h
    """

    df2.to_csv("pce_predict.csv")

    print(df2)


def df_differences_exp(df, methods):
    for i in methods:
        df["Dif. %s" % i] = df[i] - df["Exp"]
        print("Avg. Dif. %s" % i, df["Dif. %s" % i].mean(axis=0))
    return df


def theoretical_dyes_basis_set_out(
    path_results_json,
    methods_basissets=[

        "CAM-B3LYP/6-311G(d,p)",
        "bhandhlyp/6-311G(d,p)",
        "PBE1PBE/6-311G(d,p)",
    ],
    units="eV",
    output_csv="",
    output_graph="",
    output_latex="",
    plot_js={
        "weighted_avg": ["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
        "headers_colors": [
            ["CAM-B3LYP/6-311G(d,p)", "blue"],
            ["BHandHLYP/6-311G(d,p)", "red"],
            ["PBE0/6-311G(d,p)", "orange"],
            ["Weighted Average", "green"],
        ],
        "weights": [0.71, 0.29],
    },
    results_exc=False,
    homo_lumo=False,
    LSF_csv=False,
):

    df_molecules = json_pandas_molecule(path_results_json, results_exc)

    df = df_molecules_to_df_method_basisset(df_molecules, methods_basissets)
    #print('Print Statement')
    #print(df_molecules['name','generalSMILES'])
    #print(df_molecules['generalSMILES'])
    #df_molecules.to_csv("all.csv",index=False)
    #print('Print Statement')
    if units.lower() == "ev":
        df = df_conv_energy(df)

    if output_csv != "":
        if homo_lumo:
            df2 = df_molecules_to_df_method_basisset_exc(
                df_molecules, methods_basissets)
        else:
            df2 = df
        if LSF_csv:
            df2["LSF"] = (
                df2[plot_js["weighted_avg"][0]] * plot_js["weights"][0] +
                df2[plot_js["weighted_avg"][1]] * plot_js["weights"][1])
            df2 = df2.sort_values("LSF", ascending=True)
            above_ap25 = df2[df2["LSF"] > 1.8785491]
            print(len(above_ap25["LSF"]))
        else:
            df2 = df2.sort_values(methods_basissets[0], ascending=True)
        df2.to_csv("%s.csv" % output_csv, index=False)

    if output_graph != "":
        print("working on graph")
        plot_methods(
            df,
            weighted_avg=plot_js["weighted_avg"],
            headers_colors=plot_js["headers_colors"],
            weights=plot_js["weights"],
            exp=False,
            outname=output_graph,
            transparent=True,
            LSF=False,
        )
    if output_latex != "":
        if homo_lumo:
            df2 = df_molecules_to_df_method_basisset_exc(
                df_molecules, methods_basissets)
        df2 = df2.sort_values(methods_basissets[0], ascending=True)
        df2.to_latex("%s.tex" % output_csv, index=False)

    # print(df)


def benchmarks_dyes_basis_set_out(
    path_results_json,
    methods_basissets=[
        "CAM-B3LYP/6-311G(d,p)",
        "bhandhlyp/6-311G(d,p)",
        "PBE1PBE/6-311G(d,p)",
    ],
    units="nm",
    output_csv="",
    output_graph="",
    output_latex="",
    plot_js={
        "weighted_avg": [
            "CAM-B3LYP/6-311G(d,p)",
            "PBE1PBE/6-311G(d,p)",
        ],
        "headers_colors": [
            ["CAM-B3LYP/6-311G(d,p)", "blue"],
            ["BHandHLYP/6-311G(d,p)", "red"],
            ["PBE0/6-311G(d,p)", "orange"],
            ["LSF", "green"],  # ['Weighted Average', 'green']
        ],
        "weights": [0.71, 0.29],
    },
    exc_json=True,
    homo_lumo=False,
    band_gap=True,
    testing=False,
    LSF=True,
    LSF_csv=False,
):

    df_molecules = json_pandas_molecule_BM(path_results_json,
                                           exc_json=exc_json)
    # print(df_molecules)
    df = df_molecules_BM_to_df_method_basisset(df_molecules, methods_basissets)
    convert_lst = methods_basissets.copy()
    convert_lst.append("Exp")
    df = df.dropna()
    df.to_csv("ll.csv")
    df = convert_df_nm_to_eV(df, convert_lst)

    """


    unlucky = {
        # "AP25": [2.329644,2.295717,1.920780,1.880036],
        "AP25": [2.329644, 2.295717, 1.920780, 1.9342315],
        "D1": [2.337250, 2.285609, 1.742975, 2.176884],
        "D3": [2.301722, 2.209749, 1.549403, 2.207872],
        "XY1": [2.398999, 2.314932, 1.839675, 2.247870],
        "NL6": [2.250481, 2.239272, 1.383166, 2.050367],
        "ZL003": [2.488369, 2.437129, 2.031108, 2.390798],
        "JW1": [2.320036, 2.302322, 1.910812, 2.103091],
    }
    for key, val in unlucky.items():
        row = {
            "Name": key,
            methods_basissets[0]: val[0],
            methods_basissets[1]: val[1],
            methods_basissets[2]: val[2],
            "Exp": val[3],
        }

        df = df.append(row, ignore_index=True)


    """

    if units.lower() == "nm":
        df = convert_df_nm_to_eV(df, convert_lst)
    elif units.lower() == "ev":
        pass
    else:
        print("unit not acceptable")
    df = convert_df_nm_to_eV(df, convert_lst)

    # df = df_molecules_to_df_method_basisset(df, methods_basissets)
    if units.lower() == "ev":
        df = df_conv_energy(df)
    if output_csv != "":

        if homo_lumo:
            df2 = df_molecules_to_df_method_basisset_exc(df_molecules,
                                                         methods_basissets,
                                                         exp=True,
                                                         band_gap=band_gap)

            print(df2)
            # print(df2)
            # df2 = df2.sort_values(methods_basissets[0], ascending=False)
            df2 = df2.sort_values("Exp", ascending=True)
        else:
            df2 = df.sort_values(methods_basissets[0], ascending=False)
        if LSF_csv:
            df2["LSF"] = (
                df2[plot_js["weighted_avg"][0]] * plot_js["weights"][0]
                + df2[plot_js["weighted_avg"][1]] * plot_js["weights"][1]
            )
            df2 = df2.sort_values("LSF", ascending=True)
            above_ap25 = df2[df2["LSF"] > 1.8785491]
            print(len(above_ap25["LSF"]))
        else:
            df2 = df2.sort_values(methods_basissets[0], ascending=True)

        df2.to_csv("%s.csv" % output_csv, index=False)
    if output_graph != "":
        print("working on graph")
        plot_methods(
            df,
            weighted_avg=plot_js["weighted_avg"],
            headers_colors=plot_js["headers_colors"],
            weights=plot_js["weights"],
            outname=output_graph,
            exp=True,
            sort_by="Exp",
            transparent=True,
            LSF=LSF,
        )
    if output_latex != "":
        if homo_lumo:
            df2 = df_molecules_to_df_method_basisset_exc(df_molecules,
                                                         methods_basissets,
                                                         exp=True,
                                                         band_gap=band_gap)

            # df2 = df2.sort_values(methods_basissets[0], ascending=True)
            df2 = df2.sort_values("Exp", ascending=True)
        else:
            df2 = df.sort_values(methods_basissets[0], ascending=True)
        if LSF_csv:
            df2["LSF"] = (
                df2[plot_js["weighted_avg"][0]] * plot_js["weights"][0]
                + df2[plot_js["weighted_avg"][1]] * plot_js["weights"][1]
            )
            df2 = df2.sort_values("LSF", ascending=True)
            above_ap25 = df2[df2["LSF"] > 1.8785491]
            print(len(above_ap25["LSF"]))
        else:
            df2 = df2.sort_values(methods_basissets[0], ascending=True)
        df2.to_latex("%s.tex" % output_csv, index=False)

    if testing:
        df2 = df.sort_values(methods_basissets[0], ascending=False)
        least_squares(df2)

    # print(df)


def clean_solvent(solvent):
    return solvent.replace("-", "").replace(",", "")


# def mean_abs_error_weighted(df, methods=['CAM-B3LYP/6-311G(d,p)', 'PBE1PBE/6-311G(d,p)'], weights=[0.6594543456, 0.3405456544]):

#     df['Weighted Avg.'] = df[methods[0]]*weights[0] + df[methods[1]]*weights[1]
#     return (df['Weighted Avg.'] - df['Exp']).abs().mean()

# def mean_abs_error(df, method='Dif. CAM-B3LYP/6-311G(d,p)'):
#     return df[method].abs().mean()

# def weighted_avg_df(df, methods=['CAM-B3LYP/6-311G(d,p)', 'PBE1PBE/6-311G(d,p)'], weights=[0.6594543456, 0.3405456544]):


#     df['Weighted Avg.'] = df[methods[0]]*weights[0] + df[methods[1]]*weights[1]
#     return df
def least_squares(
    df,
    methods_basissets_avg=["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
    debug=False,
    verbose=False,
):
    dft1 = df[methods_basissets_avg[0]].to_numpy(dtype="float")
    dft2 = df[methods_basissets_avg[1]].to_numpy(dtype="float")

    exp = df["Exp"].to_numpy(dtype="float")

    dfts = np.vstack((dft1, dft2)).transpose()
    # test_co = np.array([0.71, 0.29])

    # print("dfts", dfts)
    # print(dft1.shape)
    # print(dft2.shape)
    if debug:
        print(dfts, exp)
        print(dfts.shape, exp.shape)
    out = np.linalg.lstsq(dfts, exp)
    first, *_, last = out
    xyzs3 = coefficients_3D_line(dfts, exp, first)

    # TODO: ensure functions exists
    print("\ncoefficients =", first, "\n")
    print("Total    Residuel =", get_residual(out, dfts, exp))
    print("Total    RSE      =", RSE(exp, xyzs3[:, 2]))
    print(
        "Total    RMSE     =",
        mean_squared_error(exp, xyzs3[:, 2], squared=False),
    )

    # A*x - exp == close to zero
    # plug in my values for A to test residuals
    if verbose:
        print("coefficients =", first)
        print("final = ", dft1[0], first[0], exp[0])

    mult = np.matmul(dfts, first)
    sub = np.subtract(mult, exp)
    squared = np.square(sub)
    summed = np.sum(squared)
    if verbose:
        print("residuel =", summed)

    # mult = np.matmul(dfts, test_co)
    # sub = np.subtract(mult, exp)
    # squared = np.square(sub)
    # summed = np.sum(squared)
    # print("old", summed)

    # say used least-squares fit
    lsf = xyzs3[:, 2]
    return first, summed, lsf


def solvent_mean_abs_error(
    df,
    methods_basissets_avg=["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
    solvents=["dichloromethane", "n,n-dimethylformamide", "tetrahydrofuran"],
    LSF=False,
):

    if LSF:
        solvents = [clean_solvent(i) for i in solvents]
        print(least_squares(df, methods_basissets_avg))
        co, residuals = least_squares(df, methods_basissets_avg)
        df["vacuum_MAE"] = (df[methods_basissets_avg[0]] * co[0] +
                            df[methods_basissets_avg[1]] * co[1])
        weighted_avg = (df["vacuum_MAE"] -
                        df["Exp"]).mean()  # should be approximately zero.
        mae = (df["vacuum_MAE"] - df["Exp"]).abs().mean()
        print("VACUUM")
        print("MAE = ", mae, "residual = ", residuals)

        mae = (df["vacuum_MAE"] - df["Exp"]).abs().mean()
        for i in solvents:
            print("solvent = ", i)
            solv_meth = [
                "%s_%s" % (methods_basissets_avg[0], i),
                "%s_%s" % (methods_basissets_avg[1], i),
            ]
            co, residuals = least_squares(df, solv_meth)
            df["%s_MAE" % i] = (df[solv_meth[0]] * co[0] +
                                df[solv_meth[1]] * co[1])
            weighted_avg = (df["%s_MAE" % i] -
                            df["Exp"]).mean()  # should be approximately zero.
            mae = (df["%s_MAE" % i] - df["Exp"]).abs().mean()
            # print("Mean Absolute Error of Weighted:", mae, '\n')
            print("MAE = ", mae, "residual = ", residuals)

    else:
        # LSF for avg1, avg2
        solvents = [clean_solvent(i) for i in solvents]
        avg1 = (df[methods_basissets_avg[0]] - df["Exp"]).mean()
        avg2 = (df[methods_basissets_avg[1]] - df["Exp"]).mean()
        # assume avg1 is positive and avg2 is negative
        # c1*avg1 + c2*avg2 = weighted_avg
        # let c2=1 and solve for constant c when weighted_avg is 0
        # c*avg1 = -avg2
        # c = -avg2/avg1
        c = -avg2 / avg1
        # ratio avg2 to avg1 1:c, convert ratio to percentages
        c1 = c / (c + 1)
        c2 = 1 / (c + 1)
        df["vacuum_MAE"] = (df[methods_basissets_avg[0]] * c1 +
                            df[methods_basissets_avg[1]] * c2)
        weighted_avg = (df["vacuum_MAE"] -
                        df["Exp"]).mean()  # should be approximately zero.
        mae = (df["vacuum_MAE"] - df["Exp"]).abs().mean()
        print("\nContributions: %s %.2f %s %.2f" %
              (methods_basissets_avg[0], c1, methods_basissets_avg[1], c2))
        print("This should be approximately zero:", weighted_avg)
        print("Mean Absolute Error of Weighted:", mae, "\n")

        for i in solvents:

            avg1 = (df["%s_%s" % (methods_basissets_avg[0], i)] -
                    df["Exp"]).mean()
            avg2 = (df["%s_%s" % (methods_basissets_avg[1], i)] -
                    df["Exp"]).mean()
            # assume avg1 is positive and avg2 is negative
            # c1*avg1 + c2*avg2 = weighted_avg
            # let c2=1 and solve for constant c when weighted_avg is 0
            # c*avg1 = -avg2
            # c = -avg2/avg1
            c = -avg2 / avg1
            # ratio avg2 to avg1 1:c, convert ratio to percentages
            c1 = c / (c + 1)
            c2 = 1 / (c + 1)
            df["%s_MAE" %
               i] = (df["%s_%s" % (methods_basissets_avg[0], i)] * c1 +
                     df["%s_%s" % (methods_basissets_avg[1], i)] * c2)
            weighted_avg = (df["%s_MAE" % i] -
                            df["Exp"]).mean()  # should be approximately zero.
            mae = (df["%s_MAE" % i] - df["Exp"]).abs().mean()
            print("Solvent: %s" % i)
            print("Contributions: %s %.2f %s %.2f" %
                  (methods_basissets_avg[0], c1, methods_basissets_avg[1], c2))
            print("This should be approximately zero:", weighted_avg)
            print("Mean Absolute Error of Weighted:", mae, "\n")

    # print(avg1, avg2, c1, c2, mae)

    # df = df.drop(columns=[col for col in df if col not in final_table_columns])


def benchmarks_solvation(
    path_results_json,
    methods_basissets=[
        "CAM-B3LYP/6-311G(d,p)",
        "bhandhlyp/6-311G(d,p)",
        "PBE1PBE/6-311G(d,p)",
    ],
    solvents=["dichloromethane", "n,n-dimethylformamide", "tetrahydrofuran"],
    units="eV",
    output_csv="",
    output_graph="",
    output_latex="",
    plot_js={
        "weighted_avg": ["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
        "headers_colors": [
            ["CAM-B3LYP/6-311G(d,p)", "blue"],
            ["BHandHLYP/6-311G(d,p)", "red"],
            ["PBE0/6-311G(d,p)", "orange"],
            ["Weighted Average", "green"],
        ],
        "weights": [0.6594543456, 0.3405456544],
    },
    weight_solvents=True,
    exc_json=True,
    homo_lumo=True,
    testing=False,
):

    df_molecules = json_pandas_molecule_BM(path_results_json,
                                           exc_json=exc_json)
    method_solvent = methods_basissets.copy()
    for i in methods_basissets:
        for j in solvents:
            name = "%s_%s" % (i, clean_solvent(j))
            method_solvent.append(name)
    # print(method_solvent)
    df = df_molecules_BM_to_df_method_basisset(df_molecules, method_solvent)
    # print(df)
    convert_lst = methods_basissets.copy()
    convert_lst.append("Exp")
    # print(df)
    # print(df)
    df = convert_df_nm_to_eV(df, convert_lst)
    """
    unlucky = {
        # "AP25": [2.329644,2.295717,1.920780,1.880036],
        "AP25": [2.329644, 2.295717, 1.920780, 1.9342315],
        "D1": [2.337250, 2.285609, 1.742975, 2.176884],
        "D3": [2.301722, 2.209749, 1.549403, 2.207872],
        "XY1": [2.398999, 2.314932, 1.839675, 2.247870],
        "NL6": [2.250481, 2.239272, 1.383166, 2.050367],
        "ZL003": [2.488369, 2.437129, 2.031108, 2.390798],
        "JW1": [2.320036, 2.302322, 1.910812, 2.103091],
    }
    for key, val in unlucky.items():
        row = {
            "Name": key,
            methods_basissets[0]: val[0],
            methods_basissets[1]: val[1],
            methods_basissets[2]: val[2],
            "Exp": val[3],
        }
        df = df.append(row, ignore_index=True)
    """
    if units.lower() == "nm":
        df = convert_df_nm_to_eV(df, convert_lst)
    elif units.lower() == "ev":
        pass
    else:
        print("unit not acceptable")

    df = convert_df_nm_to_eV(df, convert_lst)

    # df = df_molecules_to_df_method_basisset(df, methods_basissets)
    if units.lower() == "ev":
        df = df_conv_energy(df)
    # print(df)
    if weight_solvents:
        solvent_mean_abs_error(df, LSF=True)
    if output_csv != "":
        df2 = df.sort_values(methods_basissets[0], ascending=False)
        df2.to_csv("%s.csv" % output_csv, index=False)
    if output_graph != "":

        # plot_methods(df, weighted_avg=plot_js['weighted_avg'], headers_colors=plot_js['headers_colors'], weights=plot_js['weights'], outname=output_graph, exp=True, sort_by='Exp', transparent=True)
        plot_solvents(df, outname="%s.png" % (output_graph))
    if output_latex != "":
        df2 = df.sort_values(methods_basissets[0], ascending=False)
        df2.to_latex("%s.tex" % output_csv, index=False)


def df_differences_exp(df, methods):
    for i in methods:
        # print((i,'HELPPPPPPPPPPPPP'))
        df["Dif. %s" % i] = df[i] - df["Exp"]
        print("Avg. Dif. %s" % i, df["Dif. %s" % i].mean(axis=0))
    return df


### mean absolute error


def above_below(d1, d2):
    above, below = 0, 0
    for i in range(len(d1)):
        if d1[i] > d2[i]:
            above += 1
        else:
            below += 1
    return above, below


def main():

    location = os.getcwd().split("/")[-1]
    if location == "src":
        os.chdir("..")
    elif location == "results":
        os.chdir("..")
    else:
        print("need to be in src, results or Dyes directory")
    # Theoretical data
    methods_basissets = ["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"]
    methods_basissets = [
        "CAM-B3LYP/6-311G(d,p)",
        "bhandhlyp/6-311G(d,p)",
        "PBE1PBE/6-311G(d,p)",
    ]
    plot_js = {
        "weighted_avg": ["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
        "headers_colors": [
            ["CAM-B3LYP/6-311G(d,p)", "blue"],
            ["BHandHLYP/6-311G(d,p)", "red"],
            ["PBE0/6-311G(d,p)", "orange"],
            ["LSF", "green"],
        ],
        # "weights":[0.71, 0.29],
        "weights": [1.21364385, -0.35894991],
        # "weights" :  [ 0.7546616947, 0.2453383053 ]
    }

    # theoretical_dyes_basis_set_out('results.json', output_csv='theoretical', output_latex='theoretical', output_graph='theoretical', )
    # theoretical_dyes_basis_set_out('results.json', output_csv='theoretical', output_latex='theoretical', output_graph='theoretical', plot_js=plot_js, methods_basissets=methods_basissets)
    # Below is one you want to us
    """
    theoretical_dyes_basis_set_out(
        # "./json_files/results_exc.json",
        "./json_files/results_ds5.json",
        output_csv="data_analysis/Absorption_test",
     #   output_latex="data_analysis/Absorption_nm",
     #   output_graph="data_analysis/Absorption_nm",
        units="eV",
        plot_js=plot_js,
        methods_basissets=methods_basissets,
        results_exc=True,
        homo_lumo=True,
        LSF_csv=True,
    )
    """



    # theoretical_dyes_basis_set_out('results_exc.json', output_csv='theoretical_e3',
    #     output_latex='theoretical_e3', output_graph='theoreticale3',
    #     plot_js=plot_js, methods_basissets=methods_basissets, results_exc=True, #homo_lumo=True,
    #     LSF_csv=True
    #     )
    """"""
    """"""
    """"""
    # Benchmark data
    #benchmarks_dyes_basis_set_out('Benchmark/benchmarks.json', output_csv='bm', output_latex='bm', output_graph='bm', exc_json=False)


    benchmarks_dyes_basis_set_out(
        'Benchmark/benchmarks_exc.json',
        methods_basissets=[
        "CAM-B3LYP/6-311G(d,p)",
        "bhandhlyp/6-311G(d,p)",
        "PBE1PBE/6-311G(d,p)",
    #    "CAM-B3LYP/6-311G(d,p)_dichloromethane",
    #    "bhandhlyp/6-311G(d,p)_dichloromethane",
    #    "PBE1PBE/6-311G(d,p)_dichloromethane",
    #    "CAM-B3LYP/6-311G(d,p)_tetrahydrofuran",
    #    "bhandhlyp/6-311G(d,p)_tetrahydrofuran",
    #    "PBE1PBE/6-311G(d,p)_tetrahydrofuran",
    #    "CAM-B3LYP/6-311G(d,p)_nndimethylformamide",
    #    "bhandhlyp/6-311G(d,p)_nndimethylformamide",
    #    "PBE1PBE/6-311G(d,p)_nndimethylformamide",
        ],

        plot_js={
# <<<<<<< HEAD
#         "weighted_avg": ["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
#     #    "weighted_avg": ["CAM-B3LYP/6-311G(d,p)_dichloromethane", "PBE1PBE/6-311G(d,p)_dichloromethane"],
#     #  "weighted_avg": ["CAM-B3LYP/6-311G(d,p)_tetrahydrofuran", "PBE1PBE/6-311G(d,p)_tetrahydrofuran"],
#     #  "weighted_avg": ["CAM-B3LYP/6-311G(d,p)_nndimethylformamide", "PBE1PBE/6-311G(d,p)_nndimethylformamide"],
#         "headers_colors": [
#             ["CAM-B3LYP/6-311G(d,p)", "blue"],
#             ["BHandHLYP/6-311G(d,p)", "red"],
#             ["PBE0/6-311G(d,p)", "orange"],
#             ["LSF", "green"],  # ['Weighted Average', 'green']
#         ],
#         "weights": [0.71, 0.29],
#     },
#         output_csv='data_analysis/nuthin',
#         output_latex='data_analysis/nuthin',
#         output_graph='data_analysis_nuthin',
#         exc_json=True, homo_lumo=False
#     )
#
#
# =======
            "weighted_avg": ["CAM-B3LYP/6-311G(d,p)", "PBE1PBE/6-311G(d,p)"],
            #   "weighted_avg": ["CAM-B3LYP/6-311G(d,p)_dichloromethane", "PBE1PBE/6-311G(d,p)_dichloromethane"],
            #   "weighted_avg": ["CAM-B3LYP/6-311G(d,p)_tetrahydrofuran", "PBE1PBE/6-311G(d,p)_tetrahydrofuran"],
            #   "weighted_avg": ["CAM-B3LYP/6-311G(d,p)_nndimethylformamide", "PBE1PBE/6-311G(d,p)_nndimethylformamide"],
            "headers_colors": [
                ["CAM-B3LYP/6-311G(d,p)", "blue"],
                ["BHandHLYP/6-311G(d,p)", "red"],
                ["PBE0/6-311G(d,p)", "orange"],
                ["LSF", "green"],  # ['Weighted Average', 'green']
            ],
            "weights": [0.71, 0.29],
        },
        output_csv='vac',
        output_latex='vac',
        output_graph='vac',
        exc_json=True,
        homo_lumo=False)
# >>>>>>> 258d915aa06a51f8e01768b0bb867224ebd75baa
    """

    benchmarks_dyes_basis_set_out('Benchmark/benchmarks_exc.json',
        output_csv='test',
        output_latex='test_2',
        output_graph='test_4',
        exc_json=True, homo_lumo=False,
        plot_js = {
        "weighted_avg" :['CAM-B3LYP/6-311G(d,p)','PBE1PBE/6-311G(d,p)'],
        "headers_colors":[
            ['CAM-B3LYP/6-311G(d,p)', 'blue'], ['BHandHLYP/6-311G(d,p)', 'red'], ['PBE0/6-311G(d,p)', 'orange'],  ['LSF', 'green'], #['Weighted Average', 'green']
            ],
      #  "weights":[0.71, 0.29],
        },
        testing=True,
        band_gap=False,
        LSF=True,

    )
    """
    """
    benchmarks_solvation('Benchmark/benchmarks_exc.json',
            output_graph='test_ttt',
            exc_json=True, homo_lumo=True,

    )
    """
    # benchmarks_solvation('Benchmark/benchmarks.json', )

    # df_molecules = json_pandas_molecule('og_results.json')

    # df_molecules = json_pandas_molecule_BM('Benchmark/benchmarks.json')

    # benchmarkFlow()
    # benchamrkPredictPCE()


# criteria
# nm : greatest          ::: Higher
# osci : LUMO : second   ::: osci > 0.1 ::: LUMO > -0.9 eg. -0.8 is better
if __name__ == "__main__":
    main()
