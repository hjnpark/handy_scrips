#!/usr/bin/env python3
import numpy as np
import os
import json
import matplotlib.pyplot as plt 

def write_xyz(atom, coords, comments):
    if os.path.exists('./trajectory.xyz'):
        os.remove('./trajectory.xyz')
    na = len(atom)
    with open('trajectory.xyz','a') as f:
        for coord, comm in zip(coords, comments):
            f.write(f"{na}\n")
            f.write(comm[0])
            for i in range(len(coord)):
                f.write(f"{atom[i]} {coord[i][0]: 16.10f}{coord[i][1]: 16.10f}{coord[i][2]: 16.10f} \n")


def extract(filename):
    energy = []
    atoms = []
    comments = []
    atoms_filled = False
    coords = []

    temp_coord = []
    geometry = False    

    f = open(filename, 'r')
    for i in f:
        splited = i.split()        
        if splited:
            if "Coordinates (Angstroms)" in i or geometry:
                geometry = True
                if splited[0].isdigit():
                    atom, x, y, z = splited[1], splited[2], splited[3], splited[4]
                    temp_coord.append([float(x), float(y), float(z)])
                    if not atoms_filled:
                        atoms.append(atom)
                if splited[0] == "Point":
                    geometry = False
                    atoms_filled = True        
                    coords.append(temp_coord)
                    temp_coord = []
                
            if "Energy is" in i:
                comments.append([i])
                energy.append(float(splited[-1]))

            if "Final energy is" in i:
                comments.append([i])
                energy.append(float(splited[-1]))
                break

                
    return energy, atoms, comments, coords

if __name__ == '__main__':
    energy, atoms, comments, coords = extract('qchem.out')
    write_xyz(atoms, coords, comments)
    json_dict = {"Energies":energy}
    with open("energies.json","w", encoding ="utf-8") as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)

    E = np.array(energy) * 2625.5
    E -= E[0]
    plt.plot(E,'.')
    plt.xlabel("Optimization Iteration")
    plt.ylabel("Energy (kJ/mol)")
    plt.show()
    
    
    

