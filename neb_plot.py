#!/usr/bin/env python3
# Visualization script for NEB code
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


plt.rcParams.update({'font.size':20 })


def parse_arr(line):
    """get the values from a single line of output into an array"""
    output = line.strip().split(':')[1]
    values = [float(x) for x in output.split()]
    return values

def parse_data(filename):
    """get the data from the output file into nested lists"""
    spacing = []
    energies = []
    gradients = []

    with open (filename) as f:
        for line in f.readlines():
            if line.startswith("Spacing (Ang)") and "Old" not in line:
                spacing.append(parse_arr(line))
            elif line.startswith("Energies  (kcal/mol)"):
                energies.append(parse_arr(line))
            elif line.startswith("Gradients (eV/Ang)"):
                gradients.append(parse_arr(line))

    return spacing, energies, gradients

def plot_data(spacing, energies, gradients, gradient = False, name='plot'):
    """generate the energy and gradient plot from the output data"""
    if gradient:
        fig, ax = plt.subplots(nrows=2, sharex=True)
    else:
        fig, ax = plt.subplots(figsize = (15,8), sharex=True)

    N = len(spacing)
    even = np.linspace(0, 1, int(N))
    
    color = [cm.rainbow(val**(1/2)) for val in even]
    width = np.linspace(0.5, 3, int(N))#[::-1]

    max_e = np.argmax(energies[-1])
    final_TS = energies[-1][max_e]
    TS_location = 0

    for i in range(max_e-1):
        TS_location += spacing[-1][i]

    for i in range(N):
        x_coor = [0]
        for val in spacing[i]:
            x_coor.append(x_coor[-1] + val)
        x_coor = np.array(x_coor) - (x_coor[max_e]-TS_location)
        if i == 0:
            if gradient:
                ax[0].plot(x_coor, energies[i], marker = "o", color = color[i], linewidth = width[i], label = "Initial Chain")
                ax[1].plot(x_coor, gradients[i], marker = "o", color = color[i], linewidth = width[i])
            else:
                ax.plot(x_coor, energies[i], marker = "o", color = color[i], linewidth = width[i], label = "Initial Chain", alpha = 0.5)
        elif i == int(N-1):
            
            if gradient:
                ax[0].plot(x_coor, energies[i], marker = "o", color = color[i], linewidth = width[i], label = "Final Chain (%i)" %i)   
                ax[1].plot(x_coor, gradients[i], marker = "o", color = color[i], linewidth = width[i])
            else:
                ax.plot(x_coor, energies[i], marker = "o", markersize = 10,color = color[i], linewidth = width[i], label = "Final Chain (%i)" %i)
            if x_coor[max_e] < x_coor[-1]/2:
                txt_coord = (0.3, 0.95)
                txt = 1
            else:
                txt_coord = (1, 0.95)
                txt = 2
            if gradient:
                ax[0].annotate(str(np.round(final_TS,1))+"kcal/mol", xy=(x_coor[max_e], final_TS),  xycoords='data',
            xytext=txt_coord, textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.02, width = 1, headwidth = 5),
            horizontalalignment='right', verticalalignment='top',
            )
            else:
                ax.annotate("Ea="+str(np.round(final_TS - energies[-1][0],1))+"kcal/mol", xy=(x_coor[max_e], final_TS),  xycoords='data',
            xytext=txt_coord, textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.02, width = 1, headwidth = 5),
            horizontalalignment='right', verticalalignment='top',
            fontsize = 30)
        elif i%int(N/5)== 0: 
            if gradient:
                ax[0].plot(x_coor, energies[i], marker = "o", color = color[i], linewidth = width[i])
                ax[1].plot(x_coor, gradients[i], marker = "o", color = color[i], linewidth = width[i])
            else:
                ax.plot(x_coor, energies[i], marker = "o", color = color[i], linewidth = width[i], alpha = 0.5)
                

    if gradient: 
        ax[0].set_ylabel("Energy (kcal/mol)")
        ax[1].set_ylabel("Gradient (eV/Ang)")
    else:
        ax.set_ylabel("Energy (kcal/mol)", fontsize = 35)
    
    #plt.suptitle(f"Energy and Gradient of {MOLECULE} from NEB calculation")
    plt.xlabel("Spacing (Ang)", fontsize = 35)
    ax.legend(loc = txt, fontsize = 30)
    ax.tick_params(axis='x', labelsize = 25)
    ax.tick_params(axis='y', labelsize = 25)
    plt.subplots_adjust(bottom=0.15, left = 0.1, right = 0.95, top=0.95)
    plt.savefig("%s.png" %name)
    plt.show()

def main():
    FILE = sys.argv[1:] 
    fname = FILE[0].split('.')[0]
    spacing, energies, gradients = parse_data(FILE[0]) 
    plot_data(spacing, energies, gradients, False, fname)

    with open('%s.txt' %fname,'w') as f:
        f.write('Iteration : ' + str(len(spacing))+'\n')
        E_num = 1
        f.write('Energies (kcal/mol)\n')
        for i in energies:
            f.write("E%i : " %E_num + str(i).replace('[','').replace(']','') + "\n")
            E_num +=1
        G_num = 1
        f.write('\nGradients (eV/Ang)\n')
        for i in gradients:
            f.write("G%i : "%G_num + str(i).replace('[','').replace(']','')+ "\n")
            G_num += 1
        S_num = 1
        f.write('\nSpacing (Ang)\n')
        for i in spacing:
            f.write("S%i : "%S_num + str(i).replace('[','').replace(']','') + "\n")
            S_num += 1

if __name__ == "__main__":
    main()
