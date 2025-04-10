with open("interaction_extraite_gavin2006.txt", 'r') as file:
    lines = []
    line = file.readline()
    while line:
        line = line.strip('\n')
        line = line.split('\t')
        lines.append(line)
        line = file.readline()
