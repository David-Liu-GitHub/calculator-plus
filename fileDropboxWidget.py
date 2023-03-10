import os

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5.QtCore import Qt
from encryptionModule import fileEncryptor


class DropBoxWidget(QWidget):
    def __init__(self, parent=None):  # Set up the construction method like this to enable this class's object to be used like a normal QWidget
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setupUI()
        self.listOfFilePath = []
        userHome = os.path.expanduser("~")
        self.appdataFilesPath = userHome + "\AppData\Local\CalculatorPlus\TheFiles"

    def setupUI(self):
        self.setGeometry(QtCore.QRect(0, 0, 311, 321))
        self.setAutoFillBackground(False)
        self.setStyleSheet("border: 4px dashed #aaa")
        self.setObjectName("widget")

        self.dropFileLabel = QtWidgets.QLabel(self)
        self.dropFileLabel.setGeometry(QtCore.QRect(44, 140, 240, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.dropFileLabel.setFont(font)
        self.dropFileLabel.setStyleSheet("border: none")
        self.dropFileLabel.setObjectName("dropFileLabel")
        self.dropFileLabel.setText("Drop your file here")

    def paintEvent(self, pe):  # Self defined widget class need this method to be able to use stylesheet
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def dragEnterEvent(self, event):  # These 3 methods go together for the drag and drop function
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                self.listOfFilePath.append(str(url.toLocalFile()))
            for filePath in self.listOfFilePath:
                filePathFixed = filePath.replace('/', '\\')
                fileName = os.path.basename(filePath)
                destinationFilepathWithName = self.appdataFilesPath + "\\" + fileName
                fileEncryptor.encrypt(filePath, destinationFilepathWithName)
                print("File: " + str(filePathFixed))
                print("File: " + str(destinationFilepathWithName))
        else:
            event.ignore()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    theFileDropbox = DropBoxWidget()
    theFileDropbox.show()

    sys.exit(app.exec_())
