import mysql.connector
class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data,end=" ")
            current = current.next
        print()
def likedby(post_id): 
    db_connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Krishna@27',
        database='dsa'
    ) 
    cursor = db_connection.cursor()
    cursor.execute("SELECT liked_by FROM likes WHERE post_id = %s", (post_id,))
    rows = cursor.fetchall()
    
    l = LinkedList()
    for row in rows:
        l.insert(row[0])
    
    cursor.close()
    db_connection.close()
    
    # Convert LinkedList to a list
    likes_list = []
    current = l.head
    while current:
        likes_list.append(current.data)
        current = current.next
    
    return likes_list


def insert_like(post_id, username):
    try:
        db_connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Krishna@27',
            database='dsa'
        )

        cursor = db_connection.cursor()
        insert_query = "INSERT INTO likes (post_id, liked_by) VALUES (%s, %s)"
        like_data = (post_id, username)
        cursor.execute(insert_query, like_data)
        db_connection.commit()
        
        cursor.close()
        db_connection.close()
        
        return True  # Indicate successful insertion
    except mysql.connector.Error as err:
        
        return False  # Indicate failure




