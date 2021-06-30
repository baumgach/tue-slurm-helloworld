#!/bin/bash
#SBATCH --ntasks=1                # Number of tasks (see below)
#SBATCH --cpus-per-task=1         # Number of CPU cores per task
#SBATCH --nodes=1                 # Ensure that all cores are on one machine
#SBATCH --time=0-00:05            # Runtime in D-HH:MM
#SBATCH --partition=gpu-2080ti-dev # Partition to submit to
#SBATCH --gres=gpu:1              # optionally type and number of gpus
#SBATCH --mem=50G                 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH --output=logs/hostname_%j.out  # File to which STDOUT will be written
#SBATCH --error=logs/hostname_%j.err   # File to which STDERR will be written
#SBATCH --mail-type=FAIL           # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=<your-email>  # Email to which notifications will be sent

# print info about current job
scontrol show job $SLURM_JOB_ID 

# insert your commands here. these will be executed on the compute node allocated for the job (not on the slurm headnode!)

conda activate myenv

python python_example.py.py

echo "My job is done."

