import os
import shutil
import zipfile
import time
import webbrowser
from datetime import datetime

# ==========================================================
# AUTOMATED BACKUP PIPELINE
# ==========================================================
# Run this script standalone to generate a clean, compressed
# archive of the entire project and automatically open 
# your Google Drive for drag-and-drop cloud storage.
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(PROJECT_ROOT, "System_Backups")
GDRIVE_URL = "https://drive.google.com/drive/folders/1yMixtx-1IL5pVOJPiffJ6HxKFsXrtEV_?usp=drive_link"

# Folders and files to ignore during the zipping process
IGNORE_DIRS = {".git", "__pycache__", ".venv", "env", "System_Backups", ".pytest_cache", ".streamlit"}
IGNORE_FILES = {".DS_Store"}

def create_backup_zip():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    zip_filename = f"Project_Backup_WSA_{timestamp}.zip"
    zip_filepath = os.path.join(BACKUP_DIR, zip_filename)
    
    print(f"[*] Starting local backup pipeline...")
    print(f"[*] Archiving project into: {zip_filepath}")
    
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the directory
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES or file.endswith('.pyc') or file == zip_filename:
                    continue
                
                # Absolute path of file
                file_path = os.path.join(root, file)
                # Relative path for the zip structure
                rel_path = os.path.relpath(file_path, PROJECT_ROOT)
                
                try:
                    zipf.write(file_path, rel_path)
                except Exception as e:
                    print(f"[!] Warning: Could not compress {rel_path} - {e}")

    print(f"[+] Backup successfully created! Size: {os.path.getsize(zip_filepath) / (1024*1024):.2f} MB")
    print(f"[+] Backup located at: {zip_filepath}")
    return zip_filepath

def push_to_cloud():
    print(f"[*] Launching browser to designated Google Drive folder...")
    time.sleep(1)
    try:
        webbrowser.open(GDRIVE_URL, new=2)
        print(f"[+] Browser opened successfully.")
    except Exception as e:
        print(f"[-] Failed to open browser automatically: {e}")
        print(f"[!] Please navigate manually to: {GDRIVE_URL}")

def open_local_folder(folder_path):
    print(f"[*] Opening local backup directory...")
    try:
        os.startfile(folder_path)
    except AttributeError:
        # Fallback for non-Windows if ever used
        import subprocess
        import sys
        if sys.platform == 'darwin':
            subprocess.Popen(['open', folder_path])
        else:
            subprocess.Popen(['xdg-open', folder_path])
    except Exception as e:
        print(f"[-] Could not open local folder: {e}")

if __name__ == "__main__":
    print("====================================")
    print(" WESTERN SAHARA ARCHIVE - BACKUP")
    print("====================================")
    
    saved_zip = create_backup_zip()
    
    print("------------------------------------")
    push_to_cloud()
    open_local_folder(BACKUP_DIR)
    
    print("====================================")
    print(" Pipeline Execution Complete.")
    print(" -> Drag the ZIP into the Drive window!")
    print("====================================")
