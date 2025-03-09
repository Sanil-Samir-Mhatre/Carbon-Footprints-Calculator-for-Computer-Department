import tkinter as tk
from tkinter import filedialog

def show_report():
    with open("manual_output_data.txt", "r") as f:
        data = f.readlines()

    emission_factors = {
        "computers": 0.06,  # kg CO2 per hour
        "laptops": 0.05,    # kg CO2 per hour
        "monitors": 0.02,   # kg CO2 per hour
        "projectors": 0.1,  # kg CO2 per hour
        "switches": 0.01,   # kg CO2 per hour
        "servers": 0.2,     # kg CO2 per hour
        "acs": 0.5,         # kg CO2 per hour
        "fans": 0.01,       # kg CO2 per hour
        "lights": 0.01,     # kg CO2 per hour
        "ups": 0.1,         # kg CO2 per hour
        "electricity": 0.5  # kg CO2 per kWh
    }

    report_text = "Manually Calculated Carbon Footprints Report:\n\n"
    total_carbon_footprint = 0

    questions = [
        "Total number of computers in labs and offices",
        "Average daily usage of computers",
        "Number of laptops in use",
        "Average daily usage of laptops",
        "Number of monitors in use",
        "Screen sizes of the monitors",
        "Power ratings of the monitors",
        "Number of projectors installed",
        "Daily usage of projectors",
        "Number of network switches and routers operational 24/7",
        "Network servers running 24/7 and their power consumption",
        "Number of air conditioners installed",
        "Daily usage of air conditioners",
        "Number of ceiling fans used",
        "Daily operational duration of ceiling fans",
        "Number of tube lights/LED bulbs in use",
        "Power ratings of tube lights/LED bulbs",
        "UPS or generators and their power rating",
        "Usage time of UPS or generators",
        "Source of electricity",
        "Average electricity consumption per month",
        "Water coolers or dispensers used and their usage time",
        "Number of CCTV cameras operational",
        "Power rating of CCTV cameras",
        "Frequency of replacing old computers, monitors, or laptops",
        "Disposal method of old or non-functional electronic devices",
        "E-waste collection and disposal policy",
        "Safe disposal or recycling of batteries from UPS systems, laptops, or other devices",
        "Initiative to refurbish or donate old computers instead of discarding them"
    ]

    for i, question in enumerate(questions):
        answer = data[i].strip()
        if answer:
            if i == 0:
                carbon_footprint = int(answer) * emission_factors["computers"]
            elif i == 1:
                carbon_footprint = int(answer) * emission_factors["computers"]
            elif i == 2:
                carbon_footprint = int(answer) * emission_factors["laptops"]
            elif i == 3:
                carbon_footprint = int(answer) * emission_factors["laptops"]
            elif i == 4:
                carbon_footprint = int(answer) * emission_factors["monitors"]
            elif i == 5:
                carbon_footprint = int(answer) * emission_factors["monitors"]
            elif i == 6:
                carbon_footprint = int(answer) * emission_factors["monitors"]
            elif i == 7:
                carbon_footprint = int(answer) * emission_factors["projectors"]
            elif i == 8:
                carbon_footprint = int(answer) * emission_factors["projectors"]
            elif i == 9:
                carbon_footprint = int(answer) * emission_factors["switches"]
            elif i == 10:
                carbon_footprint = int(answer) * emission_factors["servers"]
            elif i == 11:
                carbon_footprint = int(answer) * emission_factors["acs"]
            elif i == 12:
                carbon_footprint = int(answer) * emission_factors["acs"]
            elif i == 13:
                carbon_footprint = int(answer) * emission_factors["fans"]
            elif i == 14:
                carbon_footprint = int(answer) * emission_factors["fans"]
            elif i == 15:
                carbon_footprint = int(answer) * emission_factors["lights"]
            elif i == 16:
                carbon_footprint = int(answer) * emission_factors["lights"]
            elif i == 17:
                carbon_footprint = int(answer) * emission_factors["ups"]
            elif i == 18:
                carbon_footprint = int(answer) * emission_factors["ups"]
            elif i == 20:
                carbon_footprint = int(answer) * emission_factors["electricity"]
            else:
                carbon_footprint = 0

            total_carbon_footprint += carbon_footprint
            report_text += f"{i+1}. {question}: {answer} - Carbon Footprint: {carbon_footprint:.2f} kg CO2\n"
        else:
            report_text += f"{i+1}. {question}: Not answered\n"

    report_text += f"\nTotal Carbon Footprint: {total_carbon_footprint:.2f} kg CO2"

    report_label.config(text=report_text)

def download_report():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(report_label.cget("text"))

root = tk.Tk()
root.title("Carbon Footprints Report")
root.state('zoomed')  # Maximize the window

report_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
report_label.pack(pady=20)

download_button = tk.Button(root, text="Download Report", command=download_report)
download_button.pack(pady=10)

show_report()

root.mainloop()