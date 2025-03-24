import pandas as pd
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
from FileManager.FileManager import FileManager
from TrafficControl.TrafficControlConfig import TRAFFIC_LIGHT_MODE
from Simulation.Simulation import TRAFFIC_GEN_SCALE


class DataLogger:
    """
    Log data using pandas and support flexible columns and data-types via **kwargs
    """
    def __init__(self, log_dir: str, plot_dir: str):
        """
        Initializes an instance of DataLogger
        :param log_dir: Directory to store log files
        :param plot_dir: Directory to store plots
        """
        self.log_manager = FileManager(log_dir)
        self.plot_dir = plot_dir
        os.makedirs(self.plot_dir, exist_ok=True)
        self.data = pd.DataFrame()

    def log_data(self, **kwargs):
        """
        Logs data dynamically based on provided keyword arguments
        :param kwargs: Key-Value pairs of data to log
        """
        new_entry = pd.DataFrame([kwargs])  # Convert kwargs to single-row DataFrame
        self.data = pd.concat([self.data, new_entry], ignore_index=True)

    def save_log(self, file_name: str):
        """
        Saves logged data to a CSV file with the given name and creation time
        File named as {file_name}_Y-M-D-H-M-S.csv
        :param file_name: Name of log file
        """
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = self.log_manager.save_csv(self.data, f"{file_name}_{current_time}.csv")
        print(f"DataLogger: Log saved to {file_path}")

    def get_dataframe(self):
        """
        Returns logged data as a pandas DataFrame
        :return: Pandas DataFrame
        """
        return self.data

    def end_collection(self, file_name: str):
        """
        Saves self.data to file_name in CSV format
        Plots average trip time and average wait time
        :param file_name: Name of log file
        """
        self.save_log(file_name)

        # Compute average trip time and average wait time
        avg_trip_time = self.compute_average_trip_time()
        avg_wait_time = self.compute_average_wait_time()

        # Plot valid averages
        if avg_trip_time is not None and avg_wait_time is not None:
            fig, ax = plt.subplots()
            bars = ax.bar(['Trip Time', 'Wait Time'], [avg_trip_time, avg_wait_time])  # Add label, data to x-axis
            # Add value labels to the bars
            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,  # x position (center of the bar)
                    bar.get_height(),  # y position (top of the bar)
                    f'{bar.get_height(): .2f}',  # Label text (the value of the bar, formatted to 2 decimal places)
                    ha='center',  # Horizontal alignment (center the label on the bar)
                    va='bottom',  # Vertical alignment (places the label above the bar)
                    fontsize=10,  # Font size
                    color='black'  # Label color
                )
            ax.set_ylabel("Time (seconds)")  # Label y-axis
            ax.set_title(f"Average Trip Time and Average Wait Time\n{TRAFFIC_LIGHT_MODE}: Congestion {TRAFFIC_GEN_SCALE}\nvehicle_count_fixed_time()")  # Label graph title
            plt.tight_layout()  # Adjust plot to fit text
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            plot_path = os.path.join(self.plot_dir, f"avg_trip_wait_times_{TRAFFIC_LIGHT_MODE}_{current_time}.png")
            plt.savefig(plot_path)  # Save plot
            plt.close()  # Close plot
            print(f"DataLogger: Plot saved to {plot_path}.")

    def compute_average_trip_time(self):
        """
        Reads tripinfo.xml and computes average trip time for all vehicles
        :return: average trip time
        """
        return self.compute_average("../tripinfo.xml", "tripinfo", "duration")

    def compute_average_wait_time(self):
        """
        Reads tripinfo.xml and computes average wait time for all vehicles
        :return average wait time
        """
        return self.compute_average("../tripinfo.xml", "tripinfo", "waitingTime")

    def compute_average(self, xml_file: str, element: str, attribute: str):
        """
        Computes averages of a child element from an xml_file
        :param xml_file: File to be parsed
        :param element: Parent element
        :param attribute: Attribute to be averaged
        :return: Average of all attributes (float), None if not found
        """
        try:
            path = os.path.join(self.log_manager.main_directory_path, "../", xml_file)
            print(f"DataLogger: Trying to open: {path}")
            tree = ET.parse(path)
            root = tree.getroot()

            # Define the XML namespace
            namespace = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

            attribute_values = []

            # Extract attribute values from element(s) and place into attribute_values
            for elem in root.findall(f".//{element}", namespaces=namespace):
                attribute_values.append(float(elem.get(attribute)))

            # Return None if no child_element values found
            if not attribute_values:
                return None

            # Average and return child_element_values
            avg = sum(attribute_values) / len(attribute_values)
            return avg

        # Handle exceptions
        except FileNotFoundError:
            print(f"DataLogger: {xml_file} not found.")
            return None
        except ET.ParseError:
            print(f"Failed to parse {xml_file} with parent element {element} and attribute {attribute}.")
            return None




