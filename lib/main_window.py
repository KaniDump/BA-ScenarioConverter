from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QStatusBar, QLabel
)
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

from lib.ui_components import ConversionTab
import config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BA Script Converter UI")
        self.setGeometry(100, 100, 800, 600)

        self._apply_dark_theme()

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)

        # Title Label
        title_label = QLabel("BA Scenario Script Converter")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("padding: 20px; color: #E0E0E0;")
        main_layout.addWidget(title_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # EN to JP Tab
        en_to_jp_instructions = (
            f"Put your English Script inside a folder called \"{config.EN_SCRIPT_FOLDER}\".\n"
            f"Put your Japanese Script inside a folder called \"{config.JP_SCRIPT_FOLDER}\".\n\n"
            f"The output path is on \"{config.EN_TO_JP_OUTPUT_FOLDER}\" folder."
        )
        self.en_to_jp_tab = ConversionTab(
            tab_name="EN to JP",
            source_folder1=config.EN_SCRIPT_FOLDER,
            source_folder2=config.JP_SCRIPT_FOLDER,
            output_folder=config.EN_TO_JP_OUTPUT_FOLDER,
            instruction_text=en_to_jp_instructions
        )
        self.en_to_jp_tab.conversion_started.connect(self._on_conversion_start)
        self.en_to_jp_tab.conversion_finished.connect(self._on_conversion_finish)
        self.tab_widget.addTab(self.en_to_jp_tab, "EN to JP")

        # JP to JP Tab
        jp_to_jp_instructions = (
            f"Put your OLD Japanese Script inside a folder called \"{config.OLD_JP_SCRIPT_FOLDER}\".\n"
            f"Put your NEW Japanese Script inside a folder called \"{config.NEW_JP_SCRIPT_FOLDER}\".\n\n"
            f"The output path is on \"{config.JP_TO_JP_OUTPUT_FOLDER}\" folder."
        )
        self.jp_to_jp_tab = ConversionTab(
            tab_name="JP to JP",
            source_folder1=config.OLD_JP_SCRIPT_FOLDER,
            source_folder2=config.NEW_JP_SCRIPT_FOLDER,
            output_folder=config.JP_TO_JP_OUTPUT_FOLDER,
            instruction_text=jp_to_jp_instructions
        )
        self.jp_to_jp_tab.conversion_started.connect(self._on_conversion_start)
        self.jp_to_jp_tab.conversion_finished.connect(self._on_conversion_finish)
        self.tab_widget.addTab(self.jp_to_jp_tab, "JP to JP")
        
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready.")

        # Connect tab change to refresh list (optional, good for dynamic changes)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D2D; /* Dark background for the main window */
            }
            QTabWidget::pane { /* The tab widget frame */
                border-top: 2px solid #C2C7CB;
                background-color: #3D3D3D; /* Slightly lighter for tab content area */
            }
            QTabBar::tab {
                background: #555555; /* Darker tab background */
                color: #E0E0E0; /* Light text */
                border: 1px solid #444444;
                border-bottom-color: #C2C7CB; /* Same as pane border color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 8px 15px; /* Increased padding */
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #6E6E6E; /* Lighter when selected/hovered */
            }
            QTabBar::tab:selected {
                border-color: #777777;
                border-bottom-color: #3D3D3D; /* Make it blend with the pane */
            }
            QWidget { /* Default for other widgets if not specified */
                background-color: #3D3D3D;
                color: #E0E0E0; /* Light text */
                border-color: #555555;
            }
            QListWidget {
                background-color: #2A2A2A; /* Even darker for list */
                color: #D0D0D0;
                border: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: #0078D7; /* Blue selection, common in dark themes */
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #555555;
                color: #E0E0E0;
                border: 1px solid #444444;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #6E6E6E;
            }
            QPushButton:pressed {
                background-color: #4A4A4A;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
            QLabel {
                color: #D0D0D0;
                background-color: transparent; /* Ensure labels don't have their own background */
            }
            QStatusBar {
                color: #C0C0C0;
            }
        """)


    def _on_tab_changed(self, index):
        current_tab = self.tab_widget.widget(index)
        if isinstance(current_tab, ConversionTab):
            current_tab.refresh_file_list()
            self.status_bar.showMessage(f"{current_tab.tab_name} tab selected. Ready.")

    def _on_conversion_start(self, message: str):
        self.status_bar.showMessage(message)

    def _on_conversion_finish(self, message: str):
        self.status_bar.showMessage(message, 5000)
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, ConversionTab):
            current_tab.refresh_file_list()