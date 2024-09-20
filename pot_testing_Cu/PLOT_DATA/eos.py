import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib
matplotlib.use('Agg')

eV_to_Ry=1/13.60569301
Ry_to_eV= 13.60569301

# Read the data
eos_eam = pd.read_csv("../REF_DATA/eos_mlip_EAM.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])
eos_ace = pd.read_csv("./eos_mlip.csv",delimiter=" ",decimal=".",header=None,names=["volume","energy"])

min_eam=min(eos_eam["energy"])
min_ace=min(eos_ace["energy"])

eos_eam["energy"] = (eos_eam["energy"] -min(eos_eam["energy"])) * 1000
eos_ace["energy"] = (eos_ace["energy"] -min(eos_ace["energy"])) * 1000


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,7))
plt.rcParams['font.size'] = '20'
ax.grid(c='gainsboro',ls='--',lw=0.7)


# plot EV curve
ax.set_title('Energy volume curve',fontsize=20)

ax.scatter(eos_eam["volume"], eos_eam["energy"],  s=20, marker='o', c = 'dodgerblue', alpha=1,label='EAM')
ax.scatter(eos_ace["volume"], eos_ace["energy"],  s=40, marker='s', c = 'red', alpha=1,label='ACE')

# ax.plot(eos_ace["volume"], eos_ace["energy"],lw=1.5,alpha=1)

ax.set_xlabel('Volume, [$\AA^3$]',fontsize='20')
ax.set_ylabel('Energy, [meV]',fontsize='20')
ax.legend(loc='upper center',fontsize=20,markerscale=1.5)


for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontsize(20)

fig.savefig('eos.png',dpi=300)
