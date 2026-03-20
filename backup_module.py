import os
import shutil
from datetime import datetime

def create_restore_point(source_dir="modules", backup_root=".backups"):
    """
    Creates a timestamped geographical copy of the source_dir.
    Returns the absolute or relative path to the new backup.
    """
    try:
        
        if not os.path.exists(backup_root):
            os.makedirs(backup_root)
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = os.path.join(backup_root, f"{source_dir}_backup_{timestamp}")
        
        # Copy the directory tree
        shutil.copytree(source_dir, backup_path, dirs_exist_ok=True)
        return backup_path
    except Exception as e:
        raise Exception(f"Failed to create restore point: {str(e)}")

# Allow direct execution via CLI
if __name__ == "__main__":
    bp = create_restore_point()
    print(f"Restore point created successfully at: {bp}")
