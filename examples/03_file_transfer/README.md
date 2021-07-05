# Slurm cluster filesystems

In the Hello World example, we got our code onto the ML cloud slurm cluster by cloning a git repository into the home directory. In this tutorial, we examine the file systems available to us on the cluster, and how to get stuff there.

## Storage on the cluster

There are a few storage volumes you can use, for example:

* Your home directory on `/home/<your_group_name>/<your_user_name>`. It is recommended you use this directory for most purposes, and it is backed up.
* Your group's directory on `/mnt/qb/<your_group_name>`.
* There's additional volumes, for example for general datasets that may be used by many people: `/mnt/qb/datasets`

All of these storage volumes are mounted on the slurm headnode as well as all the compute nodes. So anything you put there, you will be able to use from the compute nodes as well during execution of your job. Beware that some volumes, such as the datasets volume, have only read access from the compute nodes.

## How to get stuff on the cluster

There are various ways to get stuff (code and data) on the cluster. Cloning a repository is probably not what you want to do most of the time.

### Option A: Copy with scp

You can copy files from your local machine onto the cluster headnode via ssh using services like `scp` (copy over ssh) or `rsync` (backup tool):

````
scp -r some_data_folder slurm:/path/to/preferred/remote/location
````
or
````
rsync -r some_data_folder slurm:/path/to/preferred/remote/location
````

### Option B: Mount remote directory on local machine

While Option A might be useful every once in a while, it's quite cumbersome to copy code back and forth all the time during development. Alternatively, you can mount remote directories on your local machine using `sshfs` and then work in these directories locally.

As an example, we will now mount the remote slurm home directory. You can mount any of the other remote in the same way. The following steps need to be executed on your local machine.

In case you do not have `sshfs` installed, you need to do so using
````
sudo apt-get install sshfs
````
This is a program that allows us to mount a remote folder on our local machine using the `ssh` protocol.

Next, on your local machine create the mount point where you want to mount the remote folder. For example:
````
mkdir -p ~/mnt/slurm/<your-user-name>
````
The `-p` is required because we are creating a whole hierarchy, not just a single folder.

Next we mount the remote folder using the following command:

````
sudo sshfs -o allow_other,IdentityFile=/home/$USER/.ssh/id_rsa <your-slurm-username>@134.2.168.52:/home/<your_group_name>/<your_user_name> ~/mnt/slurm/<your-user-name>
````

Note: 
- You might have to map your local username's user_id and group_id to the mountpoint by adding the options `` -o uid=`id -u username` -o gid=`id -g username` ``. This is not necessarily the case, but may help if you don't have your remote user's privileges.
- The folder only stays mounted as long as your internet connection doesn't drop. So, if you for instance reboot your machine, you need to re-execute the `sshfs` command. To automatically mount the folder upon rebooting, add the following line to the file `/etc/fstab` (you need to use root access for this).

````
<your-slurm-username>@134.2.168.52:/home/<your_group_name>/<your_user_name> ~/mnt/slurm/<your-user-name> fuse.sshfs allow_other,IdentityFile=/home/$USER/.ssh/id_rsa
````

## What next?

[Running python code on slurm](./04_python_example/README.md)

