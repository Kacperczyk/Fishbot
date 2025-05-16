#Uruchmianie i zatrzymanie prawidlowo
#edit line dziala prawidlowo
#domyslnie program jest nieaktywny
#dodano konsole + podsatwowe info logi
#dodano nasluchiwanie jedynie przypisanych klawiszy
#dodano aktywacje programu w momencie wykrycia nacisniea klawisza 1
#dodano czas do konsoli
#dodno konsole go osobnej zakladki

import sys
import threading
import keyboard  # Importujemy bibliotekę keyboard
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(568, 543)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Tworzymy QTabWidget (widget do zakładek)
        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 568, 543))  # Wypełnia całe główne okno

        # Zakładka do logów (konsola)
        self.log_history_tab = QtWidgets.QWidget()
        self.log_history_tab.setObjectName("log_history_tab")

        # Konsola (QTextEdit)
        self.console_textedit = QtWidgets.QTextEdit(self.log_history_tab)
        self.console_textedit.setGeometry(QtCore.QRect(10, 10, 540, 440))  # Ustawienie konsoli w zakładce
        self.console_textedit.setObjectName("console_textedit")
        self.console_textedit.setReadOnly(True)  # Tylko do odczytu
        self.console_textedit.setPlaceholderText("Konsola...")

        # Zakładka główna (z przyciskami i polami tekstowymi)
        self.main_tab = QtWidgets.QWidget()
        self.main_tab.setObjectName("main_tab")

        # Przyciski
        self.uruchamianie_b1 = QtWidgets.QPushButton(self.main_tab)
        self.uruchamianie_b1.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.uruchamianie_b1.setObjectName("uruchamianie_b1")
        self.przynete_b2 = QtWidgets.QPushButton(self.main_tab)
        self.przynete_b2.setGeometry(QtCore.QRect(10, 50, 131, 31))
        self.przynete_b2.setObjectName("przynete_b2")
        self.zatrzymaj_b4 = QtWidgets.QPushButton(self.main_tab)
        self.zatrzymaj_b4.setGeometry(QtCore.QRect(10, 130, 131, 31))
        self.zatrzymaj_b4.setObjectName("zatrzymaj_b4")
        self.uruchom_b3 = QtWidgets.QPushButton(self.main_tab)
        self.uruchom_b3.setGeometry(QtCore.QRect(10, 90, 131, 31))
        self.uruchom_b3.setObjectName("uruchom_b3")

        # Pola do wpisywania tekstu
        self.dowolny1_lineedit = QtWidgets.QLineEdit(self.main_tab)
        self.dowolny1_lineedit.setGeometry(QtCore.QRect(150, 10, 151, 31))
        self.dowolny1_lineedit.setObjectName("dowolny1_lineedit")

        self.dowolny1_lineedit_2 = QtWidgets.QLineEdit(self.main_tab)
        self.dowolny1_lineedit_2.setGeometry(QtCore.QRect(150, 50, 151, 31))
        self.dowolny1_lineedit_2.setObjectName("dowolny1_lineedit_2")

        # Etykiety
        self.przypiszznak_label1 = QtWidgets.QLabel(self.main_tab)
        self.przypiszznak_label1.setGeometry(QtCore.QRect(310, 16, 121, 20))
        self.przypiszznak_label1.setObjectName("przypiszznak_label1")

        self.przypiszznak_label1_2 = QtWidgets.QLabel(self.main_tab)
        self.przypiszznak_label1_2.setGeometry(QtCore.QRect(310, 59, 121, 21))
        self.przypiszznak_label1_2.setObjectName("przypiszznak_label1_2")

        self.aktywnynieaktywny_label3 = QtWidgets.QLabel(self.main_tab)
        self.aktywnynieaktywny_label3.setGeometry(QtCore.QRect(10, 480, 151, 20))
        self.aktywnynieaktywny_label3.setObjectName("aktywnynieaktywny_label3")

        # Dodajemy zakładki do QTabWidget
        self.tab_widget.addTab(self.main_tab, "Program")
        self.tab_widget.addTab(self.log_history_tab, "Log History")

        MainWindow.setCentralWidget(self.tab_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 568, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Inicjalizacja ustawień dla domyślnego tekstu
        self.dowolny1_lineedit.setPlaceholderText("Dowolny znak1")
        self.dowolny1_lineedit_2.setPlaceholderText("Dowolny znak2")

        # Flagi kontrolujące stan edycji
        self.dowolny1_locked = False
        self.dowolny2_locked = False
        self.program_active = False  # Flaga, która będzie kontrolować, czy program jest aktywny

        # Lista przypisanych klawiszy
        self.assigned_keys = []  # Lista przypisanych klawiszy

        # Łączenie przycisków z akcjami
        self.uruchamianie_b1.clicked.connect(self.toggle_dowolny1)
        self.przynete_b2.clicked.connect(self.toggle_dowolny2)
        self.uruchom_b3.clicked.connect(self.toggle_program_status)
        self.zatrzymaj_b4.clicked.connect(self.toggle_program_status)

        # Zdarzenie, które usuwa placeholder, gdy użytkownik kliknie w pole tekstowe
        self.dowolny1_lineedit.textChanged.connect(self.clear_placeholder1)
        self.dowolny1_lineedit_2.textChanged.connect(self.clear_placeholder2)

        # Ustawienie programu na domyślnie nieaktywny
        self.update_ui_for_program_status()

        # Uruchomienie nasłuchu na klawisze w tle
        self.start_key_listener()

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

    def log_to_console(self, message):
        """Funkcja do wypisywania komunikatów w konsoli z aktualnym czasem"""
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Uzyskanie bieżącego czasu
        self.console_textedit.append(f"[{current_time}] {message}")

    def toggle_dowolny1(self):
        if self.dowolny1_locked:
            self.dowolny1_lineedit.setEnabled(True)
            self.dowolny1_lineedit.setStyleSheet("background-color: white;")  # Przywróć normalne tło
            self.przypiszznak_label1.setText(f"Przypisany znak1: {self.dowolny1_lineedit.text()}")
            self.log_to_console(f"Przypisano znak1: {self.dowolny1_lineedit.text()}")
            self.update_assigned_keys(self.dowolny1_lineedit.text())  # Aktualizuj przypisane klawisze
        else:
            self.dowolny1_lineedit.setEnabled(False)
            self.dowolny1_lineedit.setStyleSheet("background-color: lightgray;")  # Zablokowane tło
            self.przypiszznak_label1.setText(f"Przypisany znak1: {self.dowolny1_lineedit.text()}")
            self.log_to_console("Znak1 został zablokowany.")

        # Zmieniamy flagę
        self.dowolny1_locked = not self.dowolny1_locked

    def toggle_dowolny2(self):
        if self.dowolny2_locked:
            self.dowolny1_lineedit_2.setEnabled(True)
            self.dowolny1_lineedit_2.setStyleSheet("background-color: white;")  # Przywróć normalne tło
            self.przypiszznak_label1_2.setText(f"Przypisany znak2: {self.dowolny1_lineedit_2.text()}")
            self.log_to_console(f"Przypisano znak2: {self.dowolny1_lineedit_2.text()}")
        else:
            self.dowolny1_lineedit_2.setEnabled(False)
            self.dowolny1_lineedit_2.setStyleSheet("background-color: lightgray;")  # Zablokowane tło
            self.przypiszznak_label1_2.setText(f"Przypisany znak2: {self.dowolny1_lineedit_2.text()}")
            self.log_to_console("Znak2 został zablokowany.")

        # Zmieniamy flagę
        self.dowolny2_locked = not self.dowolny2_locked

    def clear_placeholder1(self):
        if self.dowolny1_lineedit.text() != "":
            self.dowolny1_lineedit.setPlaceholderText("")  # Usuwa placeholder

    def clear_placeholder2(self):
        if self.dowolny1_lineedit_2.text() != "":
            self.dowolny1_lineedit_2.setPlaceholderText("")  # Usuwa placeholder

    def toggle_program_status(self):
        self.program_active = not self.program_active  # Przełączenie flagi aktywności programu
        self.update_ui_for_program_status()

    def update_ui_for_program_status(self):
        # Zmieniamy widoczność przycisków i statusu
        if self.program_active:
            self.aktywnynieaktywny_label3.setText("Status programu: AKTYWNY")
            self.aktywnynieaktywny_label3.setStyleSheet("color: green;")  # Kolor zielony, gdy aktywny
            self.zatrzymaj_b4.setEnabled(True)
            self.uruchom_b3.setEnabled(False)
            self.log_to_console("Program został uruchomiony.")
        else:
            self.aktywnynieaktywny_label3.setText("Status programu: NIEAKTYWNY")
            self.aktywnynieaktywny_label3.setStyleSheet("color: red;")  # Kolor czerwony, gdy nieaktywny
            self.zatrzymaj_b4.setEnabled(False)
            self.uruchom_b3.setEnabled(True)
            self.log_to_console("Program został zatrzymany.")

    def update_assigned_keys(self, keys):
        """Aktualizuje przypisane klawisze na podstawie wprowadzonego tekstu w dowolnym1_lineedit"""
        self.assigned_keys = [key for key in keys]
        self.log_to_console(f"Przypisane klawisze: {', '.join(self.assigned_keys)}")

    def start_key_listener(self):
        """Funkcja uruchamiająca nasłuch klawiszy w osobnym wątku"""

        def listen_for_keys():
            while True:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:  # Kiedy klawisz jest naciśnięty
                    if event.name in self.assigned_keys:  # Sprawdzamy, czy naciśnięty klawisz jest przypisany
                        self.log_to_console(f"Naciśnięto przypisany klawisz: {event.name}")
                        self.toggle_program_status()  # Zmieniamy status programu (aktywujemy lub dezaktywujemy)

        # Uruchamiamy nasłuch klawiszy w osobnym wątku, aby nie blokować GUI
        key_listener_thread = threading.Thread(target=listen_for_keys, daemon=True)
        key_listener_thread.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Uzyskanie rozdzielczości ekranu
    screen_geometry = app.desktop().screenGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    # Rozmiar okna
    window_width = MainWindow.width()
    window_height = MainWindow.height()

    # Obliczamy współrzędne dla prawego górnego rogu
    x_position = screen_width - window_width
    y_position = 0

    # Ustawiamy pozycję okna
    MainWindow.move(x_position, y_position)

    MainWindow.show()
    sys.exit(app.exec_())
