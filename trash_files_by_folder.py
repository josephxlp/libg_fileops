import os
import shutil
from concurrent.futures import ThreadPoolExecutor

def delete_folder_contents(folder_path, verbose=False):
    """
    Deletes all contents (files, subdirectories, and hidden files) inside a given folder.

    Args:
        folder_path (str): Path to the folder whose contents need to be deleted.
        verbose (bool): If True, prints the names of files/folders being removed.

    Returns:
        None
    """
    def delete_path(path):
        """Deletes a file or directory recursively."""
        try:
            if os.path.isfile(path) or os.path.islink(path):
                if verbose:
                    print(f"Deleting file: {path}")
                os.unlink(path)  # Remove file or symbolic link
            elif os.path.isdir(path):
                if verbose:
                    print(f"Deleting folder: {path}")
                shutil.rmtree(path)  # Remove directory and its contents
        except Exception as e:
            print(f"Error deleting {path}: {e}")

    # Validate folder path
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
    if not os.path.isdir(folder_path):
        raise ValueError(f"'{folder_path}' is not a valid directory.")

    # Collect all paths to delete
    paths_to_delete = []
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            paths_to_delete.append(os.path.join(root, name))
        for name in dirs:
            paths_to_delete.append(os.path.join(root, name))

    # Use parallel processing to delete paths
    with ThreadPoolExecutor() as executor:
        executor.map(delete_path, paths_to_delete)

    print(f"All contents of folder '{folder_path}' have been deleted.")

# Example usage
if __name__ == "__main__":
    folder_to_clean = "/"
    delete_folder_contents(folder_to_clean, verbose=True)  # Clean everything with verbose output