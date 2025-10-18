from PyQt6.QtWidgets import QMessageBox

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app is made by sikajs.

        Icon credit:
          Filter icons created by Freepik - Flaticon
        """
        self.setText(content)