class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Метод delete
    def delete(self, key):
        key_hash = self.hash_function(key)
        # Якщо ключ знайдено
        if self.table[key_hash] is not None:
            # Перебор всіх пар у відповідному кошику
            for i in range(len(self.table[key_hash])):
                # Якщо ключ збігається
                if self.table[key_hash][i][0] == key:
                    # Видалення пари за індексом та підтвердження
                    self.table[key_hash].pop(i)
                    return True
        # Якщо ключ не знайдено
        return False
