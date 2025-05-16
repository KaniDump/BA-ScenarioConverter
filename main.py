import sys
from PySide6.QtWidgets import QApplication
from lib.main_window import MainWindow
from lib.utils import ensure_dir_exists
import config

def create_project_folders():
    folders_to_create = [
        config.EN_SCRIPT_FOLDER,
        config.JP_SCRIPT_FOLDER,
        config.EN_TO_JP_OUTPUT_FOLDER,
        config.OLD_JP_SCRIPT_FOLDER,
        config.NEW_JP_SCRIPT_FOLDER,
        config.JP_TO_JP_OUTPUT_FOLDER,
    ]
    for folder in folders_to_create:
        ensure_dir_exists(folder)
    print("Checked/created project folders.")

if __name__ == "__main__":
    create_project_folders()

    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())