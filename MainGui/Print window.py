import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit
from PyQt5.QtGui import QValidator, QDoubleValidator

lowerBound = -9999.99
upperBound = 9999.99
decimalBound = 2

def dialog():
    mbox = QMessageBox()

    mbox.setText("Pretend there's a cool plot here")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
    mbox.exec_()

def save_input():
    global input_text
    input_text = line_edit.text()
    print("Input text:", input_text)

def validatorfloat():
    #Make a method here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(500,300)
    w.setWindowTitle("Super Cool Window")
    

    btn = QPushButton(w)
    btn.setText('Print')
    btn.move(350,250)
    btn.show()
    btn.clicked.connect(dialog)

    line_edit = QLineEdit(w)
    line_edit.move(25,100)
    line_edit.show()

    validator = QDoubleValidator()
    validator.setNotation(QDoubleValidator.StandardNotation)
    validator.setRange(lowerBound, upperBound, decimals=decimalBound)  # Set the desired range and decimal precision
    line_edit.setValidator(validator)

    line_edit2 = QLineEdit(w)
    line_edit2.move(175,100)
    line_edit2.show()

    line_edit2 = QLineEdit(w)
    line_edit2.move(325,100)
    line_edit2.show()

    save_input()


    w.show()
    sys.exit(app.exec_())

