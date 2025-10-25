import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QTableWidget, QTableWidgetItem, QComboBox, \
    QDialog
from PyQt6.QtGui import QAction, QIcon, QPixmap
import requests

from search_dialog import SearchDialog
from about_dialog import AboutDialog
from process_analyze_dialog import ProcessAnalyzeDialog

from db.sqlite_connection import SqliteConnection
from db.postgresql_connection import PostgresqlConnection


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Material management system")
        self.setMinimumSize(1280, 960)
        self.db = db

        # self.db.init_material()

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        analyze_action = QAction("Process analysis", self)
        analyze_action.triggered.connect(self.usage_process_analyze)
        file_menu_item.addAction(analyze_action)

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
        # print(self.table_headers)
        self.table.setHorizontalHeaderLabels(self.table_headers)
        self.setCentralWidget(self.table)

        toolbar.addAction(search_action)
        toolbar.addWidget(filter_label)
        toolbar.addWidget(filter_combo)

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def load_data(self, category=None):
        url = "http://localhost:8000/materials"
        params = {"category": category}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data_list = response.json()
        self.render_table(data_list)

    def render_table(self, data_list):
        if not data_list:
            return

        columns = list(data_list[0].keys())
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(data_list):
            self.table.insertRow(row_number)
            for column_number, key in enumerate(columns):
                value = row_data.get(key, "")
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(value)))

    def search_material(self):
        dialog = SearchDialog(self)
        dialog.exec()

    def on_filter_combo_change(self, text):
        if text != '- Choose category -':
            main_window.load_data(category=text)
        else:
            main_window.load_data()

    def usage_process_analyze(self):
        dialog = ProcessAnalyzeDialog(self)
        dialog.exec()

    @property
    def material_category_list(self):
        result = self.db.query("SELECT DISTINCT TRIM(category) FROM materials")
        category_list = [row[0] for row in result if row[0] is not None]
        return category_list

    @property
    def table_headers(self):
        headers = "material_id, material_name, category, supplier, unit, unit_cost_usd, usage_process, \
                   storage_condition, purity, hazard_level, country_of_origin, last_updated".split(", ")
        return [item.capitalize().replace("_", " ") for item in headers]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # database = SqliteConnection()
    database = PostgresqlConnection(user='demo', password='test1234')
    main_window = MainWindow(db=database)
    main_window.show()
    main_window.load_data()
    sys.exit(app.exec())