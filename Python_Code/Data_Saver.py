import os
import json

class DataSaver:
    """A class to handle saving and loading data."""

    def __init__(self, base_directory='Data'):
        """
        Initializes the DataSaver with a base directory.

        Args:
            base_directory (str): The base directory for saving data.
        """
        self.base_directory = base_directory
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def save_output(self, data, filename, location='Scraped_Data', extension='json'):
        """
        Saves data to a file with a timestamped filename.

        Args:
            data: The data to save.
            filename (str): The base filename.
            location (str): The subdirectory to save to.
            extension (str): The file extension ('json' or 'txt').
        """
        save_path = os.path.join(self.current_dir, self.base_directory, location)
        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, f"{filename}.{extension}")

        try:
            if extension == 'json':
                self._save_json(data, file_path)
            elif extension == 'txt':
                self._save_txt(data, file_path)
            else:
                print(f"❌ Unsupported extension: {extension}")
                return

            print(f"✅ Data saved in '{filename}.{extension}'.")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def _save_json(self, data, file_path):
        """Saves data to a JSON file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _save_txt(self, data, file_path):
        """Saves data to a text file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            if isinstance(data, dict):
                for key, value in data.items():
                    file.write(f"{key}: {value}\n")
            elif isinstance(data, list):
                for item in data:
                    file.write(f"{item}\n")
            else:
                file.write(str(data))

    def upload_contexts(self, filename):
        """
        Loads data from a JSON file in the 'Scraped_Data' location.

        Args:
            filename (str): The filename (without extension).

        Returns:
            The loaded data (as a Python object).
        """
        file_path = os.path.join(self.current_dir, self.base_directory, 'Scraped_Data', f'{filename}.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"❌ File not found: {filename}.json")
            return None  # Or raise the exception, depending on your needs
        except json.JSONDecodeError:
            print(f"❌ Error decoding JSON in: {filename}.json")
            return None
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            return None