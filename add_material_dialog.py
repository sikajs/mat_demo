from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QLabel, QComboBox, QMessageBox
from PyQt6.QtCore import pyqtSignal

class AddMaterialDialog(QDialog):
    material_added = pyqtSignal(dict)

    def __init__(self, man_window, process_name):
        super().__init__()
        self.setWindowTitle("Usage Process Analyze")
        self.setFixedWidth(350)
        self.setFixedHeight(300)

        self.main_window = man_window
        self.process_name = process_name
        self.material_id = None

        layout = QGridLayout()

        material_label = QLabel("Material")
        material_combo = QComboBox()
        material_combo.addItems(['- select materials -'] + self.process_material_list)
        material_combo.currentTextChanged.connect(self.set_unit)

        unit_label = QLabel("Unit")
        self.unit_line_edit = QLineEdit()
        self.unit_text_label = QLabel("")

        select_button = QPushButton("Select")
        select_button.clicked.connect(self.select)

        layout.addWidget(material_label, 0, 0)
        layout.addWidget(material_combo, 0, 1)
        layout.addWidget(unit_label, 1, 0)
        layout.addWidget(self.unit_line_edit, 1, 1)
        layout.addWidget(self.unit_text_label, 1, 2)
        layout.addWidget(select_button, 2, 1)

        self.setLayout(layout)

    def select(self):
        try:
            unit = float(self.unit_line_edit.text())
            if isinstance(unit, float):
                self.material_added.emit({'material_id': self.material_id, 'unit_text': self.unit_line_edit.text()})
                self.accept()
        except ValueError:
            error_msg = QMessageBox()
            error_msg.setWindowTitle("Error")
            error_msg.setText("Please enter a valid number")
            error_msg.exec()

    def set_unit(self, text):
        if text != '- select materials -':
            self.material_id = text.split(' ~ (')[1]
            self.material_id = self.material_id.replace(')', '')
            result = self.main_window.db.query(f"SELECT unit FROM materials WHERE material_id = '{self.material_id}'")
            if result[0] is not None:
                self.unit_text_label.setText(result[0][0])

    @property
    def process_material_list(self):
        result = self.main_window.db.query(f"SELECT material_id, material_name, unit FROM materials WHERE usage_process = '{self.process_name}'")
        return [f"{row[1]} ~ ({row[0]})" for row in result if row[0] is not None]