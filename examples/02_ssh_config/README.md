# SSH configuration

You can connect to the slurm headnode via

````
> ssh <slurm-username>@134.2.168.52
````

If you haven't done so already, make sure to enable ssh-key authentication, which means you copied your ssh public key on the slurm headnode under `~/.ssh/authorized_keys`. Password authorised access is revoked within a few days of account activation. More information on deploying your public key can be found [here](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)

From the slurm headnode, you will be able to ssh onto any of the nodes where your jobs are running. This is not always necessary, but may be convenient sometimes. To be authorised to do that, you need to enable key forwarding from your local machine. This is done with the option `-A`:


````
> ssh -A <slurm-username>@134.2.168.52
````

In case you have trouble with the key forwarding, check out this [Stackoverflow answer](https://stackoverflow.com/a/38986908/2323484) (click [here](https://stackoverflow.com/questions/52113738/starting-ssh-agent-on-windows-10-fails-unable-to-start-ssh-agent-service-erro) for further help on Windows). Most likely, you just need to run `ssh-add` in your local terminal.


## SSH config file

We strongly recommend to create an ssh config file for your convenience, so you never have to type long ssh commands again. For this, you can create a file `~/.ssh/config`, where you can add the following lines:

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

Note: You can add all other ssh options to the config file if needed, for example if you need to connect on a specific port or enable port forwarding. For example:

````
Host some_other_host
    HostName xxx.xxx.xxx.xxx
    Port 60222
    LocalForward 6006 localhost:6006
````

## What next?

[Getting your code and data on the slurm cluster](./03_file_transfer/README.md)
