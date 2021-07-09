import numpy as np


def read_file(file):
    name = ""
    coord = np.ndarray((0, 3))
    with open(file, mode='r', encoding='windows-1251') as f:
        for line_num, line in enumerate(f.readlines()):
            if line_num == 1:
                name = line.split()[3]
            elif line_num >= 12:
                splitted = line.split()
                x = float(splitted[1])
                y = float(splitted[2])
                z = float(splitted[3])
                coord = np.append(coord, [[x, y, z]], axis=0)
    return name, coord
