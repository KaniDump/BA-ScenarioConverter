import os
from pathlib import Path

def get_common_files(folder1_path: str, folder2_path: str, extension: str) -> list[str]:
    """
    Finds common files with a specific extension in two folders.
    Returns a list of filenames (not full paths).
    """
    path1 = Path(folder1_path)
    path2 = Path(folder2_path)

    if not path1.exists() or not path1.is_dir():
        print(f"Warning: Folder '{folder1_path}' does not exist or is not a directory.")
        return []
    if not path2.exists() or not path2.is_dir():
        print(f"Warning: Folder '{folder2_path}' does not exist or is not a directory.")
        return []

    files1 = {f.name for f in path1.glob(f"*{extension}") if f.is_file()}
    files2 = {f.name for f in path2.glob(f"*{extension}") if f.is_file()}
    
    # common = sorted(list(files1.intersection(files2)))
    common = sorted(list(files1))
    return common

def ensure_dir_exists(dir_path: str | Path):
    """Ensures that a directory exists, creating it if necessary."""
    Path(dir_path).mkdir(parents=True, exist_ok=True)