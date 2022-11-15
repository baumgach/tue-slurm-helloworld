# Using Slurm with Singularity

This example contains an example workflow using Singularity which includes instructions on how to build a Singularity container and deploying it on the ML Cloud Slurm host.

In contrast, to the [virtual environment workflow](/instructions/virtual-env-workflow.md) (i.e. Conda or virtualenv) the Singularity workflow offers more flexibility for setting up your environment, but it is also arguably a bit more involved and cumbersome to use. 

## What is Singularity in a nutshell

[Singularity](https://en.wikipedia.org/wiki/Singularity_(software)) is a type of container similar to the more widely used [Docker](https://www.docker.com/resources/what-container). 

It allows you to package everything you need to run your code into a file. It is almost like a virtual machine, in which you can log in, install whatever you want and store whatever data you want. In contrast to an actual virtual machine no part of your hardware is allocated specifically to run a singularity container. Rather it just takes whatever resources it needs like any other job on your system. 

The cool thing about them is that you can just give that file to anyone else and they can exactly reproduce your experiment setup without having to do any annoying environment setups like finding the right CUDA or tensorflow versions. Rather than having instructions with your code on how to get it to run, you could technically just share the Singularity file. However, in practice these files tend to be very large so they are not typically shared widely. However, they are also very useful for packaging and sending jobs that will exactly like you want them to run on any system. 

As you will see the "pure" idea would be to package your code inside the container. However, this is pretty unwieldy for daily use with the ML Cloud, so we will also discuss a sort of hybrid setup where the container only contains the dependencies, but the code lives outside of the container. 

If containers are new to you make sure to read about [containers in general](https://www.docker.com/resources/what-container) and [singularity containers](https://en.wikipedia.org/wiki/Singularity_(software)) in particular. 

Singularity (like Conda and virtualenv in the previous tutorial) is already pre-installed on Slurm. 

## Download code and build singularity container

Make sure you are on the Slurm login node, and download the code if you haven't done so yet in the minimal example or the conda workflow example:

````
cd $WORK
git clone https://github.com/baumgach/tue-slurm-helloworld.git
cd tue-slurm-helloworld 
````

As the first step, build singularity container

````
singularity build --fakeroot deeplearning.sif src/deeplearning.def
````

Explanations:
 - `deeplearning.def` contains instructions on how to build the container. It's a text file, have a look at it if you want.
 - Importantly, this file contains the specification of the "operating system", a Ubuntu 20.04 with cuda support in this case, and instructions to install Python3 with all required packages for this example.



## Entering the new container in a shell

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

The code is also available in your current working directory. So technically it is there twice. However, when you later move your container to another location (e.g. to the Slurm host), the working directory with the code (which only mounted) will no longer be the same. The copied code in `/opt/code`, on the other hand, stays with the container.   

You can navigate to either copy of the code and execute it using

````
python3 multiply.py
````

Note that the code assumes that the following file exists on Slurm: `/mnt/qb/baumgartner/storagetest.txt`. I have put it there, so if nothing has changed it should be there. It contains a single integer specifying the size of the matrices to be multiplied in `multiply.py`. The idea behind this is to simulate dependence on external data. In a real-world example, this could for example be a medical dataset.

**An important thing to note:** When you change your code after building the container, it will be changed in
your current working directory but not under `/opt/code`.

You can exit the container using `exit` or `Ctrl+d`.

## Executing stuff in the container

You can execute the Python code without having to enter the container using the `exec` option as follows:

````
singularity exec --nv --bind /mnt/qb/baumgartner,`pwd` deeplearning.sif python3 /opt/code/multiply.py --timer_repetitions 10000 --no-gpu
````

Explanations:
 - The `--nv` option is required to enable GPU access
 - The `--bind` option mounts the `baumgartner` folder and the current working directory (which can be obtained in bash using `pwd`) inside the container.
 - Note that we are also passing some options to the Python script at the end.
 - The Slurm login nodes do not have GPUs so for now we use the `--no-gpu` option for our python script. This will change once we submit a job further down in this file. 

Further note that the above command references the code at `/opt/code`. This copy of the code is static. This means if you change something in your code, you need to rebuild the container for the changes to take effect.

However, as long as the container is still on your local machine you can change `/opt/code/multiply.py` to the path on your local machine (i.e. perhaps something like `$HOME/tue-Slurm-helloworld/multiply.py`). Because this copy of the code was not copied, but is mounted, any changes you make, will take effect and you do not need to rebuild your container each time (only once you want to deploy it remotely).

## Running code outside of the Singularity container

As alluded to in the beginning, it may be a bit cumbersome to rebuild your entire Singularity container every time you make a change to your code, especially because Singularity really rebuilds the whole thing each time even if only a few parts have changed (this is different in Docker). 

So rather than baking the code into the container we can also run some code that lives outside of the container somewhere on slurm. We can for example run the identical file that lives in the `src` folder of this tutorial. 

````
singularity exec --nv --bind /mnt/qb/baumgartner,`pwd` deeplearning.sif python3 src/multiply.py --timer_repetitions 10000 --no-gpu
````

Not all directories are available from inside the container, but the following directories will be there:
 - The home directory of your Slurm login node
 - All the paths you add using the `--bind` option in the command above. 

## Running the code on Slurm

The `deploy-with-singularity.sh` file contains instructions for your Slurm job. Those are a bunch of options for which GPUs to use etc, and which code to execute. In this case, `multiply.py`. 

We can submit the Slurm job using the following command
````
sbatch src/deploy-with-singularity.sh
````

This will run the job on Slurm as specified in `deploy.sh`. Note by the way, that the leading `#SBATCH` do not mean that those lines are commented out. This is just Slurm syntax.

Have a look at the outputs written to `logs/`.
Of course this is a very basic example, and you should later tailor `deploy-with-singularity.sh` to your needs.

More info on how to manage Slurm jobs can be found [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)

## Advantages and disadvantages of baking code into the container

The following are general remarks not related to this tutorial.

You have two options to run code on Slurm using a singularity container:
 1. Copy the code into the container locally and then move the whole container including code over to Slurm and run it there. For this you would need to install Singularity on your local machine as described below. 
 2. Do not copy your code into the container, but rather move it to your `$WORK` directory on the remote Slurm host and access it from there by mounting binding the code directory from Slurm into the container using the `--bind`option. 

The advantage of (1) is that each container is (mostly) self-contained and completely reproducible. (For this to be completely true, the data would also have to be baked into the container, which we could also do). If you give this container to someone else they can run it and get exactly the same result. You could also save containers with important experiments for later, so you can reproduce them or check what exactly you did. In fact this is what many ML companies do often in conjunction with Kubernetes, but usually using Docker rather than Singularity which is a bit more flexible and faster to build. 

However, using method (1) you will need to rebuild and copy your container to Slurm every time you change something. This, unfortunately, takes a long time because Singularity (in contrast to docker) always rebuilds everything from scratch. So practically you will be able to develop much faster using method (2). This comes at the cost of the above mentioned reproducibility.

Method (2) seems the preferable one for actual research and development. You can have your code permanently in your Slurm directory and edit it locally by mounting your Slurm home locally using `sshfs` like above. Another option is to use a SSH extension for your IDE such as the "Remote -SSH" extension for Visual Studio Code.

## Install Singularity on your local machine (optional)

You may want to install Singularity also on your local machine so you can develop your environment locally before copying it over to Slurm . 

To install singularity on your local machine, follow the steps described [here](https://sylabs.io/guides/3.7/user-guide/quick_start.html).

## What now?

Go back to the [Contents section](/README.md#contents), learn about doing [parallel parameter sweeps](/instructions/parallel-jobs.md) using `sbatch`, or [interactive jobs and debugging](/instructions/interactive-jobs.md). 
