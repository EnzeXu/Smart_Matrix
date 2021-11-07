# smart_matrix.py
# Created by ENZE XU on 2021/11/6.

import numpy as np


class SmartItem:
    def __init__(self, data):
        # example_data: "y1^3"
        self.status = 0
        self.data = data
        self.base = None
        self.power = None
        self.split = self.data.split("^")
        if len(self.split) > 2:
            self.status = 1
            print("[Smart Matrix] Error: bad format in initialing SmartItem \"{0}\" (too many \"^\")".format(self.__repr__()))
            return
        elif len(self.split) == 2:
            self.base = self.split[0]
            try:
                self.power = float(self.split[1])
            except ValueError:
                print("[Smart Matrix] Error: bad format in initialing SmartItem \"{0}\" (bad format after \"^\")".format(self.__repr__()))
        else:
            self.base = self.split[0]
            self.power = 1.0

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

    def print(self):
        print("data:", self.data)
        print("base:", self.base)
        print("power:", self.power)


class SmartPart:
    def __init__(self, data):
        # example_data: "-100*x13*y1^3*x2"
        self.status = 0
        self.data = data.replace(" ", "")
        self.data_formatted = None
        self.sig = None
        self.coefficient = None
        self.dic = None
        self.data_split = None
        self.keys = None
        self.key_string = None
        self.pure_number = None
        self.set_data()

    def __repr__(self):
        return str(self.data_formatted)

    def __str__(self):
        return str(self.data_formatted)

    def set_data(self):
        data_pure = self.data
        if data_pure[0] == '-':
            self.sig = 1
            data_pure = data_pure[1:]
        elif data_pure[0] == '+':
            self.sig = 0
            data_pure = data_pure[1:]
        else:
            self.sig = 0
        self.data_split = data_pure.split("*")
        try:
            self.coefficient = float(self.data_split[0])
            self.data_split = self.data_split[1:]
        except ValueError:
            self.coefficient = 1.0

        self.dic = dict()
        for item in self.data_split:
            si = SmartItem(item)
            if si.base not in self.dic:
                self.dic[si.base] = si.power
            else:
                self.dic[si.base] += si.power
        self.keys = sorted(list(self.dic.keys()), key=lambda x: x.replace("^", " "))
        if len(self.keys) == 0:
            self.pure_number = 1
            self.key_string = "1"
            self.data_formatted = "{0}{1}".format("-" if self.sig else "+", "%f" % self.coefficient)
        else:
            self.pure_number = 0
            self.key_string = "*".join(["{0}{1}".format(one_key, "^" + "%f" % self.dic.get(one_key) if self.dic.get(one_key) != 1 else "") for one_key in self.keys])
            self.data_formatted = "{0}{1}{2}".format("-" if self.sig else "+", "%f" % self.coefficient + "*", self.key_string)

    def print(self):
        print("data:", self.data)
        print("data_formatted:", self.data_formatted)
        print("sig:", self.sig)
        print("coefficient:", self.coefficient)
        print("key_string:", self.key_string)


class SmartCell:
    def __init__(self, data):
        # example_data: "-x13*y1^3*x2+x11+x12*x13*y1-x24*x16*y1+2*x2-3*x2"
        self.status = 0
        self.data = data.replace(" ", "")
        self.data_split = None
        self.dic = None
        self.keys = None
        self.data_formatted = None
        self.set_data()
        self.smart_part_list = None
        self.save_smart_part_list()

    def __repr__(self):
        return str(self.data_formatted)

    def __str__(self):
        return str(self.data_formatted)

    def __getitem__(self, item):
        return self.smart_part_list[item]

    def set_data(self):
        if len(self.data) == 0:
            self.data = "0"
        self.data_split = self.data.replace("-", "$-").replace("+", "$+").split("$")
        if len(self.data_split[0]) == 0:
            self.data_split = self.data_split[1:]
        self.dic = dict()
        for item in self.data_split:
            sp = SmartPart(item)
            if sp.key_string not in self.dic:
                self.dic[sp.key_string] = float("{0}{1}".format("-" if sp.sig else "+", sp.coefficient))
            else:
                self.dic[sp.key_string] += float("{0}{1}".format("-" if sp.sig else "+", sp.coefficient))
        self.keys = sorted(list(self.dic.keys()), key=lambda x: x.replace("^", " "))
        # print(self.keys)
        self.data_formatted = ""
        for one_key in self.keys:
            if self.dic.get(one_key) == 0:
                continue
            elif self.dic.get(one_key) > 0:
                self.data_formatted += " +{0}{1}".format("%f" % self.dic.get(one_key), "*" + one_key if one_key != "1" else "")
            else:
                self.data_formatted += " {0}*{1}".format("%f" % self.dic.get(one_key), one_key)
        if len(self.data_formatted) == 0:
            self.data_formatted = " +0"
        else:
            self.data_formatted = self.data_formatted.replace("^1.000000", "").replace("1.000000*", "").replace(".000000", "")

    def save_smart_part_list(self):
        # print(self.data_formatted)
        self.data_split = self.data_formatted.replace(" ", "").replace("-", "$-").replace("+", "$+").split("$")
        if len(self.data_split[0]) == 0:
            self.data_split = self.data_split[1:]
        self.smart_part_list = []
        for item in self.data_split:
            sp = SmartPart(item)
            self.smart_part_list.append(sp)

    def print(self):
        print("data:", self.data)
        print("data_formatted:", self.data_formatted)


