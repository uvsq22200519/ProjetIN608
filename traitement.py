"""with open("interaction_data.txt", 'r') as file:
    with open("interaction_extraite_2017.txt", 'w') as nv_file:
        ligne = file.readline()
        while ligne:
            if 'physical interactions' in ligne and 'genetic interactions' not in ligne:
                ligne = ligne.split("\t")
                nv_file.write(ligne[0] + '\t' + ligne[2] + '\n')
            ligne = file.readline()

with open("S000114310_physical_interactions.txt", 'r') as file1:
    with open("interaction_extraite_gavin2006.txt", 'w') as nv_file1:
        file1.readline()
        ligne = file1.readline()
        print(type(ligne))
        while ligne:
            ligne = ligne.split("\t")
            nv_file1.write(ligne[1] + '\t' + ligne[3] + '\n')
            ligne = file1.readline()

#supperssion doublons dans le fichier interaction_extraite_2006.txt
with open('interaction_extraite_gavin2006.txt', 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    lines = list(set(lines))
with open('interaction_extraite_gavin2006.txt', 'w') as file:
    for line in lines:
        file.write(line + '\n')

with open('interaction_extraite_2017.txt', 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    lines = list(set(lines))
with open('interaction_extraite_2017.txt', 'w') as file:
    for line in lines:
        file.write(line + '\n')
"""

def get_cyc2008() -> dict:
    """
    Get the CYCling 2008 dataset
    :return: The CYCling 2008 dataset
    """
    cyc2008 = {}
    with open("CYC2008.txt", 'r') as file:
        file.readline()
        ligne = file.readline()
        while ligne:
            ligne = ligne.split("\t")
            if ligne[2].replace('\n', '') not in cyc2008:
                cyc2008[ligne[2].replace('\n', '')] = []
            cyc2008[ligne[2].replace('\n', '')].append(ligne[0])
            ligne = file.readline()
    return cyc2008
