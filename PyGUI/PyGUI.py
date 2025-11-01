from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QMessageBox, QLineEdit, QCheckBox, QComboBox,
    QFileDialog, QTextEdit, QDialog, QDialogButtonBox
)
from PySide6.QtGui import QIcon, QPixmap
import sys
import os


class PyGUIHelper:
    def __init__(self):
        self.app = None
        self.window = None
        self.layout = None

    # -- App & Window creation --

    def create_app(self):
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        return self.app

    def create_window(self, title="PyGUI Window", width=400, height=300, layout_type="vbox"):
        self.window = QWidget()
        self.window.setWindowTitle(title)
        self.window.resize(width, height)

        if layout_type == "vbox":
            self.layout = QVBoxLayout()
        elif layout_type == "hbox":
            self.layout = QHBoxLayout()
        elif layout_type == "grid":
            self.layout = QGridLayout()
        else:
            raise ValueError(f"Unsupported layout_type: {layout_type}")

        self.window.setLayout(self.layout)
        return self.window

    # -- Widget adders --

    def add_label(self, text):
        label = QLabel(text)
        self.layout.addWidget(label)
        return label

    def add_button(self, text, on_click=None):
        btn = QPushButton(text)
        if on_click:
            btn.clicked.connect(on_click)
        self.layout.addWidget(btn)
        return btn

    def add_input(self, placeholder=""):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        self.layout.addWidget(line_edit)
        return line_edit

    def add_checkbox(self, label, checked=False):
        cb = QCheckBox(label)
        cb.setChecked(checked)
        self.layout.addWidget(cb)
        return cb

    def add_combobox(self, items):
        combo = QComboBox()
        combo.addItems(items)
        self.layout.addWidget(combo)
        return combo

    def add_textarea(self, placeholder="", readonly=False):
        textarea = QTextEdit()
        textarea.setPlaceholderText(placeholder)
        textarea.setReadOnly(readonly)
        self.layout.addWidget(textarea)
        return textarea

    # -- Dialog utilities --

    def show_info(self, title, message):
        QMessageBox.information(self.window, title, message)

    def show_warning(self, title, message):
        QMessageBox.warning(self.window, title, message)

    def ask_confirmation(self, message, title="Confirm"):
        reply = QMessageBox.question(self.window, title, message,
                                     QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes

    def get_text_input(self, prompt, title="Input"):
        text, ok = QInputDialog.getText(self.window, title, prompt)
        if ok:
            return text
        return None

    def open_file_dialog(self, caption="Open File", filter="All Files (*)"):
        filename, _ = QFileDialog.getOpenFileName(self.window, caption, filter=filter)
        return filename

    def save_file_dialog(self, caption="Save File", filter="All Files (*)"):
        filename, _ = QFileDialog.getSaveFileName(self.window, caption, filter=filter)
        return filename

    # -- Theming & Styling --

    def apply_stylesheet(self, qss_text):
        if self.app:
            self.app.setStyleSheet(qss_text)
        else:
            raise RuntimeError("App not created yet.")

    def load_stylesheet(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Stylesheet not found: {filepath}")
        with open(filepath, "r") as f:
            qss = f.read()
        self.apply_stylesheet(qss)

    # -- Form Builder --

class FormBuilder(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.fields = {}

    def add_field(self, name, label_text, widget_type='input', **kwargs):
        label = QLabel(label_text)
        self.layout.addWidget(label)

        if widget_type == 'input':
            widget = QLineEdit()
            if 'placeholder' in kwargs:
                widget.setPlaceholderText(kwargs['placeholder'])
        elif widget_type == 'checkbox':
            widget = QCheckBox()
            if 'checked' in kwargs:
                widget.setChecked(kwargs['checked'])
        elif widget_type == 'combobox':
            widget = QComboBox()
            items = kwargs.get('items', [])
            widget.addItems(items)
        elif widget_type == 'textarea':
            widget = QTextEdit()
            if kwargs.get('readonly', False):
                widget.setReadOnly(True)
        else:
            raise ValueError(f"Unknown widget_type {widget_type}")

        self.layout.addWidget(widget)
        self.fields[name] = widget
        return widget

    def get_values(self):
        result = {}
        for name, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                result[name] = widget.text()
            elif isinstance(widget, QCheckBox):
                result[name] = widget.isChecked()
            elif isinstance(widget, QComboBox):
                result[name] = widget.currentText()
            elif isinstance(widget, QTextEdit):
                result[name] = widget.toPlainText()
            else:
                result[name] = None
        return result

    def validate(self, validators):
        """
        validators: dict of {field_name: callable(value) -> bool}
        Returns True if all validators pass, False otherwise.
        """
        for name, validator in validators.items():
            if name not in self.fields:
                continue
            value = self.get_values().get(name)
            if not validator(value):
                return False
        return True

    def clear(self):
        for widget in self.fields.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QTextEdit):
                widget.clear()

    def set_readonly(self, readonly=True):
        for widget in self.fields.values():
            if isinstance(widget, (QLineEdit, QTextEdit)):
                widget.setReadOnly(readonly)
            elif isinstance(widget, QCheckBox):
                widget.setEnabled(not readonly)
            elif isinstance(widget, QComboBox):
                widget.setEnabled(not readonly)

    # -- Window Management --

def open_modal_dialog(widget, title="Modal Dialog", width=300, height=200):
    dialog = QDialog()
    dialog.setWindowTitle(title)
    dialog.resize(width, height)
    layout = QVBoxLayout()
    layout.addWidget(widget)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    layout.addWidget(buttons)
    dialog.setLayout(layout)

    result = {'accepted': False}

    def on_accept():
        result['accepted'] = True
        dialog.accept()

    def on_reject():
        dialog.reject()

    buttons.accepted.connect(on_accept)
    buttons.rejected.connect(on_reject)

    if dialog.exec() == QDialog.Accepted:
        return True
    return False

    # -- Event Loop Control --

def run_app():
    app = QApplication.instance() or QApplication(sys.argv)
    app.exec()

def quit_app():
    app = QApplication.instance()
    if app:
        app.quit()

    # -- Resource Manager --

def load_icon(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Icon not found: {path}")
    return QIcon(path)

def load_pixmap(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pixmap not found: {path}")
    return QPixmap(path)


# -----------------------------
# Example usage (run as script)
# -----------------------------
if __name__ == "__main__":
    gui = PyGUIHelper()
    gui.create_app()
    gui.create_window(title="PyGUI Full Helper Demo")

    gui.add_label("This is a label")
    input1 = gui.add_input("Type something here...")
    checkbox = gui.add_checkbox("Check me", True)
    combo = gui.add_combobox(["Red", "Green", "Blue"])
    textarea = gui.add_textarea("Write multi-line text here...")

    def on_button_click():
        vals = {
            "Input": input1.text(),
            "Checkbox": checkbox.isChecked(),
            "Combo": combo.currentText(),
            "Textarea": textarea.toPlainText(),
        }
        gui.show_info("Collected Values", str(vals))

    gui.add_button("Show Values", on_button_click)
    gui.run()
