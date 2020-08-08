# Course: CS261 - Data Structures
# Assignment: 5
# Student: Ryan Jensen
# Description: Implementation of a MinHeap with methods to add to the heap, get the min, remove the min, and build the
# heap with O(n) complexity.

from a5_include import *
from math import floor


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """Adds a new object to the MinHeap."""

        if self.heap.length() == 0:
            self.heap.append(node)
        elif self.heap.length() == 1:
            if self.heap.get_at_index(0) > node:
                self.heap.append(node)
                self.heap.swap(1, 0)
            else:
                self.heap.append(node)
        else:
            # Add new node to back of the linked list and set current index and parent element index
            self.heap.append(node)
            current_index = self.heap.length() - 1
            parent_index = floor(((current_index - 1) / 2))

            # Compare value at parent index to value to insert and swap places if parent is larger than new node value
            while self.heap.get_at_index(parent_index) > node and current_index > 0:
                self.heap.swap(current_index, parent_index)
                current_index = parent_index
                parent_index = floor(((current_index - 1) / 2))

    def get_min(self) -> object:
        """Returns the minimum value object in the heap. Raises an exception for an empty heap."""

        if self.heap.length() == 0:
            raise MinHeapException
        else:
            return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """Returns the minimum value object from the heap and removes it from the heap. Raises exception for an empty
        heap.
        """

        # Empty heap, raise exception
        if self.heap.length() == 0:
            raise MinHeapException
        # Heap with one value, return value
        elif self.heap.length() == 1:
            return self.heap.pop()
        # Heap with two values, find lesser value, saved it, set greater to index zero and remove lesser value
        elif self.heap.length() == 2:
            minimum_value_object = self.heap.get_at_index(0)
            self.heap.swap(0, 1)
            self.heap.pop()
            return minimum_value_object
        # Heap with three values
        elif self.heap.length() == 3:
            minimum_value_object = self.heap.get_at_index(0)
            if self.heap.get_at_index(1) > self.heap.get_at_index(2):
                self.heap.set_at_index(0, self.heap.get_at_index(2))
            else:
                self.heap.set_at_index(0, self.heap.get_at_index(1))
                self.heap.set_at_index(1, self.heap.get_at_index(2))
                self.heap.pop()
            return minimum_value_object
        # Heap with greater than 3 values
        else:
            # Save value of minimum
            minimum_value_object = self.heap.get_at_index(0)

            # Swap first and last values and remove the last from the heap (the minimum value element)
            self.heap.swap(0, self.heap.length() - 1)
            self.heap.pop()

            # If heap is now empty, return the minimum value object
            if self.heap.length() == 0:
                return minimum_value_object
            # Heap is not empty, must place swapped element in correct place
            else:
                # Define current, children indices and values
                current_index = 0
                child_one_index = (2 * current_index) + 1
                child_two_index = (2 * current_index) + 2
                child_one_value = self.heap.get_at_index(child_one_index)
                child_two_value = self.heap.get_at_index(child_two_index)

                # Find minimum child's value and index or the two children
                if child_one_value < child_two_value:
                    minimum = child_one_value
                    minimum_index = child_one_index
                else:
                    minimum = child_two_value
                    minimum_index = child_two_index

                while self.heap.get_at_index(current_index) > self.heap.get_at_index(minimum_index):
                    # Perform swap
                    self.heap.swap(minimum_index, current_index)

                    # Calculate new values/indices for current elements/children elements
                    try:
                        current_index = minimum_index
                        child_one_index = (2 * current_index) + 1
                        child_two_index = (2 * current_index) + 2
                        child_one_value = self.heap.get_at_index(child_one_index)
                        child_two_value = self.heap.get_at_index(child_two_index)
                    except IndexError:
                        break

                    # Find minimum child's value and index or the two children
                    if child_one_value < child_two_value:
                        minimum = child_one_value
                        minimum_index = child_one_index
                    else:
                        minimum = child_two_value
                        minimum_index = child_two_index

            return minimum_value_object

    def build_heap(self, da: DynamicArray) -> None:
        """Receives a dynamic array and builds a proper MinHeap from the objects within. Current content of the MinHeap
        is lost.
        """

        # Clear current contents of MinHeap
        self.heap = DynamicArray()

        # Add all contents from given dynamic array to heap, unsorted
        for i in range(da.length()):
            self.add(da.get_at_index(i))

        def sort_sub_heap(root_node_index):
            """Helper function to sort sub heaps within the MinHeap."""

            # Find indices of children and values of children and root node
            left_child = (2 * root_node_index) + 1
            right_child = (2 * root_node_index) + 2
            left_val = self.heap.get_at_index(left_child)
            right_val = self.heap.get_at_index(right_child)
            root_val = self.heap.get_at_index(root_node_index)

            # Sort sub tree so that root is less than children
            swap = False

            # Find smallest value
            if root_val > left_val:
                smallest = left_val
            else:
                smallest = root_val

            if right_val < smallest:
                smallest = right_val
            else:
                pass

            # Set smallest value to its index in the array/heap
            if smallest == left_val:
                smallest == left_child
            elif smallest == right_val:
                smallest == right_child
            else:
                smallest == root_node_index

            # If the root node is not the smallest, swap so the smallest value is the root node (sub heap sorted)
            if smallest != root_node_index:
                self.heap.swap(smallest, root_node_index)
                swap = True
            else:
                return

            # If we've swapped and there are more elements to percolate through, recursively call to continue sort
            if swap and smallest >= first_non_leaf_element:
                sort_sub_heap(smallest)

        # Find index of first non leaf element
        first_non_leaf_element = floor(da.length() / 2) - 1

        # Sort sub heap of range (first non leaf element through all earlier indices)
        try:
            for i in range(first_non_leaf_element, -1, -1):
                sort_sub_heap(i)
        except IndexError:
            pass
