#!/usr/bin/env python3
# This script can extract scan trajectories and energies from a QChem out put file

import os
import json

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
    atoms = []
    coords = []
    comments = []
    value = []
    energy = []

    temp_coord = []
 
    atoms_filled = False
    converged = False
    geoms = False
    f = open(filename, 'r')
    for i in f:
        if "OPTIMIZATION CONVERGED" in i:
            converged = True
        if converged:
            splited = i.split()
            if splited and splited[0].isdigit():
                geoms = True
            if geoms:
                if splited:
                    atom, x, y, z = splited[1], splited[2], splited[3], splited[4]                
                    temp_coord.append([float(x),float(y),float(z)])
                    if not atoms_filled:
                        atoms.append(atom)
                if not splited:
                    coords.append(temp_coord)
                    temp_coord = []
                    atoms_filled = True
                    geoms = False
                    converged = False

        if 'PES scan, value:' in i:
            splited = i.split()
            value.append(splited[splited.index('value:') + 1])
            energy.append(splited[splited.index('energy:') + 1])            
            comments.append([i])

    return atoms, coords, comments, value, energy

if __name__ == '__main__':
    atoms, coords, comments, value, energy = extract('qchem.out')
    write_xyz(atoms, coords, comments)
    json_dict = {'value': value, 'energy':energy}
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)
    
    

