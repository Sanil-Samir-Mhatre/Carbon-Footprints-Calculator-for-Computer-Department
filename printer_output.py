import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

def load_current_report():
    with open("current_report.json", "r") as file:
        return json.load(file)

def return_back():
    root.destroy()

def show_current_report():
    report = load_current_report()
    
    # Create figure with appropriate spacing
    fig, axes = plt.subplots(3, 1, figsize=(8, 10))
    fig.suptitle("Printer Carbon Footprint Report", fontsize=18, fontweight='bold', y=0.98)
    
    # Pages Printed vs Carbon Footprint
    categories = ['Pages Printed', 'Carbon Footprint']
    values = [report['pageCount'], report['carbonFootprint']]
    axes[0].bar(categories, values, color=['blue', 'green'])
    axes[0].set_ylabel("Values", fontsize=12)
    axes[0].set_title("Pages Printed vs Carbon Footprint", fontsize=14)
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Cartridge Levels
    cartridge_levels = [report['cartridges'][color] for color in report['cartridges']]
    colors = ['black', 'cyan', 'magenta', 'yellow']
    axes[1].bar(colors, cartridge_levels, color=colors)
    axes[1].set_ylabel("Level (%)", fontsize=12)
    axes[1].set_title("Cartridge Levels", fontsize=14)
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    # Paper Tray Info
    tray_labels = list(report['paperTrays'].keys())
    tray_values = list(report['paperTrays'].values())
    axes[2].bar(tray_labels, tray_values, color='orange')
    axes[2].set_ylabel("Sheets", fontsize=12)
    axes[2].set_title("Paper Tray Capacities", fontsize=14)
    axes[2].grid(axis='y', linestyle='--', alpha=0.7)

    # Adjust layout to prevent overlap
    plt.subplots_adjust(top=0.90, hspace=0.5)
    
    # Display the figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

# Create GUI
root = tk.Tk()
root.title("Printer Report")
root.state('zoomed')  # Maximize the window

# Add Title
tk.Label(root, text="Printer Carbon Footprint Analysis", font=("Arial", 18, "bold")).pack(pady=15)

# Buttons
tk.Button(root, text="Generate Report", command=show_current_report, font=("Arial", 12), width=20).pack(pady=10)
tk.Button(root, text="Return", command=return_back, font=("Arial", 12), width=20).pack(pady=10)

root.mainloop()