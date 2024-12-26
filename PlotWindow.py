from PySide6 import QtWebEngineWidgets, QtCore
from PySide6 import QtWidgets as qtw
import plotly.graph_objects as go


class PlotWindow:
    def __init__(self, fig: go.Figure = None):
        self.fig = fig

    def run(self):
        app = qtw.QApplication([])
        window = _PlotWindow(self.fig)
        window.show()
        app.exec()


class _PlotWindow(qtw.QMainWindow):
    def __init__(self, fig: go.Figure = None):
        super().__init__()
        self.fig = fig
        self.setWindowTitle("Plot Window")
        self.resize(1000, 800)
        self.webengine = QtWebEngineWidgets.QWebEngineView(self)

        # Create widgets
        widget = qtw.QWidget(self)
        self.setCentralWidget(widget)

        # Button
        # self.plot_button = qtw.QPushButton('Plot', self)
        # self.plot_button.clicked.connect(self.show_graph)

        layout = qtw.QVBoxLayout(widget)
        layout.addWidget(self.webengine)
        # layout.addWidget(self.plot_button, alignment=QtCore.Qt.AlignHCenter)

        self.webengine.setHtml(self.fig.to_html(include_plotlyjs='cdn'))

    def show_graph(self):
        """Takes graph from plotly and plots it in a PySide6 window"""
        self.webengine.setHtml(self.fig.to_html(include_plotlyjs='cdn'))
