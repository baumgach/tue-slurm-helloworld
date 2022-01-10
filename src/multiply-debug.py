import torch
from timeit import timeit
import argparse

def time_multiplication(
    timer_repetitions,
    use_gpu=True,
    data_path="/mnt/qb/baumgartner/storagetest.txt",
    random_seed=0
):

    # Simulate external data access by reading the matrix size from external file
    with open(data_path) as f:
        s = int(f.read())

    # Set random seed
    torch.manual_seed(random_seed)

    # Create tensors
    x = torch.randn(32, s)
    y = torch.randn(s, 32)
    
    import ipdb
    ipdb.set_trace()

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

    # Print some results:
    print("result:")
    print(mult)
    print("Output shape", mult.shape)
    print(f"elapsed time: {elapsed_time}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Tescript for Singularity and SLURM on GPU. It times the multiplication of two matrices, repeated `timer_repetition` times."
    )
    parser.add_argument(
        "--timer_repetitions", dest="timer_repetitions", action="store", default=1000, type=int, help="How many times to repeat the multiplication.",
    )
    parser.add_argument('--use-gpu', dest='use_gpu', action='store_true')
    parser.add_argument('--no-gpu', dest='use_gpu', action='store_false')
    parser.set_defaults(use_gpu=True)
    parser.add_argument(
        "--random-seed", dest="random_seed", action="store", default=0, type=int, help="Random seed for sampling random matrices.",
    )
    args = parser.parse_args()

    # Run main function with command line input, to test singularity arguments
    time_multiplication(
        timer_repetitions=args.timer_repetitions, 
        use_gpu=args.use_gpu, 
        random_seed=args.random_seed,
        )

    print("done.")