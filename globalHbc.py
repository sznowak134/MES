import numpy as np


class HbcGlobal:
    def __init__(self, elements, data):
        self.elements = elements
        self.data = data
        self.Hbc = np.zeros((int(self.data.nN), int(self.data.nN)), dtype=np.float64)

    def calculate_hbc(self):
        for i in range(int(self.data.nE)):
            for k in range(len(self.elements[i][4])):
                for l in range(len(self.elements[i][4])):
                    self.Hbc[self.elements[i][l][2]][self.elements[i][k][2]] += self.elements[i][6][l][k]

        return self.Hbc
