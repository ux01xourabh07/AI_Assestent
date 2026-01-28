import os
import shutil

class ShipraTools:
    
    @staticmethod
    def list_directory(path="."):
        """Lists files and directories in the given path."""
        try:
            return os.listdir(path)
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    @staticmethod
    def read_file(file_path):
        """Reads a file and returns its content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def write_file(file_path, content):
        """Writes content to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File written successfully: {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    @staticmethod
    def create_folder(folder_path):
        """Creates a folder."""
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"Folder created: {folder_path}"
        except Exception as e:
            return f"Error creating folder: {str(e)}"
