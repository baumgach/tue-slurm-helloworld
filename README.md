# Instructions

This example contains some Python PyTorch code to multiply two matrices, and the necessary files and instrutions to build a singularity container containing this code and deploying it on the ML Cloud slurm host. 

The idea is to get a first "Hello World" type example working in order to understand how all these components fit together. 

## Get access to Slurm

Apply for access to ML cloud [here](https://uni-tuebingen.de/de/199396). 

Once access is granted contact [Benjamin Gläßle](mailto:benjamin.glaessle@uni-tuebingen.de), or one of the other [ML Cloud team members](https://uni-tuebingen.de/forschung/forschungsschwerpunkte/exzellenzcluster-maschinelles-lernen/forschung/forschung/zentrale-einrichtungen/machine-learning-science-cloud/), to get access to Slurm. 

Once Slurm access is granted as well switch to SSH-key based authentication as described [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#login-and-access).

### (Optional) Create a SSH config 
Note: This will prevent you from going crazy by having to type the IP address each time. I will assume in the remainder of the document that you have this alias set. 

Create a file `$HOME/.ssh/config` with the following content:

````
Host slurm
    HostName 134.2.168.52
    User <your-slurm-username>
````

You can now `ssh` and `scp` using the following syntax 
````
ssh slurm
scp <localfile> slurm:<remote-dir>
````

## (Optional) Build singularity
Note: This step is only required if you are planing on building singularity containers on your local machine. The remote slurm host already has singularity installed. The rest of the tutorial will implicitly assume you have done this step. If you have not, then perform the following steps on the remote slurm host. 

Follow the steps described [here](https://sylabs.io/guides/3.7/user-guide/quick_start.html)

## (Optional) Locally mount shared work directory 
Note: This step will facilitate moving data around. Again this is not required if you work completely remotely on the slurm host. 

````
sudo sshfs -o allow_other,IdentityFile=/home/$USER/.ssh/id_rsa <your-slurm-username>@134.2.168.52:/mnt/qb/baumgartner /mnt/qb/baumgartner
````

The above links the remote slurm location `/mnt/qb/baumgartner` to the same path on your local machine. Note this assuming you belong to the `baumgartner` group. Adjust accordingly if you belong to a different group. 

## Download code and build singularity container

### Getting the example code and building the container

Get code using the following line:

````
git clone https://github.com/baumgach/tue-slurm-helloworld.git
````

Change to code directory

````
cd tue-slurm-helloworld
````

Build singularity container (`sudo` is required for this step.)

````
sudo singularity build deeplearning.sif deeplearning.def
````

Explanations:
 - `deeplearning.def` contains instructions on how to build the container. It's a text file, have a look at it if you want. 
 - Importantly, this file contains the specification of the "operating system", a Ubuntu 20.04 with cuda support in this case, and instructions to install Python3 with all required packages for this example. 

### Entering the new container in a shell

You can now enter a shell in your container using the following command and have a look around. 

````
singularity shell --bind /mnt/qb/baumgartner deeplearning.sif
````

The bind option is not necessary to enter the container. It will mount the `baumgartner` folder, so you have access to it from inside the container also. This is important for the `multiply.py` script to execute successfully.  

You are now running an encapsulated operating system as specified in `deeplearning.def`. 
Try opening an `ipython` terminal. 
Note that your home directory and current working directory automatically get mounted inside the container. This is not true for all paths, however. 

The following lines in the `deeplearning.sif` file 
````
%files
    multiply.py /opt/code
````
copies your code to `/opt/code` in the container. We copied it there so it would be baked into the container, so when you move the container elsewhere the code is still around. However, it is also available in your current working directory. So technically it is there twice. But when you move your container to another location, the latter code will no longer be there. You navigate to either copy of the code and execute it using 

````
python3 multiply.py
````

Note that the code assumes that the following file exists on Slurm: `/mnt/qb/baumgartner/storagetest.txt`. I have put it there, so if nothing has changed it should be there. It contains a single integer specifying the size of the matrices to be multiplied in `multiply.py`. The idea behind this is to simulate dependence on external data. In a real-world example, this could for example be a medical dataset. 

**An important thing to note:** When you change your code after building the container, it will be changed your current working directory but not under `/opt/code`. 

You can exit the container using `exit` or `Ctrl+d`. 

### Executing stuff in the container 

You can execute the Python code without having to enter the container using the `exec` option as follows: 

````
singularity exec --nv --bind /mnt/qb/baumgartner deeplearning.sif python3 /opt/code/multiply.py --timer_repetitions 10000 --use-gpu
````

Explanations:
 - The `--nv` option is required to enable GPU access
 - The `--bind` option mounts the `baumgartner` folder also inside the container
 - Note that we are also passing some options to the Python script at the end
 - Note: you may not have GPU on your local machine. In that case the GPU options are simply ignored and the code executed on CPU. 

Further note that the above command references the code at `/opt/code`. This copy of the code is static. This means if you change something in your code, you need to rebuild the container for the changes to take effect. 

However, as long as the container is still on your local machine you can change `/opt/code/multiply.py` to the path on your local machine (i.e. perhaps something like `$HOME/tue-slurm-helloworld/multiply.py`). Because this copy of the code was not copied, but is mounted, any changes you make, will take effect and you do not need to rebuild your container each time (only once you want to deploy it remotely).

## Running the code on Slurm

Move the slurm instruction file and the container over to slurm like this

````
scp deploy.sh deeplearning.sif slurm:/home/baumgartner/<your-slurm-username>
````

The `deploy.sh` file contains instructions for your slurm job. There are a bunch of options for which GPUs to use etc. and which code to execute. In this case, `multiply.py`. 

Then connect to the remote slurm host
````
ssh slurm
````

and run the following command 
````
sbatch deploy.sh
````

This will run the job on slurm as specified in `deploy.sh`. Have a look at the outputs written to `~/logs/`. 
Of course this is a very basic example, and you should later taylor `deploy.sh` to your needs. 

More info on how to manage Slurm jobs can be found [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)

## Useful links for context

 - [Singularity tutorial with GPU use and PyTorch](https://github.com/bdusell/singularity-tutorial)
 - [A python tool for deploying slurm jobs](https://github.com/sinzlab/tue-slurm/) with singularity containers developed by the Sinz lab
 - [A list of all available Docker images](https://hub.docker.com/r/nvidia/cuda/) with Cuda support to build the container from (if you are not happy with Ubunut 20.04)
 - [ML Cloud Slurm Wiki](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)
 - [Singularity user guide](https://sylabs.io/guides/3.7/user-guide/)