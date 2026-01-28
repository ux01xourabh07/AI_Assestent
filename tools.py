import os
import shutil

class ShipraTools:
    
    @staticmethod
    def list_directory(path="."):
        """Lists files and directories in the given path."""
        try:
            return os.listdir(path)
        except Exception as e:
            return str(e)

    @staticmethod
    def read_file(path):
        """Reads content of a text file."""
        if not os.path.exists(path):
            return "File does not exist."
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return str(e)

    @staticmethod
    def write_file(path, content):
        """Writes content to a file."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return str(e)
            
    @staticmethod
    def create_directory(path):
        """Creates a directory."""
        try:
            os.makedirs(path, exist_ok=True)
            return f"Directory {path} created."
        except Exception as e:
            return str(e)
