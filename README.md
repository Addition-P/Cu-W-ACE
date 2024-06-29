# Program for testing Cu-W ACE potential by using LAMMPS
### DATE: 29 June 2024
### AUTHOR: jiahaopan@stu.xjtu.edu.cn and lei.zhang@rug.nl 

## The testing properties include:
### **UNARY**
- E-V curve
- Elastic constants
- Vacancy
- Phonon spectrum
- Surface energies
- Stacking fault (curves)
- Melting point

### **BINARY**
- E-V curve
- Convex hull
- Work of separation (KS and NW)
## The required inputs are:
1. Interatomic potential: to be changed in potential folder
2. Required cores and wall time on the cluster
3. Email address
## Additional requirements on system:
- The molecular statics/dynamics is running with a parallel version of LAMMPS.
1. The ML-PACE package needs to be installed in LAMMPS.
- The phonon spectrum is running with PHONONPY.