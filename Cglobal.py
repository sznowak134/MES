import numpy as np


class CGlobal:
    def __init__(self, elements, data):
        self.elements = elements
        self.data = data
        self.CG = np.empty((int(self.data.nN), int(self.data.nN)), dtype=np.float64)

    def calculate_cg(self):
        for i in range(self.CG.shape[0]):
            for j in range(self.CG.shape[1]):
                self.CG[i][j] = 0

        for i in range(int(self.data.nE)):
            for k in range(len(self.elements[i][4])):       # mozna dodac jeszcze jeden indeks bo i tak zwraca 16
                for l in range(len(self.elements[i][4])):
                    self.CG[self.elements[i][l][2]][self.elements[i][k][2]] += self.elements[i][5][l][k]

        return self.CG
