def file_reading(filename, database):
    filepath = "deviation/" + filename + ".dev"
    coord_list = []
    with open(filepath, mode='r') as f:
        for i in range(12):
            line = f.readline()
            if i == 1:
                name = line.split()[len(line.split()) - 1]
        while 1:
            line = f.readline()
            if line == "":
                break
            coord = [float(x) for x in line.split()]
            coord_list.append(coord)
        database[name] = database.get(name, coord_list)

database = {}
while 1:
    filename = input()
    if filename == '.':
        break
    file_reading(filename, database)
for name in database:
    print(name, database[name])