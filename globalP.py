import numpy as np


class GlobalP:
    def __init__(self, elements, data):
        self.elements = elements
        self.data = data
        self.P = np.zeros(int(data.nN), dtype=np.float64)

    def calculate_global_p(self):
        for i in range(int(self.data.nE)):
            for j in range(4):
                self.P[self.elements[i][j][2]] += self.elements[i][7][j]
        return self.P
