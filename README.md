# Instructions

## Get access to SLURM

Apply for access to ML cloud [here](https://uni-tuebingen.de/de/199396). 

Once access is granted contact [Benjamin Gläßle](benjamin.glaessle@uni-tuebingen.de), or one of the other [ML Cloud team members](https://uni-tuebingen.de/forschung/forschungsschwerpunkte/exzellenzcluster-maschinelles-lernen/forschung/forschung/zentrale-einrichtungen/machine-learning-science-cloud/), to get access to Slurm. 

Once Slurm access is granted as well switch to SSH-key based authentication as described [here](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm#login-and-access).

### (Optional) Create a SSH config entry so you don't go crazy typing IP addresses

Create a file `$HOME/.ssh/config` with the following content:

````
Host slurm
    HostName 134.2.168.52
    User <your-slurm-username>
````

You can now `ssh` and `scp` using the following syntax 
````
ssh slurm
scp localfile slurm:<remote-dir>
````
