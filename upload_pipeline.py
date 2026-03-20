import os
import shutil
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# ==========================================================
# SECURE UPLOAD PIPELINE
# ==========================================================
# Run this script standalone to securely update the live 
# dashboard database without exposing upload functionality 
# to the public app. 
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ACTIVE_DB_NAME = "Matrix_Database_2020_2024.csv"
ACTIVE_DB_PATH = os.path.join(DATA_DIR, ACTIVE_DB_NAME)

ARCHIVE_DIR = os.path.join(DATA_DIR, "archive_databases")

def prompt_for_file():
    """Opens a native file dialog to select the new CSV."""
    # Hide the main Tkinter root window
    root = tk.Tk()
    root.withdraw()
    
    # Force window to top
    root.attributes('-topmost', True)
    
    file_path = filedialog.askopenfilename(
        title="Select New Database (CSV)",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    
    return file_path

def perform_upload(new_file_path):
    # 1. Ensure archive directory exists
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
        
    # 2. Backup the current active database if it exists
    if os.path.exists(ACTIVE_DB_PATH):
        timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        backup_name = f"Archive_{ACTIVE_DB_NAME.replace('.csv', '')}_{timestamp}.csv"
        backup_path = os.path.join(ARCHIVE_DIR, backup_name)
        
        print(f"[*] Archiving current live database to:\n    {backup_path}")
        shutil.copy2(ACTIVE_DB_PATH, backup_path)
    else:
        print("[!] No active database found to backup. Proceeding with fresh upload.")
        
    # 3. Replace active database with new file
    print(f"[*] Copying selected file into live system...")
    try:
        shutil.copy2(new_file_path, ACTIVE_DB_PATH)
        print(f"[+] SUCCESS! Database updated.")
        
        # Show a quick GUI confirmation
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showinfo("Upload Complete", "The Live Database has been successfully updated!")
        
    except Exception as e:
        print(f"[-] FAILED to copy database: {e}")

if __name__ == "__main__":
    print("====================================")
    print(" SECURE DATABASE UPLOADER ")
    print("====================================")
    
    print("[*] Waiting for file selection...")
    selected_file = prompt_for_file()
    
    if not selected_file:
        print("[-] Operation Cancelled. No file selected.")
    else:
        print(f"[+] Loaded: {selected_file}")
        
        # Small sanity check
        if not selected_file.lower().endswith('.csv'):
            print("[!] WARNING: Selected file is not a .csv!")
            
        perform_upload(selected_file)
        
    print("====================================")
    print(" Pipeline Execution Complete.")
    print("====================================")
