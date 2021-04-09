import numpy as np


class HGlobal:
    def __init__(self, elements, data):
        self.elements = elements
        self.data = data
        self.HG = np.zeros((int(self.data.nN), int(self.data.nN)), dtype=np.float64)

    def calculate_hg(self):
        for i in range(int(self.data.nE)):
            for k in range(len(self.elements[i][4])):
                for l in range(len(self.elements[i][4])):
                    self.HG[self.elements[i][l][2]][self.elements[i][k][2]] += self.elements[i][4][l][k]

        return self.HG
