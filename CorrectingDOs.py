import sys, csv
import fix_qt_import_error
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QGridLayout,
                             QLineEdit, QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView, QCheckBox)
from PyQt5.QtGui import QIcon, QFont
import hyproicons
import traceback


class correctDos(QWidget):


    def __init__(self, file):
        super().__init__()
        self.setWindowIcon(QIcon(':/assets/2dropsshadow.svg'))

        self.ml_to_mol_coefficient = 44.661

        self.lstfile = file

        self.initUI()

        self.setStyleSheet("""
            
            QLabel[header = true] {
                font: 14px;
                font-weight: bold;
            }
            QLabel[smallheader = true] {
                font: 13px;
                font-weight: bold;
            }
            QLabel {
                font: 13px;
            }
            QLineEdit {
                font: 13px;
            }
            QListWidget {
                font: 13px;
            }
            QPushButton {
                font: 13px;
            }
            QMessageBox {
                font: 13px;
            }
            QTableWidget {
                font: 13px;
            }
            QCheckBox {
                font: 13px;
            }
                           """)

    def initUI(self):

        deffont = QFont('Segoe UI')
        self.setFont(deffont)

        self.setGeometry(0, 0, 995, 580)
        qtRectangle = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setFixedSize(self.size())
        self.setWindowTitle('DO Recalculator calculator - View Data: ' + str(self.lstfile))

        gridlayout = QGridLayout()
        gridlayout.setSpacing(10)

        # Pull everything from the lst file
        (self.stationnum, self.castnum, self.bottlenum, self.flaskid, self.flaskvol, self.rawtiter, self.titer,
         self.oxygenmils, self.thiotemps, self.drawtemp, self.volts, self.titertime) = self.readinlst(self.lstfile)

        self.numofsamples = len(self.stationnum)

        self.o2mol = []
        try:
            for i in range(len(self.oxygenmils)):
                self.o2mol.append(round(float((self.oxygenmils[i])) * self.ml_to_mol_coefficient, 4))
        except Exception as e:
            print(e)

        self.procced = False

        headerlabels = ['Station #', 'Cast #', 'Rosette Pos', 'Flask ID', 'Flask Vol', 'Raw Titer', 'Titer', 'O2 ml/L',
                        'Thio Temp', 'Draw Temp', 'Volts', 'Titer Time', 'O2uMol']

        self.datatable = QTableWidget(self)
        self.datatable.setFont(deffont)
        self.datatable.setRowCount(len(self.stationnum))
        self.datatable.setColumnCount(13)
        self.datatable.setHorizontalHeaderLabels(headerlabels)
        self.datatable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        header = self.datatable.horizontalHeader()

        for i in range(13):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        for i in range(len(self.stationnum)):
            self.datatable.setItem(i, 0, QTableWidgetItem(str(self.stationnum[i])))
            self.datatable.setItem(i, 1, QTableWidgetItem(str(self.castnum[i])))
            self.datatable.setItem(i, 2, QTableWidgetItem(str(self.bottlenum[i])))
            self.datatable.setItem(i, 3, QTableWidgetItem(str(self.flaskid[i])))
            self.datatable.setItem(i, 4, QTableWidgetItem(str(self.flaskvol[i])))
            self.datatable.setItem(i, 5, QTableWidgetItem(str(self.rawtiter[i])))
            self.datatable.setItem(i, 6, QTableWidgetItem(str(self.titer[i])))
            self.datatable.setItem(i, 7, QTableWidgetItem(str(self.oxygenmils[i])))
            self.datatable.setItem(i, 8, QTableWidgetItem(str(self.thiotemps[i])))
            self.datatable.setItem(i, 9, QTableWidgetItem(str(self.drawtemp[i])))
            self.datatable.setItem(i, 10, QTableWidgetItem(str(self.volts[i])))
            self.datatable.setItem(i, 11, QTableWidgetItem(str(self.titertime[i])))
            self.datatable.setItem(i, 12, QTableWidgetItem(str(self.o2mol[i])))

        headerlabel = QLabel('Dissolved Oxygen Results', self)
        headerlabel.setFont(deffont)
        headerlabel.setProperty('header', True)

        filelabel = QLabel("File:  " + str(self.filename))
        filelabel.setFont(deffont)

        parameterslabel = QLabel('Parameters', self)
        parameterslabel.setFont(deffont)
        parameterslabel.setProperty('smallheader', True)

        iodatenormlabel = QLabel('Iodate Normality @20C', self)
        iodatenormlabel.setFont(deffont)

        self.iodatenormtext = QLineEdit('Iodate norm', self)
        self.iodatenormtext.setFont(deffont)
        self.iodatenormtext.setText(self.iodatenorm)
        self.iodatenormtext.setFixedWidth(150)
        self.iodatenormtext.setReadOnly(True)

        iodateburettevol = QLabel('Iodate Burette \n10mL Volume @20C', self)
        iodateburettevol.setFont(deffont)

        self.iodateburettetext = QLineEdit('Iodate vol', self)
        self.iodateburettetext.setFont(deffont)
        self.iodateburettetext.setText(self.iodatevol)
        self.iodateburettetext.setFixedWidth(150)
        self.iodateburettetext.setReadOnly(True)

        iodatetemplabel = QLabel('Iodate Temperature', self)
        iodatetemplabel.setFont(deffont)

        self.iodatetemptext = QLineEdit('Iodate temp', self)
        self.iodatetemptext.setFont(deffont)
        self.iodatetemptext.setText(self.iodatetemp)
        self.iodatetemptext.setFixedWidth(150)
        self.iodatetemptext.setReadOnly(True)

        thionormlabel = QLabel('Thio Normality @20C')
        thionormlabel.setFont(deffont)

        self.thionormtext = QLineEdit('thio norm', self)
        self.thionormtext.setFont(deffont)
        self.thionormtext.setText(self.thionorm)
        self.thionormtext.setFixedWidth(150)
        self.thionormtext.setReadOnly(True)

        self.override_thio_norm_check = QCheckBox('Override Thio N Calc?', self)

        thiotemplabel = QLabel('Thio Temperature')
        thiotemplabel.setFont(deffont)

        self.thiotemptext = QLineEdit('thio temp', self)
        self.thiotemptext.setFont(deffont)
        self.thiotemptext.setText(self.thiotemp)
        self.thiotemptext.setFixedWidth(150)
        self.thiotemptext.setReadOnly(True)

        titerlabel = QLabel('Titer @20C', self)
        titerlabel.setFont(deffont)

        self.titertext = QLineEdit('titer vol', self)
        self.titertext.setFont(deffont)
        self.titertext.setText(self.stdtiter)
        self.titertext.setFixedWidth(150)
        self.titertext.setReadOnly(True)

        blanklabel = QLabel('Blank result', self)
        blanklabel.setFont(deffont)

        self.blanktext = QLineEdit('Blank ', self)
        self.blanktext.setFont(deffont)
        self.blanktext.setText(self.blank)
        self.blanktext.setFixedWidth(150)
        self.blanktext.setReadOnly(True)

        resultslabel = QLabel('Data', self)
        resultslabel.setFont(deffont)
        resultslabel.setProperty('smallheader', True)

        self.editfields = QPushButton('Edit parameters', self)
        self.editfields.setFont(deffont)
        self.editfields.clicked.connect(self.editablefields)

        reproc = QPushButton('Recalculate...', self)
        reproc.setFont(deffont)
        reproc.clicked.connect(self.process)

        self.save = QPushButton('Save As Updated LST', self)
        self.save.setFont(deffont)
        self.save.clicked.connect(lambda: self.saveresults(self.lstfile))

        self.savecsv = QPushButton('Save as HyLIMS CSV', self)
        self.savecsv.setFont(deffont)
        self.savecsv.clicked.connect(lambda: self.saveascsv(self.lstfile))

        gridlayout.addWidget(headerlabel, 0, 0)
        gridlayout.addWidget(filelabel, 0, 1)

        gridlayout.addWidget(parameterslabel, 1, 0)
        gridlayout.addWidget(iodatenormlabel, 2, 0)
        gridlayout.addWidget(self.iodatenormtext, 3, 0)
        gridlayout.addWidget(iodatetemplabel, 4, 0)
        gridlayout.addWidget(self.iodatetemptext, 5, 0)
        gridlayout.addWidget(iodateburettevol, 6, 0)
        gridlayout.addWidget(self.iodateburettetext, 7, 0)
        gridlayout.addWidget(thionormlabel, 8, 0)
        gridlayout.addWidget(self.thionormtext, 9, 0)
        gridlayout.addWidget(self.override_thio_norm_check, 10, 0)
        gridlayout.addWidget(thiotemplabel, 11, 0)
        gridlayout.addWidget(self.thiotemptext, 12, 0)
        gridlayout.addWidget(titerlabel, 13, 0)
        gridlayout.addWidget(self.titertext, 14, 0)
        gridlayout.addWidget(blanklabel, 15, 0)
        gridlayout.addWidget(self.blanktext, 16, 0)

        gridlayout.addWidget(self.editfields, 17, 0)

        gridlayout.addWidget(resultslabel, 1, 1, 1, 2)
        gridlayout.addWidget(self.datatable, 2, 1, 15, 3)

        gridlayout.addWidget(self.save, 17, 3)
        gridlayout.addWidget(self.savecsv, 17, 2)

        gridlayout.addWidget(reproc, 17, 1)
        self.setLayout(gridlayout)

        self.show()

    def get_index(self, arr, searchitem):
        for i, x in enumerate(arr):
            for j, y in enumerate(x):
                if y == searchitem:
                    return i, j
        return "blueberry"  # if not found, but shouldn't happen unless doing check

    def readinlst(self, file):

        filebuffer = open(file)
        readbuffer = csv.reader(filebuffer, delimiter=' ')
        projectslist = list(readbuffer)
        filebuffer.close()

        dateindexx, dateindexy = self.get_index(projectslist, 'Date:')
        self.dateanalysed = projectslist[dateindexx][(dateindexy + 1)]

        labindexx, labindexy = self.get_index(projectslist, 'Ship:')
        self.lab = projectslist[labindexx][(labindexy + 7)]

        analystx, analysty = self.get_index(projectslist, 'Chemist:')
        self.analyst = projectslist[analystx][(analysty + 1)]

        self.iodatenormx, self.iodatenormy = self.get_index(projectslist, 'N(20)IO3:')
        self.iodatenorm = projectslist[self.iodatenormx][(self.iodatenormy + 1)]

        self.iodatevolx, self.iodatevoly = self.get_index(projectslist, 'Vol(20):')
        self.iodatevol = projectslist[self.iodatevolx][(self.iodatevoly + 2)]

        self.stdtiterx, self.stdtitery = self.get_index(projectslist, 'C):')
        self.stdtiter = projectslist[self.stdtiterx][(self.stdtitery + 1)]

        self.blankx, self.blanky = self.get_index(projectslist, 'Blk:')
        self.blank = projectslist[self.blankx][(self.blanky + 2)]

        self.iodatetempx, self.iodatetempy = self.get_index(projectslist, 'IO3')
        self.iodatetemp = projectslist[self.iodatetempx][(self.iodatetempy + 3)]

        self.thionormx, self.thionormy = self.get_index(projectslist, '(20C)')
        self.thionorm = projectslist[self.thionormx][(self.thionormy + 1)]

        self.thiotempx, self.thiotempy = self.get_index(projectslist, 'stdize:')
        self.thiotemp = projectslist[self.thiotempx][(self.thiotempy + 1)]

        filenamex, filenamey = self.get_index(projectslist, 'filename:')
        self.filename = projectslist[filenamex][(filenamey + 1)]

        self.startx, self.starty = self.get_index(projectslist, 'Sta')

        numberofsamples = len(projectslist) - (self.startx + 2)

        stationnum = []
        castnum = []
        bottlenum = []
        flaskid = []
        flaskvol = []
        rawtiter = []
        titer = []
        oxygenmilliter = []
        thiotemps = []
        drawtemp = []
        volts = []
        titertime = []

        for i in range(numberofsamples):
            k = i + self.startx + 2
            if projectslist[k][12] == 'ABORT':
                stationnum.append(projectslist[k][0])
                castnum.append(projectslist[k][1])
                bottlenum.append(projectslist[k][2])
                flaskid.append(projectslist[k][3])
                flaskvol.append(projectslist[k][4])
                rawtiter.append(projectslist[k][5])
                titer.append(projectslist[k][6])
                oxygenmilliter.append(projectslist[k][7])
                thiotemps.append(projectslist[k][8])
                drawtemp.append(projectslist[k][9])
                volts.append(projectslist[k][10])
                titertime.append(projectslist[k][11])
            else:
                if projectslist[k][12] == '':
                    stationnum.append(projectslist[k][0])
                    castnum.append(projectslist[k][1])
                    bottlenum.append(projectslist[k][2])
                    flaskid.append(projectslist[k][3])
                    flaskvol.append(projectslist[k][4])
                    rawtiter.append(projectslist[k][6])
                    titer.append(projectslist[k][8])
                    oxygenmilliter.append(projectslist[k][10])
                    thiotemps.append(projectslist[k][11])
                    drawtemp.append(projectslist[k][13])
                    volts.append(projectslist[k][14])
                    titertime.append(projectslist[k][15])
                else:
                    stationnum.append(projectslist[k][0])
                    castnum.append(projectslist[k][1])
                    bottlenum.append(projectslist[k][2])
                    flaskid.append(projectslist[k][3])
                    flaskvol.append(projectslist[k][4])
                    rawtiter.append(projectslist[k][6])
                    titer.append(projectslist[k][8])
                    oxygenmilliter.append(projectslist[k][10])
                    thiotemps.append(projectslist[k][11])
                    drawtemp.append(projectslist[k][12])
                    volts.append(projectslist[k][13])
                    titertime.append(projectslist[k][14])

        return stationnum, castnum, bottlenum, flaskid, flaskvol, rawtiter, titer, oxygenmilliter, thiotemps, drawtemp, volts, titertime

    def rhoddw(self, t):

        # Calculates the density of pure water

        z0 = 999.83952
        z1 = 16.945176
        z2 = -0.0079870401
        z3 = -0.000046170461
        z4 = 0.00000010556302
        z5 = -2.8054253E-10
        z6 = 0.01687985

        rhot2 = z2 + float(t) * (z3 + float(t) * (z4 + float(t) * z5))
        rhot1 = z0 + float(t) * (z1 + float(t) * rhot2)
        rhoddw = rhot1 * 0.001 / (1 + z6 * float(t))

        return rhoddw

    def h2odvdt1(self, vol1, temp1, temp2):

        # Calculates the given volume that an aqueous liquid would occupy at a given temp (temp2)
        # Uses the change from temp1 to temp2
        # See F4 Volume Properties of Water, CRC Handbook

        if temp1 == 0 or temp1 == -9:
            h2odvdt1 = 0
        else:
            rhoratio = self.rhoddw(float(temp1)) / self.rhoddw(float(temp2))
            h2odvdt1 = float(vol1) * rhoratio

        return h2odvdt1

    def glassdvdt(self, volume, known_temp, desired_temp):

        # Calculates the actual volume of a glass container at a given temperature, from the known volume at 20
        expansion_coef = 0.00000975  # For borosilicate glass

        glass_dvdt = float(volume) * (1 + expansion_coef * (float(desired_temp) - float(known_temp)))

        return glass_dvdt

    def oxycalc(self, thio20n, titer20, blank, botvol):
        # Constants
        o2mlpmeq = 5.598  # mL of O2 (STP) per milliequiv of O2 gas (5.598mL)
        doreag = 0.0017  # Dissolved O2 in reagents @ 25deg
        vreag = 2  # Volume of reagents used (2.0mL)

        if float(thio20n) == 0 or float(titer20) == 0 or float(blank) == 0 or float(botvol) == 0 or float(
                titer20) == -9:
            oxycalc = 0
        else:
            o2ml = (float(titer20) - float(blank)) * float(thio20n) * o2mlpmeq - doreag
            oxycalc = round(o2ml / ((float(botvol) - vreag) * 0.001), 3)

        return oxycalc

    def corrthionorm(self, iodatevol, iodatenorm, blank, stdtiter):
        if self.override_thio_norm_check.isChecked():
            thio20N = float(self.thionormtext.text())
        else:
            thio20N = (float(iodatevol) * float(iodatenorm)) / (float(stdtiter) - float(blank))

        return thio20N

    def completeproc(self, file):

        lst = file
        self.procced = True
        # Pull everything from the lst file
        stationnum, castnum, bottlenum, flaskid, flaskvol, rawtiter, \
        titer, oxygenmils, thiotemps, drawtemp, volts, titertime = self.readinlst(lst)

        # Find the actual volume of iodate dispensed
        #correctediodatetiter = self.h2odvdt1(self.iodateburettetext.text(), 20, self.iodatetemptext.text())
        #self.iodateburettetext.setText(str(round(correctediodatetiter, 5)))

        correctediodatetiter = float(self.iodateburettetext.text())

        # Determine the Thio normality
        actualthion = self.corrthionorm(correctediodatetiter, self.iodatenormtext.text(), self.blanktext.text(),
                                        self.titertext.text())

        roundedthio = round(actualthion, 5)
        self.thionormtext.setText(str(roundedthio))

        global oxygenresults
        oxygenresults = []
        self.o2mol = []
        corr_flaskvol = []
        for i, x in enumerate(flaskvol):
            corr_flaskvol.append(round(self.glassdvdt(x, 20, drawtemp[i]), 3))

        for i in range(len(stationnum)):
            oxygenresults.append(
                round(self.oxycalc(actualthion, titer[i], float(self.blanktext.text()), corr_flaskvol[i]), 5))
            self.o2mol.append(round(float(oxygenresults[i]) * self.ml_to_mol_coefficient, 4))

        for i in range(len(stationnum)):
            self.datatable.setItem(i, 0, QTableWidgetItem(str(stationnum[i])))
            self.datatable.setItem(i, 1, QTableWidgetItem(str(castnum[i])))
            self.datatable.setItem(i, 2, QTableWidgetItem(str(bottlenum[i])))
            self.datatable.setItem(i, 3, QTableWidgetItem(str(flaskid[i])))
            self.datatable.setItem(i, 4, QTableWidgetItem(str(flaskvol[i])))
            self.datatable.setItem(i, 5, QTableWidgetItem(str(rawtiter[i])))
            self.datatable.setItem(i, 6, QTableWidgetItem(str(titer[i])))
            self.datatable.setItem(i, 7, QTableWidgetItem(str(oxygenresults[i])))
            self.datatable.setItem(i, 8, QTableWidgetItem(str(thiotemps[i])))
            self.datatable.setItem(i, 9, QTableWidgetItem(str(drawtemp[i])))
            self.datatable.setItem(i, 10, QTableWidgetItem(str(volts[i])))
            self.datatable.setItem(i, 11, QTableWidgetItem(str(titertime[i])))
            self.datatable.setItem(i, 12, QTableWidgetItem(str(self.o2mol[i])))

    def saveresults(self, lst):
        # Replace results
        filebuffer = open(lst)
        readbuffer = csv.reader(filebuffer, delimiter=' ')
        filelist = list(readbuffer)
        filebuffer.close()

        if self.procced is True:
            for i in range(self.numofsamples):
                k = (self.startx + 2 + i)
                filelist[k][10] = oxygenresults[i]
                filelist[self.iodatenormx][(self.iodatenormy + 1)] = self.iodatenormtext.text()
                filelist[self.iodatevolx][(self.iodatevoly + 2)] = self.iodateburettetext.text()
                filelist[self.stdtiterx][(self.stdtitery + 1)] = self.titertext.text()
                filelist[self.blankx][(self.blanky + 2)] = self.blanktext.text()
                filelist[self.iodatetempx][(self.iodatetempy + 3)] = self.iodatetemptext.text()
                filelist[self.thionormx][(self.thionormy + 1)] = self.thionormtext.text()
                filelist[self.thiotempx][(self.thiotempy + 1)] = self.thiotemptext.text()

        filebuffer = open(str(lst[0:-4]) + 'updated.LST', 'w', newline='')
        writebuffer = csv.writer(filebuffer, delimiter=' ')

        for row in filelist:
            writebuffer.writerow(row)

        filebuffer.close()

        message = QMessageBox.about(self, "Saved", str(self.filename) + " is saved\nas an updated file.")

    def saveascsv(self, lst):

        filebuffer = open(str(lst[0:-4]) + '.csv', 'w', newline='')
        writebuffer = csv.writer(filebuffer, delimiter=',')

        writebuffer.writerow(['Date Analysed', self.dateanalysed])
        writebuffer.writerow(['Analyst', self.analyst])
        writebuffer.writerow(['Lab', self.lab])
        writebuffer.writerow(['IO3 Normality @ 20', self.iodatenorm])
        writebuffer.writerow(['IO3 Vol @ 20', self.iodatevol])
        writebuffer.writerow(['Std Titre @ 20', self.stdtiter])
        writebuffer.writerow(['Blank', self.blank])
        writebuffer.writerow(['IO3 Temp', self.iodatetemp])
        writebuffer.writerow(['Thio Normality @ 20', self.thionorm])
        writebuffer.writerow(['Thio Temp', self.thiotemp])
        writebuffer.writerow(['O2 Box', 'NA'])
        writebuffer.writerow(['Raw Data File', self.filename])
        writebuffer.writerow([''])
        writebuffer.writerow(
            ['Survey', 'Stn', 'RP', 'Date_Sampled', 'Bottle', 'FlaskVol', 'RawTitre', 'Titre20', 'O2ml/L', 'ThioTemp',
             'DrawTemp', 'EndVolts', 'TitreTime', 'O2µmol/L', 'Comments'])

        for i in range(self.numofsamples):
            writebuffer.writerow(
                [str(self.filename[0:-6]), self.stationnum[i], self.bottlenum[i], self.dateanalysed, self.flaskid[i],
                 self.flaskvol[i], self.rawtiter[i], self.titer[i], self.oxygenmils[i], self.thiotemps[i],
                 self.drawtemp[i], self.volts[i], self.titertime[i], self.o2mol[i]])

        filebuffer.close()
        message = QMessageBox.about(self, "Saved", str(self.filename) + " is saved\nas an CSV.")

    def process(self):
        self.completeproc(self.lstfile)

    def reloadfile(self):

        print('reload')

    def editablefields(self):

        if self.iodatenormtext.isReadOnly() is False:
            self.iodatenormtext.setReadOnly(True)
            self.iodateburettetext.setReadOnly(True)
            self.iodatetemptext.setReadOnly(True)
            self.thionormtext.setReadOnly(True)
            self.thiotemptext.setReadOnly(True)
            self.titertext.setReadOnly(True)
            self.blanktext.setReadOnly(True)
            self.editfields.setText('Edit Parameters')
        else:
            self.iodatenormtext.setReadOnly(False)
            self.iodateburettetext.setReadOnly(False)
            self.iodatetemptext.setReadOnly(False)
            self.thionormtext.setReadOnly(False)
            self.thiotemptext.setReadOnly(False)
            self.titertext.setReadOnly(False)
            self.blanktext.setReadOnly(False)
            self.editfields.setText('Lock Parameters')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = correctDos()
    sys.exit(app.exec_())
