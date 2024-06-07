import mysql.connector
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Users/dell/Downloads/windows_10_cmake_Release_Graphviz-10.0.1-win64/Graphviz-10.0.1-win64/bin'
if os.path.exists("graph.png"):
    os.remove("graph.png")
if os.path.exists("graph.pdf"):
    os.remove("graph.pdf")


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Graph:
    def __init__(self):
        self.vertices = []
        self.adj_list = {}
        self.edges = []

    def add_node(self, vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.adj_list[vertex] = []

    def remove_node(self, vertex_id):
        for vertex in self.vertices:
            if vertex.user_id == vertex_id:
                self.vertices.remove(vertex)
                del self.adj_list[vertex]
                break  

        for key, edges in self.adj_list.items():
            self.adj_list[key] = [edge for edge in edges if edge.end.user_id != vertex_id]

    def add_edge(self, start, end):
        if start in self.vertices and end in self.vertices:
            new_edge = Edge(start, end)
            self.edges.append(new_edge)
            self.adj_list[start].append(new_edge)

    def remove_edge(self, start_id, end_id):
        for edge in self.edges:
            if edge.start.user_id == start_id and edge.end.user_id == end_id:
                self.edges.remove(edge)
                self.adj_list[edge.start].remove(edge)
                break

    def bfs(self):
        start_vertex=self.vertices[0]
        visited = set()
        queue = [start_vertex]
        result = []
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                result.append(vertex)
                visited.add(vertex)
                queue.extend(edge.end for edge in self.adj_list[vertex] if edge.end not in visited)
        return result

    def dfs(self, start_vertex):
        visited = set()
        stack = [start_vertex]
        result = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                result.append(vertex)
                visited.add(vertex)
                stack.extend(edge.end for edge in self.adj_list[vertex] if edge.end not in visited)
        return result
    
    def graph_size(self):
        return len(self.adj_list)

    def print_graph(self):
        for vertex, neighbors in self.adj_list.items():
            vertex_name = vertex.name
            neighbor_names = [edge.end.name for edge in neighbors]
            print(f"Vertex {vertex_name}: {neighbor_names}")
        edge_str = ", ".join([f"({edge.start.name}, {edge.end.name})" for edge in self.edges])
        print(f"Edges: {edge_str}")
        print([x.name for x in self.vertices])
        
    def show_followers(self, username):
        user = next((vertex for vertex in self.vertices if vertex.name == username), None)
        if not user:
            print(f"User '{username}' not found.")
            return
        
        followers = [edge.start.name for edge in self.edges if edge.end == user]
        
        return followers
        
    def show_following(self, username):
        user = next((vertex for vertex in self.vertices if vertex.name == username), None)
        if not user:
            print(f"User '{username}' not found.")
            return
        
        following = [edge.end.name for edge in self.adj_list[user]]
        return following
        
        
def construct_graph_from_mysql(cursor):
    graph = Graph()  
    cursor.execute("SELECT username FROM user")
    users = cursor.fetchall()
    
    for user in users:
        user_id = users.index(user) + 1  
        username = user[0]
        graph.add_node(User(username, user_id))
    
    cursor.execute("SELECT username, following FROM following")
    for row in cursor.fetchall():
        friend, follower = row
        user_friend = next((user for user in graph.vertices if user.name == friend), None)
        user_follower = next((user for user in graph.vertices if user.name == follower), None)
        if user_friend and user_follower:
            graph.add_edge(user_friend, user_follower)
    
    return graph

def showgraph():
    dot = Digraph()
    
    for vertex in graph2.vertices:
        dot.node(str(vertex.user_id), vertex.name)
    
    for edge in graph2.edges:
        dot.edge(str(edge.start.user_id), str(edge.end.user_id))
    
    dot.render('graph2', format='png', cleanup=True)
    dot.view()

conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Krishna@27',
            database='dsa'
        )

cursor = conn.cursor()

graph2 = construct_graph_from_mysql(cursor)
cursor.close()
conn.close()






