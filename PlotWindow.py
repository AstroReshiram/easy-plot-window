from __future__ import annotations

from PySide6 import QtWebEngineWidgets, QtCore
from PySide6 import QtWidgets as qtw
from threading import Thread
import plotly.graph_objects as go


class PlotWindow:
    """Wrapper class that runs the plot window as an app in itself."""
    def __init__(self, app: qtw.QApplication = None):
        if app is None:
            app = qtw.QApplication([])
        self.app = app

    def show(self, figs: go.Figure | list[go.Figure]):
        if type(figs) is not list:
            figs = [figs]
        self.windows = [_PlotWindow(fig) for fig in figs]
        for window in self.windows:
            window.show()
        self.app.exec()

    def exit(self):
        self.app.quit()


class _PlotWindow(qtw.QMainWindow):

    def __init__(self, fig: go.Figure = None):
        super().__init__()
        self.fig = fig
        self.setWindowTitle("Plot Window")
        screen_size = qtw.QApplication.primaryScreen().availableGeometry()
        self.resize(screen_size.width() // 4 * 3, screen_size.height() // 4 * 3)
        self.webengine = QtWebEngineWidgets.QWebEngineView(self)

        # Create widgets
        widget = qtw.QWidget(self)
        self.setCentralWidget(widget)

        # Buttons
        self.export_button = qtw.QPushButton("Export", self)
        self.export_button.clicked.connect(self.export_image)
        self.close_button = qtw.QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        layout = qtw.QVBoxLayout(widget)
        layout.addWidget(self.webengine)

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self.export_button, alignment=QtCore.Qt.AlignHCenter)
        button_layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignHCenter)

        layout.addLayout(button_layout)

        self.webengine.setUrl(self.fig)
        #self.webengine.setHtml(self.fig.to_html(include_plotlyjs="cdn"))

    def export_image(self):
        """Exports an image"""
        file_path, _ = qtw.QFileDialog().getSaveFileName(self, "Save As...", "image.png", "*.png")
        self.fig.write_image(file_path)

