with open("interaction_data.txt", 'r') as file:
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
