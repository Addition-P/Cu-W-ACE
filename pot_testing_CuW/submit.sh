#!/bin/bash
#------------------------------
# This is a main/controlling code written in SHELL.
# Please read through README.md file carefully before using the script.
# DATE: 28 June 2024
# AUTHORS: 3122106004@stu.xjtu.edu.cn and lei.zhang@rug.nl
#-------------------------------
#SBATCH --job-name=CuW_ACE_test
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00:00
#SBATCH --error=slurm-%j.stderr
#SBATCH --output=slurm-%j.stdout
#SBATCH --mail-type=ALL
#SBATCH --mail-user=3122106004@stu.xjtu.edu.cn

# clear space (remove dump files from last run if they exist)
rm results.txt
rm potential*.in
#**********************************
# Customize section
#**********************************

# load the dependent modules of the cluster.

# Full path to LAMMPS excutable. 
LMMP="/home/jiahaopan/Software/lammps-28Mar2023/bin/lmp_mpi"
# Default hyperthreading number (if not spectified)
Ncores=15
# Choose interatomic potential
pot="ace"
# input the potential file name
potfilename=`ls ../potential`

# For ACE, one need to define the right coeff
if [[ ${pot} = "ace" ]]; then
	pstyle="pace"
	pcoeff="../../potential/${potfilename}"
elif [[ ${pot} = "eam" ]]; then
	pstyle="eam"
	pcoeff="../../potential/${potfilename}"
elif [[ ${pot} = "eam/alloy" ]]; then
	pstyle="eam/alloy"
	pcoeff="../../potential/${potfilename}"
elif [[ ${pot} = "eam/fs" ]]; then
	pstyle="eam/fs"
	pcoeff="../../potential/${potfilename}"
fi

# Generate the interatomic potential file
cat >./potential_Cu.in <<EOF
# Define the interatomic potential
pair_style ${pstyle}
pair_coeff * * ${pcoeff} Cu
EOF

cat >./potential_W.in <<EOF
# Define the interatomic potential
pair_style ${pstyle}
pair_coeff * * ${pcoeff} W
EOF

cat >./potential_CuW.in <<EOF
# Define the interatomic potential
pair_style ${pstyle}
pair_coeff * * ${pcoeff} Cu W
EOF

cat >./potential_WCu.in <<EOF
# Define the interatomic potential
pair_style ${pstyle}
pair_coeff * * ${pcoeff} W Cu
EOF

# create a data folder
mkdir ${potfilename}

#**********************************
# Get the information 
#**********************************
## locate the folder and grep the folder name
fullpath=${PWD}
potential_name=`echo $(basename $fullpath)`
# Grep the potential version and echo to results file
echo '#**********************************' | tee -a  ./results.txt

#**********************************
# Calculation section
#**********************************
## E-V curve and fit EOS
cd ENERGYVOLUME
rm *.csv
rm *.dat
rm log.*
rm *.log

# fit EOS
# Cu lattice parameters
mpirun -np 15 ${LMMP} -in in.eos_Cu
echo '#-----------Cu---------------------' | tee -a  ../results.txt
python eos-fit_fcc.py
mv volume_fcc.dat ../PLOT_DATA/eos_mlip_Cu.csv

# Get lattice parameter
a0_Cu=$(grep 'a0_Cu =' ../results.txt | awk '{print $3}')

# W lattice parameters
mpirun -np 15 ${LMMP} -in in.eos_W
echo '#-----------W---------------------' | tee -a  ../results.txt
python eos-fit_bcc.py
mv volume_bcc.dat ../PLOT_DATA/eos_mlip_W.csv
# Get lattice parameter
a0_W=$(grep 'a0_W =' ../results.txt | awk '{print $3}')

# Cu3W lattice parameters
mpirun -np 15 ${LMMP} -in in.eos_Cu3W
echo '#-----------Cu3W---------------------' | tee -a  ../results.txt
python eos-fit_fcc.py
mv volume_fcc.dat ../PLOT_DATA/eos_mlip_Cu3W.csv

# CuW3 lattice parameters
mpirun -np 15 ${LMMP} -in in.eos_CuW3
echo '#-----------CuW3---------------------' | tee -a  ../results.txt
python eos-fit_fcc.py
mv volume_fcc.dat ../PLOT_DATA/eos_mlip_CuW3.csv

# CuW lattice parameters
mpirun -np 15 ${LMMP} -in in.eos_CuW
echo '#-----------CuW---------------------' | tee -a  ../results.txt
python eos-fit_bcc.py
mv volume_bcc.dat ../PLOT_DATA/eos_mlip_CuW.csv

## Calculation of convex hull
cd ../CONVEXHULL
rm *.dat
mpirun -np 3 ${LMMP} -in in.eos_bcc
mpirun -np 3 ${LMMP} -in in.eos_fcc


### Calculation of interface energy
cd ../INTERFACEENERGY
rm interface*

# get interface of CuW using atomsk
## creat Cu(111)W(110)--KS
atomsk --create fcc 3.727 Cu orient [11-2] [1-10] [111] -duplicate 5 1 2 interface_CuW_111_110_KS_Cu.cif
atomsk --create bcc 3.106 W orient [1-12] [-111] [110] -duplicate 3 1 3 interface_CuW_111_110_KS_W.cif
atomsk --merge z 2 interface_CuW_111_110_KS_W.cif interface_CuW_111_110_KS_Cu.cif interface_CuW_111_110_KS.lmp

## creat Cu(111)W(110)--NW
atomsk --create fcc 3.503 Cu orient [11-2] [1-10] [111] -duplicate 1 4 2 interface_CuW_111_110_NW_Cu.cif
atomsk --create bcc 3.303 W orient [-110] [00-1] [110] -duplicate 1 3 3  interface_CuW_111_110_NW_W.cif
atomsk --merge z 2 interface_CuW_111_110_NW_W.cif interface_CuW_111_110_NW_Cu.cif interface_CuW_111_110_NW.lmp

# work of adhesion calculation --CuW
mpirun -n 10  lmp_mpi -in in.interface_CuW_111_110_KS
mpirun -n 10  lmp_mpi -in in.interface_CuW_111_110_NW

#
mv *.csv ../PLOT_DATA/
#
# return the main interface
cd ..
#**********************************
# Plotting section
#**********************************
# Execute python script to do the plots.py------------------------------
# Plot E-V curve & stacking fault energy & melting point
cd PLOT_DATA
rm *.png
python eos.py
python inter_e.py
cp *.png ../${potfilename}

echo "Finish plotting results!"

# Copy all the dump file to final
cd ..
cp results.txt ${potfilename}
cp ./PLOT_DATA/*.csv ${potfilename}



