import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import random
import os
import time
import json
import subprocess

# Carbon emission rates (kg CO₂ per page)
CARBON_STANDARD = 0.005  
CARBON_HIGH_QUALITY = 0.01  

# Default Printer IP
DEFAULT_PRINTER_IP = "127.0.0.1"

# User details (to be populated from login)
user_role = ""
user_username = ""
user_age = ""

# Load user details from file
with open("user_details.txt", "r") as file:
    user_role = file.readline().strip()
    user_username = file.readline().strip()
    user_age = file.readline().strip()

def mock_printer_data():
    """Simulates printer data instead of fetching from an API."""
    return {
        "model": "HP LaserJet Pro MFP M227fdw",
        "manufacturer": "HP",
        "status": random.choice(["Online", "Offline", "Idle", "Printing"]),
        "connectionType": "WiFi",
        "macAddress": "00:1A:2B:3C:4D:5E",
        "duplex": random.choice([True, False]),
        "pageCount": random.randint(500, 5000),
        "cartridges": {
            "Black": random.randint(20, 100),
            "Cyan": random.randint(5, 20),
            "Magenta": random.randint(20, 100),
            "Yellow": random.randint(5, 20),
        },
        "paperTrays": {
            "Tray 1": random.randint(0, 250),
            "Tray 2": random.randint(0, 250),
        },
    }

def calculate_carbon_footprint(page_count, print_type):
    """Calculate carbon footprint based on page count and print type."""
    carbon_per_page = CARBON_STANDARD if print_type == "Standard" else CARBON_HIGH_QUALITY
    return round(page_count * carbon_per_page, 4)

def download_report(printer_data, carbon_footprint, print_type):
    """Download the carbon footprint report as a text file."""
    report_text = f"""
    ======= Printer & Carbon Footprint Report =======
    Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}

    User Role: {user_role}
    Username: {user_username}
    Age: {user_age}

    Printer Model: {printer_data['model']}
    Manufacturer: {printer_data['manufacturer']}
    Printer Status: {printer_data['status']}
    Connection Type: {printer_data['connectionType']}
    MAC Address: {printer_data['macAddress']}
    Duplex Printing: {'Yes' if printer_data['duplex'] else 'No'}
    Pages Printed: {printer_data['pageCount']}
    Print Type: {print_type}
    Carbon Footprint (kg CO₂): {carbon_footprint}

    Cartridges Status:
    """
    for color, level in printer_data['cartridges'].items():
        report_text += f" - {color} ({level}% remaining)\n"
    report_text += "Paper Tray Info:\n"
    for tray, capacity in printer_data['paperTrays'].items():
        report_text += f" - {tray}: {capacity} sheets remaining\n"
    report_text += "===============================================\n"

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as text_file:
            text_file.write(report_text)
        messagebox.showinfo("Report Saved", f"Report saved as {file_path}")

def fetch_and_display_data():
    """Fetch printer data and update the GUI."""
    start_time = time.time()
    printer_ip = ip_entry.get().strip()
    print_type = print_type_var.get()

    if not printer_ip:
        messagebox.showerror("Error", "Please enter a valid printer IP address.")
        return

    printer_data = mock_printer_data()
    page_count = printer_data["pageCount"]
    carbon_footprint = calculate_carbon_footprint(page_count, print_type)

    # Save current report data
    current_report = {
        "pageCount": page_count,
        "carbonFootprint": carbon_footprint,
        "cartridges": printer_data["cartridges"],
        "paperTrays": printer_data["paperTrays"]
    }
    with open("current_report.json", "w") as file:
        json.dump(current_report, file)

    # Update Labels
    printer_model_var.set(f"Model: {printer_data['model']}")
    status_var.set(f"Status: {printer_data['status']}")
    pages_var.set(f"Pages Printed: {page_count}")
    carbon_var.set(f"Carbon Footprint: {carbon_footprint} kg CO₂")

    # Update Cartridge and Paper Tray Info
    cartridge_info.set("\n".join([f"{color} - {level}%" for color, level in printer_data["cartridges"].items()]))
    tray_info.set("\n".join([f"{tray} - {capacity} sheets" for tray, capacity in printer_data["paperTrays"].items()]))

    # Enable Download Button
    download_button.config(state=tk.NORMAL, command=lambda: download_report(printer_data, carbon_footprint, print_type))
    end_time = time.time()
    print(f"Data fetching and GUI update took {end_time - start_time:.2f} seconds")

def open_graphical_output():
    """Open the graphical output page."""
    subprocess.Popen(["python", "printer_output.py"])

# Create GUI
root = tk.Tk()
root.title("Printer Carbon Footprint Analyzer")
root.geometry("1535x813+2+42")  # Set the window size and position
root.state('zoomed')  # Maximize the window

# Main Frame with Scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame)
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# IP Address Input
tk.Label(scrollable_frame, text="Printer IP Address:", font=("Times New Roman", 20)).pack(pady=10)
ip_entry = tk.Entry(scrollable_frame, width=30, font=("Times New Roman", 18))
ip_entry.pack(pady=10)
ip_entry.insert(0, DEFAULT_PRINTER_IP)  # Default value

# Print Type Selection
tk.Label(scrollable_frame, text="Select Print Type:", font=("Times New Roman", 20)).pack(pady=10)
print_type_var = tk.StringVar(value="Standard")
ttk.Combobox(scrollable_frame, textvariable=print_type_var, values=["Standard", "High-Quality"], state="readonly", font=("Times New Roman", 18)).pack(pady=10)

# Fetch Data Button
fetch_button = tk.Button(scrollable_frame, text="Fetch Printer Data", command=fetch_and_display_data, font=("Times New Roman", 20))
fetch_button.pack(pady=20)

# Printer Information
printer_model_var = tk.StringVar(value="Model: N/A")
status_var = tk.StringVar(value="Status: N/A")
pages_var = tk.StringVar(value="Pages Printed: N/A")
carbon_var = tk.StringVar(value="Carbon Footprint: N/A")

tk.Label(scrollable_frame, textvariable=printer_model_var, font=("Times New Roman", 18), anchor="center").pack(fill=tk.X)
tk.Label(scrollable_frame, textvariable=status_var, font=("Times New Roman", 18), anchor="center").pack(fill=tk.X)
tk.Label(scrollable_frame, textvariable=pages_var, font=("Times New Roman", 18), anchor="center").pack(fill=tk.X)
tk.Label(scrollable_frame, textvariable=carbon_var, font=("Times New Roman", 18), anchor="center").pack(fill=tk.X)

# Cartridge Information
tk.Label(scrollable_frame, text="Cartridges Info:", font=("Times New Roman", 20), anchor="center").pack(pady=10)
cartridge_info = tk.StringVar(value="N/A")
tk.Label(scrollable_frame, textvariable=cartridge_info, justify="center", font=("Times New Roman", 18)).pack(fill=tk.X)

# Paper Tray Information
tk.Label(scrollable_frame, text="Paper Tray Info:", font=("Times New Roman", 20), anchor="center").pack(pady=10)
tray_info = tk.StringVar(value="N/A")
tk.Label(scrollable_frame, textvariable=tray_info, justify="center", font=("Times New Roman", 18)).pack(fill=tk.X)

# Download Report Button (Initially Disabled)
download_button = tk.Button(scrollable_frame, text="Download Report", state=tk.DISABLED, font=("Times New Roman", 20))
download_button.pack(pady=20)

# Graphical Output Button
graphical_output_button = tk.Button(scrollable_frame, text="Graphical Output", command=open_graphical_output, font=("Times New Roman", 20))
graphical_output_button.pack(pady=20)

# Run Application
root.mainloop()