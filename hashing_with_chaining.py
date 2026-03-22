# Hashing with Chaining implementation in Python
# Using universal hashing function: h(k) = ((a * k + b) mod p) mod m
# where p is a prime number larger than the maximum key value, m is the size of the hash table, and a and b are random integers such that 1 <= a < p and 0 <= b < p
# Chaining is implemented as a linked list to keep insertion and deletion at O(1)-otherwise, python's built in list have O(n) since it needs to shift elements 

import random
#Note: install sympy through pip 
from sympy import primerange


#Node for the linked list in chaining
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    #For init, we can take a set of key:value pairs and insert them into the hash table
    def __init__(self, initial_data=None):
        #default size of the hash table
        self.size = 10000
        #Allocate memory for the hash table
        self.table = [None] * self.size
        #Generate a prime number larger than the table size for the universal hashing function
        self.p = list(primerange(self.size, self.size*100))[0] 
        #Generate constants a and b for the universal hashing function
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

        #If initial data is provided, insert it into the hash table
        if initial_data is not None:
            for key, value in initial_data.items():
                self.insert(key, value)

    #Universal hashing function: h(k) = ((a * k + b) mod p) mod m
    def hash_function(self, key):
        return ((self.a * key + self.b) % self.p) % self.size

    def insert(self, key, value):
        arr_idx = self.hash_function(key)
        new_node = Node(key, value)

        #If this slice is empty, insert the new  node
        if self.table[arr_idx] is None:
            self.table[arr_idx] = new_node
        #If not empty, add it at the end of the linked list 
        else:
            current = self.table[arr_idx]
            #Keep traversing the linked list until we find the end or a node with the same key
            while current is not None:
                if current.key == key:
                    current.value = value 
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = new_node

    def search(self, key):
        #index from hash function
        index = self.hash_function(key)
        current = self.table[index]

        while current is not None:
            #key found, return the value
            if current.key == key:
                return current.value
            current = current.next
        #Return False if key not found
        return False

    def delete(self, key):
        #index from hash function
        index = self.hash_function(key)
        #Start on first element
        current = self.table[index]
        prev = None

        while current is not None:
            if current.key == key:
                if prev is None:
                    #First element matched, update the head of the linked list
                    self.table[index] = current.next 
                else:
                    #Delete current by updating the pointer of the previous node to skip current
                    prev.next = current.next
                return True #Key found and deleted
            prev = current
            current = current.next

        return False #Key not found, nothing deleted

#Entry point of the program: accept a csv file containing key:value pairs, and an operation (insert, search, delete), and output the time taken for the operation to a text file
if __name__ == "__main__":
    import argparse
    import csv
    import time
    import tracemalloc

    parser = argparse.ArgumentParser(description='Hashing with Chaining')
    parser.add_argument('--input_file', type=str, required=True, help='CSV file containing key:value pairs')
    parser.add_argument('--insert', nargs=2, type=int, help='Key and value to insert')
    parser.add_argument('--search', type=int, help='Key to search')
    parser.add_argument('--delete', type=int, help='Key to delete')
    args = parser.parse_args()
    #Read key:value pairs from the input csv file
    key_value_pairs = {}
    with open(args.input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            key_value_pairs[int(row[0])] = int(row[1])
    
    #Initialize the hash table with the key:value pairs
    hash_table = HashTable(key_value_pairs)
    #Perform the specified operation and measure time 
    if args.insert is not None:
        start_time = time.time()
        hash_table.insert(args.insert[0], args.insert[1])
        end_time = time.time()
        with open('stats.txt', 'w') as f:
            f.write(f"{end_time - start_time}")
        print (f"Inserted key {args.insert[0]} with value {args.insert[1]}")
    
    elif args.search is not None:
        start_time = time.time()
        result = hash_table.search(args.search)
        end_time = time.time()
        with open('stats.txt', 'w') as f:
            f.write(f"{end_time - start_time}")
        print (f"Search result for key {args.search}: {result}")
    
    elif args.delete is not None:
        start_time = time.time()
        result = hash_table.delete(args.delete)
        end_time = time.time()
        with open('stats.txt', 'w') as f:
            f.write(f"{end_time - start_time}")
        print (f"Delete result for key {args.delete}: {result}")


