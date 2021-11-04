import os
import math
import glob
import subprocess
import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.function_base import average
from numpy.lib.shape_base import split
import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy import stats

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def weighted_avg_calc(
        df,
        methods_basissets_avg=['CAM-B3LYP/6-311G(d,p)', 'PBE1PBE/6-311G(d,p)'],
        debug=False,
        verbose=False,
        ):
    dft1 = df[methods_basissets_avg[0]].to_numpy(dtype='float')
    dft2 = df[methods_basissets_avg[1]].to_numpy(dtype='float')

    exp = df['Exp'].to_numpy(dtype='float')

    dfts = np.vstack((dft1, dft2)).transpose()
    #test_co = np.array([0.71, 0.29])

    #print("dfts", dfts)
    #print(dft1.shape)
    #print(dft2.shape)
    if debug:
        print(dfts, exp)
        print(dfts.shape, exp.shape)
    out = np.linalg.lstsq(dfts, exp)
    # A*x - exp == close to zero
    # plug in my values for A to test residuals
    first, *_, last = out
    if verbose:
        print('coefficients =',first)
        print('final = ', dft1[0], first[0], exp[0])

    mult = np.matmul(dfts, first)
    sub = np.subtract(mult, exp)
    squared = np.square(sub)
    summed = np.sum(squared)
    if verbose:
        print("residuel =", summed)

    #mult = np.matmul(dfts, test_co)
    #sub = np.subtract(mult, exp)
    #squared = np.square(sub)
    #summed = np.sum(squared)
    #print("old", summed)

    # say used least-squares fit
    return first, summed

def RSE(y_true, y_predicted):
    """
    - y_true: Actual values
    - y_predicted: Predicted values
    """
    y_true = np.array(y_true)
    y_predicted = np.array(y_predicted)
    RSS = np.sum(np.square(y_true - y_predicted))

    rse = math.sqrt(RSS / (len(y_true) - 2))
    return rse


def get_residual(linalg_lsqf_out, x_in, y_in):
    first, *_, last = linalg_lsqf_out
    mult = np.matmul(x_in, first)
    sub = np.subtract(mult, y_in)
    squared = np.square(sub)
    summed = np.sum(squared)
    return summed

def coefficients_3D_line(xs, y_exp, coefficients):
    xyzs = np.c_[xs, y_exp]
    for i in range(len(xyzs[:, 0])):
        y = coefficients[0] * xyzs[i, 0] + coefficients[1] * xyzs[i, 1]
        xyzs[i, 2] = y
    xyzs = xyzs[xyzs[:, 2].argsort()]
    return xyzs


def correlation_function(
        df, nhe_to_ev=4.5,
        exp=['HOMO Ox', 'LUMO Ox'],
        h=[
            "CAM-B3LYP HOMO",  "CAM-B3LYP LUMO",
            "BhandLYP HOMO",  "BhandLYP LUMO",
            "PBE0 HOMO",  "PBE0 LUMO",
            ],
        deg=4

    ):

    df['HOMO'] = -1*abs(df[exp[0]] + nhe_to_ev)
    df['LUMO'] = -1*abs(df[exp[1]] + nhe_to_ev)
    df = df.sort_values(['HOMO'], ascending=True)
    df['dif'] = df[h[0]] - df[h[4]]
    df['z_score'] = stats.zscore(df['dif'])
    # 3 standard deviations away seems fine because most are less than 1
    df = df.loc[df['z_score'].abs()<=3]

    exp_homo = df['HOMO'].to_numpy()
    meths = df[[h[0], h[4]]].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
            meths, exp_homo, test_size=0.30, random_state=42)

    out = np.linalg.lstsq(X_train, y_train)

    first, *_, last = out
    print('\ncoefficients =',first, '\n')

    xyzs1 = coefficients_3D_line(X_train, y_train, first)
    print("Training Residuel =", get_residual(out, X_train, y_train))
    print("Training RSE      =", RSE(y_train, xyzs1[:, 2]) )
    print()
    xyzs2 = coefficients_3D_line(X_test, y_test, first)
    print("Testing  Residuel =", get_residual(out, X_test, y_test))
    print("Testing  RSE      =", RSE(y_test, xyzs2[:, 2]) )
    print()
    xyzs3 = coefficients_3D_line(meths, exp_homo, first)
    print("Total    Residuel =", get_residual(out, meths, exp_homo))
    print("Total    RSE      =", RSE(exp_homo, xyzs3[:, 2]) )
    print("Total    RMSE     =", mean_squared_error(exp_homo, xyzs3[:, 2], squared=False ))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(X_train[:, 0], X_train[:, 1], y_train, 'k.', label="Train")
    ax.scatter(X_test[:, 0], X_test[:, 1], y_test, 'r.', label="Test")
    ax.plot(xyzs1[:, 0], xyzs1[:, 1], xyzs1[:, 2], 'g.',  label="LSF Train")
    ax.plot(xyzs2[:, 0], xyzs2[:, 1], xyzs2[:, 2], 'b.',  label="LSF Test")
    ax.set_xlabel("CAM-B3LYP HOMO")
    ax.set_ylabel("PBE0 HOMO")
    ax.set_zlabel("EXP HOMO")
    plt.legend()
    plt.show()
    """
    1. How can we find outliers in theoretical dataset?
        potentially use a difference between PBE0 and CAM-B3LYP?
            - beyond certain value, consider outlier -> g-test
            for point on graph, PBE0 really low but cam and exp in middle of data



    """


    """
    plt.plot(xs, ys, 'b--', label='Test')
    plt.plot(xs, ys, 'b--', label='Test')
    #plt.plot(meth_homo, exp_homo, 'k.', label=h[0])
    #plt.plot(meth_homo2, exp_homo, 'r.', label=h[4])
    plt.xlabel("Theoretical energies")
    plt.ylabel("Experiment Energies")
    plt.legend()
    plt.show()
    """
    """
    poly = np.polyfit(meth_homo, exp_homo, deg)

    xs = np.arange(-5.5, -7, -0.05)
    ys = []
    for x in xs:
        y = 0
        for j in range(deg+1):
            y += poly[j] * x**(deg-j)

        ys.append(y)
    ys = np.array(ys)
    plt.plot(xs, ys, 'b--', label='Poly')
    plt.plot(meth_homo, exp_homo, 'k-')
    plt.show()
    """




def main():
    df = pd.read_csv('exp_homo_lumo.csv').dropna()
    correlation_function(df)



if __name__ == '__main__':
    main()
