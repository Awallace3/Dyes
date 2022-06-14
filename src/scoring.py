import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd


def normalize(ls, max_y):
    ma = max(ls)
    for n, i in enumerate(ls):
        ls[n] = i / ma * max_y
    print(max_y / ma)
    return ls


def generate_gaussian(m,
                      ss=[0.1, 0.25],
                      max_y=100,
                      x_range=[-2, -4],
                      cut_off=-3.85):
    xs = range(int(x_range[0] * 100), int(x_range[1] * 100), -1)
    xs = [i / 100 for i in xs]
    ys_1 = []
    ys_2 = []
    zeros = []
    for i in xs:
        x = i
        #print(i)
        if x < cut_off:
            y = 0
            zeros.append(0)


#        elif x >= -3.75 and x <= -3.59:
#            y = 100
#            ys_1.append(y)

        elif x < m:
            s = ss[0]
            y = math.exp(-(x - m)**2 /
                         (2 * s**2)) / (s * math.sqrt(2 * math.pi))
            ys_1.append(y)
        elif x >= m:
            s = ss[1]
            y = math.exp(-(x - m)**2 /
                         (2 * s**2)) / (s * math.sqrt(2 * math.pi))
            ys_2.append(y)
    ys_1 = normalize(ys_1, max_y)
    ys_2 = normalize(ys_2, max_y)
    ys = []
    for i in ys_2:
        ys.append(i)
    for i in ys_1:
        ys.append(i)
    for i in zeros:
        ys.append(i)
    # np.savetxt('gaussian.csv', np.column_stack((xs, ys)))
    data = np.column_stack((xs, ys))
    return data


def score_dye_LUMO(LUMO_energy):
    x = LUMO_energy
    m = -3.7
    if x < -3.85:
        y = 0
    elif x < m:
        s = 0.15
        y = math.exp(
            -(x - m)**2 /
            (2 * s**2)) / (s * math.sqrt(2 * math.pi)) * 37.68307130217745
    elif x >= m:
        s = 0.25
        y = math.exp(
            -(x - m)**2 /
            (2 * s**2)) / (s * math.sqrt(2 * math.pi)) * 62.66570686577501
    return y


def absorption_score(lambd):
    score = ((lambd - 600) / 400) * 100
    return score


def orbital_score(homodonor, lumoacceptor, lumoanchor):
    a = (float(lumoacceptor) + float(lumoanchor)) / 2
    b = (float(homodonor) + float(lumoacceptor)) / 2
    s = (a + b) / 2
    return s


def test_graph():
    data = generate_gaussian(-3.7,
                             ss=[0.15, 0.25],
                             cut_off=-3.85,
                             x_range=[-2.5, -4])
    fig = plt.figure(dpi=1000)
    plt.plot(data[:, 0], data[:, 1], label="MO Scoring")
    plt.xlabel("LUMO energy (eV)")
    plt.ylabel("Score")
    plt.savefig("../data_analysis/scoring.png")
    plt.show()

def score_dyes():
    filename = '../data_analysis/fin.csv'
    #    filename = '../data_analysis/benchscore.csv'
    df = {
        'Name': [],
        'Absorption Score': [],
        'LUMO Score': [],
        'Charge Transfer Score': [],
        'HOMO Donor': [],
        'LUMO Acceptor': [],
        'LUMO Anchor': [],
        'HOMO Energy': [],
        'LUMO energy': [],
        'Wave': [],
        'Total Score': []
    }
    with open(filename, 'r') as fp:
        data = fp.readlines()
        for line in data[1:]:
            line = line.split(',')
            '''
            # Benchmark Dyes
            LUMO_energy = float(line[5])
            HOMO_energy = float(line[4])
            lambd = float(line[6])
            homodonor=line[1]
            lumoacceptor=line[2]
            lumoanchor=line[3]
            c = orbital_score(homodonor,lumoacceptor,lumoanchor)
            ###
            '''

            LUMO_energy = float(line[9])
            HOMO_energy = float(line[10])
            lambd = float(line[11])
            homodonor = line[1]
            lumoacceptor = line[6]
            lumoanchor = line[8]

            if float(lambd) < 600 or float(LUMO_energy) < -3.75 or float(
                    lumoanchor) < 4.0:
                v = score_dye_LUMO(LUMO_energy)
                y = absorption_score(lambd)
                c = orbital_score(homodonor, lumoacceptor, lumoanchor)
                df['Name'].append(line[0])
                df['Absorption Score'].append(y)
                df['LUMO Score'].append(v)
                df['Charge Transfer Score'].append(c)
                df['HOMO Donor'].append(homodonor)
                df['LUMO Acceptor'].append(lumoacceptor)
                df['LUMO Anchor'].append(lumoanchor)
                df['HOMO Energy'].append(HOMO_energy)
                df['LUMO energy'].append(LUMO_energy)
                df['Wave'].append(lambd)
                df['Total Score'].append('FAIL')
            else:

                v = score_dye_LUMO(LUMO_energy)
                y = absorption_score(lambd)
                c = orbital_score(homodonor, lumoacceptor, lumoanchor)
                df['Name'].append(line[0])
                df['Absorption Score'].append(y)
                df['LUMO Score'].append(v)
                df['Charge Transfer Score'].append(c)
                df['HOMO Donor'].append(homodonor)
                df['LUMO Acceptor'].append(lumoacceptor)
                df['LUMO Anchor'].append(lumoanchor)
                df['HOMO Energy'].append(HOMO_energy)
                df['LUMO energy'].append(LUMO_energy)
                df['Wave'].append(lambd)
                df['Total Score'].append(v + y + c)
                print('LUMO score:', v)
                print('Absorption score:', y)
                print('Charge transfer score:', int(c))
    df = pd.DataFrame(df)
    print(df)

    df.to_csv('../data_analysis/scoring.csv', index=False)

    #   test_graph()
    #   LUMO_ener= [-3.41,-3.50,-3.35,-3.64,-3.34,-3.74]
    #   for i in LUMO_ener:


def main():
    test_graph()
    # score_dyes()

    return


if __name__ == "__main__":
    main()
