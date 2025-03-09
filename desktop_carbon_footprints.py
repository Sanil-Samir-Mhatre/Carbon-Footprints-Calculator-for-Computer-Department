import tkinter as tk
from tkinter import Toplevel
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import time
import threading

# Try to import pynvml for GPU monitoring
try:
    from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetPowerUsage, nvmlDeviceGetName
    nvmlInit()  # Initialize NVML for GPU monitoring
    gpu_monitoring_available = True
except ImportError:
    print("pynvml module not found. GPU monitoring will be disabled.")
    gpu_monitoring_available = False
except Exception as e:
    print(f"Error initializing NVML: {e}")
    gpu_monitoring_available = False

def get_gpu_info():
    if gpu_monitoring_available:
        gpu_handle = nvmlDeviceGetHandleByIndex(0)  # First GPU
        gpu_name = nvmlDeviceGetName(gpu_handle).decode("utf-8")
        return gpu_name
    else:
        return "GPU monitoring not available"

# Global variables for live data
cpu_data = []
gpu_data = []
ram_data = []
monitor_data = []
carbon_data = []
cost_data = []
network_data = []
time_stamps = []

# Conversion factor for carbon footprint (kg CO₂ per kWh)
CARBON_CONVERSION_FACTOR = 0.82  # Regional factor for Navi Mumbai
ELECTRICITY_COST_PER_KWH = 9.0  # Cost in ₹ per kWh (average for Kharghar)

# Start time for system runtime
start_time = time.time()

# Function to update CPU utilization and power draw
def update_cpu_data():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        power_draw = cpu_usage / 100 * 65  # Assuming max power draw of 65W
        cpu_data.append((cpu_usage, power_draw))
        time_stamps.append(time.time())
        time.sleep(1)

# Function to update GPU utilization and power draw
def update_gpu_data():
    if gpu_monitoring_available:
        gpu_handle = nvmlDeviceGetHandleByIndex(0)  # First GPU
        while True:
            try:
                gpu_power = nvmlDeviceGetPowerUsage(gpu_handle) / 1000  # Convert to watts
                gpu_usage = gpu_power / 150 * 100  # Approximation based on max power draw
                gpu_data.append((gpu_usage, gpu_power))
            except Exception as e:
                print(f"Error reading GPU data: {e}")
            time.sleep(1)

# Function to update RAM utilization and power draw
def update_ram_data():
    while True:
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        power_draw = ram_usage / 100 * 4  # Assuming max power draw of 4W for RAM
        ram_data.append((ram_usage, power_draw))
        time.sleep(1)

# Function to update monitor power usage (approximation)
def update_monitor_data():
    while True:
        resolution_factor = 0.01  # Approximation factor for resolution impact
        base_power = 20  # Base power draw in watts
        power_draw = base_power + (1920 * 1080 * resolution_factor) / 1e6  # Example for 1080p
        monitor_data.append(power_draw)
        time.sleep(1)

# Function to update carbon footprint and cost
def update_carbon_and_cost():
    while True:
        if len(cpu_data) > 0 and len(gpu_data) > 0 and len(ram_data) > 0 and len(monitor_data) > 0:
            total_power = cpu_data[-1][1] + (gpu_data[-1][1] if gpu_monitoring_available else 0) + ram_data[-1][1] + monitor_data[-1]  # Total power in watts
            energy_kwh = (total_power / 1000) * (1 / 3600)  # Convert watts to kWh (per second)
            carbon_footprint = energy_kwh * CARBON_CONVERSION_FACTOR  # kg CO₂
            cost = energy_kwh * ELECTRICITY_COST_PER_KWH  # ₹

            carbon_data.append(carbon_footprint)
            cost_data.append(cost)
        time.sleep(1)

# Function to update network data (sent/received)
def update_network_data():
    while True:
        net_io = psutil.net_io_counters()
        data_sent = net_io.bytes_sent / (1024 * 1024)  # Convert to MB
        data_received = net_io.bytes_recv / (1024 * 1024)  # Convert to MB
        network_data.append((data_sent, data_received))
        time.sleep(1)

