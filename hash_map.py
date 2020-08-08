# Course: CS261 - Data Structures
# Assignment: 5 - Part 1
# Student: Ryan Jensen
# Description: An implementation of a hash map with methods to clear, get, resize, put, remove, get keys, check if keys
# are in the hash table, check the number of empty buckets, and get the load value of the table.

from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    """

    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """Init new HashMap based on DA with SLL for collision resolution"""

        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """Return content of hash map t in human-readable form"""

        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """Clears the content of the hash map. Does not alter underlying capacity."""

        # Find all keys and store in dynamic array object
        key_array = self.get_keys()

        # Increment through keys, removing key/value pairs from hash map until dynamic array is empty
        while key_array.length() != 0:
            key_to_remove = key_array.pop()
            self.remove(key_to_remove)

    def get(self, key: str) -> object:
        """Returns the value associated with the given key, if key is not in hash map, returns None."""

        # Hash the input value to get index
        hashed_key = self.hash_function(key)
        index = hashed_key % self.buckets.length()

        bucket = self.buckets.get_at_index(index)

        # Search bucket for matching key, return value if found, None if not found
        if bucket.contains(key):
            for node in bucket:
                if node.key == key:
                    return node.value
        else:
            return None

    def put(self, key: str, value: object) -> None:
        """Updates the key/value pair in the hash map. If given key already exists, it's associated value should be
        replaced with the new value. Otherwise, a key/value pair should be added.
        """

        # Hash the input value to get index
        hashed_key = self.hash_function(key)
        index = hashed_key % self.buckets.length()

        bucket = self.buckets.get_at_index(index)

        # Check for key already in use, in which case update value
        if bucket.contains(key):
            bucket.remove(key)
            bucket.insert(key, value)
        # Key not already in use, create new key/value pair
        else:
            bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """Removes the given key and it's associated value from the hash map. If given not found, does nothing."""

        if not self.contains_key(key):
            return
        else:
            # Hash the input value to get index
            hashed_key = self.hash_function(key)
            index = hashed_key % self.buckets.length()

            bucket = self.buckets.get_at_index(index)

            # Search bucket for matching key, remove key/value pair, decrement hash map size
            for node in bucket:
                if node.key == key:
                    bucket.remove(key)
                    self.size -= 1

    def contains_key(self, key: str) -> bool:
        """Returns True if the given key is in the hash map, otherwise returns False."""

        # Hash the input value to get index
        hashed_key = self.hash_function(key)
        index = hashed_key % self.buckets.length()

        bucket = self.buckets.get_at_index(index)

        # Search bucket for matching key, return True if found
        for node in bucket:
            if node.key == key:
                return True
        return False

    def empty_buckets(self) -> int:
        """Returns the number of empty buckets in the hash table."""

        empty_buckets_count = 0

        # Check for empty linked list in buckets
        for z in range(self.capacity):
            bucket = self.buckets.get_at_index(z)
            if bucket.length() == 0:
                empty_buckets_count += 1

        return empty_buckets_count

    def table_load(self) -> float:
        """Returns current hash table load factor. (Average number of elements in each bucket.)"""

        load = float(self.size/self.buckets.length())

        return load

    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the hash table. All key/value pairs must remain in the new hash map and links must
        be rehashed. If new capacity is less than one, this method does nothing."""

        # Create new hash map with desired capacity and same hash function
        temp_hash_map = HashMap(new_capacity, self.hash_function)

        if new_capacity < 1:
            return

        # Store all the keys
        key_array = self.get_keys()
        key_array_copy = self.get_keys()

        # Iterate through keys list, rehashing and adding key/value pairs to temporary hash map
        while key_array.length() != 0:
            old_key = key_array.pop()
            value = self.get(old_key)
            temp_hash_map.put(old_key, value)

        # Clear hash map contents
        self.clear()

        # Add buckets and update capacity
        capacity_difference = new_capacity - self.capacity
        # Growing capacity
        if capacity_difference > 0:
            for i in range(capacity_difference):
                self.buckets.append(LinkedList())
        # Shrinking capacity
        elif capacity_difference < 0:
            self.buckets = DynamicArray()
            for i in range(new_capacity):
                self.buckets.append(LinkedList())

        self.capacity = new_capacity

        # Iterate through keys list, rehashing and adding key/value pairs to new sized hash map
        while key_array_copy.length() != 0:
            old_key = key_array_copy.pop()
            value = temp_hash_map.get(old_key)
            self.put(old_key, value)

    def get_keys(self) -> DynamicArray:
        """Returns a DynamicArray that contains all keys stored in the hash map."""

        key_array = DynamicArray()

        # Iterate through keys in each bucket, storing those keys in a dynamic array
        for z in range(self.capacity):
            bucket = self.buckets.get_at_index(z)
            for x in bucket:
                key_array.append(x.key)

        return key_array
