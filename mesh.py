import numpy as np


class Mesh:
    def __init__(self, data, schema):
        self.data = data
        self.elements = []
        self.nodes = []
        self.HL = np.empty((4, 4))
        self.CL = np.empty((4, 4))
        self.Hbc = np.empty((4, 4))
        self.P_local = []
        self.temp = 100

    def creating_mesh(self):
        for i in range(4):
            self.P_local.append(0)

        temp = 0
        for i in range(int(self.data.nW)):
            for j in range(int(self.data.nH)):
                buff1 = i * self.data.deltaX
                buff2 = j * self.data.deltaY
                self.nodes.append((buff1, buff2))
                temp += 1

        elem_num = 0
        id2 = int(self.data.nH)
        id3 = int(self.data.nH + 1)
        for i in range(int(self.data.nE + (self.data.nW - 1))):
            if ((self.data.nH + i) % self.data.nH) == (self.data.nH - 1):
                continue
            self.elements.append(list())
            self.elements[elem_num].append([self.nodes[i][0], self.nodes[i][1], i])
            self.elements[elem_num].append([self.nodes[i + id2][0], self.nodes[i + id2][1], (i + id2)])
            self.elements[elem_num].append([self.nodes[i + id3][0], self.nodes[i + id3][1], (i + id3)])
            self.elements[elem_num].append([self.nodes[i + 1][0], self.nodes[i + 1][1], (i + 1)])
            self.elements[elem_num].append(self.HL)
            self.elements[elem_num].append(self.CL)
            self.elements[elem_num].append(self.Hbc)
            self.elements[elem_num].append(self.P_local)
            # self.elements[elem_num] = list((x, y, node_number, bc)x4, HL, CL, Hbc, P)
            elem_num += 1

        # print('\n')
        # elem_num = 0
        # variable = 0
        # for i in range(int(self.data.nE + (self.data.nW - 1))):
        #     if ((self.data.nH + i) % self.data.nH) == (self.data.nH - 1):
        #         variable += 1
        #         continue
        #     print(f"[{i}] x = {self.elements[elem_num][0][0]} y = {self.elements[elem_num][0][1]}")
        #     print(f"[{i + id2}] x = {self.elements[elem_num][1][0]} y = {self.elements[elem_num][1][1]}")
        #     print(f"[{i + id3}] x = {self.elements[elem_num][2][0]} y = {self.elements[elem_num][2][1]}")
        #     print(f"[{i + 1}] x = {self.elements[elem_num][3][0]} y = {self.elements[elem_num][3][1]}", end='\n\n')
        #     elem_num += 1

        for i in range(int(self.data.nE)):
            for j in range(4):
                if self.elements[i][j][0] == 0 or self.elements[i][j][0] == self.data.W or self.elements[i][j][1] == 0 or self.elements[i][j][1] == self.data.H:
                    self.elements[i][j].append(1)
                else:
                    self.elements[i][j].append(0)

        for i in range(int(self.data.nE)):
            for j in range(4):
                self.elements[i][j].append(self.temp)

        return self.elements
