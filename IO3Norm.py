from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QDesktopWidget, QLabel, QPushButton, QLineEdit, QFrame)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import traceback
from decimal import Decimal

# To calculate the normality of iodate solution made up

AIR_DENSITY = 0.0012 # g/cm3 - General density of air
CALIBRATED_WEIGHT_DENSITY = 8.36  # g/cm3 - Density of weights to calibrate balance
POTASSIUM_IODATE_DENSITY = 3.89  # g/cm3 - Denstiy of Iodate salt
IODATE_EQUIVALENT_WEIGHT = 35.667  # g - Equiv weight in mederately acidic solution

class IodateNorm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(':/assets/icon.svg'))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()

        self.setStyleSheet('''
                QLabel {
                    font: 14px;
                }   
                QPushButton {
                    font: 14px;
                }
                QComboBox {
                    font: 14px;
                }
                QListWidget {

                    font: 14px;
                }
                QTableWidget {
                    font: 14px;
                }
                QCheckBox {
                    font: 14px;
                }
                QLineEdit {
                    font: 14px;
                }
                ''')

    def init_ui(self):
        self.setFont(QFont('Segoe UI'))

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        self.setGeometry(0, 0, 450, 350)
        qtRect = self.frameGeometry()
        centrePoint = QDesktopWidget().availableGeometry().center()
        qtRect.moveCenter(centrePoint)
        self.move(qtRect.topLeft())

        self.setWindowTitle('Calculate Iodate Normality')

        flask_vol_label = QLabel('Volume of volumetric flask at 20°C (mL):')
        self.flask_vol = QLineEdit(self)

        iodate_weight_label = QLabel('Weight of KIO3 standard (g):')
        self.iodate_weight = QLineEdit(self)

        temperature_label = QLabel('Temperature of solution when prepared (°C):')
        self.temperature = QLineEdit(self)

        calculate = QPushButton('Calculate')
        calculate.pressed.connect(self.calculate_norm)
        calculate.setFixedWidth(200)

        linesep1 = QFrame()
        linesep1.setFrameShape(QFrame.HLine)
        linesep1.setFrameShadow(QFrame.Sunken)

        self.corrected_flask_vol_label = QLabel('Glass volume at XX°C (mL): ')
        self.corrected_flask_vol = QLineEdit(self)
        self.corrected_flask_vol.setReadOnly(True)

        corrected_water_vol_label = QLabel('Volume of water in flask corrected to 20°C (mL):')
        self.corrected_water_vol = QLineEdit(self)
        self.corrected_water_vol.setReadOnly(True)

        true_mass_label = QLabel('True Iodate mass (g):')
        self.true_mass = QLineEdit(self)
        self.true_mass.setReadOnly(True)

        equiv_iodate_label = QLabel('Equivalent Iodate (g):')
        self.equiv_iodate_line = QLineEdit(self)
        self.equiv_iodate_line.setReadOnly(True)

        linesep2 = QFrame()
        linesep2.setFrameShape(QFrame.HLine)
        linesep2.setFrameShadow(QFrame.Sunken)

        calc_normality_label = QLabel('Standard normality at 20°C (N):')
        self.calc_normality = QLineEdit(self)
        self.calc_normality.setReadOnly(True)


        grid_layout.addWidget(flask_vol_label, 0, 0)
        grid_layout.addWidget(self.flask_vol, 0, 1)

        grid_layout.addWidget(iodate_weight_label, 1, 0)
        grid_layout.addWidget(self.iodate_weight, 1, 1)

        grid_layout.addWidget(temperature_label, 2, 0)
        grid_layout.addWidget(self.temperature, 2, 1)

        grid_layout.addWidget(calculate, 3, 0, 1, 2, Qt.AlignHCenter)

        grid_layout.addWidget(linesep1, 4, 0, 1, 2)

        grid_layout.addWidget(self.corrected_flask_vol_label, 5, 0)
        grid_layout.addWidget(self.corrected_flask_vol, 5, 1)

        grid_layout.addWidget(corrected_water_vol_label, 6, 0)
        grid_layout.addWidget(self.corrected_water_vol, 6, 1)

        grid_layout.addWidget(true_mass_label, 7, 0)
        grid_layout.addWidget(self.true_mass, 7, 1)

        grid_layout.addWidget(equiv_iodate_label, 8, 0)
        grid_layout.addWidget(self.equiv_iodate_line, 8, 1)

        grid_layout.addWidget(linesep2, 9, 0, 1, 2)

        grid_layout.addWidget(calc_normality_label, 10, 0)
        grid_layout.addWidget(self.calc_normality, 10, 1)

        self.centralWidget().setLayout(grid_layout)

        self.show()

    def calculate_norm(self):
        try:
            vol = float(self.flask_vol.text())
            meas_weight = float(self.iodate_weight.text())
            temp = float(self.temperature.text())

            glass_vol = self.glass_dvdt(vol, 20, temp)
            self.corrected_flask_vol.setText(str(round(glass_vol, 3)))
            self.corrected_flask_vol_label.setText('Glass volume at ' + str(temp) + '°C (mL): ')

            water_vol = self.water_dvdt(glass_vol, temp, 20)
            self.corrected_water_vol.setText(str(round(water_vol, 3)))

            iodate_tw = self.true_weight(meas_weight)
            self.true_mass.setText(str(round(iodate_tw, 6)))

            iodate_equiv = self.iodate_equivalent(iodate_tw)
            self.equiv_iodate_line.setText(str(round(iodate_equiv, 5)))

            iodate_normality = self.normality(iodate_equiv, water_vol)
            self.calc_normality.setText(str(round(float(iodate_normality), 7)))

        except ValueError:
            print('Need numbers in the fields')
        except Exception:
            print(traceback.print_exc())


    def normality(self, equivalent, water_vol):

        normality = equivalent / (Decimal(water_vol) / Decimal(1000))
        return normality

    def iodate_equivalent(self, weight):
        # Calculated assuming potassium iodate is in moderately acidic solution
        # meaning molarity to normal conversion is 6 to 1, equivalent weight therefore
        # 214.00 divided by 6 to equal 35.667 - this was rounded but to match
        # legacy dos software it was expanded to that exact number
        dec_weight = Decimal(weight)
        equiv_coef = Decimal(214.00/6.00)
        dec_eq = dec_weight / equiv_coef

        eq = weight / (214 / 6)

        return dec_eq

    def true_weight(self, meas_weight):
        # Calculated from Single pan balances, buoyancy and gravity, R. Battino 1984.
        tw = meas_weight * (1 + ((1/POTASSIUM_IODATE_DENSITY) - (1/CALIBRATED_WEIGHT_DENSITY)) * AIR_DENSITY)

        return tw

    def rhoddw (self, temp):
        # The density of pure water, rhoddw, is calculated as give on page F-4 from
        # Volume Properties of Water, Equation 1, CRC Handbook, 69th Edition, 1989

        z0 = 999.83952
        z1 = 16.945176
        z2 = -0.0079870401
        z3 = -0.000046170461
        z4 = 0.00000010556302
        z5 = -2.8054253E-10
        z6 = 0.01687985

        rhot2 = z2 + temp * (z3 + temp * (z4 + temp * z5))
        rhot1 = z0 + temp * (z1 + temp * (rhot2))
        rhoddw = rhot1 * 0.001 / (1 + z6 * temp)

        return rhoddw

    def water_dvdt(self, volume, temperature_start, temperature_final):
        # Calculate the volume that would be occupied by a given amount of aqueous liquid at a
        # given temperature (temp final) if it were changed from an initial temperature (temp initial)
        # Determined by multiplying the volume by the density ratio, rho(temp_initial)/rho(temp_final)
        # Rho(temp) is extracted from F-4, Volume Properties of Water, Equation 1, CRC Handbook

        if temperature_start == 0:
            return 0

        else:
            ratio = self.rhoddw(temperature_start) / self.rhoddw(temperature_final)

            final_volume = volume * ratio

            return final_volume


    def glass_dvdt(self, volume, temperature_known, temperature_desired):
        # Calculates the actual volume of a glass container at a given temperature,
        # from the calibrated volume at a given temperature, e.g. 20 degrees C
        # Using glass coefficient for borosilicate glass from A. Dickson SOP13
        glass_coefficient = 0.00000975

        final_volume = volume * (1 + glass_coefficient * (temperature_desired - temperature_known))

        return final_volume
