from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem

from add_material_dialog import AddMaterialDialog

class ProcessAnalyzeDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Usage Process Analysis")
        self.setFixedWidth(600)
        self.setFixedHeight(600)

        self.main_window = main_window
        self.selected_materials = []
        self.total_cost = None

        layout = QGridLayout()

        self.process_combo = QComboBox()
        self.process_combo.addItems(['- Select process -'] + self.process_list)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Material id', 'Material Name', 'Unit', 'Unit count', 'Total Cost (USD)'])

        self.total_cost_label = QLabel("Total Cost (USD): 0")

        button = QPushButton("Add material")
        button.clicked.connect(self.add_material)

        layout.addWidget(self.process_combo, 0, 0)
        layout.addWidget(button, 1, 0)
        layout.addWidget(self.table, 2, 0, 1, 2)
        layout.addWidget(self.total_cost_label, 3, 1)

        self.setLayout(layout)

    def add_material(self):
        if self.process_combo.currentText() != '- Select process -':
            dialog = AddMaterialDialog(self.main_window, self.process_combo.currentText())
            dialog.material_added.connect(self.add_material_to_table)
            dialog.exec()

    def add_material_to_table(self, material: dict):
        self.selected_materials.append(material)
        materials_list = []
        self.total_cost = 0
        if len(self.selected_materials) > 0:
            material_ids = [item['material_id'] for item in self.selected_materials]
            quote_ids = [f"'{mid}'" for mid in material_ids]
            material_ids_str = ','.join(quote_ids)
            sql = f"SELECT material_id, material_name, unit, unit_cost_usd FROM materials WHERE material_id in ({material_ids_str})"
            result = self.main_window.db.query(sql)
            self.form_materials_list(result, materials_list)
        self.refresh_table(materials_list)

    def find_count(self, material_id):
        result = next((item for item in self.selected_materials if item['material_id'] == material_id), None)
        return result['unit_text'] or None

    def form_materials_list(self, db_result, materials_list):
        for item in db_result:
            unit_count = float(self.find_count(item[0]))
            item_cost = round(float(item[3]) * unit_count, 2)
            self.total_cost += item_cost
            materials_list.append((item[0], item[1], item[2], unit_count, item_cost))

    def refresh_table(self, materials):
        if len(materials) > 0:
            self.table.setRowCount(0)
            for row_num, row_data in enumerate(materials):
                self.table.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
        self.total_cost_label.setText("Total Cost (USD): " + str(round(self.total_cost, 2)))

    @property
    def process_list(self):
        result = self.main_window.db.query("SELECT DISTINCT TRIM(usage_process) FROM materials")
        return [row[0] for row in result if row[0] is not None]