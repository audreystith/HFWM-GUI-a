import sys
from PyQt5.QtWidgets import QMainWindow ,QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit,QVBoxLayout
from PyQt5.QtGui import QValidator, QDoubleValidator
from ctypes import *
import math
import matplotlib.figure as fig 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 
lowerBound = -9999.99
upperBound = 9999.99
decimalBound = 2
ccs_handle=c_int(0)

lib = cdll.LoadLibrary("TLCCS_64.dll")
integration_time=c_double(.1)
lib.tlccs_init(b"USB0::0x1313::0x8081::M00316293::RAW", 1, 1, byref(ccs_handle))   
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

def save_input():
    global input_text
    global input_text2
    global input_text3
    input_text = line_edit.text()
    input_text2 = line_edit2.text()
    input_text3 = line_edit3.text()
    print(input_text)
    print(input_text2)
    print(input_text3)

def take_data():
    lib.tlccs_startScan(ccs_handle)
    data_array_ref =(c_double*3648)()
    status = c_int(0)
    while (status.value & 0x0010) == 0:
        lib.tlccs_getDeviceStatus(ccs_handle, byref(status))
    lib.tlccs_getScanData(ccs_handle, byref(data_array_ref))
    print("Reference spectrum recorded.")
    print()

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, figure=None):
        fig1 = fig.Figure(figsize=(5,4),dpi=100)
        self.axes = fig1.add_subplot(111)
        super(MplCanvas,self).__init__(fig1)
        

if __name__ == "__main__":
    #Makes window
    app = QApplication(sys.argv)
    w = QVBoxLayout()
    qw=QWidget()
    qw.setLayout(w)
 
    
    #print button
    btn = QPushButton()
    btn.setText('Print')
    btn.move(350,250)
    btn.show()
    btn.clicked.connect(save_input)
    w.addWidget(btn)
    #spectrometer button
    btn2 = QPushButton()
    btn2.setText('Button')
    btn2.move(50,250)
    btn2.show()
    btn2.clicked.connect(take_data)
    w.addWidget(btn2)

    #makes the input box only accept floats
    validator = QDoubleValidator()
    validator.setNotation(QDoubleValidator.StandardNotation)
    validator.setRange(lowerBound, upperBound, decimals=decimalBound)  # Set the desired range and decimal precision
    
    line_edit = QLineEdit()
    line_edit.move(25,100)
    line_edit.show()
    input_text = line_edit.text()
    line_edit.setValidator(validator)
    w.addWidget(line_edit)
    line_edit2 = QLineEdit()
    line_edit2.move(175,100)
    line_edit2.show()
    line_edit2.setValidator(validator)
    input_text2 = line_edit2.text()
    w.addWidget(line_edit2)

    line_edit3 = QLineEdit()
    line_edit3.move(325,100)
    line_edit3.show()
    line_edit3.setValidator(validator)
    input_text3 = line_edit3.text()
    w.addWidget(line_edit3)
    wavelengths=(c_double*3648)()
    lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

    sc = MplCanvas()
    sc.axes.plot([0,1,2,3,4],[10,1,20,3,40])
    
    pw = w.addWidget(sc)
    
    save_input()


    sys.exit(app.exec_())

