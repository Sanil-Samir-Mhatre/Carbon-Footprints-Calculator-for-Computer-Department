import tkinter as tk
from tkinter import ttk
import os

def calculate_carbon_footprints():
    data = []
    for entry in entries:
        data.append(entry.get())
    with open("manual_output_data.txt", "w") as f:
        for item in data:
            f.write("%s\n" % item)
    os.system('python manual_output.py')

root = tk.Tk()
root.title("Manually Calculate Carbon Footprints")
root.state('zoomed')  # Maximize the window

# Create a canvas and a scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Add questions
questions = [
    "What is the total number of computers in labs and offices? (units)",
    "What is the average daily usage (in hours) of computers? (hours)",
    "How many laptops are in use? (units)",
    "What is the average daily usage of laptops? (hours)",
    "How many monitors are in use? (units)",
    "What are the screen sizes of the monitors? (inches)",
    "What are the power ratings of the monitors? (watts)",
    "How many projectors are installed? (units)",
    "How long are the projectors used daily? (hours)",
    "How many network switches and routers are operational 24/7? (units)",
    "Are there any network servers running 24/7? If yes, what is their power consumption? (watts)",
    "How many air conditioners (ACs) are installed? (units)",
    "How many hours are the air conditioners used daily? (hours)",
    "How many ceiling fans are used? (units)",
    "What is the daily operational duration of the ceiling fans? (hours)",
    "How many tube lights/LED bulbs are in use? (units)",
    "What are the power ratings of the tube lights/LED bulbs? (watts)",
    "Are there any UPS (Uninterruptible Power Supplies) or generators? If yes, what is their power rating? (watts)",
    "What is the usage time of the UPS or generators? (hours)",
    "What is the source of electricity (grid, solar, or generator)? (source)",
    "What is the average electricity consumption per month? (kWh)",
    "Are water coolers or dispensers used? If yes, how many? (units)",
    "How long are the water coolers or dispensers used daily? (hours)",
    "How many CCTV cameras are operational? (units)",
    "What is the power rating of the CCTV cameras? (watts)",
    "How often are old computers, monitors, or laptops replaced? (frequency)",
    "What happens to old or non-functional electronic devices? Are they recycled or disposed of? (disposal)",
    "Is there an e-waste collection and disposal policy in place? (policy)",
    "Are batteries from UPS systems, laptops, or other devices safely disposed of or recycled? (disposal)",
    "Is there any initiative to refurbish or donate old computers instead of discarding them? (initiative)"
]

entries = []

for question in questions:
    label = ttk.Label(scrollable_frame, text=question)
    label.pack(pady=5)
    entry = ttk.Entry(scrollable_frame, width=50)
    entry.pack(pady=5)
    entries.append(entry)

# Add Calculate button
calculate_button = ttk.Button(scrollable_frame, text="Calculate Carbon Footprints", command=calculate_carbon_footprints)
calculate_button.pack(pady=20)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()