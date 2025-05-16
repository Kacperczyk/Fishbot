from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(568, 543)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Główny layout pionowy
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(20)  # Stały odstęp 20 pikseli między układami

        # Pierwszy layout poziomy (Uruchamianie programu + pole tekstowe + etykieta)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        # Kontener dla pierwszego układu poziomego
        self.container_1 = QtWidgets.QWidget(self.centralwidget)
        self.container_1.setLayout(self.horizontalLayout_1)
        self.container_1.setMaximumWidth(500)  # Maksymalna szerokość dla całego układu
        self.container_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Zapobiega rozciąganiu

        # Przycisk "Uruchamianie programu"
        self.uruchamianie_b1 = QtWidgets.QPushButton(self.container_1)
        self.uruchamianie_b1.setObjectName("uruchamianie_b1")
        self.horizontalLayout_1.addWidget(self.uruchamianie_b1)
        self.uruchamianie_b1.setMaximumWidth(130)
        self.uruchamianie_b1.setMinimumHeight(30)
        self.uruchamianie_b1.setMinimumWidth(130)

        # Pole tekstowe "Dowolny znak1"
        self.dowolny1_lineedit = QtWidgets.QLineEdit(self.container_1)
        self.dowolny1_lineedit.setObjectName("dowolny1_lineedit")
        self.horizontalLayout_1.addWidget(self.dowolny1_lineedit)

        # Etykieta "Przypisany znak1"
        self.przypiszznak_label1 = QtWidgets.QLabel(self.container_1)
        self.przypiszznak_label1.setObjectName("przypiszznak_label1")
        self.horizontalLayout_1.addWidget(self.przypiszznak_label1)

        self.verticalLayout.addWidget(self.container_1)  # Dodajesz kontener, a nie układ poziomy

        # Drugi layout poziomy (Przynęta + pole tekstowe + etykieta)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Kontener dla drugiego układu poziomego
        self.container_2 = QtWidgets.QWidget(self.centralwidget)
        self.container_2.setLayout(self.horizontalLayout_2)
        self.container_2.setMaximumWidth(500)  # Maksymalna szerokość dla całego układu
        self.container_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Zapobiega rozciąganiu

        # Przycisk "Przynęta"
        self.przynete_b2 = QtWidgets.QPushButton(self.container_2)
        self.przynete_b2.setObjectName("przynete_b2")
        self.horizontalLayout_2.addWidget(self.przynete_b2)
        self.przynete_b2.setMaximumWidth(130)
        self.przynete_b2.setMinimumHeight(30)
        self.przynete_b2.setMinimumWidth(130)

        # Pole tekstowe "Dowolny znak2"
        self.dowolny1_lineedit_2 = QtWidgets.QLineEdit(self.container_2)
        self.dowolny1_lineedit_2.setObjectName("dowolny1_lineedit_2")
        self.horizontalLayout_2.addWidget(self.dowolny1_lineedit_2)

        # Etykieta "Przypisany znak2"
        self.przypiszznak_label1_2 = QtWidgets.QLabel(self.container_2)
        self.przypiszznak_label1_2.setObjectName("przypiszznak_label1_2")
        self.horizontalLayout_2.addWidget(self.przypiszznak_label1_2)

        self.verticalLayout.addWidget(self.container_2)  # Dodajesz kontener, a nie układ poziomy

        # Trzeci layout poziomy (Uruchom teraz + Zatrzymaj)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # Kontener dla trzeciego układu poziomego
        self.container_3 = QtWidgets.QWidget(self.centralwidget)
        self.container_3.setLayout(self.horizontalLayout_3)
        self.container_3.setMaximumWidth(500)  # Maksymalna szerokość dla całego układu
        self.container_3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Zapobiega rozciąganiu

        # Przycisk "Uruchom teraz"
        self.uruchom_b3 = QtWidgets.QPushButton(self.container_3)
        self.uruchom_b3.setObjectName("uruchom_b3")
        self.horizontalLayout_3.addWidget(self.uruchom_b3)
        self.uruchom_b3.setMaximumWidth(130)
        self.uruchom_b3.setMinimumHeight(30)
        self.uruchom_b3.setMinimumWidth(130)

        # Przycisk "Zatrzymaj"
        self.zatrzymaj_b4 = QtWidgets.QPushButton(self.container_3)
        self.zatrzymaj_b4.setObjectName("zatrzymaj_b4")
        self.horizontalLayout_3.addWidget(self.zatrzymaj_b4)
        self.zatrzymaj_b4.setMaximumWidth(130)
        self.zatrzymaj_b4.setMinimumHeight(30)
        self.zatrzymaj_b4.setMinimumWidth(130)

        self.verticalLayout.addWidget(self.container_3)  # Dodajesz kontener, a nie układ poziomy

        # Etykieta statusu programu
        self.aktywnynieaktywny_label3 = QtWidgets.QLabel(self.centralwidget)
        self.aktywnynieaktywny_label3.setObjectName("aktywnynieaktywny_label3")
        self.verticalLayout.addWidget(self.aktywnynieaktywny_label3)

        # Dodaj elastyczną przestrzeń na końcu, aby odstępy były stałe
        self.verticalLayout.addStretch()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 568, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.uruchamianie_b1.setText(_translate("MainWindow", "Uruchamianie programu"))
        self.przynete_b2.setText(_translate("MainWindow", "Przynęta"))
        self.zatrzymaj_b4.setText(_translate("MainWindow", "Zatrzymaj"))
        self.uruchom_b3.setText(_translate("MainWindow", "Uruchom teraz"))
        self.przypiszznak_label1.setText(_translate("MainWindow", "Przypisany znak1: "))
        self.przypiszznak_label1_2.setText(_translate("MainWindow", "Przypisany znak2: "))
        self.aktywnynieaktywny_label3.setText(_translate("MainWindow", "Program aktywny/nieaktywny"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())