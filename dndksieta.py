import numpy as np


class DNdksieta:
    def __init__(self, iterations, ksi: list, eta: list):
        self.iterations = iterations
        self.ksi = ksi
        self.eta = eta
        self.dNdksi = np.empty((self.iterations, 4))
        self.dNdeta = np.empty((self.iterations, 4))

    def calculate(self):
        for i in range(self.iterations):
            for j in range(4):
                if j == 0:
                    self.dNdksi[i][j] = -0.25 * (1 - self.eta[i])
                    self.dNdeta[i][j] = -0.25 * (1.0 - self.ksi[i])
                elif j == 1:
                    self.dNdksi[i][j] = 0.25 * (1.0 - self.eta[i])
                    self.dNdeta[i][j] = -0.25 * (1.0 + self.ksi[i])
                elif j == 2:
                    self.dNdksi[i][j] = 0.25 * (1.0 + self.eta[i])
                    self.dNdeta[i][j] = 0.25 * (1.0 + self.ksi[i])
                elif j == 3:
                    self.dNdksi[i][j] = -0.25 * (1.0 + self.eta[i])
                    self.dNdeta[i][j] = 0.25 * (1.0 - self.ksi[i])
        return self.dNdksi, self.dNdeta
