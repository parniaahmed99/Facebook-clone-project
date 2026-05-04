import tkinter as tk
from tkinter import messagebox, simpledialog
from pymongo import MongoClient
import ast 

client = MongoClient("mongodb://localhost:27017/")
db = client["facebook_db"]
users = db["users"]


root = tk.Tk()
root.title("Facebook MongoDB GUI with SQL-style Query Support")
root.geometry("800x600")


tk.Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="we")

tk.Label(root, text="Enter MongoDB Query: " ).grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="w")
entry_mongo_query = tk.Entry(root, width=60)
entry_mongo_query.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="we")

tk.Label(root, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="we")

tk.Label(root, text="User ID (for update/delete)").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_id = tk.Entry(root)
entry_id.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="we")


tk.Label(root, text="Collection Name").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_collection = tk.Entry(root)
entry_collection.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="we")

tk.Label(root, text="Enter SQL-like Query").grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")
entry_query = tk.Entry(root, width=60)
entry_query.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="we")


listbox = tk.Listbox(root, width=100, height=20)
listbox.grid(row=7, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

def execute_mongo_query():
    query_text = entry_mongo_query.get().strip()
    listbox.delete(0, tk.END)
    try:
       
        query_obj = ast.literal_eval(query_text)

        if isinstance(query_obj, list):
           
            results = users.aggregate(query_obj)
        elif isinstance(query_obj, dict):
           
            results = users.find(query_obj)
        else:
            messagebox.showwarning("Invalid Query", "Query must be a dict (filter) or a list (aggregation pipeline).")
            return

        for user in results:
            listbox.insert(tk.END, f"UserID: {user.get('user_id')} | Name: {user.get('name')} | Email: {user.get('email')}")

    except Exception as e:
        messagebox.showerror("MongoDB Query Error", f"Error running query:\n{str(e)}")

tk.Button(root, text="Run MongoDB Query", command=execute_mongo_query).grid(row=9, column=2, padx=5, pady=5, sticky="ew")


def insert_user():
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    if name and email:

        user_id = users.count_documents({}) + 1
        users.insert_one({"user_id": user_id, "name": name, "email": email})
        messagebox.showinfo("Success", f"User inserted with User ID {user_id}!")
        show_users()
    else:
        messagebox.showwarning("Missing Info", "Enter both Name and Email!")

def show_users():
    listbox.delete(0, tk.END)
    for user in users.find().sort("user_id", 1):
        listbox.insert(tk.END, f"UserID: {user.get('user_id')} | Name: {user['name']} | Email: {user['email']}")

def update_user():
    user_id = entry_id.get().strip()
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    if user_id.isdigit() and name and email:
        user_id = int(user_id)
        result = users.update_one({"user_id": user_id}, {"$set": {"name": name, "email": email}})
        if result.modified_count:
            messagebox.showinfo("Success", "User updated!")
        else:
            messagebox.showinfo("No Change", "User not found or no changes.")
        show_users()
    else:
        messagebox.showwarning("Missing Info", "Enter valid User ID (numeric), Name, and Email.")

def delete_user():
    user_id = entry_id.get().strip()
    if not user_id.isdigit():
        messagebox.showwarning("Invalid Input", "Please enter a valid numeric User ID.")
        return

    user_id = int(user_id)
    result = users.delete_one({"user_id": user_id})
    if result.deleted_count > 0:
        messagebox.showinfo("Deleted", f"User with ID {user_id} deleted.")
    else:
        messagebox.showwarning("Not Found", f"No user found with ID {user_id}.")
    show_users()

def search_user():
    name = entry_name.get().strip()
    listbox.delete(0, tk.END)
    for user in users.find({"name": {"$regex": name, "$options": "i"}}).sort("user_id", 1):
        listbox.insert(tk.END, f"UserID: {user.get('user_id')} | Name: {user['name']} | Email: {user['email']}")

# def execute_query():
#     query = entry_query.get().strip()
#     listbox.delete(0, tk.END)
#     try:
#         query_lower = query.lower()
        
#         if query_lower.startswith("select"):
#             results = users.find()
#             if "where" in query_lower:
#                 _, where_part = query_lower.split("where", 1)
#                 where_part = where_part.strip()
#                 if "=" in where_part:
#                     key, value = [x.strip().strip("'") for x in where_part.split("=", 1)]
#                     if key == "user_id" and value.isdigit():
#                         value = int(value)
#                     results = users.find({key: value})
#             for user in results.sort("user_id", 1):
#                 listbox.insert(tk.END, f"UserID: {user.get('user_id')} | Name: {user['name']} | Email: {user['email']}")

#         elif query_lower.startswith("insert"):
#             if "values" in query_lower:
#                 values_section = query_lower.split("values", 1)[1].strip()
#                 values = values_section.strip("()").split(",")
#                 if len(values) >= 2:
#                     name = values[0].strip().strip("'")
#                     email = values[1].strip().strip("'")
#                     user_id = users.count_documents({}) + 1
#                     users.insert_one({"user_id": user_id, "name": name, "email": email})
#                     messagebox.showinfo("Inserted", f"User '{name}' added with ID {user_id}.")
#                     show_users()
#                 else:
#                     messagebox.showwarning("Syntax Error", "INSERT requires name and email values.")
#             else:
#                 messagebox.showwarning("Syntax Error", "INSERT query must contain VALUES.")

#         elif query_lower.startswith("update"):
#             if "set" in query_lower and "where" in query_lower:
#                 set_part = query_lower.split("set",1)[1].split("where",1)[0].strip()
#                 where_part = query_lower.split("where",1)[1].strip()
#                 if "=" in set_part and "=" in where_part:
#                     set_key, set_value = [x.strip().strip("'") for x in set_part.split("=",1)]
#                     where_key, where_value = [x.strip().strip("'") for x in where_part.split("=",1)]
#                     if where_key == "user_id" and where_value.isdigit():
#                         where_value = int(where_value)
#                     users.update_one({where_key
#                                       : where_value}, {"$set": {set_key: set_value}})
#                     messagebox.showinfo("Updated", "User updated via query.")
#                     show_users()
#                 else:
#                     messagebox.showwarning("Syntax Error", "UPDATE query requires SET and WHERE clauses with key=value.")

#             else:
#                 messagebox.showwarning("Syntax Error", "UPDATE query must contain SET and WHERE clauses.")

#         elif query_lower.startswith("delete"):
#             if "where" in query_lower:
#                 where_part = query_lower.split("where",1)[1].strip()
#                 if "=" in where_part:
#                     key, value = [x.strip().strip("'") for x in where_part.split("=",1)]
#                     if key == "user_id" and value.isdigit():
#                         value = int(value)
#                     result = users.delete_one({key: value})
#                     if result.deleted_count:
#                         messagebox.showinfo("Deleted", f"User where {key} = {value} deleted.")
#                     else:
#                         messagebox.showwarning("Not Found", f"No user found with {key} = {value}.")
#                     show_users()
#                 else:
#                     messagebox.showwarning("Syntax Error", "DELETE query WHERE clause must be key=value.")
#             else:
#                 messagebox.showwarning("Syntax Error", "DELETE query requires WHERE clause.")

#         else:
#             messagebox.showwarning("Unsupported", "Only basic SELECT, INSERT, UPDATE, DELETE supported.")
#     except Exception as e:
#         messagebox.showerror("Query Error", str(e))
def execute_query():
    collection_name = entry_collection.get().strip()
    if not collection_name:
        messagebox.showwarning("Missing Info", "Please enter a collection name!")
        return
    
    collection = db[collection_name]
    query = entry_query.get().strip()
    listbox.delete(0, tk.END)
    try:
        query_lower = query.lower()
        
        if query_lower.startswith("select"):
            results = collection.find()
            if "where" in query_lower:
                _, where_part = query_lower.split("where", 1)
                where_part = where_part.strip()
                if "=" in where_part:
                    key, value = [x.strip().strip("'") for x in where_part.split("=", 1)]
                    # Try to convert numeric values to int
                    if value.isdigit():
                        value = int(value)
                    filter_query = {key: value}
                    results = collection.find(filter_query)
            for doc in results.sort("_id", 1):
                listbox.insert(tk.END, str(doc))
        
        elif query_lower.startswith("insert"):
            if "values" in query_lower:
                values_section = query_lower.split("values", 1)[1].strip()
                values = values_section.strip("()").split(",")
                # You have to map values to keys; for generic insert, ask user to use JSON format or a fixed schema
                # For simplicity, let's just insert a dict with fields "field1", "field2", ...
                doc = {}
                for i, val in enumerate(values):
                    val = val.strip().strip("'")
                    doc[f"field{i+1}"] = val
                collection.insert_one(doc)
                messagebox.showinfo("Inserted", f"Document inserted into {collection_name}.")
                # Optionally refresh display
            else:
                messagebox.showwarning("Syntax Error", "INSERT query must contain VALUES.")
        
        elif query_lower.startswith("update"):
            if "set" in query_lower and "where" in query_lower:
                set_part = query_lower.split("set",1)[1].split("where",1)[0].strip()
                where_part = query_lower.split("where",1)[1].strip()
                if "=" in set_part and "=" in where_part:
                    set_key, set_value = [x.strip().strip("'") for x in set_part.split("=",1)]
                    where_key, where_value = [x.strip().strip("'") for x in where_part.split("=",1)]
                    if where_value.isdigit():
                        where_value = int(where_value)
                    filter_query = {where_key: where_value}
                    update_query = {"$set": {set_key: set_value}}
                    collection.update_one(filter_query, update_query)
                    messagebox.showinfo("Updated", f"Document updated in {collection_name}.")
                else:
                    messagebox.showwarning("Syntax Error", "UPDATE query requires SET and WHERE clauses with key=value.")
            else:
                messagebox.showwarning("Syntax Error", "UPDATE query must contain SET and WHERE clauses.")
        
        elif query_lower.startswith("delete"):
            if "where" in query_lower:
                where_part = query_lower.split("where",1)[1].strip()
                if "=" in where_part:
                    key, value = [x.strip().strip("'") for x in where_part.split("=",1)]
                    if value.isdigit():
                        value = int(value)
                    result = collection.delete_one({key: value})
                    if result.deleted_count:
                        messagebox.showinfo("Deleted", f"Document deleted from {collection_name}.")
                    else:
                        messagebox.showwarning("Not Found", f"No document found with {key} = {value} in {collection_name}.")
                else:
                    messagebox.showwarning("Syntax Error", "DELETE query WHERE clause must be key=value.")
            else:
                messagebox.showwarning("Syntax Error", "DELETE query requires WHERE clause.")
        else:
            messagebox.showwarning("Unsupported", "Only basic SELECT, INSERT, UPDATE, DELETE supported.")
    except Exception as e:
        messagebox.showerror("Query Error", str(e))


tk.Button(root, text="Insert User", command=insert_user).grid(row=6, column=0, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Show All Users", command=show_users).grid(row=6, column=1, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Search by Name", command=search_user).grid(row=6, column=2, padx=5, pady=5, sticky="ew")

tk.Button(root, text="Update User", command=update_user).grid(row=8, column=0, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Delete User", command=delete_user).grid(row=8, column=1, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Execute Query", command=execute_query).grid(row=8, column=2, padx=5, pady=5, sticky="ew")


root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(7, weight=1)

show_users()
root.mainloop()