class SmartMatrix:
    def __init__(self, data):
        # example_data: [["x11", "x12", "x13"], ["x21", "x22", "x23"]]
        self.status = 0
        self.data = np.asarray(data)
        self.shape = self.data.shape
        self.data_standard = None
        self.data_formatted = None
        self.width_max = None
        self.set_data()

    def __repr__(self):
        return str(self.data_formatted)

    def __str__(self):
        return str(self.data_formatted)

    def __getitem__(self, item):
        return self.data_standard[item]

    def set_data(self):
        self.data_standard = []
        self.width_max = -1
        for i in range(self.shape[0]):
            row = []
            for j in range(self.shape[1]):
                try:
                    sc = SmartCell(self.data[i][j])
                    self.width_max = max(self.width_max, len(sc.data_formatted))
                    row.append(sc)
                except Exception as e:
                    print(e)
                    print("[Smart Matrix] Error: bad format in initialing SmartMatrix (i, j) = ({0}, {1}) data = \"{2}\"".format(i, j, self.data[i][j]))
            self.data_standard.append(row)
        self.data_formatted = "shape = {0}\n".format(self.shape)
        for i in range(self.shape[0]):
            self.data_formatted += "["
            for j in range(self.shape[1]):
                self.data_formatted += self.data_standard[i][j].data_formatted.rjust(self.width_max)
                if j < self.shape[1] - 1:
                    self.data_formatted += ", "
                else:
                    self.data_formatted += " ]\n"


def times_smart_part(smart_part_1: SmartPart, smart_part_2: SmartPart):
    new_sig = (smart_part_1.sig + smart_part_2.sig) % 2
    new_coefficient = smart_part_1.coefficient * smart_part_2.coefficient
    new_data = "{0}{1}{2}{3}".format("-" if new_sig else "+", new_coefficient, "*" + smart_part_1.key_string if smart_part_1.key_string != "1" else "", "*" + smart_part_2.key_string if smart_part_2.key_string != "1" else "")
    return SmartPart(new_data)


def times_smart_cell(smart_cell_1: SmartCell, smart_cell_2: SmartCell):
    new_data = ""
    for sp1 in smart_cell_1.smart_part_list:
        for sp2 in smart_cell_2.smart_part_list:
            new_data += times_smart_part(sp1, sp2).data_formatted
    # print(new_data)
    return SmartCell(new_data)


def plus_smart_cell(smart_cell_1: SmartCell, smart_cell_2: SmartCell):
    return SmartCell(smart_cell_1.data_formatted + smart_cell_2.data_formatted)


def times_smart_matrix(smart_matrix_1: SmartMatrix, smart_matrix_2: SmartMatrix):
    if smart_matrix_1.shape[1] != smart_matrix_2.shape[0]:
        print("[Smart Matrix] Error: shape{0} mismatches shape{1} on matrix-times".format(smart_matrix_1.shape, smart_matrix_2.shape))
        return None
    new_data = []
    for i in range(smart_matrix_1.shape[0]):
        row = []
        for j in range(smart_matrix_2.shape[1]):
            tmp_sc = SmartCell("")
            for k in range(smart_matrix_1.shape[1]):
                tmp_sc = plus_smart_cell(tmp_sc, times_smart_cell(smart_matrix_1.data_standard[i][k], smart_matrix_2.data_standard[k][j]))
            row.append(tmp_sc.data_formatted)
        new_data.append(row)
    return SmartMatrix(new_data)


