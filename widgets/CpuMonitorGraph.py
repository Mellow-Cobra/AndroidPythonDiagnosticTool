# Third Part Imports
import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore



class CpuTempGraphMainWindow(QMainWindow):
    """Class used to plot real time data from CPU temperature monitor"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Temperature Monitor")
        self.resize(600, 300)
        self.graph = pg.PlotWidget()
        self.setCentralWidget(self.graph)


        self.graph.setLabel('left', 'Temperature (C)')
        self.graph.setLabel('bottom', 'Time (s)')
        self.graph.setBackground("k")
        self.graph.setYRange(0, 100)
        self.graph.showGrid(x=True, y=True)

        self.x = []
        self.y = []
        self.ptr = 0
        self.curve = self.graph.plot(self.x, self.y, pen=pg.mkPen('orange', width=2))





    def update_plot(self, temp):
        self.x.append(self.ptr)
        print(type(temp))
        self.y.append(temp)
        self.ptr += 1
        self.curve.setData(self.x, self.y)
        self.graph.repaint()

