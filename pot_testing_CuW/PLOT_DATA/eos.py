import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib
matplotlib.use('Agg')

eV_to_Ry=1/13.60569301
Ry_to_eV= 13.60569301

eos_Cu_DFT = pd.read_csv("../REF_DATA/eos_mlip_Cu_DFT.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_Cu3W_DFT = pd.read_csv("../REF_DATA/eos_mlip_Cu3W_DFT.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_CuW_DFT = pd.read_csv("../REF_DATA/eos_mlip_CuW_DFT.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_CuW3_DFT = pd.read_csv("../REF_DATA/eos_mlip_CuW3_DFT.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_W_DFT = pd.read_csv("../REF_DATA/eos_mlip_W_DFT.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])

eos_Cu_ace = pd.read_csv("./eos_mlip_Cu.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_Cu3W_ace = pd.read_csv("./eos_mlip_Cu3W.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_CuW_ace = pd.read_csv("./eos_mlip_CuW.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_CuW3_ace = pd.read_csv("./eos_mlip_CuW3.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_W_ace = pd.read_csv("./eos_mlip_W.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])

min_Cu_DFT=min(eos_Cu_DFT["energy"])
min_W_DFT=min(eos_W_DFT["energy"])
min_Cu_ace=min(eos_Cu_ace["energy"])
min_W_ace=min(eos_W_ace["energy"])

eos_Cu_DFT["energy"] = (eos_Cu_DFT["energy"] - min_Cu_DFT)
eos_W_DFT["energy"] = (eos_W_DFT["energy"] - min_W_DFT)
eos_Cu_ace["energy"] = (eos_Cu_ace["energy"] - min_Cu_ace)
eos_W_ace["energy"] = (eos_W_ace["energy"] - min_W_ace)

eos_Cu3W_DFT["energy"] = (eos_Cu3W_DFT["energy"] - min_Cu_DFT * 3/4 - min_W_DFT * 1/4)
eos_CuW_DFT["energy"] = (eos_CuW_DFT["energy"] - min_Cu_DFT * 1/2 - min_W_DFT * 1/2)
eos_CuW3_DFT["energy"] = (eos_CuW3_DFT["energy"] - min_Cu_DFT * 1/4 - min_W_DFT * 3/4)

eos_Cu3W_ace["energy"] = (eos_Cu3W_ace["energy"] - min_Cu_ace * 3/4 - min_W_ace * 1/4)
eos_CuW_ace["energy"] = (eos_CuW_ace["energy"] - min_Cu_ace * 1/2 - min_W_ace * 1/2)
eos_CuW3_ace["energy"] = (eos_CuW3_ace["energy"] - min_Cu_ace * 1/4 - min_W_ace * 3/4)


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,7))
plt.rcParams['font.size'] = '20'
ax.grid(c='gainsboro',ls='--',lw=0.7)

colormap = plt.get_cmap('tab20c')
colors   = colormap(np.linspace(0.3, 0.6, 5))


# plot EV curve
ax.set_title('Energy volume curve',fontsize=20)

ax.scatter(eos_Cu_DFT["volume"], eos_Cu_DFT["energy"],  s=300, marker='o', color = colors[0], edgecolors='k', linewidths=2, alpha=1)
ax.scatter(eos_Cu3W_DFT["volume"], eos_Cu3W_DFT["energy"],  s=400, marker='p', color = colors[1], edgecolors='k', linewidths=2, alpha=1)
ax.scatter(eos_CuW_DFT["volume"], eos_CuW_DFT["energy"],  s=300, marker='D', color = colors[2], edgecolors='k', linewidths=2, alpha=1)
ax.scatter(eos_CuW3_DFT["volume"], eos_CuW3_DFT["energy"],  s=300, marker='v', color = colors[3], edgecolors='k', linewidths=2, alpha=1)
ax.scatter(eos_W_DFT["volume"], eos_W_DFT["energy"],  s=300, marker='s', color = colors[4], edgecolors='k', linewidths=2, alpha=1)

ax.plot(eos_Cu_ace["volume"], eos_Cu_ace["energy"],lw=2.5, color = colors[0], alpha=1, label="Cu")
ax.plot(eos_Cu3W_ace["volume"], eos_Cu3W_ace["energy"],lw=2.5, color = colors[1], alpha=1, label="Cu3W")
ax.plot(eos_CuW_ace["volume"], eos_CuW_ace["energy"],lw=2.5, color = colors[2], alpha=1, label="CuW")
ax.plot(eos_CuW3_ace["volume"], eos_CuW3_ace["energy"],lw=2.5, color = colors[3], alpha=1, label="CuW3")
ax.plot(eos_W_ace["volume"], eos_W_ace["energy"],lw=2.5, color = colors[4], alpha=1, label="W")


ax.set_xlabel('Volume, [$\AA^3$]',fontsize='20')
ax.set_ylabel('Energy, [eV]',fontsize='20')
ax.legend(loc='best',fontsize=20,markerscale=1.5, ncol=2)


for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontsize(20)
ax.set_xlim(10, 20)
ax.set_ylim(-0.1, 2.1)

fig.savefig('eos.png',dpi=300)
