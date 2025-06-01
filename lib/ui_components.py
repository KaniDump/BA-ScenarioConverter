from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal

from lib.utils import get_common_files, ensure_dir_exists
from config import FILE_EXTENSION
from lib.converter_logic import convert_single_en_to_jp, convert_single_jp_to_jp

class ConversionTab(QWidget):
    conversion_started = Signal(str)
    conversion_finished = Signal(str) # Message to display

    def __init__(self, tab_name: str, source_folder1: str, source_folder2: str,
                 output_folder: str, instruction_text: str, parent=None):
        super().__init__(parent)
        self.tab_name = tab_name
        self.source_folder1 = source_folder1
        self.source_folder2 = source_folder2
        self.output_folder = output_folder
        self.instruction_text = instruction_text

        self._init_ui()
        self.refresh_file_list()

    def _init_ui(self):
        main_layout = QHBoxLayout(self) # Main layout: list on left, info/buttons on right

        # Left side: File list
        self.file_list_widget = QListWidget()
        self.file_list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        main_layout.addWidget(self.file_list_widget, 1) # Add with stretch factor 1

        # Right side: Instructions and buttons
        right_panel_layout = QVBoxLayout()
        
        self.instruction_label = QLabel(self.instruction_text)
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setAlignment(Qt.AlignTop)
        right_panel_layout.addWidget(self.instruction_label)

        right_panel_layout.addStretch(1) # Pushes buttons to the bottom

        buttons_layout = QHBoxLayout()
        self.convert_button = QPushButton("Convert")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self._on_convert_selected)
        buttons_layout.addWidget(self.convert_button)

        self.convert_all_button = QPushButton("Convert All")
        self.convert_all_button.clicked.connect(self._on_convert_all)
        buttons_layout.addWidget(self.convert_all_button)
        
        right_panel_layout.addLayout(buttons_layout)
        main_layout.addLayout(right_panel_layout, 1)

    def refresh_file_list(self):
        self.file_list_widget.clear()
        ensure_dir_exists(self.source_folder1) # Ensure source folders exist for user convenience
        ensure_dir_exists(self.source_folder2)
        ensure_dir_exists(self.output_folder) # Ensure output folder exists

        common_files = get_common_files(self.source_folder1, self.source_folder2, FILE_EXTENSION)
        if not common_files:
            self.file_list_widget.addItem("No common files found.")
            self.convert_all_button.setEnabled(False)
        else:
            for filename in common_files:
                self.file_list_widget.addItem(QListWidgetItem(filename))
            self.convert_all_button.setEnabled(True)
        self._on_selection_changed()

    def _on_selection_changed(self):
        selected_items = self.file_list_widget.selectedItems()
        # Enable convert button only if one item is selected and it's a real file (not "No common files...")
        is_real_file_selected = bool(selected_items) and selected_items[0].text() != "No common files found."
        self.convert_button.setEnabled(is_real_file_selected)

    def _on_convert_selected(self):
        selected_items = self.file_list_widget.selectedItems()
        if not selected_items:
            self.conversion_finished.emit("No file selected.")
            return

        filename = selected_items[0].text()
        self.conversion_started.emit("Converting...")
        
        success = False
        if self.tab_name == "EN to JP":
            success = convert_single_en_to_jp(filename, self.source_folder1, self.source_folder2, self.output_folder)
        elif self.tab_name == "JP to JP":
            success = convert_single_jp_to_jp(filename, self.source_folder1, self.source_folder2, self.output_folder)
        
        if success:
            self.conversion_finished.emit(f"Successfully converted: {filename}")
        else:
            self.conversion_finished.emit(f"Failed to convert: {filename}")

    def _on_convert_all(self):
        num_files = self.file_list_widget.count()
        if num_files == 0 or (num_files == 1 and self.file_list_widget.item(0).text() == "No common files found."):
            self.conversion_finished.emit("No files to convert.")
            return

        self.conversion_started.emit("Converting...")
        converted_count = 0
        failed_count = 0

        for i in range(num_files):
            item = self.file_list_widget.item(i)
            filename = item.text()
            if filename == "No common files found.":
                continue

            success = False
            if self.tab_name == "EN to JP":
                success = convert_single_en_to_jp(filename, self.source_folder1, self.source_folder2, self.output_folder)
            elif self.tab_name == "JP to JP":
                success = convert_single_jp_to_jp(filename, self.source_folder1, self.source_folder2, self.output_folder)
            
            if success:
                converted_count += 1
            else:
                failed_count += 1
        
        self.conversion_finished.emit(
            f"Convert All complete. Succeeded: {converted_count}, Failed: {failed_count}."
        )