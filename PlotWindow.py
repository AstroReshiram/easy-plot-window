from PySide6 import QtWebEngineWidgets, QtCore
from PySide6 import QtWidgets as qtw
import plotly.graph_objects as go


class PlotWindow:
    """Wrapper class that runs the plot window as an app in itself."""
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
        screen_size = qtw.QApplication.primaryScreen().availableGeometry()
        self.resize(screen_size.width() // 4 * 3, screen_size.height() // 4 * 3)
        self.webengine = QtWebEngineWidgets.QWebEngineView(self)

        # Create widgets
        widget = qtw.QWidget(self)
        self.setCentralWidget(widget)

        # Button
        self.export_button = qtw.QPushButton("Export", self)
        self.export_button.clicked.connect(self.export_image)

        layout = qtw.QVBoxLayout(widget)
        layout.addWidget(self.webengine)
        layout.addWidget(self.export_button, alignment=QtCore.Qt.AlignHCenter)

        self.webengine.setHtml(self.fig.to_html(include_plotlyjs="cdn"))

    def export_image(self):
        """Exports an image"""
        self.fig.write_image("image.png")
