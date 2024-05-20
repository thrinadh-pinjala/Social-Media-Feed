import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import hash
import post
from post import Post
import likes
from datetime import datetime
import mysql.connector
import graph as graph_module
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Function Definitions

def login():
    username = username_entry.get()
    password = password_entry.get()

    logging.debug(f"Attempting login with username: {username}")
    if hash.checkpass(hashtable, username, password):
        global current_user
        current_user = username
        logging.debug(f"Login successful for user: {username}")
        show_homepage()
    else:
        logging.error(f"Login failed for user: {username}")
        messagebox.showerror("Login Failed", "Invalid username or password")

def logout():
    global current_user
    current_user = ""
    logging.debug("User logged out")
    show_login()

def show_login():
    for widget in root.winfo_children():
        widget.destroy()

    login_frame = tk.Frame(root, bg="#e8e8e8")
    login_frame.pack(expand=True)

    tk.Label(login_frame, text="Username:", bg="#e8e8e8").pack(pady=5)
    global username_entry
    username_entry = tk.Entry(login_frame)
    username_entry.pack(pady=5)

    tk.Label(login_frame, text="Password:", bg="#e8e8e8").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(login_frame, show='*')
    password_entry.pack(pady=5)

    ttk.Button(login_frame, text="Login", command=login).pack(pady=20)

def show_homepage():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="#F0F0F0")  # Change background color
    frame.pack(expand=True, fill='both')

    tk.Label(frame, text=f"Welcome, {current_user}", font=("Helvetica", 18, "bold"), bg="#F0F0F0").pack(pady=20)

    buttons = [
        ("Show My Posts", show_my_posts),
        ("Show Followers", show_followers),
        ("Show Following", show_following),
        ("See Feed", see_feed),
        ("Show Likes", show_likes),
        ("Add Post", add_post_window),
        ("Add Like", add_like),
        ("Show Graph", show_graph),
        ("Logout", logout)  # Add Logout button
    ]

    button_frame = tk.Frame(frame, bg="#F0F0F0")
    button_frame.pack(pady=20)

    for text, command in buttons:
        btn = ttk.Button(button_frame, text=text, command=command, style='TButton')  # Apply style
        btn.pack(pady=5, fill='x')

def show_my_posts():
    posts = post.showpost(current_user)
    display_posts(posts)

def display_posts(posts_heap):
    posts_window = tk.Toplevel(root)
    posts_window.title("My Posts")
    posts_window.geometry("800x600")
    posts_window.configure(bg="#F0F0F0")

    frame = tk.Frame(posts_window, bg="#F0F0F0")
    frame.pack(expand=True, fill='both', padx=10, pady=10)

    canvas = tk.Canvas(frame, bg="#F0F0F0", highlightthickness=0)
    canvas.pack(expand=True, fill='both')

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    post_frame = tk.Frame(canvas, bg="#F0F0F0")
    canvas.create_window((0, 0), window=post_frame, anchor="nw")

    # Extract Post objects from PostHeap
    posts_list = []
    while not posts_heap.is_empty():
        posts_list.append(posts_heap.pop())

    def animate_display(posts):
        for i, post_item in enumerate(posts):
            post_content = f"User ID: {post_item.username}\nPost ID: {post_item.post_id}\nContent: {post_item.content}\nTimestamp: {post_item.timestamp}\n\n"
            label = tk.Label(post_frame, text=post_content, bg="#F0F0F0", font=("Helvetica", 12))
            label.grid(row=i, column=0, sticky="w", padx=10, pady=10)
            label.update_idletasks()  # Update the label to allow smooth animation
            label.grid_remove()  # Remove label before animation
            label.grid(row=i, column=0, sticky="w", padx=10, pady=10)
            label.after(100 * i, label.grid)  # Delayed grid animation

    animate_display(posts_list)


def show_followers():
    try:
        followers = graph_module.graph2.show_followers(current_user)
        if followers:
            plt.bar(range(len(followers)), [1] * len(followers), tick_label=followers, width=0.1)  # Adjust the width here
            plt.xlabel('Followers')
            plt.ylabel('Count')
            plt.title(f'Followers of {current_user}')
            plt.show()
        else:
            messagebox.showinfo("Followers", f"'{current_user}' has no followers.")
    except Exception as e:
        logging.error(f"Error fetching followers: {e}")
        messagebox.showerror("Error", f"An error occurred while fetching followers: {str(e)}")

