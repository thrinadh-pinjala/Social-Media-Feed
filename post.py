import mysql.connector
class Post:
    def __init__(self, username,post_id, content, timestamp):
        self.username=username
        self.post_id = post_id
        self.content = content
        self.timestamp = timestamp
        self.likes_count = 0
        self.comments_count = 0

class PostHeap:
    def __init__(self):
        self.heap = []
    
    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def push(self, post):
        self.heap.append(post)
        self.heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        self.swap(0, len(self.heap) - 1)
        post = self.heap.pop()
        self.heapify_down(0)
        return post

    def heapify_up(self, index):
        while index > 0 and self.heap[index].timestamp > self.heap[self.parent(index)].timestamp:
            self.swap(index, self.parent(index))
            index = self.parent(index)

    def heapify_down(self, index):
        while True:
            left_child_idx = self.left_child(index)
            right_child_idx = self.right_child(index)
            largest = index
            if (left_child_idx < len(self.heap) and 
                self.heap[left_child_idx].timestamp > self.heap[largest].timestamp):
                largest = left_child_idx
            if (right_child_idx < len(self.heap) and 
                self.heap[right_child_idx].timestamp > self.heap[largest].timestamp):
                largest = right_child_idx
            if largest != index:
                self.swap(index, largest)
                index = largest
            else:
                break

    def peek(self):
        if self.heap:
            return self.heap[0]
        return None

    def is_empty(self):
        return len(self.heap) == 0
    
    
    
    def merge_heaps(self, other_heap):
        """
        Merges the current heap with another heap.
        """
        merged = [None] * (len(self.heap) + len(other_heap.heap))
        self._merge_arrays(merged, self.heap, other_heap.heap)
        self.heap = merged
        self.build_max_heap(len(merged))

    def _max_heapify(self, arr, n, idx):
        left = 2 * idx + 1
        right = 2 * idx + 2
        largest = idx

        if left < n and arr[left].timestamp > arr[largest].timestamp:
            largest = left
        if right < n and arr[right].timestamp > arr[largest].timestamp:
            largest = right

        if largest != idx:
            arr[idx], arr[largest] = arr[largest], arr[idx]
            self._max_heapify(arr, n, largest)

    def build_max_heap(self, n):
        for i in range((n // 2) - 1, -1, -1):
            self._max_heapify(self.heap, n, i)

    def _merge_arrays(self, merged, arr1, arr2):
        for i in range(len(arr1)):
            merged[i] = arr1[i]
        for i in range(len(arr2)):
            merged[len(arr1) + i] = arr2[i]
# Example Usage:
    '''
post_heap = PostHeap()



post1 = Post("post001", "Hello World!", "2024-05-11 10:00:00")
post2 = Post("post002", "How is everyone doing?", "2024-05-11 11:00:00")
post3 = Post("post003", "This is a new post", "2024-05-11 09:00:00")
post_heap.push(post1)
post_heap.push(post2)
post_heap.push(post3)

# Displaying posts in descending order of time
while not post_heap.is_empty():
    post = post_heap.pop()
    print(f"Post ID: {post.post_id}, Timestamp: {post.timestamp}")
 '''


def showpost(u_id):
    db_connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Krishna@27',
        database='dsa'
    )
    cursor = db_connection.cursor()
    cursor.execute("SELECT post_id,username, contents, time FROM posts WHERE username = %s", (u_id,))
    rows = cursor.fetchall()
    post_heap = PostHeap()
    
    for row in rows:
        post_heap.push(Post(row[1],row[0], row[2], row[3]))
    cursor.close()
    db_connection.close()
    return post_heap
   
def printheap(post_heap):
    while not post_heap.is_empty():
        post = post_heap.pop()
        print(f"User ID:{post.username},Post ID: {post.post_id},content: {post.content}, Timestamp: {post.timestamp}")
        
        
def add_post(post):
        """
        Adds a new post to MySQL database and to the heap.
        """
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Krishna@27',
            database='dsa'
        )
        cursor = db_connection.cursor()

        # Insert the post into MySQL
        insert_query = "INSERT INTO posts (username, contents, time) VALUES (%s, %s, %s)"
        post_data = (post.username, post.content, post.timestamp)
        cursor.execute(insert_query, post_data)
        db_connection.commit()

        # Close MySQL connection
        cursor.close()
        db_connection.close()