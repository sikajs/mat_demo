from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class SearchDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        # setup search window
        self.setWindowTitle("Search materials")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.main_window = main_window

        layout = QVBoxLayout()

        self.material_id = QLineEdit()
        self.material_id.setPlaceholderText("Material id")
        layout.addWidget(self.material_id)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        material_id = self.material_id.text().upper()
        conn = self.main_window.db.connect()
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM materials WHERE material_id = ?", (material_id,))

        rows = list(result)
        items = self.main_window.table.findItems(material_id, Qt.MatchFlag.MatchFixedString)
        self.close()
        if len(items) > 0:
            for item in items:
                self.main_window.table.selectRow(item.row())
        else:
            message = QMessageBox()
            message.setWindowTitle("Error")
            message.setText(f"Cannot find material with id {material_id}" )
            message.exec()
