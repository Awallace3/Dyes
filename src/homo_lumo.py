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


import numba


@numba.jit
def minmax(x):
    maximum = x[0]
    minimum = x[0]
    for i in x[1:]:
        if i > maximum:
            maximum = i
        elif i < minimum:
            minimum = i
    return (minimum, maximum)

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

def coefficients_3D_equation(xs, y_exp, coefficients, deg, x_range=False, plot_x_range=[-7, -5.5]):
    if len(coefficients) != deg + 1:
        print("coefficients must be the same length as deg+1")
        return 0
    xys = np.c_[xs, y_exp]
    if x_range:
        #ma, mi = minmax(xs)
        xs = np.arange(plot_x_range[0], plot_x_range[1], 0.01)
        print(xs)
        ys = []
        for x in xs:
            y = 0
            for d in range(deg+1):
                y += coefficients[d] * x ** (deg - d)
            ys.append(y)
        ys = np.array(ys)
        xys = np.c_[xs, ys]


    else:
        for i in range(len(xys[:, 0])):
            y = 0
            for d in range(deg+1):
                y += coefficients[d] * xys[i, 0] ** (deg - d)

            xys[i, 1] = y
        xys = xys[xys[:, 1].argsort()]
    return xys

def correlation_function_nhe(
        df, nhe_to_ev=4.5,
        exp=['HOMO Ox', 'LUMO Ox'],
        h=[
            "CAM-B3LYP HOMO",  "CAM-B3LYP LUMO",
            "BhandLYP HOMO",  "BhandLYP LUMO",
            "PBE0 HOMO",  "PBE0 LUMO",
            ],
        type='LSF',
        deg=4,
        train=True

    ):
    """
    perhaps see how the absorption maps to the bandgaps?
        - experimentally bandgap determines LUMO but computation has the bandgap too large
        - is that because not large enough basis set to account for the lowest energy transitions?
    """

    #df['HOMO'] = -1*abs(df[exp[0]] + nhe_to_ev)
    #df['LUMO'] = -1*abs(df[exp[1]] + nhe_to_ev)
    df['HOMO'] = df[exp[0]]
    df['LUMO'] = df[exp[1]]

    df = df.sort_values(['HOMO'], ascending=True)
    for i in h:
        df[i] = abs(df[i] + 4.5) * -1
    df['dif'] = df[h[0]] - df[h[4]]
    df['z_score'] = stats.zscore(df['dif'])
    # 3 standard deviations away seems fine because most are less than 1
    df = df.loc[df['z_score'].abs()<=3]
    df = df.reset_index().drop(columns=['index'])
    df['count'] = df.index

    exp_homo = df['HOMO'].to_numpy()
    exp_lumo = df['LUMO'].to_numpy()

    if type == 'LSF':
        meths = df[[h[0], h[4]]].to_numpy()
        meths2 = df[[h[1], h[5]]].to_numpy()

        if train:

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
        else:

            out = np.linalg.lstsq(meths, exp_homo)
            first, *_, last = out
            xyzs3 = coefficients_3D_line(meths, exp_homo, first)
            print("\n\t HOMO\n")
            print("Total    Residuel =", get_residual(out, meths, exp_homo))
            print("Total    RSE      =", RSE(exp_homo, xyzs3[:, 2]) )
            print("Total    RMSE     =", mean_squared_error(exp_homo, xyzs3[:, 2], squared=False ))

            out2 = np.linalg.lstsq(meths2, exp_lumo)
            first2, *_, last = out2
            xyzs4 = coefficients_3D_line(meths2, exp_lumo, first2)
            print("\n\t LUMO\n")
            print("Total    Residuel =", get_residual(out, meths2, exp_homo))
            print("Total    RSE      =", RSE(exp_homo, xyzs3[:, 2]) )
            print("Total    RMSE     =", mean_squared_error(exp_homo, xyzs3[:, 2], squared=False ))

            """
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(X_train[:, 0], X_train[:, 1], y_train, 'k.', label="Train")
        ax.scatter(X_test[:, 0], X_test[:, 1], y_test, 'r.', label="Test")
        ax.plot(xyzs1[:, 0], xyzs1[:, 1], xyzs1[:, 2], 'g.',  label="LSF Train")
        ax.plot(xyzs2[:, 0], xyzs2[:, 1], xyzs2[:, 2], 'b.',  label="LSF Test")
        ax.set_xlabel("CAM-B3LYP HOMO")
        ax.set_ylabel("PBE0 HOMO")
        ax.set_zlabel("EXP HOMO")
        """
        fig = plt.figure(dpi=400)
        ax1 = fig.add_subplot()
        ax1.plot(df['count'], exp_homo, 'k', label='Exp. HOMO')
        ax1.plot(df['count'], meths[:,0], label='CAM-B3LYP HOMO')
        ax1.plot(df['count'], meths[:,1], label='PBE0 HOMO')
        ax1.plot(df['count'], xyzs3[:,2], label='LSF HOMO')
        horz_lst = [0.55 for i in df['count']]
        ax1.plot(df['count'], horz_lst, label='0.55 NHE')
        ax1.set_xlabel('Benchmark Dyes')
        ax1.set_ylabel('HOMO Energy (NHE)')
        ax1.legend()
        plt.savefig('../data_analysis/homo_fitting_nhe.png')

        fig = plt.figure(dpi=400)
        ax2 = fig.add_subplot()
        ax2.plot(df['count'], exp_lumo, 'k', label='Exp. LUMO')
        ax2.plot(df['count'], meths2[:,0], label='CAM-B3LYP LUMO')
        ax2.plot(df['count'], meths2[:,1], label='PBE0 LUMO')
        ax2.plot(df['count'], xyzs4[:,2], label='LSF LUMO')
        horz_lst = [-0.90 for i in df['count']]
        ax2.plot(df['count'], horz_lst, label='-0.90 NHE')
        ax2.legend()
        ax2.set_xlabel('Benchmark Dyes')
        ax2.set_ylabel('HOMO Energy (NHE)')
        plt.savefig('../data_analysis/lumo_fitting_nhe.png')

    elif type == 'poly':
        meths = df[h[0]].to_numpy()

        if train:
            X_train, X_test, y_train, y_test = train_test_split(
                meths, exp_homo, test_size=0.30, random_state=42)
            co = np.polyfit(X_train, y_train, deg)
            print(co)
            xys = coefficients_3D_equation(X_train, y_train, co, deg, x_range=True)
        else:
            co = np.polyfit(meths, exp_homo, deg)
            print(co)
            xys = coefficients_3D_equation(meths, exp_homo, co, deg, x_range=True)


        fig = plt.figure()
        ax = fig.add_subplot()

        ax.plot(X_train, y_train, 'k.', label="Train")
        ax.plot(X_test, y_test, 'r.', label="Test")
        ax.plot(xys[:,0], xys[:, 1], 'b-', label="Line")
        #ax.plot(xyz1[:, 0], xyz1[:, 1], 'g.',  label="LSF Train")
        #ax.plot(xyzs2[:, 0], xyzs2[:, 1], xyzs2[:, 2], 'b.',  label="LSF Test")
        ax.set_xlabel("CAM-B3LYP HOMO")
        #ax.set_ylabel("PBE0 HOMO")
        ax.set_ylabel("EXP HOMO")
        plt.legend()
        plt.show()

