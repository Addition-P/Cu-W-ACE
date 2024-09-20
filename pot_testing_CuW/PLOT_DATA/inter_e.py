from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.family'] = ['SimSun', 'Times New Roman']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.figsize'] = (5,3)


int_CuW_111_110_KS_EAM = pd.read_csv("../REF_DATA/interface_CuW_111_110_KS_EAM.csv",delimiter=" ",decimal=".",header=0,names=["index", "energyeV", "energyJ"])
int_CuW_111_110_NW_EAM = pd.read_csv("../REF_DATA/interface_CuW_111_110_NW_EAM.csv",delimiter=" ",decimal=".",header=0,names=["index", "energyeV", "energyJ"])

int_CuW_111_110_KS_ace = pd.read_csv("./interface_CuW_111_110_KS.csv",delimiter=" ",decimal=".",header=0,names=["index", "energyeV", "energyJ"])
int_CuW_111_110_NW_ace = pd.read_csv("./interface_CuW_111_110_NW.csv",delimiter=" ",decimal=".",header=0,names=["index", "energyeV", "energyJ"])



max_int_CuW_111_110_KS_EAM = -min(int_CuW_111_110_KS_EAM["energyJ"] - int_CuW_111_110_KS_EAM["energyJ"].values[-1])
max_int_CuW_111_110_NW_EAM = -min(int_CuW_111_110_NW_EAM["energyJ"] - int_CuW_111_110_NW_EAM["energyJ"].values[-1])

max_int_CuW_111_110_KS_ace = -min(int_CuW_111_110_KS_ace["energyJ"] - int_CuW_111_110_KS_ace["energyJ"].values[-1])
max_int_CuW_111_110_NW_ace = -min(int_CuW_111_110_NW_ace["energyJ"] - int_CuW_111_110_NW_ace["energyJ"].values[-1])



interface_index = ['Cu(111)W(110)_KS', 'Cu(111)W(110)_NW']
interface_energy_EAM = [max_int_CuW_111_110_KS_EAM, max_int_CuW_111_110_NW_EAM]
interface_energy_ace = [ max_int_CuW_111_110_KS_ace, max_int_CuW_111_110_NW_ace]
interface_energy_DFT = ['3.11', '2.983787886']

x = np.arange(len(interface_index))

width = 0.25
index_x_eam = x
index_x_ace = x + width
index_x_DFT = x + width * 2

plt.bar(index_x_eam,interface_energy_EAM,width=width,color="gold",label="EAM", zorder = 100)
plt.bar(index_x_ace,interface_energy_ace,width=width,color="silver",label="ACE", zorder = 100)
plt.bar(index_x_DFT, [float(x) for x in interface_energy_DFT], width=width, color="red", label="DFT", zorder = 100)

plt.xticks(x + width,labels=interface_index, fontsize=10, rotation=0)

for i in range(len(interface_index)):
    plt.text(index_x_eam[i],interface_energy_EAM[i], f'{interface_energy_EAM[i]:.2f}', va="bottom", ha="center", fontsize=8)
    plt.text(index_x_ace[i],interface_energy_ace[i], f'{interface_energy_ace[i]:.2f}', va="bottom", ha="center", fontsize=8)
    plt.text(index_x_DFT[i], float(interface_energy_DFT[i]), f'{float(interface_energy_DFT[i]):.2f}', va="bottom", ha="center", fontsize=8)

plt.ylabel('Work of Separation (J/m$^2$)')
plt.grid(True, lw = 1, ls = '--', c = '.85', zorder = 0)
plt.ylim(0, 5)

plt.legend(loc="upper right", ncol=3)
plt.savefig('interface_energy.png',dpi=300)
