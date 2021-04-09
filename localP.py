import numpy as np
from math import sqrt


class LocalP:
    def __init__(self, bcksi, bceta, schema, elements, waga, alfa, temp_oto):   # tablice bcksi, bceta odpowiadaja tez w tym przypadku
        self.bcksi = bcksi
        self.bceta = bceta
        self.schema = schema
        self.shape_f_tab = np.empty(((self.schema * 4), 4))   # * 4 bo sa 4 sciany
        self.elements = elements
        self.det_tab = []
        self.p_local = []
        self.bc1 = elements[0][3]
        self.bc2 = elements[1][3]
        self.bc3 = elements[2][3]
        self.bc4 = elements[3][3]
        self.waga = waga
        self.alfa = alfa
        self.tem_oto = temp_oto

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

    def calculate_p_local(self):
        self.calculate_shape_f_tab()
        self.calculate_det()
        flags = [(self.bc1 == 1 and self.bc2 == 1), (self.bc2 == 1 and self.bc3 == 1),
                 (self.bc3 == 1 and self.bc4 == 1), (self.bc4 == 1 and self.bc1 == 1)]

        for i in range(int(4)):
            self.p_local.append(0)

        value = 0
        for i in range(int(self.schema * 4)):
            if i % self.schema == 0:
                value += 1
            if not flags[value - 1]:
                i += 1
                continue
            for j in range(4):
                self.p_local[j] += self.shape_f_tab[i][j] * self.waga[i] * self.alfa * self.tem_oto * self.det_tab[j]
        return self.p_local

    def print(self):
        self.calculate_p_local()
        print(self.shape_f_tab)
        print(self.p_local)
