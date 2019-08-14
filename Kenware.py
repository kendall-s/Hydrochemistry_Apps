import sys
from time import sleep
import fix_qt_import_error
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QDesktopWidget, QLabel, QPushButton,
                             QFrame, QHBoxLayout)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
import DOCalculator
import QCReader
import DataQC
import NutrientStatPlotter
import IO3Norm
import NC_Checker_Main

import hyproicons

class KenWareMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(':/assets/icon.svg'))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f8ff;
                border: 0px;
                alpha: 0;
            }
            QFrame[bg=true] {
                background-color: #f4f8ff;
                border: 5px solid #4e546c;
                border-radius: 30px;
            }
            
            QFrame[headerframe=true] {
                background-color: #4e546c;
                border-radius: 10px;
            }
            QLabel[headertext=true] {
                font: 17px;
                color: #ffffff;
                font-weight: bold;
            }
            QLabel {
                font: 15px;
                font-weight: bold;
            }
            QFrame[bodyframe=true] {
                background-color: #f4f8ff;
                border-radius: 10px;
                padding-top: 10px;
            }
            QPushButton {
                font: 15px;
                border: 1px solid #ededed;
                background: #ededed;
                border-radius:5px;
            }
            QPushButton:hover {
                color: #222222;
                border: 1px solid #8f98a8;
                background: #f7f7f7;
            }
            QPushButton:pressed {
                background-color: #e8e8e8;
                border: 1px solid #8f98a8;
                border-style: inset;
            }
            QPushButton[close=true] {
                font: 12px;
                border: 0px solid;
                background-color: none;   
            }
            QPushButton[close=true]:hover {
                background-color: #d9d9d9;
                border-radius: 5px;
            }
            QPushButton[close=true]:pressed {
                font-weight: bold;
                border-style: inset;pip   
            }
                            """)



    def init_ui(self):
        self.setFont(QFont('Segoe UI'))

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setGeometry(0, 0, 400, 450)
        qtRect = self.frameGeometry()
        centrePoint = QDesktopWidget().availableGeometry().center()
        qtRect.moveCenter(centrePoint)
        self.move(qtRect.topLeft())

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('Hydro Apps')

        x_close = QPushButton('x')
        x_close.setProperty('close', True)
        x_close.setFont(QFont('Verdana'))
        x_close.clicked.connect(self.close_app)
        x_close.setToolTip('Close')

        __min = QPushButton(' - ')
        __min.setProperty('close', True)
        __min.setFont(QFont('Verdana'))
        __min.clicked.connect(self.min_app)
        __min.setToolTip('Minimise')


        header_logo = QLabel()
        header_logo.setPixmap(QPixmap(':/assets/2dropsshadow.ico').scaled(32, 32, Qt.KeepAspectRatio))

        header_label = QLabel('    Hydro Applications')
        header_label.setProperty('headertext', True)
        header_frame = QFrame()
        header_frame.setProperty('headerframe', True)

        docalc_label = QLabel('DO Calculator')
        docalc_launch = QPushButton('Launch DO Calc')
        docalc_launch.clicked.connect(self.open_docalc)
        docalc_label.setToolTip('The DO Calculator can reprocess results and format the results for HyLIMS upload.')

        linesep1 = QFrame()
        linesep1.setFrameShape(QFrame.HLine)
        linesep1.setFrameShadow(QFrame.Sunken)

        dataqc_label = QLabel('Hydrology Data QCer')
        dataqc_launch = QPushButton('Launch QCer')
        dataqc_launch.clicked.connect(self.open_dataqc)

        linesep2 = QFrame()
        linesep2.setFrameShape(QFrame.HLine)
        linesep2.setFrameShadow(QFrame.Sunken)

        qctable_label = QLabel('QC Table Stats')
        qctable_launch = QPushButton('Launch QCTab Stats')
        qctable_launch.clicked.connect(self.open_qctable)
        qctable_launch.setFixedWidth(160)

        baseline_label = QLabel('Base Offset Plotter')
        baseline_launch = QPushButton('Launch BO Plotter')
        baseline_launch.clicked.connect(self.open_boplot)

        iodate_label = QLabel('Iodate Normality')
        iodate_launch = QPushButton('Launch IO3 Norm')
        iodate_launch.clicked.connect(self.open_ionorm)

        nccheck_label = QLabel('NC Checker')
        nccheck_launch = QPushButton('Launch NC Checker')
        nccheck_launch.clicked.connect(self.open_nccheck)

        linesep3 = QFrame()
        linesep3.setFrameShape(QFrame.HLine)
        linesep3.setFrameShadow(QFrame.Sunken)

        linesep4 = QFrame()
        linesep4.setFrameShape(QFrame.HLine)
        linesep4.setFrameShadow(QFrame.Sunken)

        linesep5 = QFrame()
        linesep5.setFrameShape(QFrame.HLine)
        linesep5.setFrameShadow(QFrame.Sunken)

        linesep6 = QFrame()
        linesep6.setFrameShape(QFrame.HLine)
        linesep6.setFrameShadow(QFrame.Sunken)

        window_surround = QFrame()
        window_surround.setProperty('bg', True)

        close = QPushButton('Close')
        close.clicked.connect(self.close_app)
        close.setFixedWidth(125)

        grid_layout.addWidget(window_surround, 0, 0, 16, 4)
        grid_layout.addWidget(header_frame, 1, 1, 2, 2)
        grid_layout.addWidget(header_logo, 1, 1, 2, 1, Qt.AlignHCenter)
        grid_layout.addWidget(header_label, 1, 1, 2, 2, Qt.AlignHCenter)
        #grid_layout.addWidget(body_frame, 1, 0, 5, 2)
        grid_layout.addWidget(docalc_label, 3, 1)
        grid_layout.addWidget(docalc_launch, 3, 2)
        grid_layout.addWidget(linesep1, 4, 1, 1, 2)
        grid_layout.addWidget(qctable_label, 5, 1)
        grid_layout.addWidget(qctable_launch, 5, 2)
        grid_layout.addWidget(linesep2, 6, 1, 1, 2)
        grid_layout.addWidget(dataqc_label, 7, 1)
        grid_layout.addWidget(dataqc_launch, 7, 2)
        grid_layout.addWidget(linesep3, 8, 1, 1, 2)
        grid_layout.addWidget(baseline_label, 9, 1)
        grid_layout.addWidget(baseline_launch, 9, 2)
        grid_layout.addWidget(linesep4, 10, 1, 1, 2)
        grid_layout.addWidget(iodate_label, 11, 1)
        grid_layout.addWidget(iodate_launch, 11, 2)
        grid_layout.addWidget(linesep5, 12, 1, 1, 2)
        grid_layout.addWidget(nccheck_label, 13, 1)
        grid_layout.addWidget(nccheck_launch, 13, 2)
        grid_layout.addWidget(linesep6, 14, 1, 1, 2)
        #grid_layout.addWidget(close, 15, 1, 1, 2, Qt.AlignHCenter)

        dialog_buttons_layout = QHBoxLayout()

        grid_layout.addLayout(dialog_buttons_layout, 0, 2, Qt.AlignBottom | Qt.AlignRight)

        dialog_buttons_layout.addWidget(__min)
        dialog_buttons_layout.addWidget(x_close)

        #grid_layout.addWidget(x_close, 0, 3, Qt.AlignLeft | Qt.AlignBottom)
        #grid_layout.addWidget(__min, 0, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.centralWidget().setLayout(grid_layout)

        self.show()

    def open_boplot(self):
        self.bo_plot = NutrientStatPlotter.NutrientStatPlotter()
        sleep(0.3)

    def open_docalc(self):
        self.do_calc = DOCalculator.Mainmenu()
        sleep(0.3)

    def open_qctable(self):
        self.qc_table = QCReader.qcReaderMain()
        sleep(0.3)

    def open_dataqc(self):
        self.dat_qc = DataQC.Dataqc()
        sleep(0.3)

    def open_ionorm(self):
        self.io_norm = IO3Norm.IodateNorm()
        sleep(0.3)

    def open_nccheck(self):
        self.nc_check = NC_Checker_Main.NC_check_main()
        sleep(0.3)

    def close_app(self):
        self.close()

    def min_app(self):
        self.showMinimized()

    # Reimplement dragging of window as with no title bar it doesn't exist
    def mousePressEvent(self, event, *args, **kwargs):
        if event.buttons() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event, *args, **kwargs):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KenWareMain()
    sys.exit(app.exec_())
