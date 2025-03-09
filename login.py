import tkinter as tk
from tkinter import messagebox
import os

def open_index():
    os.system('python index.py')

def login():
    """Handle the login process."""
    global user_role, user_username, user_age
    role = role_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    age = age_entry.get().strip()

    if not role or not username or not password or not age:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    user_role = role
    user_username = username
    user_age = age

    # Save user details to a file
    with open("user_details.txt", "w") as file:
        file.write(f"{user_role}\n{user_username}\n{user_age}")

    # Hide login frame and show options frame
    login_frame.pack_forget()
    options_frame.pack(expand=True)

# Create GUI
root = tk.Tk()
root.title("Login")
root.geometry("1535x813+2+42")  # Set the window size and position
root.state('zoomed')  # Maximize the window

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

tk.Label(login_frame, text="Role:", font=("Times New Roman", 20)).pack(pady=10)
role_entry = tk.Entry(login_frame, width=30, font=("Times New Roman", 18))
role_entry.pack(pady=10)

tk.Label(login_frame, text="Username:", font=("Times New Roman", 20)).pack(pady=10)
username_entry = tk.Entry(login_frame, width=30, font=("Times New Roman", 18))
username_entry.pack(pady=10)

tk.Label(login_frame, text="Password:", font=("Times New Roman", 20)).pack(pady=10)
password_entry = tk.Entry(login_frame, width=30, show="*", font=("Times New Roman", 18))
password_entry.pack(pady=10)

tk.Label(login_frame, text="Age:", font=("Times New Roman", 20)).pack(pady=10)
age_entry = tk.Entry(login_frame, width=30, font=("Times New Roman", 18))
age_entry.pack(pady=10)

login_button = tk.Button(login_frame, text="Login", command=login, font=("Times New Roman", 20))
login_button.pack(pady=20)

# Options Frame
options_frame = tk.Frame(root)

# New Button to Open Index Page
tk.Button(options_frame, text="Start Calculating Carbon Footprints", command=open_index, font=("Times New Roman", 20)).pack(expand=True)

# Run Application
root.mainloop()