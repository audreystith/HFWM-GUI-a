import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
from PyQt5.QtGui import QValidator, QDoubleValidator
from ctypes import *
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 
import numpy as np 
#This is some code taken from the absorbtion measurement document. Needed for taking data 
ccs_handle=c_int(0)
lib = cdll.LoadLibrary("TLCCS_64.dll")
integration_time=c_double(0)
lib.tlccs_init(b"USB0::0x1313::0x8081::M00316293::RAW", 1, 1, byref(ccs_handle))   
collections = c_double(0)



class MyApp(QWidget):
    #this makes the window
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Set Matplotlib Chart Value with QLineEdit Widget')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        #This is how I add the widgets in
        layout = QVBoxLayout()
        self.setLayout(layout)

        #the 3 text boxes
        self.input = QLineEdit()
        #self.input.textChanged.connect(self.update_chart)
        layout.addWidget(self.input)

        self.input2 = QLineEdit()
        #self.input2.textChanged.connect(self.update_chart)
        layout.addWidget(self.input2)

        self.input3 = QLineEdit()
        #self.input3.textChanged.connect(self.update_chart)
        layout.addWidget(self.input3)

        #the 2 buttons
        self.input4 = QPushButton()
        #self.input4.clicked.connect(take_data)
        layout.addWidget(self.input4)

        self.input5 = QPushButton()
        self.input5.clicked.connect(self.update_chart)
        layout.addWidget(self.input5)

        #setting up plot
        self.canvas = FigureCanvas(plt.Figure(figsize=(15, 6)))
        layout.addWidget(self.canvas)

        wavelengths=(c_double*3648)()
        lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

        self.insert_ax()
    #plot stuff Matthew wrote this, ask him if u have questions
    def insert_ax(self):
        font = {
            'weight': 'normal',
            'size': 16
        }
        matplotlib.rc('font', **font)

        self.ax = self.canvas.figure.subplots()
        self.ax.set_ylim([0, .5])
        self.ax.set_xlim([0, 1000])
        self.plot1 = None
    #When you type in the text box and push the button it takes the data and shows the plot
    def update_chart(self):
        value = self.input.text()
        try:
            value= float(value)
            value = c_double(value)
        except ValueError:
            value = 0
        integration_time=value
        lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

        value2 = self.input2.text()
        try:
            value2= int(value2)
        #    value2 = c_double(value2)
        except ValueError:
            value2 = 0
        collections =value2
        i = int(0)
        while i < collections:
            lib.tlccs_startScan(ccs_handle)
            data_array_ref =(c_double*3648)()
            status = c_int(0)
            while (status.value & 0x0010) == 0:
                lib.tlccs_getDeviceStatus(ccs_handle, byref(status))
            lib.tlccs_getScanData(ccs_handle, byref(data_array_ref))
            wavelengths=(c_double*3648)()
            lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))
            lib.tlccs_startScan(ccs_handle)
            x_position = [0.5]
            if(i==0):
                data_array = np.asarray(data_array_ref)
            else:
                data_array +=np.asarray(data_array_ref)
            i=i+1
        data_array=data_array/collections

        if self.plot1:
             self.plot1.remove()
        self.plot = self.ax.plot(wavelengths, data_array)
        self.canvas.draw()
        
if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
