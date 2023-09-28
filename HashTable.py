# Chaining hash table to store package data
class HashTable:
    # Constructor with initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, capacity=10):
        # initializes the hash table with empty bucket list entries.
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, package):
        # gets the bucket list this item goes to.
        bucket = hash(package.ID) % len(self.table)

        # inserts the item to the end of the bucket list.
        self.table[bucket].append(package)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, p_id):
        # gets the bucket list this key would be in.
        bucket = hash(p_id) % len(self.table)

        # searches for the key in the bucket list
        for p in self.table[bucket]:
            if p.ID == p_id:
                return p
        return None
