import tkinter as tk
from tkinter import messagebox
import psutil
import time
import subprocess

# Configuration
POWER_CONSUMPTION_WATTS = 10  # Approx. power usage (W)
EMISSION_FACTOR = 0.8  # kg CO₂ per kWh (coal-based)
INTERFACE_NAME = "Ethernet"  # Name of the Ethernet interface

def get_interface_uptime(interface_name):
    """Get the uptime of the specified network interface."""
    net_if_stats = psutil.net_if_stats()
    net_if_addrs = psutil.net_if_addrs()
    if interface_name in net_if_stats and interface_name in net_if_addrs:
        if net_if_stats[interface_name].isup:
            # Assuming the interface was up since the system boot
            boot_time = psutil.boot_time()
            current_time = time.time()
            uptime_seconds = current_time - boot_time
            uptime_hours = uptime_seconds / 3600
            return uptime_hours
    return 0  # Interface is down or not found

def calculate_carbon_footprint(hours):
    """Calculate carbon footprint based on uptime and power consumption."""
    energy_kwh = (POWER_CONSUMPTION_WATTS * hours) / 1000
    carbon_footprint = energy_kwh * EMISSION_FACTOR
    return carbon_footprint

def calculate_footprint():
    uptime_hours = get_interface_uptime(INTERFACE_NAME)
    if uptime_hours == 0:
        messagebox.showerror("Error", f"{INTERFACE_NAME} is not connected or not found.")
        return

    carbon_footprint = calculate_carbon_footprint(uptime_hours)
    result_label.config(text=f"Estimated Carbon Footprint: {carbon_footprint:.2f} kg CO₂")

def calculate_wifi_footprint():
    router_ip = ip_entry.get().strip()
    if not router_ip:
        messagebox.showerror("Error", "Please enter the router IP address.")
        return

    uptime_hours = get_router_uptime(router_ip)
    if uptime_hours == 0:
        messagebox.showerror("Error", "Unable to fetch router uptime. Ensure the IP address is correct and SSH is enabled on the router.")
        return

    carbon_footprint = calculate_carbon_footprint(uptime_hours)
    result_label.config(text=f"Estimated Carbon Footprint: {carbon_footprint:.2f} kg CO₂")

def get_router_uptime(router_ip):
    """Fetch router uptime using SSH."""
    try:
        result = subprocess.run(["ssh", f"admin@{router_ip}", "uptime -p"], capture_output=True, text=True)
        if result.returncode == 0:
            uptime_str = result.stdout.strip()
            print(f"Router Uptime: {uptime_str}")
            return extract_hours(uptime_str)
        else:
            print(f"SSH command failed with return code {result.returncode}")
    except Exception as e:
        print("Error fetching uptime:", e)
    return 0  # Return 0 if unable to fetch uptime

def extract_hours(uptime_str):
    """Convert uptime string to hours."""
    uptime_str = uptime_str.replace("up ", "")
    days, hours = 0, 0
    for part in uptime_str.split(", "):
        if "day" in part:
            days = int(part.split()[0])
        elif "hour" in part:
            hours = int(part.split()[0])
    return days * 24 + hours

# Create GUI
root = tk.Tk()
root.title("Carbon Footprint Calculator")
root.state('zoomed')  # Maximize the window

# Ethernet Section
tk.Label(root, text="Connect to Ethernet and click Calculate", font=("Times New Roman", 16)).pack(pady=10)
calculate_button = tk.Button(root, text="Calculate Ethernet Carbon Footprint", command=calculate_footprint, font=("Times New Roman", 16))
calculate_button.pack(pady=20)

# WiFi Section
tk.Label(root, text="Or enter the default gateway for WiFi", font=("Times New Roman", 16)).pack(pady=10)
tk.Label(root, text="(Run 'ipconfig' in CMD to find the default gateway)", font=("Times New Roman", 12)).pack(pady=5)
ip_entry = tk.Entry(root, width=30, font=("Times New Roman", 14))
ip_entry.pack(pady=10)
calculate_wifi_button = tk.Button(root, text="Calculate WiFi Carbon Footprint", command=calculate_wifi_footprint, font=("Times New Roman", 16))
calculate_wifi_button.pack(pady=20)

result_label = tk.Label(root, text="", font=("Times New Roman", 16))
result_label.pack(pady=10)

# Run Application
root.mainloop()