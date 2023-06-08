import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QVBoxLayout

def dialog():
    mbox = QMessageBox()
    mbox.setText("Pretend there's a cool plot here")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    mbox.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(500, 300)
    w.setWindowTitle("Super Cool Window")

    layout = QVBoxLayout()

    btn = QPushButton()
    btn.setText('Print')
    btn.clicked.connect(dialog)
    layout.addWidget(btn)

    line_edit = QLineEdit()
    line_edit.setPlaceholderText("Enter text here")
    layout.addWidget(line_edit)

    w.setLayout(layout)
    w.show()
    sys.exit(app.exec_())