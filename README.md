# Tübingen ML Cloud Hello World Example(s)

The goal of this repository is to give an easy entry point to people who want to use the [Tübingen ML Cloud](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/home), and in particular [Slurm](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#common-slurm-commands), to run Python code on GPUs.

Specifically, this tutorial contains a small Python code sample for multiplying two matrices using PyTorch and instructions for setting up the required environments and executing this code on CPU or GPU on the ML Cloud. 

The tutorial consists of a minimal example for getting started quickly, and a number of slightly more detailed instructions explaining different workflows and aspects of the ML Cloud. 

**This is not an official introduction**, but rather a tutorial put together by the members of the [Machine Learning in Medical Image Analysis (MLMIA) lab](www.mlmia-unitue.de). The official ML Cloud Slurm wiki can be found [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#common-slurm-commands). If you do spot mistakes or have suggestions, comments and pull requests are very welcome.  

## Contents

Contents of this tutorial:
  * [Who is this for?](#who-is-this-for): Short description of target audience
  * [Minimal example](#minimal-example): The shortest path from getting an account to running the `multiply.py` code on GPU. 

In-depth instructions:
  * [Initial Setup](/instructions/initial-setup.md): Some useful tricks for setting up your SSH connections and mounting Slurm volumes locally for working more efficiently. 
  * [Virtual environment workflow](/instructions/virtual-env-workflow.md): A more in detailed explanation of the workflow based on virtual environments also used in the minimal example. 
  * [Singularity workflow](/instructions/singularity-workflow.md): An alternative workflow using Singularity containers, which allows for more flexibility.
  * [Running parallel jobs](/instructions/parallel-jobs.md): A short introduction to executing a command for a list of parameters in parallel on multiple GPUs. 
  * [Interactive Jobs and Debugging](/instructions/interactive-jobs.md): How to run interactive jobs and how to debug Python code on Slurm. 
  * [Useful commands](/instructions/useful-commands.md): Some commonly used Slurm commands for shepherding jobs. 

## Who is this for?

This repository was compiled with members of the [MLMIA lab](www.mlmia-unitue.de) in mind to enable them to have a smooth start with the ML Cloud. 

You will notice that in many places, paths refer to locations only accessible to the MLMIA group such as `/mnt/qb/baumgartner`. However, there should be equivalent paths for members of all groups. For example, if you are part of the Berens group there would be an equivalent `/mnt/qb/berens` folder to which you *will* have access. 

The instructions were written with Linux users in mind. Most of the instructions will translate to Mac, as well. If you use windows, you may have to resort to [Putty](https://www.putty.org/), although newer versions now also support `ssh` in the [Windows terminal](https://docs.microsoft.com/en-us/windows/terminal/tutorials/ssh). 

## Minimal example

So you have just obtained access to Slurm from the [ML Cloud Masters](mailto:mlcloudmaster@uni-tuebingen.de)? What now? 

### Access via ssh keys

Once Slurm access is granted as well switch to SSH-key based authentication as described [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#login-and-access). Password access is disabled after a few days. 

### Download the tutorial code

Login to the Slurm login node using 

````
ssh <your-slurm-username>@134.2.168.52
```` 
Switch to your work directory using 
````
cd $WORK
````
Download the contents (including code) of this tutorial into your current working directory using the following line:
````
git clone https://github.com/baumgach/tue-slurm-helloworld.git
````

Change to code directory

````
cd tue-slurm-helloworld
````

The code for `multiply.py`, which we want to execute is now on Slurm. You can look at it using 
````
cat src/multiply.py
````
or your favourite command line editor. 

### Setting up a Python environment 

This code depends on a number of specific Python packages that are not installed on the Slurm nodes globally. We also cannot install them ourselves because we lack permissions. Instead we will create a virtual environment using [Conda](https://docs.conda.io/en/latest/). 

Create an environment called `myenv` using the following command


````
conda create -n myenv 
````

and confirm with `y`. 

Activate the new environment using 

````
conda activate myenv
````

We can install packages using `conda install` 

````
conda install numpy matplotlib ipython pytorch torchvision 
````
Note that this will also automatically install a newer Python version as a dependency of PyTorch. We can also choose a specific Python version as explained in the [more detailed instructions](/instructions/virtual-env-workflow.md). 

### Running the code on GPU 

Code can be deployed to GPUs using the Slurm `sbatch` command and a "deployment" script that specifies what resources specifically we request, and what code should be executed. 

Such a deployment script for Conda is provided in [src/deploy-with-conda.sh](src/deploy-with-conda.sh). The top part consists of our requested resources:

````bash
# Part of deploy-with-conda.sh
#SBATCH --ntasks=1                # Number of tasks (see below)
#SBATCH --cpus-per-task=1         # Number of CPU cores per task
#SBATCH --nodes=1                 # Ensure that all cores are on one machine
#SBATCH --time=0-00:05            # Runtime in D-HH:MM
#SBATCH --partition=gpu-2080ti-dev # Partition to submit to
#SBATCH --gres=gpu:1              # optionally type and number of gpus
#SBATCH --mem=50G                 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH --output=logs/job_%j.out  # File to which STDOUT will be written
#SBATCH --error=logs/job_%j.err   # File to which STDERR will be written
#SBATCH --mail-type=FAIL           # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=<your-email>  # Email to which notifications will be sent
````

For example, we are requesting 1 GPU from the gpu-2080ti-dev partition. See [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#partitions) for a list of all available partitions and [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#submitting-batch-jobs) for an explanations of the available options. Note: the lines starting with `#SBATCH` are *not* comments. 

The bottom part of the `deploy-with-conda.sh` script consists of bash instructions that will be executed on the assigned work node. In particular it contains the following four lines, which make a logs directory, activate the environment, run the code, and deactivate the environment again.

````bash
# Part of deploy-with-conda.sh
mkdir -p logs 
conda activate myenv
python3 src/multiply.py --timer_repetitions 10000 --use-gpu
conda deactivate
````

You can submit this job using the following command 
````
sbatch src/deploy-with-conda.sh
````

### Checking job and looking at results

After submitting the job you can check its progress using 
````
squeue --me
````

After it has finished you can look at the results in the log files in the `logs` directory for example using `cat`. 

````
ls logs
cat logs/<logfilename>.out
````

The file ending in `.out` contains the STDOUT, i.e. all print statement and things like that. The file ending in `.err` contains the STDERR, i.e. any error messages that were generated (hopefully none). 

### What now?

This concludes the minimal example. If you want to learn more, you can have a look at the more detailed instructions described in the [Contents section](#contents) above. 