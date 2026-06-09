import os
import shutil

# Change this path to the folder you want to organize.
# Example: r"C:\Users\YourName\Downloads"
SOURCE_FOLDER = r"******path to the folder you want to organize******"

# This list stores all files before moving them.
# This helps when files are inside many nested folders.
files_to_move = []

# Keep track of folders that had files moved from them.
moved_folders = set()
# Keep track of extension folders created during sorting.
extension_folders = set()

FOLDER_MARK_SUFFIX = "-data extractid from-"


def get_unique_destination(dest_folder, filename):
    # If the file name is free, use it normally.
    # Example: report.txt -> TXT\report.txt
    destination = os.path.join(dest_folder, filename)
    if not os.path.exists(destination):
        return destination

    name, ext = os.path.splitext(filename)
    counter = 1

    # If same name exists, add _1, _2, etc.
    # Example: report.txt -> report_1.txt
    while True:
        new_filename = f"{name}_{counter}{ext}"
        destination = os.path.join(dest_folder, new_filename)

        if not os.path.exists(destination):
            return destination

        counter += 1


def get_unique_folder_name(folder_path):
    if not os.path.exists(folder_path):
        return folder_path

    parent, folder_name = os.path.split(folder_path)
    counter = 1

    while True:
        candidate = os.path.join(parent, f"{folder_name}_{counter}")
        if not os.path.exists(candidate):
            return candidate
        counter += 1


for root, dirs, filenames in os.walk(SOURCE_FOLDER):
    # os.walk goes through folders inside folders.
    # Example: test_data\A\B\C\file.txt
    for filename in filenames:
        filepath = os.path.join(root, filename)
        files_to_move.append((filepath, filename))

for filepath, filename in files_to_move:
    # Get file extension.
    # Example: photo.JPG -> .jpg
    ext = os.path.splitext(filename)[1].lower()

    # Files with no extension go into NO_EXTENSION.
    # Example: README -> NO_EXTENSION
    if ext == "":
        ext = "NO_EXTENSION"
    else:
        ext = ext[1:]  # Remove the dot: .jpg -> jpg

    # Create destination folder using the extension name.
    # Example: jpg -> JPG folder
    dest_folder = os.path.join(SOURCE_FOLDER, ext.upper())
    abs_dest_folder = os.path.abspath(dest_folder)
    os.makedirs(dest_folder, exist_ok=True)
    extension_folders.add(abs_dest_folder)

    # Track the source folder so it can be marked later.
    source_folder = os.path.dirname(filepath)
    moved_folders.add(os.path.abspath(source_folder))

    # Pick a safe destination path before moving.
    destination = get_unique_destination(dest_folder, filename)

    # If the file is already in the right place, skip it.
    if os.path.abspath(filepath) == os.path.abspath(destination):
        continue

    # Move the file into the extension folder.
    shutil.move(filepath, destination)

    print(f"Moved: {filename} -> {ext.upper()}")

# Rename folders that had data extracted from them during sorting.
# Skip the root source folder and extension folders.
root_source = os.path.abspath(SOURCE_FOLDER)
for folder_path in sorted(moved_folders, key=lambda p: p.count(os.sep), reverse=True):
    if folder_path == root_source:
        continue
    if folder_path in extension_folders:
        continue
    folder_name = os.path.basename(folder_path)
    if folder_name.endswith(FOLDER_MARK_SUFFIX):
        continue

    marked_folder_path = os.path.join(os.path.dirname(folder_path), folder_name + FOLDER_MARK_SUFFIX)
    marked_folder_path = get_unique_folder_name(marked_folder_path)
    try:
        os.rename(folder_path, marked_folder_path)
        print(f"Marked folder: {folder_path} -> {marked_folder_path}")
    except OSError:
        print(f"Warning: could not rename folder {folder_path}")

print("\nFinished!")