# Function to create live graph pop-ups
def create_popup(title, data_fetcher, ylabel, labels=None, gpu_info=None):
    popup = Toplevel()
    popup.title(title)
    popup.configure(bg="white")  # White background

    if gpu_info:
        gpu_frame = tk.Frame(popup, bg="white")
        gpu_frame.pack(pady=10)

        tk.Label(gpu_frame, text=f"GPU Info:", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(gpu_frame, text=gpu_info, font=("Arial", 12), bg="white", fg="black").grid(row=0, column=1, sticky="w", padx=5)

    figure, ax = plt.subplots(figsize=(8, 4))
    canvas = FigureCanvasTkAgg(figure, master=popup)
    canvas.get_tk_widget().pack()

    def update_graph():
        ax.clear()
        ax.set_title(title, fontsize=14, fontweight="bold", color="black")
        
        # Set axis labels with darker grey for better visibility
        ax.set_xlabel("Time (s)", fontsize=12, color="black")
        ax.set_ylabel(ylabel, fontsize=12, color="black")
        
        # Add grid for better readability
        ax.grid(True, linestyle='--', alpha=0.7, color="gray")
        
        # Adjust tick parameters for better contrast
        ax.tick_params(axis='x', labelsize=10, colors="black")
        ax.tick_params(axis='y', labelsize=10, colors="black")
        
        data = data_fetcher()
        
        if len(data) > 0:
            if labels:
                for i, label in enumerate(labels):
                    data_points = [item[i] for item in data]
                    ax.plot(range(len(data)), data_points, label=label, marker="o", markersize=5, color="blue")  # Updated line color
                    # Add data values on the graph for clarity
                    for j, txt in enumerate(data_points):
                        ax.annotate(f'{txt:.2f}', (j, data_points[j]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=9, color="black")
                ax.legend()
            else:
                data_points = [item for item in data]
                ax.plot(range(len(data)), data_points, marker="o", markersize=5, color="green")  # Default line color with markers
                # Add data values on the graph for clarity
                for j, txt in enumerate(data_points):
                    ax.annotate(f'{txt:.2f}', (j, data_points[j]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=9, color="black")
        
        # Redraw the canvas to update the plot
        canvas.draw()
        
        # Call update_graph again after 1 second for live updates
        popup.after(1000, update_graph)

    update_graph()

# Function to create numerical output pop-ups
def create_numerical_popup(title, data_fetcher, labels=None):
    popup = Toplevel()
    popup.title(title)
    popup.configure(bg="white")  # White background

    frame = tk.Frame(popup, bg="white")
    frame.pack(pady=10, padx=10)

    data = data_fetcher()
    if len(data) > 0:
        for i, label in enumerate(labels):
            tk.Label(frame, text=f"{label}:", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=i, column=0, sticky="w", padx=5)
            tk.Label(frame, text=f"{data[-1][i]:.2f}", font=("Arial", 12), bg="white", fg="black").grid(row=i, column=1, sticky="w", padx=5)
    else:
        tk.Label(frame, text="No data available", font=("Arial", 12), bg="white", fg="black").pack()

# Functions to fetch live data
def fetch_cpu_data():
    return cpu_data[-60:] if len(cpu_data) > 60 else cpu_data

def fetch_gpu_data():
    return gpu_data[-60:] if len(gpu_data) > 60 else gpu_data

def fetch_ram_data():
    return ram_data[-60:] if len(ram_data) > 60 else ram_data

def fetch_monitor_data():
    return monitor_data[-60:] if len(monitor_data) > 60 else monitor_data

def fetch_carbon_data():
    return carbon_data[-60:] if len(carbon_data) > 60 else carbon_data

def fetch_network_data():
    return network_data[-60:] if len(network_data) > 60 else network_data

# Function to display system runtime
def calculate_runtime():
    elapsed_time = time.time() - start_time
    runtime = str(timedelta(seconds=int(elapsed_time)))
    return runtime

# Main function
def main():
    root = tk.Tk()
    root.title("System Performance Monitor")
    root.state('zoomed')  # Maximize the window
    root.configure(bg="white")  # White background

    # Enable dynamic resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Layout frame
    frame = tk.Frame(root, bg="white")
    frame.pack(pady=20, fill="both", expand=True)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Buttons for graphs
    tk.Button(frame, text="CPU Utilization & Power Draw", command=lambda: create_popup(
        "CPU Utilization & Power Draw", fetch_cpu_data, "Percentage (%) / Power (W)", labels=["CPU Utilization (%)", "Power Draw (W)"]
    ), bg="lightblue", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="GPU Utilization & Power Draw", command=lambda: create_popup(
        "GPU Utilization & Power Draw", fetch_gpu_data, "Percentage (%) / Power (W)", labels=["GPU Utilization (%)", "Power Draw (W)"], gpu_info=get_gpu_info()
    ), bg="lightcoral", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="RAM Utilization & Power Draw", command=lambda: create_popup(
        "RAM Utilization & Power Draw", fetch_ram_data, "Percentage (%) / Power (W)", labels=["RAM Utilization (%)", "Power Draw (W)"]
    ), bg="lightgreen", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="Monitor Power Usage", command=lambda: create_popup(
        "Monitor Power Usage", fetch_monitor_data, "Power (W)"
    ), bg="lightblue", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="Carbon Footprint", command=lambda: create_popup(
        "Carbon Footprint", fetch_carbon_data, "Carbon Footprint (kg CO₂)"
    ), bg="lightgreen", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="Network Data (Sent/Received)", command=lambda: create_popup(
        "Network Data", fetch_network_data, "Data (MB)", labels=["Sent (MB)", "Received (MB)"]
    ), bg="lightblue", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

    # Buttons for numerical outputs
    tk.Button(frame, text="CPU Carbon Footprint", command=lambda: create_numerical_popup(
        "CPU Carbon Footprint", fetch_cpu_data, labels=["CPU Utilization (%)", "Power Draw (W)"]
    ), bg="lightblue", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="GPU Carbon Footprint", command=lambda: create_numerical_popup(
        "GPU Carbon Footprint", fetch_gpu_data, labels=["GPU Utilization (%)", "Power Draw (W)"]
    ), bg="lightcoral", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=3, column=1, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="RAM Carbon Footprint", command=lambda: create_numerical_popup(
        "RAM Carbon Footprint", fetch_ram_data, labels=["RAM Utilization (%)", "Power Draw (W)"]
    ), bg="lightgreen", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

    tk.Button(frame, text="Monitor Carbon Footprint", command=lambda: create_numerical_popup(
        "Monitor Carbon Footprint", fetch_monitor_data, labels=["Power Draw (W)"]
    ), bg="lightblue", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=4, column=1, padx=20, pady=20, sticky="nsew")

    # Runtime label
    runtime_label = tk.Label(root, text=f"System Runtime: {calculate_runtime()}", font=("Arial", 12, "bold"), fg="black", bg="white")
    runtime_label.pack(pady=10)

    # Updating runtime every second
    def update_runtime():
        runtime_label.config(text=f"System Runtime: {calculate_runtime()}")
        root.after(1000, update_runtime)

    update_runtime()

    # Start data collection in separate threads
    threads = [
        threading.Thread(target=update_cpu_data, daemon=True),
        threading.Thread(target=update_gpu_data, daemon=True) if gpu_monitoring_available else None,
        threading.Thread(target=update_ram_data, daemon=True),
        threading.Thread(target=update_monitor_data, daemon=True),
        threading.Thread(target=update_carbon_and_cost, daemon=True),
        threading.Thread(target=update_network_data, daemon=True),
    ]
    
    for t in threads:
        if t is not None:
            t.start()

    root.mainloop()

if __name__ == "__main__":
    main()