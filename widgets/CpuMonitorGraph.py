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
        self.initialized = None


        self.graph.setLabel('left', 'Temperature (C)')
        self.graph.setLabel('bottom', 'Time (s)')
        self.graph.setBackground("k")
        self.graph.setYRange(0, 100)
        self.graph.showGrid(x=True, y=True)

        self.labels = []
        self.x_data = []
        self.y_data = []
        self.ptr = 0
        self.curves = []


    def update_plot(self, temps: list[float], cpu_x: list[str]):
        """Method used to generate temperature monitor plots"""
        if self.initialized is None:
            num_lines = len(temps)
            self.labels = [[] for _ in range(num_lines)]
            self.x_data = [[] for _ in range(num_lines)]
            self.y_data = [[] for _ in range(num_lines)]
            colors = ['orange', 'green', 'red', 'cyan', 'magenta', 'white']

            for i in range(num_lines):
                pen = pg.mkPen(colors[i % len(colors)], width=2)
                curve = self.graph.plot([], [], name=cpu_x[i], pen=pen)
                self.curves.append(curve)
            self.initialized = True

        for index, temp in enumerate(temps):
            self.x_data[index].append(self.ptr)
            self.y_data[index].append(temp)
            self.curves[index].setData(self.x_data[index], self.y_data[index])

        self.ptr += 1
        self.graph.repaint()

