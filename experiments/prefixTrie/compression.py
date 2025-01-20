import time
import gc
from pympler import asizeof
from memory_profiler import profile
from structures.prefix_trie import PrefixTrie, lz_compress
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

dataset_paths = {
    "small": os.path.join(ROOT_DIR, "datasets/compression/random_words_small.txt"),
    "medium": os.path.join(ROOT_DIR, "datasets/compression/random_words_medium.txt"),
    "large": os.path.join(ROOT_DIR, "datasets/compression/random_words_large.txt"),
}

def load_dataset(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()

def measure_time_on_dataset(dataset_path):
    dataset = load_dataset(dataset_path)
    times = [] 
    memory_usage = []
    compressed_data = []

    for input_string in dataset:
        trie = PrefixTrie() 

        start_time = time.time()
        compressed = lz_compress(trie, input_string)
        elapsed_time = time.time() - start_time

        compressed_data.append(compressed)
        times.append(elapsed_time)

        trie_size = asizeof.asizeof(trie)
        memory_usage.append(trie_size)

        del trie
        gc.collect()

    total_time = sum(times)
    return total_time, compressed_data, times, memory_usage

def process_datasets():
    for size, path in dataset_paths.items():
        print(f"\nProcessing {size} dataset from '{path}'...")

        total_time, compressed_data, times, memory_usage = measure_time_on_dataset(path)
        print(f"  Total time for compression: {total_time:.6f} seconds")
        print(f"  Average time per string: {sum(times)/len(times):.6f} seconds")
        print(f"  Average memory used per trie: {sum(memory_usage)/len(memory_usage) / 1024:.2f} KB")
        print(f"  Times per string (first 5 shown): {times[:5]} seconds")
        print(f"  Memory per string (first 5 shown): {[f'{mem / 1024:.2f}' for mem in memory_usage[:5]]} KB")


if __name__ == "__main__":
    @profile
    def run_with_memory_profiling():
        process_datasets()
        

    run_with_memory_profiling()
