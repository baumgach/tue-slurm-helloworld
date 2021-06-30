# Hello World Example

In this tutorial you will connect to the ML cloud slurm cluster and allocate computing resources to run some very basic example code. This is just a starting point, and you will probably need to work through some or all of the follow-up examples to use slurm for your more sophisticated needs.


## Login to Slurm head node using SSH


Once Slurm access is granted, you can open a terminal and connect to the slurm head node:

````
ssh <your-slurm-username>@134.2.168.52
````

Note: You should switch to SSH-key based authentication as soon as possible, as described in the [next tutorial](../02_ssh_config/02_ssh_config.md) and [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#login-and-access).

## Download tutorial code

Download the code in your current working directory on the slurm headnode using the following line:

````
git clone https://github.com/baumgach/tue-slurm-helloworld.git
````

Change to code directory

````
cd tue-slurm-helloworld
````

## Running a hello world example on slurm

The file `01_hello_world.sbatch` contains instructions for your slurm job. Those are a bunch of options for which GPUs to use etc (lines starting with `#SBATCH`), followed by the code that must be executed.

Among other things `01_hello_world.sbatch` contains the following two lines

````
#SBATCH --output=logs/hostname_%j.out  # File to which STDOUT will be written
#SBATCH --error=logs/hostname_%j.err   # File to which STDERR will be written
````
specifying where the log and error files for each job will be written to. You can see, that this script writes them to a `logs` directory relative to your working directory, i.e. the folder where you execute your container command. Slurm will not create this folder automatically, so we need to do it manually first using

````
mkdir logs
````

Then submit your slurm job using the following command

````
sbatch 01_hello_world.sbatch
````

This will allocate resources on the slurm cluster as specified in `01_hello_world.sbatch`, and run the code specified there on these resources. Note that the leading `#SBATCH` do not mean that those lines are commented out. This is just slurm syntax.

Have a look at the outputs written to `~/logs/`.
Of course this is a very basic example, and you should later taylor `01_hello_world.sbatch` to your needs.

More info on how to manage Slurm jobs can be found [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)

## What next?

- [SSH configuration](./02_ssh_config.md)
- [Getting your code and data on the slurm cluster](./03_file_transfer.md)
- Running python code on slurm
- Running jobs with complex dependencies using containers
- Interactive sessions

## Useful links for context

 - [Singularity tutorial with GPU use and PyTorch](https://github.com/bdusell/singularity-tutorial)
 - [A python tool for deploying slurm jobs](https://github.com/sinzlab/tue-slurm/) with singularity containers developed by the Sinz lab
 - [A list of all available Docker images](https://hub.docker.com/r/nvidia/cuda/) with Cuda support to build the container from (if you are not happy with Ubunut 20.04)
 - [ML Cloud Slurm Wiki](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)
 - [Singularity user guide](https://sylabs.io/guides/3.7/user-guide/)
