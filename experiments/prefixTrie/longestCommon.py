import time
import gc
from pympler import asizeof
from memory_profiler import profile
from structures.prefix_trie import PrefixTrie
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

dataset_paths = {
    "small": os.path.join(ROOT_DIR, "datasets/longestCommon/word_pairs_with_common_pattern_small.csv"),
    "medium": os.path.join(ROOT_DIR, "datasets/longestCommon/word_pairs_with_common_pattern_medium.csv"),
    "large": os.path.join(ROOT_DIR, "datasets/longestCommon/word_pairs_with_common_pattern_large.csv"),
}


def load_dataset(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()

@profile
def measure_time_on_dataset(dataset_path):
    dataset = load_dataset(dataset_path)
    times = []
    memory_usage = []
    results = []

    for i in range(len(dataset) - 1):
        str1, str2 = dataset[i].split(',')

        trie = PrefixTrie()
        trie.insert(str1) 

        start_time = time.time()
        lcs = trie.find_longest_common_substring(str2)
        elapsed_time = time.time() - start_time

        results.append(lcs)
        times.append(elapsed_time)

        current_memory = asizeof.asizeof(locals())
        memory_usage.append(current_memory)

        gc.collect()

    total_time = sum(times)
    return total_time, results, times, memory_usage

def process_datasets():
    for size, path in dataset_paths.items():
        print(f"\nProcessing {size} dataset from '{path}'...")

        total_time, results, times, memory_usage = measure_time_on_dataset(path)
        print(f"  Total time for computation: {total_time:.6f} seconds")
        print(f"  Average time per string pair: {sum(times)/len(times):.6f} seconds")
        print(f"  Average memory used per computation: {sum(memory_usage)/len(memory_usage) / 1024:.2f} KB")
        print(f"  Times per pair (first 5 shown): {times[:5]} seconds")
        print(f"  Memory per pair (first 5 shown): {[f'{mem / 1024:.2f}' for mem in memory_usage[:5]]} KB")
        print(f"  Results (first 5 shown): {results[:5]}")

if __name__ == "__main__":
    @profile
    def run_with_memory_profiling():
        process_datasets()

    run_with_memory_profiling()
