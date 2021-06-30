# Running python code on SLURM

Most likely, you are interested in running python code remotely. In the example we have seen before, we didn't have any dependencies in our code. Now, however, we move on to the more realistic scenario where you depend on a python installation and a python virtual environment, for example for training a neural network.

The example we look at is simple matrix multiplication, which can be executed on CPU or GPU. The example code can be seen in `04_python_example.py`.

## Editing the code

Have a look at the code and edit the variables that highlighted variables that relate to your system. Remember, the code should be in a remote directory, which you can mount and edit using a local code editor.

## Installing python

The code will eventually be executed with

````
python 04_python_example.py
````

You can do this locally using your local python installation. On the slurm cluster, you will need to specify your own python installation, which the code has access to from all compute nodes. The safest way to do this is using container software such as singularity, which is recommended by the ML cloud administrators. When you use containers, you remove any dependencies to the operating system where the code is executed. You should probably use singularity containers [todo: link future tutorial] as soon as your dependencies get relatively complex. However, if you use python only and have some confidence that the operating system doesn't vary across the cluster nodes, you can probably get away with using a standalone python installation, for example using [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

### Installing Miniconda

To install Miniconda, download the installer script in the link provided above, store it somewhere in your remote home directory and follow the [installation instructions](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent).


### Installing dependencies in virtual environment

WIth your newly installed python and a virtual environment tool of your choice (for example `conda` or `pipenv`), you can now create a virtual environment and install the packages you want there:

````
> conda create -n myenv python
> conda activate myenv
(myenv) > pip install torch numpy
````

In your `sbatch` deploy script `04_python_example.sbatch` you can now simply activate this environment and run your program from within it:

````
...

conda activate myenv
python python_example.py.py

````

You can try this out by running from the slurm headnode `sbatch 04_python_example.sbatch` (as before, don't forget to adjust the logdir paths).
