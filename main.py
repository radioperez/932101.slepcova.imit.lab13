import sys
import random
import numpy as np
from numpy.random import default_rng
import scipy.stats
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QSpinBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)
from PyQt6.QtGui import QFont
import pyqtgraph as QtGraph
from enum import Enum

class Weather(Enum):
    SUNNY = 0
    CLOUDY = 1
    OVERCAST = 2

class Graph(QtGraph.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground("w")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Геометрическое броуновское движение')

        panel = QHBoxLayout()
        # start button
        start_button = QPushButton("СТАРТ")
        start_button.clicked.connect(self.start)

        self.timer = QTimer()
        stop_button = QPushButton("СТОП")
        stop_button.clicked.connect(self.stats)
        panel.addWidget(start_button)
        panel.addWidget(stop_button)

        # graph
        self.graph = Graph()
        params = QFormLayout()
        self.mu_line = QLineEdit("0.625")
        params.addRow("μ: ", self.mu_line)
        self.sigma_line = QLineEdit("0.123")
        params.addRow("σ: ", self.sigma_line)

        layout = QVBoxLayout()
        layout.addLayout(panel)
        layout.addWidget(self.graph)
        layout.addLayout(params)
        root = QWidget()
        root.setLayout(layout)
        self.setCentralWidget(root)

    def start(self):
        self.graph.clear()
        
        self.currency1 = [1]
        self.w1 = [0]
        self.currency2 = [1]
        self.w2 = [0]
        self.t = [0]
        
        self.delta = 1/100

        pen1 = QtGraph.mkPen(color=(0, 0, 255), width=5)
        self.line1 = self.graph.plot(self.t, self.currency1, pen=pen1)
        pen2 = QtGraph.mkPen(color=(0,255,0), width=5)
        self.line2 = self.graph.plot(self.t, self.currency2, pen=pen2)

        self.timer.setInterval(100)
        self.timer.timeout.connect(self.run)
        self.timer.start()

    def run(self):
        delta = 1/100
        self.t.append(self.t[-1] + delta)
        
        nrm = default_rng().normal

        try:
            mu = float(self.mu_line.text()) # drift
        except ValueError:
            mu = 0.625
        try:
            sigma = float(self.sigma_line.text()) # volatility -- st deviation
        except ValueError:
            sigma = 0.123

        self.w1.append(self.w1[-1] + nrm()*np.sqrt(delta))
        coin1 = self.currency1[-1] * np.exp((mu - sigma**2 / 2)*(delta)+ sigma * self.w1[-1])
        self.currency1.append(coin1)

        self.w2.append(self.w2[-1] + nrm()*np.sqrt(delta))
        coin2 = self.currency2[-1] * np.exp((mu - sigma**2 / 2)*(delta) + sigma * self.w2[-1])
        self.currency2.append(coin2)
        
        self.line1.setData(self.t, self.currency1)
        self.line2.setData(self.t, self.currency2)
    def stats(self):
        self.timer.stop()
        text1 = QtGraph.TextItem(f'{self.currency1[-1]}', color=(0, 0, 0))
        text1.setPos(self.t[-1], self.currency1[-1])
        text2 = QtGraph.TextItem(f'{self.currency2[-1]}', color=(0, 0, 0))
        text2.setPos(self.t[-1], self.currency2[-1])
        self.graph.addItem(text1)
        self.graph.addItem(text2)


random.seed()
app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()
