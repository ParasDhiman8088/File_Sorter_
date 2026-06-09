# File Sorter

A simple Python utility to organize files by extension and mark folders that had files extracted during sorting.

## Features

- Recursively scans a source directory for all files
- Moves files into folders named after their extension, such as `JPG`, `PDF`, `MP4`, or `NO_EXTENSION`
- Handles nested directories and keeps files safe by avoiding name collisions
- Marks source folders that had files moved out by appending `-data extractid from-` to the folder name
- Preserves existing folder names while indicating which directories were partially emptied

## How it works

1. The script collects all files under the configured source folder.
2. It determines each file's extension and creates a matching destination folder inside the source directory.
3. Files are moved into the appropriate extension folder.
4. Any source folders from which files were moved are renamed with the suffix `-data extractid from-`, except the root source folder and newly created extension folders.

## Usage

1. Open `File_Sorter_.py`.
2. Update the `SOURCE_FOLDER` constant to point to the folder you want to organize.
3. Run the script with Python:

```bash
python File_Sorter_.py
```
## Notes

- The root source folder itself is not renamed.
- Newly created extension folders are excluded from marking.
- Files without an extension are moved into `NO_EXTENSION`.

## Requirements

- Python 3

## License

Use this script freely and adapt it as needed for your own file organization workflows.
