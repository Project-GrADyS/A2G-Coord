import os
from zipfile import ZipFile, ZIP_DEFLATED

def create_folder(folder_path):
    """
    Creates a folder at the specified path if it doesn't already exist.

    Parameters:
    - folder_path (str): The path of the folder to create.
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating folder: {e}")

def create_zip_from_folder(folder_path, zip_name):
   """
    Creates a zip file of a folder.

    Parameters:
    - folder_path (str): The path of the folder.
    - zip_nanme (str): Name of he file.
    """
   with ZipFile(zip_name, "w", ZIP_DEFLATED) as zipf:
      for root, dirs, files in os.walk(folder_path):
         for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, start=folder_path))
