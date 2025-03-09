## Carbon-Footprints-Calculator-for-Computer-Department
A comprehensive tool for calculating and analyzing the carbon footprints of various devices and activities within a computer department, using both automated and manual data inputs.

# Carbon Footprints Calculator for Computer Department

## Overview

This project is a comprehensive tool designed to calculate and analyze the carbon footprints of various devices and activities within a computer department. It leverages both automated data inputs from devices and manual data inputs from users to provide accurate and reliable carbon footprint calculations.

## Features

- **Automated Data Collection**: Automatically fetches data from devices such as printers, desktops, and network equipment.
- **Manual Data Entry**: Allows users to manually input data for devices and activities not covered by automated collection.
- **Detailed Reports**: Generates detailed reports on carbon footprints, including graphical representations.
- **User Authentication**: Includes a login system to personalize the experience and save user details.
- **Graphical User Interface (GUI)**: User-friendly interface built with Tkinter for easy interaction.

## Project Structure

- `index.py`: Main entry point for the application, providing options to calculate carbon footprints for different categories.
- `login.py`: Handles user authentication and saves user details.
- `printer_carbon_footprints.py`: Calculates carbon footprints for printers.
- `desktop_carbon_footprints.py`: Monitors and calculates carbon footprints for desktops.
- `wifi_carbon_footprints.py`: Calculates carbon footprints for network devices using WiFi.
- `manuallycalculated_carbon_footprints.py`: Allows users to manually input data for various devices and activities.
- `printer_output.py`: Generates graphical reports for printer data.
- `manual_output.py`: Processes and displays manually entered data.
- `fake_printer_server.py`: Simulates a printer API for testing purposes.
- `other_programs.py`: Placeholder for additional features.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/carbon-footprints-calculator.git
    cd carbon-footprints-calculator
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the `login.py` script to start the application:
    ```bash
    python login.py
    ```

2. Log in with your details and navigate through the options to calculate carbon footprints for different categories.

## Flow of the Project

1. **Login**: Users log in using the `login.py` script, which saves their details.
2. **Main Menu**: The `index.py` script provides options to calculate carbon footprints for printers, desktops, network devices, and manual entry.
3. **Automated Data Collection**: Scripts like `printer_carbon_footprints.py` and `desktop_carbon_footprints.py` automatically fetch data from devices.
4. **Manual Data Entry**: The `manuallycalculated_carbon_footprints.py` script allows users to input data manually.
5. **Report Generation**: Scripts like `printer_output.py` and `manual_output.py` generate detailed reports and graphical representations of the data.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
