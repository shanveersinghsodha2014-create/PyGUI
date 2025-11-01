from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt

class MiniGUIDesigner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyGUI Mini GUI Designer")
        self.resize(400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter button text:")
        self.layout.addWidget(self.label)

        self.input = QLineEdit()
        self.layout.addWidget(self.input)

        self.add_btn = QPushButton("Add Button")
        self.add_btn.clicked.connect(self.add_button)
        self.layout.addWidget(self.add_btn)

        self.buttons_container = QVBoxLayout()
        self.layout.addLayout(self.buttons_container)

        self.setLayout(self.layout)

    def add_button(self):
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Button text cannot be empty.")
            return

        new_btn = QPushButton(text)
        new_btn.clicked.connect(lambda: QMessageBox.information(self, "Button Clicked", f"You clicked '{text}'!"))
        self.buttons_container.addWidget(new_btn)
        self.input.clear()


class DesignerApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = MiniGUIDesigner()

    def run(self):
        self.window.show()
        self.app.exec()
