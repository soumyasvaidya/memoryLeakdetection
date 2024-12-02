import os

def list_directory(directory_path):
    try:
        # List all files and directories in the specified path
        files = os.listdir(directory_path)
        
        # Return the list of files and directories
        return files
    except FileNotFoundError:
        print(f"Error: The directory {directory_path} does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to access {directory_path}.")
    except Exception as e:
        print(f"Error: {e}")


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file {file_path}.")
    except Exception as e:
        print(f"Error: {e}")

import os

def find_file_in_folder(folder_path, file_name):
    try:
        # List all files in the folder
        files_in_directory = os.listdir(folder_path)

        # Check if the file is in the directory
        if file_name in files_in_directory:
            return f"File '{file_name}' found in {folder_path}."
        else:
            return f"File '{file_name}' not found in {folder_path}."
    except FileNotFoundError:
        return f"Error: The folder {folder_path} does not exist."
    except PermissionError:
        return f"Error: You do not have permission to access {folder_path}."
    except Exception as e:
        return f"Error: {e}"

