# Instructions

This repository contains a number of tutorials to get started running code on the ML Cloud SLURM cluster.

The idea is to get a number of "Hello World" type examples working in order to understand how all the different components fit together: slurm, ssh, file and data storage, python environments, and containers. This is not intented as a fully functional tools for getting productive. Consider it a starting point.

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


## Useful links for context

 - [Singularity tutorial with GPU use and PyTorch](https://github.com/bdusell/singularity-tutorial)
 - [A python tool for deploying slurm jobs](https://github.com/sinzlab/tue-slurm/) with singularity containers developed by the Sinz lab
 - [A list of all available Docker images](https://hub.docker.com/r/nvidia/cuda/) with Cuda support to build the container from (if you are not happy with Ubunut 20.04)
 - [ML Cloud Slurm Wiki](https://gitlab.mlcloud.uni-tuebingen.de/doku/public/-/wikis/Slurm)
 - [Singularity user guide](https://sylabs.io/guides/3.7/user-guide/)
