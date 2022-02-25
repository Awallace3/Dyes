import matplotlib.pyplot as plt
import pandas as pd


def makeLSFdata(csv_cam, csv_pbe, coefficients=[1.255, -0.408]):
    cam = pd.read_csv(
        csv_cam, delimiter=" ", names=["1", "CAM-B3LYP/6-311G(d,p)"]
    )
    pbe = pd.read_csv(csv_pbe, delimiter=" ", names=["2", "PBE0/6-311G(d,p)"])
    data = pd.concat([cam, pbe], axis=1)

    data["LSF_energy"] = (
        data["1"] * coefficients[0] + data["2"] * coefficients[1]
    )
    data["LSF_osci"] = (
        data["CAM-B3LYP/6-311G(d,p)"] * coefficients[0]
        + data["PBE0/6-311G(d,p)"] * coefficients[1]
    )
    data = data[["LSF_energy", "LSF_osci"]]
    print(data)
    data.to_csv("lsf.csv", sep=" ", index=False, header=False)
    return data["LSF_energy"]


def convUnits(df, columns_convert=["Exp"]):
    h = 6.626e-34
    c = 3e17
    Joules_to_eV = 1.602e-19
    for i in columns_convert:
        df[i] = df[i].apply(lambda x: h * c / (x * Joules_to_eV))
    return df


def dyeCamPbeLsf(csv_cam, csv_pbe, csv_lsf="lsf_data.csv"):
    cam = pd.read_csv(
        csv_cam, delimiter=" ", names=["Energy(eV)", "CAM-B3LYP/6-311G(d,p)"]
    )
    pbe = pd.read_csv(csv_pbe, delimiter=" ", names=["2", "PBE0/6-311G(d,p)"])
    lsf = pd.read_csv(csv_lsf, delimiter=" ", names=["3", "LSF"])
    data = pd.concat([cam, pbe], axis=1)
    df = pd.concat([data, lsf], axis=1)
    df = convUnits(df, ["Energy(eV)", "2", "3"])

    print(data)
    ax = df.plot(
        x="Energy(eV)",
        y="CAM-B3LYP/6-311G(d,p)",
        color="r",
        label="CAM-B3LYP/6-311G(d,p)",
    )
    df.plot(
        x="Energy(eV)",
        y="PBE0/6-311G(d,p)",
        color="g",
        label="PBE0/6-311G(d,p)",
        ax=ax,
    )
    df.plot(x="Energy(eV)", y="LSF", color="b", label="LSF", ax=ax)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Oscillator Strength")
    plt.show()
    return


# makeLSFdata('./5_28_6cam.csv', './5_28_6pbe0.csv')
dyeCamPbeLsf("./cam.csv", "./pbe0.csv")
