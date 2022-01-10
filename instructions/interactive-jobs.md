# Running interactive jobs and debugging 

It is also possible to open interactive sessions which can be very useful for debugging. However, **do not** use this as your main way of developing. Interactive sessions don't automatically exit when your job is finished on so will be blocking resources unnecessarily. 

## Starting an interactive session on a work node

When we ssh onto the Slurm login node, we do not have access to any of the computational resources such as GPU. For that usually deploy a job using `sbatch` which will then be executed on one of the work nodes. 

It is also possible to enter one of the work nodes directly, by using the following `srun` command:

````
srun --pty bash
````

This will start and interactive job, login to an available work node and run the bash shell. However, we will still not have access to GPUs because we didn't request any.

Requesting resources works exactly the same as in the deployment scripts, but we provide the variables as command line arguments (which incidentally you can also do for `sbatch` if you want to). For example:

````
srun --pty --partition=gpu-2080ti-dev --time=0-00:30 --gres=gpu:1 bash 
````

This will start an interactive session with a 2080ti GPU for 30 minutes. A description of the meaning of all command line arguments can be found in [this section](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#submitting-batch-jobs) of the ML Cloud Slurm wiki.

You can now navigate to the source code if you are not already there
````
cd $WORK/tue-slurm-helloworld
````

Assuming you are using Conda, activate your environment using 
````
conda activate myenv
````
Otherwise use the appropriate virtualenv or Singularity equivalent. 


Then you can run Python as you would on your local system
````
python src/multiply.py --timer_repetitions 10000 --use-gpu
````

## Debugging

There is also a version of the `multiply.py` script, where I added a `ipdb` breakpoint around line 22: [src/multiply-debug.py](/src/multiply-debug.py). 

We can also run that file instead:
````
python src/multiply-debug.py --timer_repetitions 10000 --use-gpu
````

This will run the code until line 24 and then open an interactive debug terminal which is similar to the `ipython` console and allows you to execute any Python commands that you want. In there you can for example check the value and shape of the variables that have already been defined
````python
print(x)
print(x.shape)
````

You can also step through the code line-by-line by typing "n", step into functions using "s", or continue executing the rest of the code using "c". 

## Starting other interactive jobs  

Starting an interactive session with a `bash` terminal is a very sensible way of doing things. However, you can technically run whatever you want using `srun`. Here is an example of directly running the code using a singularity container if you have been following that workflow:

````
srun --pty --partition=gpu-2080ti-dev --time=0-00:30 --gres=gpu:1 \
   singularity exec \
   --nv \
   --bind /mnt/qb/baumgartner,`pwd` deeplearning.sif \
       python3 src/multiply-debug.py \
       --timer_repetitions 10000 \
       --use-gpu 
````

## SSH-ing into the worknode on which a job is running

When you run `squeue --me` you can check on which nodes your jobs are running. When I, for example deploy the `deploy-with-conda-multiple.sh` script, my `squeue --me` output is the following:

````
     JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
 1121515_0 gpu-2080t deploy-w cbaumgar  R       0:03      1 bg-slurmb-bm-2
 1121515_1 gpu-2080t deploy-w cbaumgar  R       0:03      1 bg-slurmb-bm-2
 1121515_2 gpu-2080t deploy-w cbaumgar  R       0:03      1 bg-slurmb-bm-2
 1121515_3 gpu-2080t deploy-w cbaumgar  R       0:03      1 slurm-bm-64
 1121515_4 gpu-2080t deploy-w cbaumgar  R       0:03      1 slurm-bm-63
````

This tells me for example, that job `1121515_4` is running on work node `slurm-bm-63`. I can now simply ssh into this work node using 

````
ssh slurm-bm-63
````

A requirement for this to work is that all the identity forwarding stuff in the [initial setup](/instructions/initial-setup.md) section of this tutorial were completed correctly. If it is not working for some reason try running `ssh-add` on your local machine. 

Note also that you can only ssh onto nodes, on which you have jobs running. 

Once we ssh-ed to the work node (in this case node `slurm-bm-63`) we can for example check what the GPU is up to using
````
nvidia-smi -l
````

or we can see what is stored on the local temporary storage:

````
ls /scratch_local
````