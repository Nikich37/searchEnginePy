from sys import argv
from mainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
from qdarktheme import setup_theme


app = QApplication(argv)
setup_theme()
window = MainWindow()
app.exec()
