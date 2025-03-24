import os

import joblib
import pandas as pd


class FileManager:
    """
    Manages File I/O from a given main directory
    """
    def __init__(self, main_directory_path):
        """
        Initializes an instance of a File Manager
        :param main_directory_path: Path to the main working directory
        """
        self.main_directory_path = main_directory_path
        os.makedirs(self.main_directory_path, exist_ok=True)

    def create_sub_dir(self, directory_name: str):
        """
        Creates a sub-directory with the given name
        :param directory_name: Name to give the sub-directory
        :return: sub_directory_path: Path to created sub-directory
        """
        sub_directory_path = os.path.join(self.main_directory_path, directory_name)
        os.makedirs(sub_directory_path)
        return sub_directory_path

    def get_latest_sub_dir(self):
        """
        Returns the path to the most recently created sub-directory, or None if none exist
        :return: Path to most recently created sub-directory
        """
        sub_directories = [f for f in os.listdir(self.main_directory_path) if os.path.isdir(os.path.join(self.main_directory_path, f))]

        if not sub_directories:
            return None

        latest_sub_dir = max(sub_directories, key=lambda f: os.path.getctime(os.path.join(self.main_directory_path, f)))
        return os.path.join(self.main_directory_path, latest_sub_dir)

    def get_latest_csv(self):
        """
        Returns the path to the most recently created CSV file in the managed directory, or None if none exist
        :return: Path to most recently created CSV
        """
        csv_files = [f for f in os.listdir(self.main_directory_path) if f.endswith('.csv')]

        if not csv_files:
            return None

        latest_csv = max(csv_files, key=lambda f: os.path.getctime(os.path.join(self.main_directory_path, f)))
        return os.path.join(self.main_directory_path, latest_csv)

    def load_csv(self, file_name):
        """
        Loads the given CSV file from the managed directory into a Pandas dataframe
        :param file_name: Name of the CSV file to load
        :return: Pandas dataframe of loaded CSV data
        """
        return pd.read_csv(os.path.join(self.main_directory_path, file_name))

    def load_latest_csv(self):
        """
        Loads the most recently created CSV file in the managed directory into a Pandas dataframe
        :return: Pandas dataframe of loaded CSV data
        """
        return pd.read_csv(self.get_latest_csv())

    def save_csv(self, data: pd.DataFrame, file_name):
        """
        Saves the given Pandas dataframe to a CSV file with the given name
        :param data: Pandas dataframe to save
        :param file_name: File to save to
        :return: Path file saved to
        """
        file_path = os.path.join(self.main_directory_path, file_name)
        data.to_csv(file_path, index=False)
        return file_path

    def load_pkl(self, file_name):
        """
        Loads the given .pkl file in the managed directory into a Pandas dataframe
        :param file_name: Name of the .pkl file to load
        :return: Object loaded from given .pkl file
        """
        return joblib.load(os.path.join(self.main_directory_path, file_name))

    def save_pkl(self, data, file_name, sub_dir_path=None):
        """
        Saves the given data into a .pkl file
        :param data: Data to save to file
        :param file_name: Name of file to save to
        :param sub_path: Path inside main directory to save file within, if provided
        :return: Path file saved to
        """
        path = os.path.join(self.main_directory_path, sub_dir_path if not None else "", file_name)
        joblib.dump(data, path)
        return path
