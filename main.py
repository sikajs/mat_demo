import sys
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QGridLayout, QPushButton, \
    QMainWindow, QToolBar, QTableWidget, QTableWidgetItem, QDialog, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sqlite3

from search_dialog import SearchDialog

class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection

    def init_material(self, csv_file = "semiconductor_materials_200.csv"):
        table_name = "materials"
        df = pd.read_csv(csv_file)
        print(df)
        df.to_sql(table_name, con=self.connect(), if_exists='replace', index=False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material management system")
        self.setMinimumSize(1280, 960)
        self.db = DatabaseConnection()

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search_material)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        print(self.table_headers)
        self.table.setHorizontalHeaderLabels(self.table_headers)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(search_action)

    def load_data(self):
        conn = self.db.connect()
        result = conn.execute("SELECT * FROM materials")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.close()

    def search_material(self):
        dialog = SearchDialog(self)
        dialog.exec()

    @property
    def table_headers(self):
        headers = "material_id, material_name, category, supplier, unit, unit_cost_usd, usage_process, \
                   storage_condition, purity, hazard_level, country_of_origin, last_updated".split(", ")
        table_headers = []
        for item in headers:
            table_headers.append(item.capitalize().replace("_", " "))
        return table_headers




app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())