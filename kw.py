
import tkinter as tk
from tkinter import ttk

# Define color palette
BG_COLOR = "#f0f0f0"
FG_COLOR = "#333333"
BTN_COLOR = "#4CAF50"
BTN_TEXT_COLOR = "#ffffff"
ENTRY_BG_COLOR = "#ffffff"
ENTRY_FG_COLOR = "#333333"

# Create the main application window
root = tk.Tk()
root.title("Employee Management System")
root.geometry("400x300")
root.configure(bg=BG_COLOR)

# Define styles
style = ttk.Style()
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Helvetica", 12))
style.configure("TButton", background=BTN_COLOR, foreground=BTN_TEXT_COLOR, font=("Helvetica", 12))
style.configure("TEntry", fieldbackground=ENTRY_BG_COLOR, foreground=ENTRY_FG_COLOR, font=("Helvetica", 12))

# Create and place widgets
ttk.Label(root, text="Employee Name:").grid(row=0, column=0, padx=10, pady=10, sticky="W")
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="EW")

ttk.Label(root, text="Employee ID:").grid(row=1, column=0, padx=10, pady=10, sticky="W")
id_entry = ttk.Entry(root)
id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

ttk.Label(root, text="Department:").grid(row=2, column=0, padx=10, pady=10, sticky="W")
dept_entry = ttk.Entry(root)
dept_entry.grid(row=2, column=1, padx=10, pady=10, sticky="EW")

# Define button functions
def add_employee():
    print(f"Added: {name_entry.get()}, {id_entry.get()}, {dept_entry.get()}")

def update_employee():
    print(f"Updated: {name_entry.get()}, {id_entry.get()}, {dept_entry.get()}")

def delete_employee():
    print(f"Deleted: {name_entry.get()}, {id_entry.get()}, {dept_entry.get()}")

# Create and place buttons
ttk.Button(root, text="Add", command=add_employee).grid(row=3, column=0, padx=10, pady=10, sticky="EW")
ttk.Button(root, text="Update", command=update_employee).grid(row=3, column=1, padx=10, pady=10, sticky="EW")
ttk.Button(root, text="Delete", command=delete_employee).grid(row=3, column=2, padx=10, pady=10, sticky="EW")

# Configure grid weights
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Run the application
root.mainloop()
