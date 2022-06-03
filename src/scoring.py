import numpy as np
import matplotlib.pyplot as plt
import math


def normalize(ls, max_y):
    ma = max(ls)
    for n, i in enumerate(ls):
        ls[n] = i / ma * max_y
    print(max_y / ma)
    return ls


def generate_gaussian(m,
                      ss=[0.1, 0.5],
                      max_y=100,
                      x_range=[-2, -4],
                      cut_off=-3.6):
    xs = range(int(x_range[0] * 100), int(x_range[1] * 100), -1)
    xs = [i / 100 for i in xs]
    ys_1 = []
    ys_2 = []
    zeros = []
    for i in xs:
        x = i
        if x < cut_off:
            y = 0
            zeros.append(0)
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
    m = -3.6
    if x < -3.75:
        y = 0
    elif x < m:
        s = 0.1
        y = math.exp(
            -(x - m)**2 /
            (2 * s**2)) / (s * math.sqrt(2 * math.pi)) * 25.191928011443522
    elif x >= m:
        s = 0.25
        y = math.exp(
            -(x - m)**2 /
            (2 * s**2)) / (s * math.sqrt(2 * math.pi)) * 62.66570686577501
    return y


def test_graph():
    data = generate_gaussian(-3.6,
                             ss=[0.1, 0.25],
                             cut_off=-3.75,
                             x_range=[-2.5, -4])
    plt.plot(data[:, 0], data[:, 1], label="LUMO Scoring")
    plt.xlabel("LUMO energy (eV)")
    plt.ylabel("Score")
    plt.savefig("../data_analysis/scoring.png")
    plt.show()


def main():
    # test_graph()
    LUMO_energy = -3.5
    v = score_dye_LUMO(LUMO_energy)
    print('score:', v)

    return


if __name__ == "__main__":
    main()
