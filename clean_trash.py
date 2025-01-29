import os
import shutil
import concurrent.futures
from tqdm import tqdm

def delete_items(directory_path, delete_files=True, delete_dirs=True):
    full_path = os.path.expanduser(directory_path)
    
    try:
        items = os.listdir(full_path)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing {full_path}: {e}")
        return
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for item in items:
            item_path = os.path.join(full_path, item)
            
            if os.path.isfile(item_path) and delete_files:
                futures.append(executor.submit(os.remove, item_path))
            elif os.path.isdir(item_path) and delete_dirs:
                futures.append(executor.submit(shutil.rmtree, item_path))
        
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Deleting items", unit="item"):
            pass
    
    print(f"Cleanup complete for {full_path}.")

# Example usage
if __name__ == "__main__":
    trash_path = "~/.local/share/Trash/files"
    print("Starting cleanup...")
    delete_items(trash_path)