from math import sqrt
from sys import exit
import numpy as np

from global_data import Data
from mesh import Mesh
from dndksieta import DNdksieta
from Hlocal import HLocal
from Hglobal import HGlobal
from Clocal import CLocal
from Cglobal import CGlobal
from localHBC import LocalHBC
from globalHbc import HbcGlobal
from localP import LocalP
from globalP import GlobalP

file = open('data.txt', 'r')
data = file.readlines()
file.close()
data_final = []
for x in data:
    data_final.append(float(x))

data_object = Data(data_final)
print(data_object.nN)


schema = int(input("WYBIERZ SCHEMAT CALKWOWANIA\n"))
wagi = []
waga = []
ksi = []
eta = []
bcksi = []
bceta = []
waga_bc = []
value1 = (1 / sqrt(3))
value2 = sqrt(0.6)
if schema == 2:
    ksi.extend((-value1, value1, value1, -value1))
    eta.extend((-value1, -value1, value1, value1))
    bcksi.extend((-value1, value1, 1, 1, value1, -value1, -1, -1))
    bceta.extend((-1, -1, -value1, value1, 1, 1, value1, -value1))
    wagi.extend((1, 1))
    waga_bc.extend((1, 1, 1, 1, 1, 1, 1, 1))
    for i in range(schema):
        for j in range(schema):
            waga.append(wagi[i] * wagi[j])
elif schema == 3:
    ksi.extend((-value2, 0, value2, -value2, 0, value2, -value2, 0, value2))
    eta.extend((-value2, -value2, -value2, 0, 0, 0, value2, value2, value2))
    bcksi.extend((-value2, 0, value2, 1, 1, 1, value2, 0, -value2, -1, -1, -1))
    bceta.extend((-1, -1, -1, -value2, 0, value2, 1, 1, 1, value2, 0, -value2))
    wagi.extend((0.5555555555555556, 0.8888888888888889, 0.5555555555555556))
    waga_bc.extend((0.5555555555555556, 0.8888888888888889, 0.5555555555555556,
                    0.5555555555555556, 0.8888888888888889, 0.5555555555555556,
                    0.5555555555555556, 0.8888888888888889, 0.5555555555555556,
                    0.5555555555555556, 0.8888888888888889, 0.5555555555555556
                    ))
    for i in range(schema):
        for j in range(schema):
            waga.append(wagi[i] * wagi[j])
elif schema == 4:
    ksi.extend((-0.861136, -0.339981, 0.339981, 0.861136, -0.861136, -0.339981, 0.339981, 0.861136,
                -0.861136, -0.339981, 0.339981, 0.861136, -0.861136, -0.339981, 0.339981, 0.861136))
    eta.extend((-0.861136, -0.861136, -0.861136, -0.861136, -0.339981, -0.339981, -0.339981, -0.339981,
                0.339981, 0.339981, 0.339981, 0.339981, 0.861136, 0.861136, 0.861136, 0.861136))
    bcksi.extend((-0.861136, -0.339981, 0.339981, 0.861136, 1, 1,
                  1, 1, 0.861136, 0.339981, -0.339981, -0.861136, -1, -1, -1, -1))
    bceta.extend((-1, -1, -1, -1, -0.861136, -0.339981, 0.339981,
                  0.861136, 1, 1, 1, 1, 0.861136, 0.339981, -0.339981, -0.861136))
    wagi.extend((0.347855, 0.652145, 0.652145, 0.347855))
    waga_bc.extend((0.347855, 0.652145, 0.652145, 0.347855,
                    0.347855, 0.652145, 0.652145, 0.347855,
                    0.347855, 0.652145, 0.652145, 0.347855,
                    0.347855, 0.652145, 0.652145, 0.347855))
    for i in range(schema):
        for j in range(schema):
            waga.append(wagi[i] * wagi[j])
else:
    print("Wybrano niepoprawny schemat calkowania")
    exit(0)

# siatka
mesh_obj = Mesh(data_object, schema)
elements = mesh_obj.creating_mesh()

del value1, value2
value = schema * schema
dNdksi, dNdeta = DNdksieta(value, ksi, eta).calculate()

x_list = []
y_list = []

det = []
for i in range(int(data_object.nE)):
    for j in range(4):
        x_list.append(elements[i][j][0])
        y_list.append(elements[i][j][1])
    elements[i][4] = HLocal(x_list, y_list, dNdksi, dNdeta, value, waga, data_object.temp).get_hl()
    if i == int(data_object.nE) - 1:
        det = HLocal(x_list, y_list, dNdksi, dNdeta, value, waga, data_object.temp).calculate_det()
    x_list = []
    y_list = []

for i in range(int(data_object.nE)):
    elements[i][5] = CLocal(data_object.c, data_object.ro, det, waga, value, ksi, eta).get_cl()

for i in range(int(data_object.nE)):
    elements[i][6] = LocalHBC(bcksi, bceta, schema, elements[i], data_object.alfa, waga_bc).get_localhbc()

for i in range(int(data_object.nE)):
    elements[i][7] = LocalP(bcksi, bceta, schema, elements[i],
                            waga_bc, data_object.alfa, data_object.temp_oto).calculate_p_local()

temperatures = np.zeros(int(data_object.nN), float)
temperatures = temperatures + 100

for iteration in range(int(data_object.time / data_object.deltatau)):
    HG = HGlobal(elements, data_object).calculate_hg()
    CG = CGlobal(elements, data_object).calculate_cg()

    Hbc = HbcGlobal(elements, data_object).calculate_hbc()
    HG += Hbc

    PG = GlobalP(elements, data_object).calculate_global_p()

    CG = CG / data_object.deltatau
    HG += CG

    for i in range(len(PG)):
        for j in range(len(PG)):
            PG[i] += CG[i][j] * temperatures[j]

    temperatures = np.linalg.solve(HG, PG)
    print(f"Time[s] = {iteration * data_object.deltatau + data_object.deltatau}      "
          f"MinTemp = {np.around(np.min(temperatures), decimals= 3)}      "
          f"MaxTemp = {np.around(np.max(temperatures), decimals= 3)}")
