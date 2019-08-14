import sys, os
import fix_qt_import_error
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QLabel, QGridLayout, QDesktopWidget, QFileDialog,
                             QLineEdit, QListWidget)
from PyQt5.QtGui import QFont, QIcon
import CorrectingDOs
import traceback
import hyproicons

class Mainmenu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'DO Recalculator calculator'
        self.setWindowIcon(QIcon(':/assets/2dropsshadow.svg'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.browsed = False

        self.initUI()

        self.setStyleSheet("""
            QListWidget{
            }
            QLabel {
                font: 13px;
            }
            QListWidget {
                font: 13px;
            }
            QPushButton {
                font: 13px;
            }
            QLineEdit {
                font:13px;
            } 
                            """)


    def initUI(self):

        deffont = QFont('Segoe UI')

        self.setGeometry(0, 0, 320, 400)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setFixedSize(self.size())

        self.setWindowTitle(self.title)

        gridlayout = QGridLayout()
        gridlayout.setSpacing(4)

        headinglabel = QLabel('Browse for the folder containing .LST files...', self)

        browsebutton = QPushButton('Browse...', self)
        browsebutton.setFont(deffont)
        browsebutton.clicked.connect(self.browsePath)
        browsebutton.setFixedWidth(120)
        #browsebutton.setFixedHeight(25)

        self.loadbutton = QPushButton('Load file', self)
        self.loadbutton.setFont(deffont)
        self.loadbutton.clicked.connect(self.loadfile)
        self.loadbutton.setFixedHeight(25)
        #loadbutton.setFixedWidth(120)

        self.fileslist = QListWidget(self)
        self.fileslist.setFont(deffont)

        self.directext = QLineEdit('', self)
        self.directext.setFont(deffont)

        gridlayout.addWidget(headinglabel, 0, 0, 1, 2)
        gridlayout.addWidget(browsebutton, 1, 1)
        gridlayout.addWidget(self.directext, 1, 0)
        gridlayout.addWidget(self.fileslist, 2, 0, 1, 2)
        gridlayout.addWidget(self.loadbutton, 3, 1)

        self.centralWidget().setLayout(gridlayout)

        self.show()


    def browsePath(self):
        path = QFileDialog.Options()
        files = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if os.path.exists(files):
            self.fileslist.clear()
            self.directext.setText(files)
            lstfiles = []
            for file in [f for f in os.listdir(files) if f.endswith('.LST')]:
                lstfiles.append(file)
            self.fileslist.addItems(lstfiles)
            self.browsed = True
            self.loadbutton.setText('Load file')

        self.pathoffile = files

    def loadfile(self):
        try:
            if self.browsed is True:
                lstfile = self.fileslist.currentItem().text()
                lstfilepath = (str(self.pathoffile) + "/" + str(lstfile))
                self.processwindow = CorrectingDOs.correctDos(lstfilepath)
                self.processwindow.show()
            if self.browsed is False:
                self.loadbutton.setText('Select a file first...')
        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mainmenu()
    sys.exit(app.exec_())