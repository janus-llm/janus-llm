import os
import shutil
import random

def stratified_file_selection(src_dir, dest_dir, mandatory_file="PSSBPSUT.m", num_files=20):
    """
    Select files from src_dir using stratified sampling based on file size and move them to dest_dir.

    Parameters:
    - src_dir: Source directory containing the files.
    - dest_dir: Destination directory to move the selected files.
    - mandatory_file: A file that must be included in the selection.
    - num_files: Number of files to select and move. Default is 20.
    """

    # Ensure the source directory exists
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist!")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Get all files from the source directory and their sizes
    all_files = [(f, os.path.getsize(os.path.join(src_dir, f))) for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]

    # Sort files by size
    all_files.sort(key=lambda x: x[1])

    # Ensure the mandatory file is in the directory
    if mandatory_file not in [f[0] for f in all_files]:
        print(f"Mandatory file {mandatory_file} not found in the source directory!")
        return

    # Remove the mandatory file from the list and reduce the num_files by 1
    all_files = [f for f in all_files if f[0] != mandatory_file]
    num_files -= 1

    # Divide the files into intervals and select one from each
    interval_size = len(all_files) // num_files
    selected_files = []

    for i in range(num_files):
        start_idx = i * interval_size
        end_idx = start_idx + interval_size
        selected_file = random.choice(all_files[start_idx:end_idx])
        selected_files.append(selected_file[0])

    # Add the mandatory file to the selection
    selected_files.append(mandatory_file)

    # Move the selected files to the destination directory
    for file in selected_files:
        shutil.move(os.path.join(src_dir, file), os.path.join(dest_dir, file))

    print(f"Moved {len(selected_files)} files from {src_dir} to {dest_dir}.")

    
    
src_directory = "scripts/pharmacy_input"
dest_directory = "scripts/pharmacy_input_subset"
stratified_file_selection(src_directory, dest_directory)