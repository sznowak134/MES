import numpy as np
from math import sqrt


class LocalHBC:
    def __init__(self, bcksi, bceta, schema, elements, alfa, waga):
        self.bcksi = bcksi
        self.bceta = bceta
        self.size_value = schema * 4
        self.shape_f_tab = np.empty((self.size_value, 4))
        self.bc1 = elements[0][3]
        self.bc2 = elements[1][3]
        self.bc3 = elements[2][3]
        self.bc4 = elements[3][3]
        self.elements = elements
        self.bc_part = np.empty((self.size_value, 4, 4))
        self.alfa = alfa
        self.waga = waga
        self.local_bc = np.zeros((4, 4))  # liczba wezlow w elemecie
        self.det_tab = []
        self.schema = schema

    def calculate_shape_f_tab(self):
        for i in range(self.shape_f_tab.shape[0]):
            for j in range(self.shape_f_tab.shape[1]):
                if j == 0:
                    self.shape_f_tab[i][j] = 0.25 * ((1.0 - self.bcksi[i]) * (1.0 - self.bceta[i]))
                elif j == 1:
                    self.shape_f_tab[i][j] = 0.25 * ((1.0 + self.bcksi[i]) * (1.0 - self.bceta[i]))
                elif j == 2:
                    self.shape_f_tab[i][j] = 0.25 * ((1.0 + self.bcksi[i]) * (1.0 + self.bceta[i]))
                elif j == 3:
                    self.shape_f_tab[i][j] = 0.25 * ((1.0 - self.bcksi[i]) * (1.0 + self.bceta[i]))

    def calculate_det(self):
        for i in range(4):
            if i == 3:
                j = 0
                det = pow((self.elements[j][0] - self.elements[i][0]), 2) + pow((self.elements[i][1] - self.elements[j][1]), 2)
                det = sqrt(det) / 2
                self.det_tab.append(det)
            else:
                det = pow((self.elements[i + 1][0] - self.elements[i][0]), 2) + pow((self.elements[i + 1][1] - self.elements[i][1]), 2)
                det = sqrt(det) / 2
                self.det_tab.append(det)

    def calculate_bc_parts(self):
        self.calculate_shape_f_tab()
        self.calculate_det()
        for k in range(self.size_value):
            for i in range(4):
                for j in range(4):
                    self.bc_part[k][i][j] = self.shape_f_tab[k][i] * self.shape_f_tab[k][j] * self.waga[k] * self.alfa * self.det_tab[k % 4]  # (0.0166666)

    def calculate_bc_local(self):
        self.calculate_bc_parts()
        flags = [(self.bc1 == 1 and self.bc2 == 1), (self.bc2 == 1 and self.bc3 == 1),
                 (self.bc3 == 1 and self.bc4 == 1), (self.bc4 == 1 and self.bc1 == 1)]

        value = 0
        for k in range(self.size_value):
            if k % self.schema == 0:
                value += 1
            if not flags[value - 1]:
                k += 1
                continue
            for i in range(4):
                for j in range(4):
                    self.local_bc[i][j] += self.bc_part[k][i][j]

    def get_localhbc(self):
        self.calculate_bc_local()
        return self.local_bc

    def print(self):
        self.calculate_bc_local()
        print(self.local_bc)
