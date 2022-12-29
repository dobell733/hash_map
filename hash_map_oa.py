from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Receives a key and value as parameters.
        Updates the key/value pair in the hash map.
        If given key already exists in the hash map, its associated value is replaced with the new value.
        If given key is not in the hash map, a new key/value pair is added.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash_index = self._hash_function(key) % self._capacity
        starting_hash = hash_index
        j = 1
        while self._buckets[hash_index] is not None:
            if self._buckets[hash_index].key == key or self._buckets[hash_index].is_tombstone is True:
                self._buckets[hash_index] = HashEntry(key, value)
                self._size -= 1
                break
            else:
                hash_index = (starting_hash + (j**2)) % self._capacity
                j += 1
        self._size += 1
        self._buckets[hash_index] = HashEntry(key, value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty = 0

        for i in range(self._buckets.length()):
            if self._buckets[i] is None:
                empty += 1

        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Receives new capacity as a parameter.
        Changes the capacity of the internal hash table.
        """
        if new_capacity < self._size:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        old_arr = self._buckets
        old_arr_capacity = self._capacity
        self._capacity = new_capacity
        new_arr = DynamicArray()
        self._buckets = new_arr
        self._size = 0

        for _ in range(self._capacity):
            self._buckets.append(None)

        for i in range(old_arr_capacity):
            if old_arr[i] is not None and old_arr[i].is_tombstone == False:
                entry = old_arr[i]
                self.put(entry.key, entry.value)

    def get(self, key: str) -> object:
        """
        Receives key as parameter.
        Returns the value associated with the given key.
        """
        hash_index = self._hash_function(key) % self._capacity
        starting_hash = hash_index
        j = 1
        while self._buckets[hash_index]:
            if self._buckets[hash_index].key == key and self._buckets[hash_index].is_tombstone == False:
                return self._buckets[hash_index].value
            else:
                hash_index = (starting_hash + (j ** 2)) % self._capacity
                j += 1

    def contains_key(self, key: str) -> bool:
        """
        Receives key as a parameter.
        Returns True if the given key is in the hash map, False otherwise.
        """
        if self.get(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Receives key as a parameter.
        Removes the given key and its associated value from the hash map.
        """
        if self.get(key) is not None:
            hash_index = self._hash_function(key) % self._capacity
            starting_hash = hash_index
            j = 1
            while self._buckets[hash_index]:
                if self._buckets[hash_index].key == key and self._buckets[hash_index].is_tombstone == False:
                    self._buckets[hash_index].is_tombstone = True
                    self._size -= 1
                    break
                else:
                    hash_index = (starting_hash + (j ** 2)) % self._capacity
                    j += 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        Does not change the underlying hash table capacity.
        """
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        Order isn't guaranteed in the returned array.
        """
        return_arr = DynamicArray()

        for i in range(self._capacity):
            curr_element = self._buckets[i]
            if curr_element is not None and curr_element.is_tombstone is False:
                return_arr.append((curr_element.key, curr_element.value))

        return return_arr

    def __iter__(self):
        """
        Enables the HashMap to iterate across itself.
        """
        for i in range(self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                self._index = i
                break

        for i in range(self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                self._greatest = i

        return self

    def __next__(self):
        """
        Returns the next item in the HashMap, based on the current location of the iterator.
        """
        if self._index > self._greatest:
            raise StopIteration
        else:
            value = self._buckets[self._index]

        for i in range(self._index + 1, self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                self._index = i
                break
            # allow the loop to go one index past the last existing element in order to raise StopIteration above
            self._index = i

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
