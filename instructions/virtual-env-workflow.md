# Using Conda environments instead of Singularity

In this section, we will describe an example worklow for setting up a virtual python environment and then running the `multiply.py` code which relies on PyTorch and some other libraries. 

For many this may be a more accessible workflow compared to the [Singularity based approach](/instructions/singularity-workflow.md). However, for some cases it may be lacking in flexibility, especially if you need you need special libraries or a custum operating system for your experiments. 

In the following we will describe a [Conda](https://docs.conda.io/en/latest/)-based workflow in more detail and will then give a brief alternative workflow using [virtualenv](https://virtualenv.pypa.io/en/latest/). 

## What is Conda in a Nutshell

[Conda](https://docs.conda.io/en/latest/) is and environment manager for Python and other languages. It allows you to create and activate virtual environments in which you can install Python packages. The advantage is that the packages will not be installed globally on your machine, but only in this environment. This means you can use different versions of packages for different projects. 

One drawback with respect to Singularity is that you can only influence the version of Python and Python packages, but not for example Cuda or the operating system. Usually, this isn't a problem, however. 

Like Singularity, Conda is already installed on the Slurm login nodes. 

## Setting up a Conda environment 

Again make sure you are on the Slurm login node and move to the home directory (if you aren't already there)

````
cd 
````

Make a Conda environment called `myenv` 

````
conda create -n myenv 
````

and confirm with `y`. 

Activate the new environment using 

````
conda activate myenv
````

Let's see which Python version we have by default.

````
python --version 
````

That is the system-wide Python version and is at the time of writing pretty old (2.7.5). We can instead install whichever specific Python version we like. For example

````
conda install python==3.9
````

We can install packages using `conda install` or `pip install`. `conda install` works for some stuff `pip install` doesn't and vice versa. 

So mimicking the dependencies in our `deeplearning.def` from the Singularity tutorial: 

````
conda install numpy matplotlib ipython pytorch torchvision 
````

The debugging package `ipdb` is not available using conda by default, so we have to use `pip install` instead:

````
pip install ipdb
````

## Other conda commands 

There are many other useful Conda commands for managing your packages and environments such as 
  * `conda env list` for displaying all existing environments
  * `conda env remove --name myenv` for deleting an environment

Have a look at this helpful [cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).

## Running the code 

As before we can now run our matrix multiplication code directly on the login node without GPU. 

````
cd $WORK/tue-slurm-helloworld
python src/multiply.py --timer_repetitions 10000 --no-gpu 
````

But of course we would rather submit this as a job with GPU usage. For this, I prepared another deploy script. 

````
sbatch src/deploy-with-conda.sh
````

The results will be written to the newly created `logs` directory which should have been created in your current working directory. You can list the files sorted by most recent and some useful extra information using 

````
ls -ltrh 
````

You can then look at the output log file and error file corresponding to your job using the `cat` or `less` commands. For example:

````
cat logs/hostname_<job-id>.out
````

## Alternative workflow using virtualenv 

The following describes the equivalent of the above in virtualenv. 

Setting up the environment

```` 
virtualenv -p python3 env 
source env/bin/activate
pip install --upgrade pip
pip install numpy matplotlib ipython torch torchvision ipdb
````

Deactivating the environment
````
deactivate
````

Running the code 

````
sbatch src/deploy-with-virtualenv.sh
````

## What now?

Go back to the [Contents section](/README.md#contents), continue with the more flexible  [Singularity](/instructions/singularity-workflow.md) based workflow, or learn about [interactive jobs and debugging](/instructions/interactive-jobs.md). 