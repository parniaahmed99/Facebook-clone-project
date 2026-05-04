from pymongo import MongoClient
import datetime

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["facebook_db"]

        self.users = self.db["users"]
        self.posts = self.db["posts"]
        self.groups = self.db["groups"]
        self.user_groups = self.db["user_groups"]
        self.messages = self.db["messages"]
        self.likes = self.db["likes"]
        self.follows = self.db["follows"]
        self.events = self.db["events"]

    def get_user_by_id(self, user_id):
        return self.users.find_one({"user_id": user_id})

    def get_users(self):
        return list(self.users.find())

    def add_user(self, name, email):
        user_id = self.users.count_documents({}) + 1
        user = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "dob": None,
            "gender": None
        }
        self.users.insert_one(user)
        return user_id

    def get_posts_by_user(self, user_id):
        return list(self.posts.find({"user_id": user_id}))

    def add_post(self, user_id, content):
        post_id = self.posts.count_documents({}) + 1
        post = {
            "post_id": post_id,
            "user_id": user_id,
            "content": content,
            "timestamp": datetime.datetime.now()
        }
        self.posts.insert_one(post)
        return post

    def get_friends(self, user_id):
        return list(self.users.find({"user_id": {"$ne": user_id}}))

    def get_groups(self):
        groups = list(self.groups.find())
        if not groups:
            self.groups.insert_many([
                {"group_id": 1, "group_name": "Tech Enthusiasts", "description": "All about latest in tech"},
                {"group_id": 2, "group_name": "Food Lovers", "description": "Share and explore recipes"},
                {"group_id": 3, "group_name": "Study Group", "description": "Helping each other with studies"}
            ])
            groups = list(self.groups.find())
        return groups

    def join_group(self, user_id, group_id):
        self.user_groups.insert_one({"user_id": user_id, "group_id": group_id})

    def get_user_groups(self, user_id):
        return list(self.user_groups.find({"user_id": user_id}))

    def get_events_by_user(self, user_id):
        events = list(self.events.find())
        if not events:
            self.events.insert_many([
                {"event_id": 1, "user_id": user_id, "event_name": "Welcome Meetup", "event_date": "2025-07-01", "location": "Main Hall", "description": "Welcome party for new users"},
                {"event_id": 2, "user_id": user_id, "event_name": "AI Workshop", "event_date": "2025-07-15", "location": "Lab 2", "description": "Intro to Machine Learning"}
            ])
            events = list(self.events.find())
        return events

    def send_message(self, sender_id, receiver_id, message_text):
        message = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message_text": message_text,
            "timestamp": datetime.datetime.now()
        }
        self.messages.insert_one(message)

    def get_messages(self, user_id, friend_id):
        messages = list(self.messages.find({
            "$or": [
                {"sender_id": user_id, "receiver_id": friend_id},
                {"sender_id": friend_id, "receiver_id": user_id}
            ]
        }))
        if not messages:
            self.send_message(user_id, friend_id, "Hi, how are you?")
            self.send_message(friend_id, user_id, "I'm good, thanks!")
            messages = list(self.messages.find({
                "$or": [
                    {"sender_id": user_id, "receiver_id": friend_id},
                    {"sender_id": friend_id, "receiver_id": user_id}
                ]
            }))
        return messages

    def add_like(self, user_id, post_id):
        self.likes.insert_one({"user_id": user_id, "post_id": post_id})

    def get_likes_for_post(self, post_id):
        return list(self.likes.find({"post_id": post_id}))

    def follow_user(self, follower_id, followee_id):
        self.follows.insert_one({"follower_id": follower_id, "followee_id": followee_id})

    def get_following(self, user_id):
        return list(self.follows.find({"follower_id": user_id}))

    def get_followers(self, user_id):
        return list(self.follows.find({"followee_id": user_id}))
