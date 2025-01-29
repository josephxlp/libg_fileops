import os
import time
import shutil
import subprocess
import tarfile
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def copy_file(source, destination, threshold=1_000_000_000):
    try:
        file_size = os.path.getsize(source)
        if file_size > threshold:
            subprocess.run(['rsync', '-avh', source, destination], check=True)
        else:
            shutil.copy2(source, destination)
        print("File copied successfully")
    except Exception as e:
        print(f"Error copying file: {e}")

def move_file(source, destination, threshold=1_000_000_000):
    try:
        file_size = os.path.getsize(source)
        if file_size > threshold:
            subprocess.run(['rsync', '-avh', source, destination], check=True)
            os.remove(source)
        else:
            shutil.move(source, destination)
        print("File moved successfully")
    except Exception as e:
        print(f"Error moving file: {e}")

def delete_path(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        print(f"Deleted {path}")
    except Exception as e:
        print(f"Error deleting {path}: {e}")

def remove_directory_contents(directory_path):
    try:
        items = [os.path.join(directory_path, item) for item in os.listdir(directory_path)]
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(delete_path, item): item for item in items}
            for _ in tqdm(as_completed(futures), total=len(futures), desc="Deleting items", unit="item"):
                pass
        print(f"All contents of {directory_path} deleted.")
    except FileNotFoundError:
        print(f"Directory {directory_path} not found.")
    except Exception as e:
        print(f"Error deleting contents of {directory_path}: {e}")

def copy_directory(src, dst):
    os.makedirs(dst, exist_ok=True)
    try:
        subprocess.run(['tar', 'cf', '-', '-C', src, '.'], stdout=subprocess.PIPE, check=True)
        subprocess.run(['tar', 'xf', '-', '-C', dst], stdin=subprocess.PIPE, check=True)
        subprocess.run(['rsync', '--info=progress2', '-auvz', src, dst], check=True)
        print("Files copied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def extract_tarball(source, destination):
    if not os.path.exists(source):
        print(f"Error: {source} does not exist.")
        return
    os.makedirs(destination, exist_ok=True)
    try:
        with tarfile.open(source, "r:*") as tar:
            tar.extractall(path=destination)
        print(f"Extracted {source} to {destination}")
    except Exception as e:
        print(f"Error extracting tarball: {e}")

def create_tarball(source, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    try:
        with tarfile.open(destination, "w:gz") as tar:
            tar.add(source, arcname=os.path.basename(source))
        print(f"Tarball created at {destination}")
    except Exception as e:
        print(f"Error creating tarball: {e}")


def fast_copy_all(idpath, odpath, max_workers=8):
    files_to_copy = []
    
    for root, _, files in os.walk(idpath):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, idpath)
            dest_path = os.path.join(odpath, rel_path)
            files_to_copy.append((src_path, dest_path))
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with tqdm(total=len(files_to_copy), desc="Copying files") as pbar:
            futures = {executor.submit(copy_file, *args): args for args in files_to_copy}
            for future in as_completed(futures):
                pbar.update(1)
    end_time = time.time()
    print(f"Copy completed in {end_time - start_time:.2f} seconds")






def move_file(source, destination, threshold):
    try:
        file_size = os.path.getsize(source)
        if file_size > threshold:
            subprocess.run(['rsync', '-avh', source, destination], check=True)
            os.remove(source)
        else:
            shutil.move(source, destination)
        print("File moved successfully")
    except Exception as e:
        print(f"Error moving file: {e}")

def delete_path(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        print(f"Deleted {path}")
    except Exception as e:
        print(f"Error deleting {path}: {e}")

def remove_directory_contents(directory_path):
    try:
        items = [os.path.join(directory_path, item) for item in os.listdir(directory_path)]
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(delete_path, item): item for item in items}
            for _ in tqdm(as_completed(futures), total=len(futures), desc="Deleting items", unit="item"):
                pass
        print(f"All contents of {directory_path} deleted.")
    except FileNotFoundError:
        print(f"Directory {directory_path} not found.")
    except Exception as e:
        print(f"Error deleting contents of {directory_path}: {e}")

def copy_directory(src, dst):
    os.makedirs(dst, exist_ok=True)
    try:
        subprocess.run(['tar', 'cf', '-', '-C', src, '.'], stdout=subprocess.PIPE, check=True)
        subprocess.run(['tar', 'xf', '-', '-C', dst], stdin=subprocess.PIPE, check=True)
        subprocess.run(['rsync', '--info=progress2', '-auvz', src, dst], check=True)
        print("Files copied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def extract_tarball(source, destination):
    if not os.path.exists(source):
        print(f"Error: {source} does not exist.")
        return
    os.makedirs(destination, exist_ok=True)
    try:
        with tarfile.open(source, "r:*") as tar:
            tar.extractall(path=destination)
        print(f"Extracted {source} to {destination}")
    except Exception as e:
        print(f"Error extracting tarball: {e}")

def create_tarball(source, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    try:
        with tarfile.open(destination, "w:gz") as tar:
            tar.add(source, arcname=os.path.basename(source))
        print(f"Tarball created at {destination}")
    except Exception as e:
        print(f"Error creating tarball: {e}")



