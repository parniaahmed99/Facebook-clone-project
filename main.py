try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
except ImportError:
    import tkinter as tk

    class SimpleCTk(tk.Tk):
        def __init__(self, *args, **kwargs):
            filtered = {k: v for k, v in kwargs.items() if k not in ("corner_radius", "width", "height")}
            super().__init__(*args, **filtered)

    class SimpleCTkFrame(tk.Frame):
        def __init__(self, *args, **kwargs):
            filtered = {k: v for k, v in kwargs.items() if k not in ("corner_radius", "width", "height")}
            super().__init__(*args, **filtered)

    class SimpleCTkLabel(tk.Label):
        def __init__(self, *args, **kwargs):
            filtered = {k: v for k, v in kwargs.items() if k != "corner_radius"}
            super().__init__(*args, **filtered)

    class SimpleCTkButton(tk.Button):
        def __init__(self, *args, **kwargs):
            filtered = {k: v for k, v in kwargs.items() if k != "corner_radius"}
            super().__init__(*args, **filtered)

    class SimpleCTkEntry(tk.Entry):
        def __init__(self, *args, **kwargs):
            placeholder = kwargs.pop("placeholder_text", None)
            filtered = {k: v for k, v in kwargs.items() if k != "corner_radius"}
            super().__init__(*args, **filtered)
            if placeholder:
                self.insert(0, placeholder)

    class CustomTkFallback:
        CTk = SimpleCTk
        CTkFrame = SimpleCTkFrame
        CTkLabel = SimpleCTkLabel
        CTkButton = SimpleCTkButton
        CTkEntry = SimpleCTkEntry

    ctk = CustomTkFallback()

from database import Database

class FacebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Clone")
        self.root.geometry("1200x700")
        self.db = Database()
        self.current_user_id = 1

        self.create_sidebar()
        self.create_topbar()
        self.create_main_content()
        self.show_home()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nswe")

        nav_buttons = [
            ("Home", self.show_home),
            ("Profile", self.show_profile),
            ("Friends", self.show_friends),
            ("Groups", self.show_groups),
            ("Events", self.show_events),
            ("Messages", self.show_messages)
        ]
        for i, (text, command) in enumerate(nav_buttons):
            btn = ctk.CTkButton(
                self.sidebar, text=text, command=command,
                corner_radius=10, font=("Arial", 14)
            )
            btn.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

    def create_topbar(self):
        self.topbar = ctk.CTkFrame(self.root, height=60, corner_radius=0)
        self.topbar.grid(row=0, column=1, sticky="nwe")

        user = self.db.get_user_by_id(self.current_user_id)
        ctk.CTkLabel(self.topbar, text=f"Welcome, {user['name']}", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=20, pady=10)

        ctk.CTkButton(self.topbar, text="Logout", command=self.root.quit, corner_radius=10).grid(row=0, column=1, padx=20, pady=10)

    def create_main_content(self):
        self.main_content = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_content.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_main_content()

        post_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        post_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        post_entry = ctk.CTkEntry(post_frame, placeholder_text="What's on your mind?", width=500)
        post_entry.grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(post_frame, text="Post", command=lambda: self.create_post(post_entry.get()), corner_radius=10).grid(row=0, column=1, padx=10, pady=10)

        posts = self.db.get_posts_by_user(self.current_user_id)
        for i, post in enumerate(posts, 1):
            post_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
            post_frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

            user = self.db.get_user_by_id(post["user_id"])
            ctk.CTkLabel(post_frame, text=f"{user['name']}: {post['content']}\n{post['timestamp']}", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)

            post_id = post.get("post_id")  # Safe access
            likes = len(self.db.get_likes_for_post(post_id)) if post_id else 0
            ctk.CTkLabel(post_frame, text=f"{likes} Likes").grid(row=1, column=0, padx=10, pady=2)

    def create_post(self, content):
        if content.strip():
            self.db.add_post(self.current_user_id, content.strip())
            self.show_home()

    def show_profile(self):
        self.clear_main_content()
        user = self.db.get_user_by_id(self.current_user_id)
        ctk.CTkLabel(
            self.main_content,
            text=f"Profile\nName: {user['name']}\nEmail: {user['email']}\nDOB: {user['dob']}\nGender: {user['gender']}",
            font=("Arial", 14), anchor="w"
        ).grid(row=0, column=0, padx=20, pady=20)

    def show_friends(self):
        self.clear_main_content()
        friends = self.db.get_friends(self.current_user_id)
        for i, friend in enumerate(friends):
            ctk.CTkLabel(self.main_content, text=f"{friend['name']} ({friend['email']})", font=("Arial", 12)).grid(row=i, column=0, padx=20, pady=5, sticky="w")

    def show_groups(self):
        self.clear_main_content()
        groups = self.db.get_groups()
        for i, group in enumerate(groups):
            ctk.CTkLabel(self.main_content, text=f"{group['group_name']}: {group['description']}", font=("Arial", 12)).grid(row=i, column=0, padx=20, pady=5, sticky="w")

    def show_events(self):
        self.clear_main_content()
        events = self.db.get_events_by_user(self.current_user_id)
        for i, event in enumerate(events):
            ctk.CTkLabel(self.main_content, text=f"{event['event_name']} on {event['event_date']} at {event['location']}: {event['description']}", font=("Arial", 12)).grid(row=i, column=0, padx=20, pady=5, sticky="w")

    def show_messages(self):
        self.clear_main_content()
        messages = self.db.get_messages(self.current_user_id, 2)
        for i, msg in enumerate(messages):
            sender = self.db.get_user_by_id(msg["sender_id"])["name"]
            ctk.CTkLabel(self.main_content, text=f"{sender}: {msg['message_text']} ({msg['timestamp']})", font=("Arial", 12)).grid(row=i, column=0, padx=20, pady=5, sticky="w")

if __name__ == "__main__":
    root = ctk.CTk()
    app = FacebookApp(root)
    root.mainloop()
