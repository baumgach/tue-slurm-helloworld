# Running multiple jobs in parallel 

You can of course use `sbatch` to start multiple jobs simultaneously by running it multiple times, for example, with different parameters. 

However, Slurm also offers a convenient possibility to run multiple jobs for an array of parameters which we will explore in this tutorial. 

## Running multiple jobs sequentially 

Our `multiply.py` script has a `--random-seed` option to start the random matrix generation with different random seeds. Say we want to run the code with 5 different random seeds, a common problem when evaluating machine learning problems. 

Note, that the bottom half of the deploy scripts (e.g. [src/deploy-with-conda.sh](/src/deploy-with-conda.sh), are just regular bash. So there is nothing keeping us from using a bash for loop in our `sbatch` deployment script. 

For example, in [src/deploy-with-conda-multiple.sh](/src/deploy-with-conda-multiple.sh) we could replace
````bash
python3 src/multiply.py --timer_repetitions 10000 --use-gpu
````
with 
````bash
for seed in 1 2 3 4 5
do
   python3 src/multiply.py --timer_repetitions 10000 --use-gpu --random-seed $seed
done
````

With this replacement `deploy-with-conda.sh` would start a single Slurm job that would run `multiply.py` 5 times, one after the other, each time with a different random seed. 

However, it would be neat if we could actually run the 5 jobs in parallel on different GPUs. 

## Running multiple jobs in parallel 

Slurm provides a nice functionality, to explore different parameter ranges like the different random seeds in the example above. Specifically, different parameter ranges can be explored using the `--array` option. 

An example, is given in [src/deploy-with-conda-multiple.sh](/src/deploy-with-conda-multiple.sh). The changes with respect to `deploy-with-conda.sh` are adding the following line to the sbatch arguments:

````bash
#SBATCH --array=0,1,2,3,4
````

and replacing the python call by the following 
````bash
python3 src/multiply.py --timer_repetitions 10000 --use-gpu --random-seed ${SLURM_ARRAY_TASK_ID} 
````

This will start 5 separate jobs each with the different values from the specified array which will be contained in the automatically generated bash variable `${SLURM_ARRAY_TASK_ID}`. 

The example script can be deployed using 

````bash
sbatch src/deploy-with-conda-multiple.sh
````

You can check with `squeue --me` that 5 jobs have in fact been started. 

Learn more about the `--array` option in [this excellent article](https://slurm.schedmd.com/job_array.html).

## What now?

Go back to the [Contents section](/README.md#contents) or learn about [interactive jobs and debugging](/instructions/interactive-jobs.md). 