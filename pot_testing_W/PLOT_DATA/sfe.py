import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Read the data for <112>{111} stacking fault energy.
# Read the data for <110>{111} stacking fault energy.

sfe_112_ace = pd.read_csv("./sfe_112.csv",delimiter=" ", decimal=".", header=0, names=["dis", "energyeV", "energyJ"])
sfe_110_ace = pd.read_csv("./sfe_110.csv", delimiter=" ", decimal=".", header=0, names=["dis", "energyeV", "energyJ"])

# plot data
fig, (ax, bx) = plt.subplots(nrows=1, ncols=2, figsize=(15,8))
plt.rcParams['font.size'] = '20'

# Plot for <112>{111}.
ax.grid(c='gainsboro',ls='--',lw=0.7)
ax.set_title('<112>{111}',fontsize=20)

ax.scatter(sfe_112_ace["dis"], sfe_112_ace["energyJ"], s=60, marker='o', c='orange', label='ACE')
ax.plot(sfe_112_ace["dis"], sfe_112_ace["energyJ"], c='blue',lw=2,ls='--')

ax.set_xlim([0,4.43])
ax.set_xlabel('Displacements, [$\AA$]', fontsize=20)
ax.set_ylabel('Stacking Fault Energy, [J/m$^2$])', fontsize=20)
ax.legend(loc='upper right',fontsize=20)

# Plot for <110>{111}.
bx.grid(c='gainsboro',ls='--',lw=0.7)
bx.set_title('<110>{111}',fontsize=20)

bx.scatter(sfe_110_ace["dis"], sfe_110_ace["energyJ"], s=60, marker='o', c='orange', label='ACE')
bx.plot(sfe_110_ace["dis"], sfe_110_ace["energyJ"], c='blue',lw=2,ls='--')

bx.set_xlim([0,2.505])
bx.set_xlabel('Displacements, [$\AA$]', fontsize=20)
bx.set_ylabel('Stacking Fault Energy, [J/m$^2$])', fontsize=20)
bx.legend(loc='upper right',fontsize=20)

#plt.show()
fig.savefig('sfe.png',dpi=300)
