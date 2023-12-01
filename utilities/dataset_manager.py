import os
import shutil
from typing import cast

from utilities.base import Base


class DatasetManager(Base):
  def get_files_in_directory(self, base_path: str):
    """
    function return dict where keys are paths to directories and values are paths to the content of folders, except folders paths
    """
    directory_files_map = {}

    # Walking through the directory
    for root, dirs, files in os.walk(base_path):
        file_paths = [os.path.join(root, file) for file in files]
        directory_files_map[root] = file_paths

    return directory_files_map
  
  def get_not_empty_subfolder_paths(self, base_path: str, pattern: str = 'закол', threshold: int = 0):
    """
    returns all subfolder paths that contain
    """
    # Get the dictionary with folder paths as keys and file lists as values
    folder_files_map = self.get_files_in_directory(base_path)

    paths = []

    # Print the result (optional)
    for folder, files in folder_files_map.items():
        folder = cast(str, folder)
        if pattern in folder.lower() and len(files) > threshold:
          print(f"Folder: {folder} \nfile_count={len(files)}\n")
          paths.append(folder)

        # for file in files:
        #     print(f"  - {file}")
    return paths

  def print_tree(self, directory: str, prefix=''):
    files_and_directories = sorted(os.listdir(directory))
    for count, item in enumerate(files_and_directories):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            print(prefix + '├── ' + item)
            if count == len(files_and_directories) - 1:
                new_prefix = prefix + '    '
            else:
                new_prefix = prefix + '│   '
            self.print_tree(path, new_prefix)
        else:
            print(prefix + '├── ' + item)

  def copy_relevant_datasets(self, root_directory: str, destionation_path: str) -> list[tuple[str, str, str]]:
    """
    copies only relevant data organizing in subfolders convenient for prediction
    """
    paths = self.get_not_empty_subfolder_paths(root_directory, 'закол', 0)
    folder_files_map = self.get_files_in_directory(root_directory)
    extracted_subpaths = []

    i = 0

    for path in paths:
        # Find the index of "КЦТ_Фото_Шахты" in the path
        index = path.find("КЦТ_Фото_Шахты")

        if index != -1:
            working_dir = os.path.join(destionation_path, f'{i}')
            image_path = os.path.join(working_dir, 'input')
            self.copy_and_rename_files(f'{i}', folder_files_map[path], image_path)
            extracted_subpaths.append((path, working_dir, image_path))
            i += 1
    
    return extracted_subpaths

  def copy_and_rename_files(self, prefix: str, file_paths: list[str], destination_folder: str):
    """
    copies files with provided paths to destionation_folder and renames enumerate
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for i, file_path in enumerate(file_paths, start=1):
      if os.path.isfile(file_path):
        # Extract the extension from the original file
        extension = os.path.splitext(file_path)[1]

        # Construct the new file name
        new_file_name = f"{prefix}_{i}{extension}"

        # Construct the full path for the new file
        new_file_path = os.path.join(destination_folder, new_file_name)

        # Copy and rename the file
        shutil.copy(file_path, new_file_path)
        print(f"Copied {file_path} to {new_file_path}")
      else:
        print(f"Skipped non-existing file: {file_path}")