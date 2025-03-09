import tkinter as tk
import os

def show_printer_carbon_footprints():
    os.system('python printer_carbon_footprints.py')

def show_desktop_carbon_footprints():
    os.system('python desktop_carbon_footprints.py')

def show_other_programs():
    os.system('python other_programs.py')

def show_wifi_carbon_footprints():
    os.system('python wifi_carbon_footprints.py')

def show_manually_calculated_carbon_footprints():
    os.system('python manuallycalculated_carbon_footprints.py')

# Create GUI
root = tk.Tk()
root.title("Calculate Carbon Footprints For")
root.geometry("1535x813+2+42")  # Set the window size and position
root.state('zoomed')  # Maximize the window

# Configure grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

# Add Title
tk.Label(root, text="Calculate Carbon Footprints For", font=("Times New Roman", 32)).grid(row=0, column=0, pady=40)

# Add Buttons
tk.Button(root, text="Printer", command=show_printer_carbon_footprints, font=("Times New Roman", 24)).grid(row=1, column=0, padx=20, pady=20)
tk.Button(root, text="Desktop", command=show_desktop_carbon_footprints, font=("Times New Roman", 24)).grid(row=2, column=0, padx=20, pady=20)
tk.Button(root, text="Other", command=show_other_programs, font=("Times New Roman", 24)).grid(row=3, column=0, padx=20, pady=20)
tk.Button(root, text="Internet", command=show_wifi_carbon_footprints, font=("Times New Roman", 24)).grid(row=4, column=0, padx=20, pady=20)
tk.Button(root, text="Calculate Manually", command=show_manually_calculated_carbon_footprints, font=("Times New Roman", 24)).grid(row=5, column=0, padx=20, pady=20)

# Run Application
root.mainloop()