def correlation_function(
        df, nhe_to_ev=4.5,
        exp=['HOMO Ox', 'LUMO Ox'],
        h=[
            "CAM-B3LYP HOMO",  "CAM-B3LYP LUMO",
            "BhandLYP HOMO",  "BhandLYP LUMO",
            "PBE0 HOMO",  "PBE0 LUMO",
            ],
        type='LSF',
        deg=4,
        train=True

    ):
    """
    perhaps see how the absorption maps to the bandgaps?
        - experimentally bandgap determines LUMO but computation has the bandgap too large
        - is that because not large enough basis set to account for the lowest energy transitions?
    """

    df['HOMO'] = -1*abs(df[exp[0]] + nhe_to_ev)
    df['LUMO'] = -1*abs(df[exp[1]] + nhe_to_ev)
    df = df.sort_values(['HOMO'], ascending=True)
    df['dif'] = df[h[0]] - df[h[4]]
    df['z_score'] = stats.zscore(df['dif'])
    # 3 standard deviations away seems fine because most are less than 1
    df = df.loc[df['z_score'].abs()<=3]
    df = df.reset_index().drop(columns=['index'])
    df['count'] = df.index

    exp_homo = df['HOMO'].to_numpy()
    exp_lumo = df['LUMO'].to_numpy()

    if type == 'LSF':
        meths = df[[h[0], h[4]]].to_numpy()
        meths2 = df[[h[1], h[5]]].to_numpy()

        if train:

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
        else:

            out = np.linalg.lstsq(meths, exp_homo)
            first, *_, last = out
            xyzs3 = coefficients_3D_line(meths, exp_homo, first)
            print("\n\t HOMO\n")
            print("Total    Residuel =", get_residual(out, meths, exp_homo))
            print("Total    RSE      =", RSE(exp_homo, xyzs3[:, 2]) )
            print("Total    RMSE     =", mean_squared_error(exp_homo, xyzs3[:, 2], squared=False ))

            out2 = np.linalg.lstsq(meths2, exp_lumo)
            first2, *_, last = out2
            xyzs4 = coefficients_3D_line(meths2, exp_lumo, first2)
            print("\n\t LUMO\n")
            print("Total    Residuel =", get_residual(out, meths2, exp_homo))
            print("Total    RSE      =", RSE(exp_homo, xyzs3[:, 2]) )
            print("Total    RMSE     =", mean_squared_error(exp_homo, xyzs3[:, 2], squared=False ))

            """
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(X_train[:, 0], X_train[:, 1], y_train, 'k.', label="Train")
        ax.scatter(X_test[:, 0], X_test[:, 1], y_test, 'r.', label="Test")
        ax.plot(xyzs1[:, 0], xyzs1[:, 1], xyzs1[:, 2], 'g.',  label="LSF Train")
        ax.plot(xyzs2[:, 0], xyzs2[:, 1], xyzs2[:, 2], 'b.',  label="LSF Test")
        ax.set_xlabel("CAM-B3LYP HOMO")
        ax.set_ylabel("PBE0 HOMO")
        ax.set_zlabel("EXP HOMO")
        """
        fig = plt.figure(dpi=400)
        ax1 = fig.add_subplot()

        ax1.plot(df['count'], exp_homo, 'k', label='Exp. HOMO')
        ax1.plot(df['count'], meths[:,0], label='CAM-B3LYP HOMO')
        ax1.plot(df['count'], meths[:,1], label='PBE0 HOMO')
        ax1.plot(df['count'], xyzs3[:,2], label='LSF HOMO')
        ax1.legend()
        plt.savefig('../data_analysis/homo_fitting.png')



        fig = plt.figure(dpi=400)
        ax2 = fig.add_subplot()
        ax2.plot(df['count'], exp_lumo, 'k', label='Exp. LUMO')
        ax2.plot(df['count'], meths2[:,0], label='CAM-B3LYP LUMO')
        ax2.plot(df['count'], meths2[:,1], label='PBE0 LUMO')
        ax2.plot(df['count'], xyzs4[:,2], label='LSF LUMO')
        ax2.legend()
        plt.savefig('../data_analysis/lumo_fitting.png')

    elif type == 'poly':
        meths = df[h[0]].to_numpy()

        if train:
            X_train, X_test, y_train, y_test = train_test_split(
                meths, exp_homo, test_size=0.30, random_state=42)
            co = np.polyfit(X_train, y_train, deg)
            print(co)
            xys = coefficients_3D_equation(X_train, y_train, co, deg, x_range=True)
        else:
            co = np.polyfit(meths, exp_homo, deg)
            print(co)
            xys = coefficients_3D_equation(meths, exp_homo, co, deg, x_range=True)


        fig = plt.figure()
        ax = fig.add_subplot()

        ax.plot(X_train, y_train, 'k.', label="Train")
        ax.plot(X_test, y_test, 'r.', label="Test")
        ax.plot(xys[:,0], xys[:, 1], 'b-', label="Line")
        #ax.plot(xyz1[:, 0], xyz1[:, 1], 'g.',  label="LSF Train")
        #ax.plot(xyzs2[:, 0], xyzs2[:, 1], xyzs2[:, 2], 'b.',  label="LSF Test")
        ax.set_xlabel("CAM-B3LYP HOMO")
        #ax.set_ylabel("PBE0 HOMO")
        ax.set_ylabel("EXP HOMO")
        plt.legend()
        plt.show()





def main():
    df = pd.read_csv('exp_homo_lumo.csv').dropna()
    #correlation_function(df, type='LSF', deg=9, train=False)
    correlation_function_nhe(df, type='LSF', deg=9, train=False)



if __name__ == '__main__':
    main()
