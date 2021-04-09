import numpy as np


class HLocal:
    def __init__(self, x_list, y_list, dNdksi, dNdeta, size_value, waga, temp):
        self.x_list = x_list
        self.y_list = y_list
        self.dNdksi = dNdksi
        self.dNdeta = dNdeta
        self.size_value = size_value
        self.jacobian = np.empty((4, size_value))
        self.det = []
        self.jac_inverse = np.empty((4, size_value))
        self.dNdx = np.empty((4, size_value))
        self.dNdy = np.empty((4, size_value))
        self.dndx_T = np.empty((size_value, 4, 4))
        self.dndy_T = np.empty((size_value, 4, 4))
        self.dndxdndy = np.empty((size_value, 4, 4))
        self.waga = waga
        self.wsp = temp
        self.HL = np.zeros((4, 4))

    def calculate_jacobian(self):
        for i in range(4):
            for j in range(self.size_value):
                self.jacobian[i][j] = 0

        for i in range(self.size_value):
            for j in range(4):
                for k in range(4):
                    if j == 0:
                        self.jacobian[j][i] += self.x_list[k] * self.dNdksi[j][k]
                    elif j == 1:
                        self.jacobian[j][i] += self.y_list[k] * self.dNdksi[j][k]
                    elif j == 2:
                        self.jacobian[j][i] += self.x_list[k] * self.dNdeta[j][k]
                    elif j == 3:
                        self.jacobian[j][i] += self.y_list[k] * self.dNdeta[j][k]

    def calculate_det(self):
        self.calculate_jacobian()
        for i in range(self.size_value):
            self.det.append(self.jacobian[0][i] * self.jacobian[3][i] - self.jacobian[1][i] * self.jacobian[2][i])
        return self.det

    def calculate_jac_inv(self):
        self.calculate_det()
        k = 0
        for i in range(self.size_value):
            for j in range(3, -1, -1):
                if k == 1 or k == 2:
                    self.jac_inverse[k][i] = -(self.jacobian[j][i] / self.det[i])
                elif k == 0 or k == 3:
                    self.jac_inverse[k][i] = self.jacobian[j][i] / self.det[i]
                k += 1
            k = 0

    def calculate_dndx_dndy(self):
        self.calculate_jac_inv()
        for i in range(self.size_value):
            for j in range(4):
                self.dNdx[j][i] = (self.jac_inverse[0][j] * self.dNdksi[i][j] + self.jac_inverse[1][j] * self.dNdeta[i][j])
                self.dNdy[j][i] = (self.jac_inverse[2][j] * self.dNdksi[i][j] + self.jac_inverse[3][j] * self.dNdeta[i][j])

    def calculate_dndxdndy(self):
        self.calculate_dndx_dndy()
        for k in range(self.size_value):
            for i in range(4):
                for j in range(4):
                    self.dndxdndy[k][i][j] = self.waga[k] * self.wsp * self.det[k] * (self.dNdx[j][k] * self.dNdx[i][k] + self.dNdy[j][k] * self.dNdy[i][k])
                    # wsp - > wsp przewodzenia ciepla

    def calculate_hl(self):
        self.calculate_dndxdndy()
        for i in range(self.HL.shape[0]):
            for j in range(self.HL.shape[1]):
                for k in range(self.size_value):
                    self.HL[i][j] += self.dndxdndy[k][i][j]

    def get_hl(self):
        self.calculate_hl()
        return self.HL
