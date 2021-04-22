# Instructions

This example contains some Python PyTorch code to multiply two matrices, and the necessary files and instrutions to build a singularity container containing this code and deploying it on the ML Cloud slurm host. 

The idea is to get a first "Hello World" type example working in order to understand how all these components fit together. This is not intented as a fully functional tool for getting productive. Consider it a starting point. 

## Prerequisites 

This example assumes that you are using [Ubuntu Linux](https://ubuntu.com/). Generally speaking, all of the below stuff is also possible with other Linux distirbutions, Macs and Windows (using [Putty](https://www.putty.org/)). The instructions below may partially work using those other operating systems, but it is likely that some commands or steps will require changes. 

Useful things to familiarise yourself with before starting:
 - [SSH and SSH keys](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)
 - [Containers in general](https://www.docker.com/resources/what-container) and [singularity containers](https://en.wikipedia.org/wiki/Singularity_(software))
 - The [Slurm job scheduling system](https://slurm.schedmd.com/overview.html) and its [user guide on the ML Cloud](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)

## Get access to Slurm

Apply for access to ML cloud [here](https://uni-tuebingen.de/de/199396). 

Once access is granted contact [Benjamin Gläßle](mailto:benjamin.glaessle@uni-tuebingen.de), or one of the other [ML Cloud team members](https://uni-tuebingen.de/forschung/forschungsschwerpunkte/exzellenzcluster-maschinelles-lernen/forschung/forschung/zentrale-einrichtungen/machine-learning-science-cloud/), to get access to Slurm. 

Once Slurm access is granted as well switch to SSH-key based authentication as described [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#login-and-access).

### Create a SSH config 
Note: This will prevent you from going crazy by having to type the IP address each time. 

On your local machine, create a file `$HOME/.ssh/config` with the following content:

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

## Build singularity
Note: This step is required to build singularity containers on your local machine. The remote slurm host already has singularity installed, however, you do not have `sudo` permissions there, so you will only be able to execute singularity containers, but not build. Hence we need to locally build our containers on a machine where we have `sudo` permissions, and then copy the container over, as you will see in later steps. 

To locally build singularity, follow the steps described [here](https://sylabs.io/guides/3.7/user-guide/quick_start.html) on your local machine. 

## Locally mount shared work directory 
Note: In general, this step will facilitate moving data around. Again this is not generally required. You could for instance completely rely on `scp` and `ssh` to move stuff around. However, it is required in the scope of this tutorial if you want to test your container locally first before moving it over to the slurm host. This is because the `multiply.py` script that we will run later relies on some "data" that is located in a remote shared folder on the slurm host. 

Therefore, in the follwing we will mount the remote shared folder `/mnt/qb/baumgartner` to the same location on your local system. It could also be a different location on your local system, but if we keep the path exactly the same, we do not need to change the paths in the code each time. 

All the following steps need to be executed on your local machine. 

In case you do not have `sshfs` installed, you need to do so using
````
sudo apt-get install sshfs
````
This is a program that allows us to mount a remote folder on our local machine using the `ssh` protocol. 

Next, on your local machine create the mount point where you want to mount the remote folder. In our case:
````
sudo mkdir -p /mnt/qb/baumgartner
````
The `-p` is required because we are creating a whole hierarchy, not just a single folder. `sudo` is required because we are creating the folders in the root directory `/`, where the user does not have write access.

Next we mount the remote folder using the following command:

````
sudo sshfs -o allow_other,IdentityFile=/home/$USER/.ssh/id_rsa <your-slurm-username>@134.2.168.52:/mnt/qb/baumgartner /mnt/qb/baumgartner
````
This is assuming you belong to the `baumgartner` group. Adjust accordingly if you belong to a different group. You might have to map your local username's user_id and group_id to the mountpoint by adding the options `` -o uid=`id -u username` -o gid=`id -g username` ``. This is not necessarily the case, but may help if you don't have your remote user's privileges.


Note: The folder only stays mounted as long as your internet connection doesn't drop. So, if you for instance reboot your machine, you need to re-execute the `sshfs` command. To automatically mount the folder upon rebooting, add the following line to the file `/etc/fstab` (you need to use root access for this).

````
<your-slurm-username>@134.2.168.52:/mnt/qb/baumgartner /mnt/qb/baumgartner fuse.sshfs allow_other,IdentityFile=/home/$USER/.ssh/id_rsa
````

## Download code and build singularity container

### Getting the example code and building the container

Download the code in your current working directory using the following line:

````
git clone https://github.com/baumgach/tue-slurm-helloworld.git
````

Change to code directory

````
cd tue-slurm-helloworld
````

Build singularity container (`sudo` rights are required for this step.)

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

The following lines in the `deeplearning.def` file 
````
%files
    multiply.py /opt/code
````
copies your code to `/opt/code` in the container. We copied it there so it would be baked into the container, so when you move the container elsewhere the code is still around. 

The code is also available in your current working directory. So technically it is there twice. However, when you later move your container to another location (e.g. to the slurm host), the working directory with the code (which only mounted) will no longer be the same. The copied code in `/opt/code`, on the other hand, stays with the container.   

You can navigate to either copy of the code and execute it using 

````
python3 multiply.py
````

Note that the code assumes that the following file exists on Slurm: `/mnt/qb/baumgartner/storagetest.txt`. I have put it there, so if nothing has changed it should be there. It contains a single integer specifying the size of the matrices to be multiplied in `multiply.py`. The idea behind this is to simulate dependence on external data. In a real-world example, this could for example be a medical dataset. 

**An important thing to note:** When you change your code after building the container, it will be changed in 
your current working directory but not under `/opt/code`. 

You can exit the container using `exit` or `Ctrl+d`. 

### Advantages and disadvantages of baking code into the container

The following are general remarks not related to this tutorial. 

You have two options to run code on slurm using a singularity container:
 1. Copy it into the container locally and then move the whole container including code over to slurm and run it there (as we do in this tutorial). 
 2. Do not copy your code into the container, but rather move it to your home directory on the remote slurm host and access it from there (which we can do because singularity always automatically mounts the home directory no matter where we run it)

 The advantage of (1) is that each container is (mostly) self-contained completely reproducible. (For this to be completely true, the data would also have to be baked into the container, which we could also do). If you give this container to someone else they can run it and get exactly the same result. You could also save containers with important experiments for later, so you can reproduce them or check what exactly you did. 

 However, using method (1) you will need to rebuild and copy your container to slurm everytime you change something. This, unfortunately, takes a long time because singularity (in contrast to docker) always rebuilds everything from scratch. So practically you will be able to develop much faster using method (2). This comes at the cost of the above mentioned reproducibility.

Method (2) seemes the preferable one for actual research and development. You can have your code permanently in your slurm directory and edit it locally by mounting your slurm home locally using `sshfs` like above. Another option is to use a SSH extension for yor IDE such as the "Remote -SSH" extension for Visual Studio Code. 

### (Optional) Use Pipenv to manage python environment

As an alternative to the workflow described above, check out [these additional instructions](https://github.com/lmkoch/tue-slurm-helloworld/blob/master/pipenv_singularity_tutorial.md) on how to work with pipenv virtual environments.

## Running the code on Slurm

Move the slurm instruction file and the container over to slurm like this

````
scp deploy.sh deeplearning.sif slurm:/home/baumgartner/<your-slurm-username>
````

The `deploy.sh` file contains instructions for your slurm job. Those are a bunch of options for which GPUs to use etc, and which code to execute. In this case, `multiply.py`. 

Then connect to the remote slurm host
````
ssh slurm
````

Among other things `deploy.sh` contains the following two lines

````
#SBATCH --output=logs/hostname_%j.out  # File to which STDOUT will be written
#SBATCH --error=logs/hostname_%j.err   # File to which STDERR will be written
````
specifying where the log and error files for each job will be written to. You can see, that this script writes them to a `logs` directory relative to your working directory, i.e. the folder where you execute your container command. Unfortunately, Slurm will not create this folder automatically, so we need to do it manually first using 
````
mkdir logs
````

Then submit your slurm job using the following command 
````
sbatch deploy.sh
````

This will run the job on slurm as specified in `deploy.sh`. Note by the way, that the leading `#SBATCH` do not mean that those lines are commented out. This is just slurm syntax. 

Have a look at the outputs written to `~/logs/`. 
Of course this is a very basic example, and you should later taylor `deploy.sh` to your needs. 

More info on how to manage Slurm jobs can be found [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)

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

## Useful links for context

 - [Singularity tutorial with GPU use and PyTorch](https://github.com/bdusell/singularity-tutorial)
 - [A python tool for deploying slurm jobs](https://github.com/sinzlab/tue-slurm/) with singularity containers developed by the Sinz lab
 - [A list of all available Docker images](https://hub.docker.com/r/nvidia/cuda/) with Cuda support to build the container from (if you are not happy with Ubunut 20.04)
 - [ML Cloud Slurm Wiki](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)
 - [Singularity user guide](https://sylabs.io/guides/3.7/user-guide/)
