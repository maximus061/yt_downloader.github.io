import os
import shutil

# Define the source and destination directories
source_dir = 'C:/Users/Korisnik/Documents/yt_down'
dest_dir = 'C:/Users/Korisnik/Documents/yt_down/yt_downloader.github.io'

# Ensure the destination directory exists
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Move all files and directories from source to destination, excluding .git
for item in os.listdir(source_dir):
    if item == '.git':
        continue
    s = os.path.join(source_dir, item)
    d = os.path.join(dest_dir, item)
    try:
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    except PermissionError as e:
        print(f"Permission denied: {e}")

print("All files have been moved to the GitHub folder, excluding .git.")