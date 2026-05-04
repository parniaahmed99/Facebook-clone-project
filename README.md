# Facebook-clone-project


## Introduction
The Facebook Clone project is a full-stack social media application designed to emulate core functionalities of the Facebook platform. The application features a user-friendly frontend built with Python's `customtkinter` and `tkinter` libraries, and a robust backend powered by MongoDB, a NoSQL database.

This project demonstrates full-stack development skills, modular architecture, and scalable system design.

---

## Project Overview
The project replicates essential social media features such as:
- User profiles  
- Posts  
- Friendships  
- Groups  
- Events  
- Messaging  

### Main Components
- **Frontend:** Python GUI using `customtkinter` and `tkinter`
- **Backend:** MongoDB database with Python (PyMongo)

---

## Frontend Implementation

### CustomTkinter GUI (`main.py`)
- Sidebar navigation (Home, Profile, Friends, Groups, Events, Messages)
- Topbar with user info and logout button
- Dynamic content area for posts and profiles
- Post creation feature
- Responsive grid-based layout

---

### Tkinter Admin GUI (`gui.py`)
- User CRUD operations (Insert, Update, Delete, Search)
- MongoDB query execution interface
- SQL-like query support (SELECT, INSERT, UPDATE, DELETE)
- Scrollable result display listbox

---

## Backend Implementation

###  Database Layer (`database.py`)
- MongoDB connection (`facebook_db`)
- Full CRUD support for all collections
- Auto-initialized sample data (groups & events)
- Timestamp tracking for posts and messages

---

### Database Collections
- `users` → user profiles  
- `posts` → user posts  
- `comments` → post comments  
- `likes` → post likes  
- `friendship` → friend relationships  
- `messages` → private messages  
- `groups` → community groups  
- `events` → event details  
- `event_attendees` → event participation  
- `pages` → user pages  

---

## Key Features

### User Management
- View profiles
- Add / update / delete users
- Unique user ID system

### Social Features
- Create posts
- Like posts
- Comment system (backend ready)
- Friendship tracking

### Groups & Events
- View groups
- Event listing
- Attendance tracking (GOING / NOT_GOING / INTERESTED)

### Messaging
- Private messaging system
- Timestamped conversations

### Database Query Interface
- MongoDB query support
- SQL-like query parser
- Collection-wide operations

---

## 🏗️ Technical Architecture
