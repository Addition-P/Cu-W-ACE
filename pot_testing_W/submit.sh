#!/bin/bash
#------------------------------
# This is a main/controlling code written in SHELL.
# Please read through README.md file carefully before using the script.
#------------------------------
#SBATCH --job-name=IAP_test
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00:00
#SBATCH --error=slurm-%j.stderr
#SBATCH --output=slurm-%j.stdout
#SBATCH --mail-type=ALL
#SBATCH --mail-user=3122106004@stu.xjtu.edu.cn

# clear space (remove dump files from last run if they exist)
rm results.txt
rm potential.in
#**********************************
# Customize section
#**********************************

# Full path to LAMMPS excutable. 
LMMP="/home/jiahaopan/Software/lammps-28Mar2023/bin/lmp_mpi"
# Default hyperthreading number (if not spectified)
Ncores=15
# Choose interatomic potential
pot="ace"
# input the potential file name
potfilename=`ls ../potential`
if [[ ${pot} = "ace" ]]; then
	pstyle="pace"
	pcoeff="../../potential/${potfilename} W"
elif [[ ${pot} = "eam" ]]; then
	pstyle="eam"
	pcoeff="../../potential/${potfilename}"
elif [[ ${pot} = "eam/alloy" ]]; then
	pstyle="eam/alloy"
	pcoeff="../../potential/${potfilename} W"
elif [[ ${pot} = "eam/fs" ]]; then
	pstyle="eam/fs"
	pcoeff="../../potential/${potfilename} W"
fi

# Generate the interatomic potential file
cat >./potential.in <<EOF
# Define the interatomic potential
pair_style ${pstyle}
pair_coeff * * ${pcoeff} 
EOF
# create a data folder
mkdir ${potfilename}

#**********************************
# Get the information 
#**********************************
## locate the folder and grep the folder name
# Grep the potential version and echo to results file
echo '#**********************************' | tee -a  ./results.txt
awk '/^pair_style*/' ./potential.in | tee -a ./results.txt
awk '/^pair_coeff*/' ./potential.in | tee -a ./results.txt
echo '#**********************************' | tee -a ./results.txt

#**********************************
# Calculation section
#**********************************
# E-V curve 
cd ENERGYVOLUME
rm *.csv
rm *.dat
rm log.*
rm *.log
mpirun -np 4 ${LMMP} -in in.eos
# fit EOS
python eos-fit.py
cp volume.dat ../PLOT_DATA/eos_mlip.csv
# Get lattice parameter
a0=$(grep 'a0 =' ../results.txt | awk '{print $3}')

# Get relaxed structure
cd ../RELAX
mpirun -n 4 lmp_mpi -in in.relax -v lat ${a0}

# Phonon
cd ../PHONON
cp ../RELAX/relax_W.data .
phonopy --lammps -c relax_W.data -d --dim 1 1 1
phonopy --symmetry
phonopy --lammps -c Punitcell -d --dim 4 4 4
mpirun -n 4 lmp_mpi -in in.phonopy
phonopy -f force
phonopy -p mesh.conf --full-fc
phonopy -p band.conf
phonopy-bandplot --gnuplot > phononband.csv
mv phononband.csv ../PLOT_DATA/phononband.csv

# Vacancy formation energy
cd ../VACANCY
rm log.*
rm *.log
mpirun -n 14 ${LMMP} -in in.vac -v lat ${a0}

# Calculation of elastic constants.--------------------------------
cd ../ELASTIC
rm log.*
rm *.log
rm restart.equil
mpirun -n 14  ${LMMP} -in in.elastic -v lat ${a0}

# Calculation of surface energies.---------------------------------
cd ../SURFACEENERGY
rm dump*
rm log*
rm *.log
# (100) plane
mpirun -n 14  ${LMMP} -in in.surf1 -v lat ${a0}
# (110) plane
mpirun -n 14  ${LMMP} -in in.surf2 -v lat ${a0}
# (111) plane
mpirun -n 14  ${LMMP} -in in.surf3 -v lat ${a0}
# (112) plane
mpirun -n 14  ${LMMP} -in in.surf4 -v lat ${a0}

# Calculation of melting point.-----------------------------------
cd ../MELTINGPOINT
rm *.csv
rm *.data
mpirun -n 14  ${LMMP} -in in.melting_TPS_data -v lat ${a0}
for i in $(seq 12 22)
 do
    mpirun -n 14  ${LMMP} -in in.melting -v epoch ${i}
done
cp ./melting_point.csv ../PLOT_DATA/melting_point.csv

# Stacking fault energy---------------------------------------------
cd ../SFE
rm sfe*
rm log*
rm *log
# W <111>(112)
mpirun -np 15 ${LMMP} -in in.sfe_112 -v lat ${a0}
# W <111>(110)
mpirun -np 15 ${LMMP} -in in.sfe_110 -v lat ${a0}
cp ./sfe_112.csv ../PLOT_DATA/sfe_112.csv
cp ./sfe_110.csv ../PLOT_DATA/sfe_110.csv

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
python sfe.py
python melting_point.py
python basic_pro.py
python plot_phonon.py
cp *.png ../${potfilename}

echo "Finish plotting results!"

# Copy all the dump file to final
cd ..
cp results.txt ${potfilename}
cp ./PLOT_DATA/*.csv ${potfilename}


