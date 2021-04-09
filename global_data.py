class Data:
    def __init__(self, data):
        self.H = data[0]
        self.W = data[1]
        self.nH = data[2]
        self.nW = data[3]
        self.nE = (self.nH - 1) * (self.nW - 1)
        self.nN = self.nH * self.nW
        self.deltaX = self.W / (float(self.nW) - 1.0)
        self.deltaY = self.H / (float(self.nH) - 1.0)
        self.temp = data[4]
        self.c = data[5]
        self.ro = data[6]
        self.alfa = data[7]
        self.temp_oto = data[8]
        self.deltatau = data[9]
        self.time = data[10]
