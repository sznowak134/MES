import numpy as np


class CLocal:
    def __init__(self, c, ro, det, waga, size_value, ksi, eta):
        self.c = c
        self.ro = ro
        self.det = det
        self.waga = waga
        self.size_value = size_value
        self.ksi = ksi
        self.eta = eta
        self.n_tab = np.empty((size_value, 4))
        self.nt_tab = np.empty((size_value, 4, 4))
        self.nn_tab = np.empty((size_value, 4, 4))
        self.CL = np.zeros((4, 4))

    def calculate_n_tab(self):
        for i in range(self.n_tab.shape[0]):
            for j in range(self.n_tab.shape[1]):
                if j == 0:
                    self.n_tab[i][j] = 0.25 * ((1.0 - self.ksi[i]) * (1.0 - self.eta[i]))
                elif j == 1:
                    self.n_tab[i][j] = 0.25 * ((1.0 + self.ksi[i]) * (1.0 - self.eta[i]))
                elif j == 2:
                    self.n_tab[i][j] = 0.25 * ((1.0 + self.ksi[i]) * (1.0 + self.eta[i]))
                elif j == 3:
                    self.n_tab[i][j] = 0.25 * ((1.0 - self.ksi[i]) * (1.0 + self.eta[i]))

    def calculate_nn_tab(self):
        self.calculate_n_tab()
        for k in range(self.size_value):
            for i in range(self.nn_tab.shape[1]):
                for j in range(self.nn_tab.shape[2]):
                    self.nn_tab[k][i][j] = self.det[k] * self.ro * self.c * self.n_tab[k][j] * self.n_tab[k][i] * self.waga[k]

    def calculate_cl(self):
        self.calculate_nn_tab()
        for i in range(self.CL.shape[0]):
            for j in range(self.CL.shape[1]):
                for k in range(self.size_value):
                    self.CL[i][j] += self.nn_tab[k][i][j]

    def get_cl(self):
        self.calculate_cl()
        return self.CL

    def print(self):
        print(self.nn_tab)
