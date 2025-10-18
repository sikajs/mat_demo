import sys
import pandas as pd
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QTableWidget, QTableWidgetItem, QComboBox
from PyQt6.QtGui import QAction, QIcon, QPixmap
from abc import ABC, abstractmethod

from search_dialog import SearchDialog
from about_dialog import AboutDialog

class AbstractDatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql: str):
        pass


class SqliteConnection(AbstractDatabaseConnection):
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        import sqlite3
        return sqlite3.connect(self.database_file)

    def query(self, sql: str):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            if sql.strip().lower().startswith("select"):  # process select query
                data = cursor.fetchall()
                return data
            else:  # proceed DML
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    def init_material(self, csv_file = "semiconductor_materials_200.csv"):
        table_name = "materials"
        df = pd.read_csv(csv_file)
        print(df)
        df.to_sql(table_name, con=self.connect(), if_exists='replace', index=False)


class MainWindow(QMainWindow):
    def __init__(self, db: AbstractDatabaseConnection):
        super().__init__()
        self.setWindowTitle("Material management system")
        self.setMinimumSize(1280, 960)
        self.db = db

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search_material)
        edit_menu_item.addAction(search_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        filter_icon_pixmap = QPixmap('icons/filter.png').scaled(toolbar.iconSize(), Qt.AspectRatioMode.KeepAspectRatio,
                                                                Qt.TransformationMode.SmoothTransformation)
        filter_label = QLabel()
        filter_label.setPixmap(filter_icon_pixmap)
        filter_combo = QComboBox()
        filter_combo.addItems(['- Choose category -'] + self.material_category_list)
        filter_combo.currentTextChanged.connect(self.on_filter_combo_change)

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        print(self.table_headers)
        self.table.setHorizontalHeaderLabels(self.table_headers)
        self.setCentralWidget(self.table)

        toolbar.addAction(search_action)
        toolbar.addWidget(filter_label)
        toolbar.addWidget(filter_combo)

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def load_data(self, sql="SELECT * FROM materials"):
        result = self.db.query(sql)
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search_material(self):
        dialog = SearchDialog(self)
        dialog.exec()

    def on_filter_combo_change(self, text):
        if text != '- Choose category -':
            sql = "SELECT * FROM materials WHERE category = '" + text + "'"
            main_window.load_data(sql=sql)
        else:
            main_window.load_data()

    @property
    def material_category_list(self):
        result = self.db.query("SELECT DISTINCT category FROM materials")
        print(result)
        category_list = list(map(lambda x: x[0].strip(), result))
        return category_list

    @property
    def table_headers(self):
        headers = "material_id, material_name, category, supplier, unit, unit_cost_usd, usage_process, \
                   storage_condition, purity, hazard_level, country_of_origin, last_updated".split(", ")
        table_headers = []
        for item in headers:
            table_headers.append(item.capitalize().replace("_", " "))
        return table_headers


app = QApplication(sys.argv)
database = SqliteConnection()
main_window = MainWindow(db=database)
main_window.show()
main_window.load_data()
sys.exit(app.exec())