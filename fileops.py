import os
import shutil
import concurrent.futures
import time
from tqdm import tqdm


#libg_fileops

def copy_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)

def fast_copy_all(idpath, odpath, max_workers=8):
    files_to_copy = []
    
    for root, _, files in os.walk(idpath):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, idpath)
            dest_path = os.path.join(odpath, rel_path)
            files_to_copy.append((src_path, dest_path))
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        with tqdm(total=len(files_to_copy), desc="Copying files") as pbar:
            futures = {executor.submit(copy_file, *args): args for args in files_to_copy}
            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)
    end_time = time.time()
    print(f"Copy completed in {end_time - start_time:.2f} seconds")