import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import hash
import post  # Import the post module
from post import Post  
import likes
from datetime import datetime
import mysql.connector
import graph as graph_module  # Import the module that contains the Graph class and the graph2 instance

# Function Definitions
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if hash.checkpass(hashtable, username, password):
        global current_user
        current_user = username
        show_homepage()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def show_homepage():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="#fafafa")
    frame.pack(expand=True, fill='both')
    
    tk.Label(frame, text=f"Welcome, {current_user}", font=("Helvetica", 18, "bold"), bg="#fafafa").pack(pady=20)

    buttons = [
        ("Show My Posts", show_my_posts),
        ("Show Followers", show_followers),
        ("Show Following", show_following),
        ("See Feed", see_feed),
        ("Show Likes", show_likes),
        ("Add Post", add_post_window),
        ("Add Like", add_like),
        ("Show Graph", show_graph)
    ]

    button_frame = tk.Frame(frame, bg="#fafafa")
    button_frame.pack(pady=20)

    for text, command in buttons:
        btn = ttk.Button(button_frame, text=text, command=command)
        btn.pack(pady=5, fill='x')

def show_my_posts():
    posts = post.showpost(current_user)
    display_posts(posts)

def display_posts(posts):
    posts_window = tk.Toplevel(root)
    posts_window.title("My Posts")
    posts_window.geometry("600x400")
    posts_window.configure(bg="#fafafa")
    
    frame = tk.Frame(posts_window, bg="#fafafa")
    frame.pack(expand=True, fill='both', padx=10, pady=10)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_area = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg="#fafafa", font=("Helvetica", 12))
    text_area.pack(expand=True, fill='both')
    
    scrollbar.config(command=text_area.yview)
    
    while not posts.is_empty():
        post_item = posts.pop()
        post_content = f"User ID: {post_item.username}\nPost ID: {post_item.post_id}\nContent: {post_item.content}\nTimestamp: {post_item.timestamp}\n\n"
        text_area.insert(tk.END, post_content)

def show_followers():
    try:
        followers = graph_module.graph2.show_followers(current_user)
        if followers:
            followers_list = '\n'.join(followers)
            messagebox.showinfo("Followers", f"Followers of '{current_user}':\n{followers_list}")
        else:
            messagebox.showinfo("Followers", f"'{current_user}' has no followers.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching followers: {str(e)}")

def show_following():
    try:
        following = graph_module.graph2.show_following(current_user)
        if following:
            following_list = '\n'.join(following)
            messagebox.showinfo("Following", f"Following of '{current_user}':\n{following_list}")
        else:
            messagebox.showinfo("Following", f"'{current_user}' is not following anyone.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching following users: {str(e)}")

def see_feed():
    following = graph_module.graph2.show_following(current_user)
    postheap1 = post.showpost(following[0])
    for user in following[1:]:
        postheap1.merge_heaps(post.showpost(user))
    display_posts(postheap1)

def show_likes():
    post_heap = post.showpost(current_user)
    while not post_heap.is_empty():
        post_item = post_heap.pop()
        liked_by = likes.likedby(post_item.post_id)
        messagebox.showinfo("Post Likes", f"Post ID: {post_item.post_id}, Liked by: {liked_by}")

def add_post_window():
    add_post_window = tk.Toplevel(root)
    add_post_window.title("Add Post")
    add_post_window.geometry("400x200")
    add_post_window.configure(bg="#fafafa")

    tk.Label(add_post_window, text="Enter your post text:", bg="#fafafa").pack(pady=10)
    post_text_entry = tk.Entry(add_post_window, width=50)
    post_text_entry.pack(pady=10)
    
    def submit_post():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = post_text_entry.get()
        new_post = Post(current_user, None, text, current_time)
        post.add_post(new_post)
        add_post_window.destroy()
    
    ttk.Button(add_post_window, text="Submit", command=submit_post).pack(pady=10)

def add_like():
    add_like_window = tk.Toplevel(root)
    add_like_window.title("Add Like")
    add_like_window.geometry("300x150")
    add_like_window.configure(bg="#fafafa")

    tk.Label(add_like_window, text="Enter Post ID to like:", bg="#fafafa").pack(pady=10)
    post_id_entry = tk.Entry(add_like_window, width=20)
    post_id_entry.pack(pady=10)
    
    def submit_like():
        post_id = int(post_id_entry.get())
        likes.insert_like(post_id, current_user)
        liked_by = likes.likedby(post_id)
        messagebox.showinfo("Post Liked", f"Post ID: {post_id} liked by {current_user}")
        add_like_window.destroy()
    
    ttk.Button(add_like_window, text="Submit", command=submit_like).pack(pady=10)

def show_graph():
    if current_user == "sujan":
        graph_module.showgraph()
    else:
        messagebox.showerror("Access Denied", "You do not have permission to view the graph")

# Main application
hashtable = hash.gethash()
current_user = ""

# Root window
root = tk.Tk()
root.title("Login System")
root.geometry("400x600")
root.configure(bg="#fafafa")

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', background="#fafafa", font=('Helvetica', 12))

# Login interface
frame = tk.Frame(root, bg="#fafafa")
frame.pack(expand=True, fill='both')

tk.Label(frame, text="Username", font=("Helvetica", 14), bg="#fafafa").pack(pady=10)
username_entry = ttk.Entry(frame, width=30)
username_entry.pack(pady=10)

tk.Label(frame, text="Password", font=("Helvetica", 14), bg="#fafafa").pack(pady=10)
password_entry = ttk.Entry(frame, width=30, show="*")
password_entry.pack(pady=10)

ttk.Button(frame, text="Login", command=login).pack(pady=20)

root.mainloop()
