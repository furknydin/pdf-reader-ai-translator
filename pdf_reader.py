import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import requests

class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern PDF Reader")
        self.setGeometry(100, 100, 800, 600)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.open_pdf()

    def open_pdf(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            self.load_pdf(file_name)

    def load_pdf(self, file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.text_edit.setText(text)

    def show_context_menu(self, position):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            menu = self.text_edit.createStandardContextMenu()
            translate_action = menu.addAction("Translate")
            action = menu.exec_(self.text_edit.mapToGlobal(position))
            if action == translate_action:
                self.translate_text(selected_text)

    def translate_text(self, text):
        try:
            response = requests.post("http://localhost:5000/translate", json={"text": text})
            if response.status_code == 200:
                translated_text = response.json().get("translated_text", "")
                QMessageBox.information(self, "Translation", translated_text)
            else:
                QMessageBox.warning(self, "Error", "Translation failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    reader = PDFReader()
    reader.show()
    sys.exit(app.exec_()) 