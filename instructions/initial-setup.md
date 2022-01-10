# Initial setup

The following steps will describe essential some useful SSH and mounting setups. 

## Create a SSH config

In order to prevent you from going crazy by having to type the IP address each time, you can setup a shortcut in your SSH config file. 

On your **local machine**, create a file `$HOME/.ssh/config` with the following content:

````
Host slurm
    HostName 134.2.168.52
    User <your-slurm-username>
    ForwardAgent yes
````

Then, on your local machine, run 

````
ssh-add
````
to enable the forwarding of your identity to different Slurm nodes. This will allow you to ssh into the node on which your job is running. You may need to periodically rerun the `ssh-add` command in the future (if `ssh-add -L` return empty, then you need to run `ssh-add` again)

You can now `ssh` to the Slurm login node using the following command
````
ssh slurm
````

and copy files from your local workstation to Slurm  using the following syntax
````
scp <localfile> slurm:<remote-dir>
````

## Locally mount shared work directory

Locally mounting the Slurm work directories will facilitate editing your code and moving around data. It could for example make sense to mount your data directory for moving files, or your `$WORK` directory so you can edit code on your local workstation using your favourite editor. 

In the following we will mount the remote shared folder `/mnt/qb/work/baumgartner/<your-username>` to the same location on your local system. It could also be a different location on your local system, but if we keep the path exactly the same, we do not need to change the paths in the code each time.

All the following steps need to be executed on your local machine.

In case you do not have `sshfs` installed, you need to do so using (assuming you are on Ubuntu)
````
sudo apt-get install sshfs
````
This is a program that allows us to mount a remote folder on our local machine using the `ssh` protocol.

Next, on your local machine create the mount point where you want to mount the remote folder. Obviously, first change to the term in the brackets to your own username (command `whoami` if you don't know)
````
sudo mkdir -p /mnt/qb/work/baumgartner/<your-slurm-username>
````
The `-p` is required because we are creating a whole hierarchy, not just a single folder. `sudo` is required because we are creating the folders in the root directory `/`, where the user does not have write access.

Next we mount the remote folder using the following command:

````
sudo sshfs -o allow_other,IdentityFile=/home/$USER/.ssh/id_rsa <your-slurm-username>@134.2.168.52:/mnt/qb/work/baumgartner/<your-username> /mnt/qb/work/baumgartner/<your-username>
````
This is assuming you belong to the `baumgartner` group. Adjust accordingly if you belong to a different group. 

Note: The folder only stays mounted as long as your internet connection doesn't drop. So, if you for instance reboot your machine, you need to re-execute the `sshfs` command. To automatically mount the folder upon rebooting, add the following line to the file `/etc/fstab` (you need to use root access for this).

````
<your-slurm-username>@134.2.168.52:/mnt/qb/work/baumgartner/<your-username> /mnt/qb/work/baumgartner/<your-username> fuse.sshfs allow_other,IdentityFile=/home/$USER/.ssh/id_rsa
````

### Trouble shooting

You might have to map your local username's user_id and group_id to the mount point by adding the options `` -o uid=`id -u username` -o gid=`id -g username` `` to the `sshfs` command. This is not necessarily the case, but may help if you don't have your remote user's privileges.

## Workflows for editing code remotely 

If you mounted your code directory as described above, you can now open that folder on your local machine using your favourite editor. 

Drawbacks:
  * Some people report some laggy behaviour due to the slowness of the SSH connection. 
  * Also like this your code is *only* on the ML Cloud so if it goes down you don't have access to your code 

Instead of mounting the drive, some editors have functionality or plugins specifically for editing code remotely via SSH. For example, Visual Code Studio has the "Remote -SSH" which allows you to do exactly that. 

An alternative workflow is to develop locally and commit+push your changes to a git repository. Before running your code you can `git pull` on the Slurm node. As a side effect this will require you to commit your changes frequently which is generally a good thing. 

## What now?

Go back to the [Contents section](/README.md#contents) or continue with a more detailed description of the [virtual environment](/instructions/virtual-env-workflow.md) or [Singularity](/instructions/singularity-workflow.md) based workflow. 