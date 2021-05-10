# Interactive Session

Interactive slurm sessions can be used (among other ways) to ssh onto a cluster node - this is probably the easiest way to get started.

## Access the SLURM headnode

To get started, we ssh to the slurm headnode (this assumes you have deployed your keys before, see main tutorial).

````
> ssh -A <slurm-username>@134.2.168.52
````

The `-A` option enables key forwarding of the authentication agent. You can ssh to the slurm headnode without it, but you need the setting in order to hop on to your final compute node. More elegantly, you can add the following to your ssh config in `~/.ssh/config`:

````
Host slurm
    HostName 134.2.168.52
    User lkoch54
    ForwardAgent yes
````

this allows you to simply do 

````
> ssh slurm
````

In case you have trouble with the key forwarding, check out this [Stackoverflow answer](https://stackoverflow.com/a/38986908/2323484) (click here for further help on [Windows](https://stackoverflow.com/questions/52113738/starting-ssh-agent-on-windows-10-fails-unable-to-start-ssh-agent-service-erro).


## Allocating resources

You can now allocate your desired resources. There are plenty of options to specify number of CPU cores, GPUs, memory, etc, for example:

````
--gres=gpu:1              # Request one GPU
--mem=50G                 # Total memory
--ntasks=1                # Number of tasks
--cpus-per-task=1         # Number of CPU cores per 
````

A more comprehensive overview is given in the [MLcloud wiki](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm). Let's allocate a job:

````
> salloc --gres gpu:1 --mem=50G

salloc: Granted job allocation 262198
salloc: Waiting for resource configuration
salloc: Nodes slurm-bm-36 are ready for job

````

Nice! You now have a slurm job (job-id 262198), and a node (slurm-bm-36) available. You can check check out the status of your jobs with `squeue --me`, or later cancel a job with `scancel <job-id>`.

You can now ssh to your allocated node with

````
> ssh slurm-bm-36     # node provided for this job
````

That's it, now you can get to work.

## Running a jupyter notebook

Let's run a simple Jupyter notebook that measures matrix multiplication time and writes the result to a file somewhere on `/mnt/qb/berens/`. to access the remote jupyter notebook server, we need to do some clever ssh tunneling, since we're doing two hops: first from our local machine to the slurm headnode, then on to the node we have allocated.

````
local> ssh -L 8001:localhost:8002 slurm
slurm> ssh -L 8002:localhost:8003 slurm-bm-36
slurm-bm-36>
````

We are now on our remote host. To run the jupyter notebook server, we need a singularity container. We can build it from the container definition `interactive_session.def`:

````
> singularity build --fakeroot interactive_session.sif interactive_session.def
````

Since this takes a while, I also put a pre-built container in `/mnt/qb/berens/lkoch/slurm-tutorial` - feel free to use that one. Now you can run the notebook server on port 8003:

````
> singularity exec --bind /mnt/qb/berens interactive_session.sif jupyter-notebook --port 8003
````

That's it. You can now go to `localhost:8001` in your local browser to run the remote notebook.

Note that we mounted `/mnt/qb/berens` in the container. This way you have read/write access to directories there. I suggest you create your personal directory in your group storage. Now you can adapt the paths in the notebook `interactive_session.ipynb` to make sure you're writing to a location you have access to.

## Release your resources

When you're done, remember to release your resources with `scancel <job-id>`!
