# Useful commands

Some common commands are explained in [this section](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#common-slurm-commands) of the ML Cloud Slurm Wiki. 

They are reproduced here with some useful options. 

## Show jobs 

Your own jobs 

````
squeue --me
````

Any users jobs

````
squeue -u <username>
````

## Cancel jobs

Cancel specific job 

````
scancel <job-id>
````

Cancel all my jobs 

````
scancel -u <your-slurm-username>
````

## Check fairshare

Check on a group level 

````
sshare
````

Check on an individual level

````
sshare --all
````

## What now?

Go back to the [Contents section](/README.md#contents) or give feed-back about the tutorial on [github](https://github.com/baumgach/tue-slurm-helloworld/issues)! 