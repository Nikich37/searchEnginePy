from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QListWidget, \
    QGridLayout, QFileDialog
from searchEngine import SearchEngine
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.searchEngine = SearchEngine()
        self.setWindowTitle("Search Engine")
        self.setFixedSize(500, 300)
        self.initButtons()
        self.initSearchArea()
        self.initInfoArea()
        self.initLayout()
        self.show()

    def initButtons(self):
        self.addDocBtn = QPushButton("Add doc")
        self.addDocBtn.clicked.connect(self.addDocClick)

    def initSearchArea(self):
        self.searchArea = QLineEdit()
        self.searchArea.setPlaceholderText(
            "Type something and press enter to search..."
        )
        self.searchArea.returnPressed.connect(self.searchClick)

    def initInfoArea(self):
        self.infoList = QListWidget()
        self.infoList.addItem("The found results will appear here")
        self.infoList.itemClicked.connect(self.fileClick)

    def initLayout(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.searchArea, 0, 0)
        self.grid.addWidget(self.addDocBtn, 0, 1)
        self.grid.addWidget(self.infoList, 1, 0, 1, 2)
        self.setLayout(self.grid)

    def addDocClick(self):
        fname = QFileDialog.getOpenFileName(self, "Select file")
        if len(fname[0]) != 0:
            self.searchEngine.addDoc(fname[0])

    def searchClick(self):
        documents = self.searchEngine.getDocumentsList(self.searchArea.text())
        self.infoList.clear()
        if len(documents) != 0:
            for document in documents:
                self.infoList.addItem(document)
        else:
            self.infoList.addItem("Nothing was found...")

    def fileClick(self, item):
        QDesktopServices.openUrl(QUrl.fromLocalFile(f"./docs/{item.text()}"))