def show_following():
    try:
        following = graph_module.graph2.show_following(current_user)
        if following:
            # Count the occurrences of each following user
            following_counts = {user: following.count(user) for user in following}
            # Get the labels (usernames) and counts
            labels = list(following_counts.keys())
            counts = list(following_counts.values())
            # Define colors for each slice
            colors = plt.cm.tab20.colors[:len(labels)]
            # Create the pie chart
            plt.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title(f'Following Distribution of {current_user}')
            plt.show()
        else:
            messagebox.showinfo("Following", f"'{current_user}' is not following anyone.")
    except Exception as e:
        logging.error(f"Error fetching following: {e}")
        messagebox.showerror("Error", f"An error occurred while fetching following users: {str(e)}")

def see_feed():
    try:
        following = graph_module.graph2.show_following(current_user)
        if following:
            postheap1 = post.showpost(following[0])
            for user in following[1:]:
                postheap1.merge_heaps(post.showpost(user))
            display_posts(postheap1)
        else:
            messagebox.showinfo("Feed", "You are not following anyone.")
    except Exception as e:
        logging.error(f"Error fetching feed: {e}")
        messagebox.showerror("Error", f"An error occurred while fetching the feed: {str(e)}")

def show_likes():
    try:
        post_heap = post.showpost(current_user)
        likes_count = {}
        while not post_heap.is_empty():
            post_item = post_heap.pop()
            liked_by = likes.likedby(post_item.post_id)
            if liked_by is not None:
                likes_count[post_item.post_id] = len(liked_by)
            else:
                logging.warning(f"No likes found for post {post_item.post_id}")
        if likes_count:
            # Plotting bar graph
            plt.bar(likes_count.keys(), likes_count.values(), color='skyblue', width=0.4)  # Adjust the width here
            plt.xlabel('Post ID')
            plt.ylabel('Likes')
            plt.title('Likes Count')
            plt.show()
        else:
            messagebox.showinfo("No Likes", "No likes found for your posts.")
    except Exception as e:
        logging.error(f"Error showing likes: {e}")
        messagebox.showerror("Error", f"An error occurred while showing likes: {str(e)}")



def add_post_window():
    add_post_window = tk.Toplevel(root)
    add_post_window.title("Add Post")
    add_post_window.geometry("400x200")
    add_post_window.configure(bg="#F0F0F0")

    tk.Label(add_post_window, text="Enter your post text:", bg="#F0F0F0").pack(pady=10)
    post_text_entry = tk.Entry(add_post_window, width=50)
    post_text_entry.pack(pady=10)

    def submit_post():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = post_text_entry.get()
        if not text:
            messagebox.showerror("Error", "Post text cannot be empty.")
            return
        new_post = Post(current_user, None, text, current_time)
        post.add_post(new_post)
        add_post_window.destroy()
        messagebox.showinfo("Success", "Post added successfully.")

    ttk.Button(add_post_window, text="Submit", command=submit_post, style='TButton').pack(pady=10)

def add_like():
    add_like_window = tk.Toplevel(root)
    add_like_window.title("Add Like")
    add_like_window.geometry("300x150")
    add_like_window.configure(bg="#F0F0F0")

    tk.Label(add_like_window, text="Enter Post ID to like:", bg="#F0F0F0").pack(pady=10)
    post_id_entry = tk.Entry(add_like_window, width=20)
    post_id_entry.pack(pady=10)

    def submit_like():
        try:
            post_id = int(post_id_entry.get())
            if likes.insert_like(post_id, current_user):
                liked_by = likes.likedby(post_id)
                messagebox.showinfo("Post Liked", f"Post ID: {post_id} liked by {current_user}\nLiked by: {', '.join(liked_by)}")
            else:
                messagebox.showerror("Error", "Failed to like the post. Please check the Post ID and try again.")
            add_like_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid Post ID. Please enter a valid number.")
        except Exception as e:
            logging.error(f"Error adding like: {e}")
            messagebox.showerror("Error", f"An error occurred while adding the like: {str(e)}")

    ttk.Button(add_like_window, text="Submit", command=submit_like, style='TButton').pack(pady=10)

def show_graph():
    if current_user == "Divianth":
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
root.configure(bg="#d4d4d4")

# Style configuration
style = ttk.Style()
style.theme_use('clam')

style.configure('TButton', 
                padding=6, 
                relief='flat', 
                background="#4CAF50", 
                foreground="#FFFFFF",
                font=("Helvetica", 12, "bold"))

style.map('TButton', background=[('active', '#45a049')])

style.configure('TLabel', 
                background="#d4d4d4",
                foreground="#333333",
                font=("Helvetica", 12))

show_login()

root.mainloop()
