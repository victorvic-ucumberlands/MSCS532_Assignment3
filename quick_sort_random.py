
#Quick sort implementation with random pivot selection
#args: array; min index, max index
def quick_sort_random(arr, min_idx, max_idx):
    #Base case: array empty or already sorted
    if min_idx >= max_idx:
        return
    
    #check for already sorted array: improve performance on sorted arrays
    
    else:
        sorted = True
        #hopefully this becomes a register to avoid too many memory accesses
        prev_val = arr[min_idx]
        for i in range(min_idx + 1, max_idx + 1):
            curr_val = arr[i]
            if curr_val < prev_val:
                sorted = False
                break
            prev_val = curr_val

        if sorted:
            return


    #Select a random pivot
    pivot_idx = random.randint(min_idx, max_idx)
    pivot = arr[pivot_idx]

    #i: Left of the pivot (less or equal to the pivot)
    i = min_idx
    #j: Right of the pivot (greater than the pivot)
    j = max_idx + 1

    #if the pivot is repeated, it may skew the pariitioning towards the right side
    #To mitigate this, keep track of the number of pivots, and recalculate i at the end of the loop to ensure a more balanced partitioning
    pivot_count = 0


    while i < j:
        if arr[i] <= pivot:
            if arr[i] == pivot:
                pivot_count += 1
            i += 1

        else:
            #Swap arr[i] and arr[j]
            j -= 1
            tmp_val = arr[i]
            arr[i] = arr[j]
            arr[j] = tmp_val

    #Adjust i to account for duplicate pivots
    #i will always be i[pivot[]] + 1 at the end if the loop
    i = i - (pivot_count//2)

    #Recursively sort the subarrays
    quick_sort_random(arr, min_idx, i - 1)
    quick_sort_random(arr, i, max_idx)

#Entry point of the program: accept a csv file containing an array, and output the sorted array to a new csv file
if __name__ == "__main__":
    import csv
    import random
    #Memory profiler
    import tracemalloc
    #Time profiler
    import time

    #Parse arguments from the command line
    import argparse
    parser = argparse.ArgumentParser(description='Sort an array using quick sort with random pivot selection.')
    parser.add_argument('--input_file', type=str, help='The input csv file containing the array to be sorted.')
    parser.add_argument('--output_file', type=str, help='The output csv file to write the sorted array to.')
    args = parser.parse_args()
    #Read the array from the input csv file
    with open(args.input_file, 'r') as f:
        reader = csv.reader(f)
        arr = list(reader)[0]
        arr = [int(x) for x in arr]
    #Sort the array using quick sort with random pivot selection
    start_time = time.time()
    tracemalloc.start()
    quick_sort_random(arr, 0, len(arr) - 1)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    
    tracemalloc.stop()
    #Write the sorted array to the output csv file
    with open(args.output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(arr)

    #Write the stats to a text file 
    #seconds, peak memory usage in KB
    peak_kb = peak / 1024

    with open('stats.txt', 'w') as f:
        f.write(f"{end_time - start_time},{peak_kb}")  



