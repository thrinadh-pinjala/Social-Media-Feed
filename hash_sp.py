import mysql.connector

class Node: 
    def __init__(self, key, value): 
        self.key = key 
        self.value = value 
        self.next = None
  
class HashTable: 
    def __init__(self, capacity): 
        self.capacity = capacity 
        self.size = 0
        self.table = [None] * capacity 
  
    def _hash(self, key): 
        return hash(key) % self.capacity 
  
    def insert(self, key, value): 
        index = self._hash(key) 
  
        if self.table[index] is None: 
            self.table[index] = Node(key, value) 
            self.size += 1
        else: 
            current = self.table[index] 
            while current: 
                if current.key == key: 
                    current.value = value 
                    return
                current = current.next
            new_node = Node(key, value) 
            new_node.next = self.table[index] 
            self.table[index] = new_node 
            self.size += 1
  
    def search(self, key): 
        index = self._hash(key) 
  
        current = self.table[index] 
        while current: 
            if current.key == key: 
                return current.value 
            current = current.next
  
        raise KeyError(key) 
  
    def remove(self, key): 
        index = self._hash(key) 
  
        previous = None
        current = self.table[index] 
  
        while current: 
            if current.key == key: 
                if previous: 
                    previous.next = current.next
                else: 
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current 
            current = current.next
  
        raise KeyError(key) 
  
    def __len__(self): 
        return self.size 
  
    def __contains__(self, key): 
        try: 
            self.search(key) 
            return True
        except KeyError: 
            return False
    
    def __iter__(self):
        self.current_index = 0
        self.current_node = self.table[self.current_index]
        return self

    def __next__(self):
        while self.current_index < self.capacity:
            if self.current_node:
                key = self.current_node.key
                value = self.current_node.value
                self.current_node = self.current_node.next
                return key, value
            else:
                self.current_index += 1
                if self.current_index < self.capacity:
                    self.current_node = self.table[self.current_index]
        raise StopIteration


def gethash():
    ht = HashTable(100)
    try:
        db_connection = mysql.connector.connect(host='localhost', port=3306, user='root',
                                                 password='Krishna@27',
                                                 database='dsa')
        
        cursor = db_connection.cursor()
        cursor.execute("SELECT username, password FROM Passwords")
        rows = cursor.fetchall()
        for row in rows:
            ht.insert(row[0], row[1])
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()
    return ht


def checkpass(ht, u, p):
    if u in ht:
        return p == ht.search(u)
    return False
