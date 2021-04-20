# Using Pipenv with Singularity

This is an alternative workflow where:
* I use pipenv for managing my python environment
* No code is baked into the container. Instead, the code and the pipenv environment live in a folder that is mounted in the container

Check [this](https://github.com/bdusell/singularity-tutorial#separating-python-modules-from-the-image) tutorial to convince yourself that using pipenv 
is a good idea, also in combination with singularity containers. 

## Container definition 

The adapted singularity definition file `deeplearning.def` looks like this: 


````
BootStrap: docker
From: nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

%post
    # Downloads the latest package lists.
    apt-get update -y

    # Install Python3 requirements
    # --> python3-tk is required by matplotlib.
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-tk \
        python3-pip \
        python3-distutils \
        python3-setuptools

    # Reduce the size of the image by deleting the package lists we downloaded,
    # which are useless now.
    apt-get -y clean
    rm -rf /var/lib/apt/lists/*

    # Install Pipenv.
    pip3 install pipenv

%environment
    # Pipenv requires a certain terminal encoding.
    export LANG=C.UTF-8
    export LC_ALL=C.UTF-8
    # This configures Pipenv to store the packages in a specific directory
    export WORKON_HOME=/mnt/qb/groupname/path/to/venvs/
````

Go ahead and build your container as described in the main tutorial.

## Installing your python environment

I assume you have a share `/mnt/qb/groupname/` under which you have your project code somehwere, e.g. `/mnt/qb/groupname/path/to/code`. Now also make sure to create the folder where your all of your pipenv environments for your containers should live, as specified in the container definition above:

````
mkdir -p /mnt/qb/groupname/path/to/venvs/
````
Note that when you use pipenv outside your container, the environments will be stored elsewhere (probably in `~/.venv/`). This is desirable, because now you can just use pipenv in your project code from different systems (container and locally) and the environments will not interfere with each other.


You can now install dependencies with:

````
cd /mnt/qb/groupname/path/to/code
singularity exec --bind /mnt/qb/groupname deeplearning.sif pipenv install
````

You can also specific packages irrespective whether you already have a `Pipfile` or an existing environment. Pipenv will check your current working directory and create the environment if it doesn't already exist:

````
cd /mnt/qb/groupname/path/to/code
singularity exec --bind /mnt/qb/groupname deeplearning.sif pipenv install numpy torch
````

You can now run your code like this:

````
singularity exec --bind /mnt/qb/groupname deeplearning.sif pipenv run python multiply.py
````


Important points:
* Your code lives outside the container, and maybe you don't always execute it through the container. So you might have a different pipenv environment that was created using your local system. Make sure you are aware of this.

