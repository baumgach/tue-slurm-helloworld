import torch
from timeit import timeit
import argparse


def time_multiplication(timer_repetitions, use_gpu=True):

    # Create tensors
    x = torch.randn(32, 40000)
    y = torch.randn(40000, 32)
    
    # Check if Cuda available and move tensor to Cuda if yes
    cuda_available = torch.cuda.is_available() 
    print(f"Cuda_available={cuda_available}")
    if cuda_available and use_gpu:
        device = torch.cuda.current_device()
        print(f"Current Cuda device: {device}")
        x = x.to(device)
        y = y.to(device)

    # Multiply matrix first once for result and then multiple times for measuring elapsed time
    mult = torch.matmul(x, y)
    elapsed_time = timeit(lambda: torch.matmul(x, y), number=timer_repetitions)

    return mult, elapsed_time


if __name__ == "__main__":
    
    #####################################################################################################  
    # Adapt these variables as needed:
    
    # Caveat: Please adapt the path to somewhere you have write access
    # Caveat: If you execute the code from a container, make sure you bind the directory you write to
    results_file = 'path/to/experiments/results.txt'
    use_gpu = False
    #####################################################################################################

    
    # Measure matrix multiplication time
    mult, elapsed_time = time_multiplication(timer_repetitions=100, use_gpu=use_gpu)

    # Print some results:
    print("result:")
    print(mult)
    print("Output shape", mult.shape)
    print(f"elapsed time: {elapsed_time}")
    
    with open(results_file, 'w') as fhandle:
        fhandle.write(f"elapsed time: {elapsed_time}")
    
    print("done.")
    