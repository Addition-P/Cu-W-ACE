import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Read the data for melting point
melting_eam = pd.read_csv("../REF_DATA/melting_point_EAM.csv", delimiter=" ", decimal=".", header=0, names=["temp", "Density"])
melting_ace = pd.read_csv("./melting_point.csv", delimiter=" ", decimal=".", header=0, names=["temp", "Density"])

# plot data
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,8))
plt.rcParams['font.size'] = '20'

# Plot for Cu melting point.
ax.grid(c='gainsboro',ls='--',lw=0.7)
ax.set_title('Cu melting point',fontsize=20)

ax.scatter(melting_eam["temp"], melting_eam["Density"], s=60, marker='v', c='blue', label='EAM')
ax.scatter(melting_ace["temp"], melting_ace["Density"], s=60, marker='o', c='orange', label='ACE')
#ax.plot(melting_ace["temp"], melting_ace["Density"], c='blue',lw=2,ls='--')

ax.set_xlim([1100, 1500])
ax.set_xlabel('Temperature, K', fontsize=20)
ax.set_ylabel('Density, [g/cm$^3$])', fontsize=20)
ax.legend(loc='upper right',fontsize=20)

#plt.show()
fig.savefig('melting point.png',dpi=300)
