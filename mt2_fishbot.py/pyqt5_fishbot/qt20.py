import sys
import ctypes
from ctypes import wintypes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEvent, QPoint
from PyQt5.QtWidgets import (QLineEdit, QApplication, QLabel, QMainWindow,
                             QTextEdit, QPushButton, QTabWidget, QWidget, QDialog, QVBoxLayout, QMessageBox,
                             QSystemTrayIcon, QMenu, QAction, QFrame)
from PyQt5.QtGui import QIcon, QKeySequence
import datetime
from toggle_button_module import ToggleButton
import qdarkstyle
from custom_modes import get_customstyles_dark, get_customstyles_light
import traceback


def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    print("Nieoczekiwany wyjątek:", "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))


sys.excepthook = exception_handler

# Stałe Windows
WM_HOTKEY = 0x0312

# Globalna mapa kodów wirtualnych dla klawiszy F1-F12 (rozszerz według potrzeb)
global_vk_map = {
    # Klawisze funkcyjne
    "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73,
    "F5": 0x74, "F6": 0x75, "F7": 0x76, "F8": 0x77,
    "F9": 0x78, "F10": 0x79, "F11": 0x7A, "F12": 0x7B,

    "A": 0x41, "B": 0x42, "C": 0x43, "D": 0x44, "E": 0x45,
    "F": 0x46, "G": 0x47, "H": 0x48, "I": 0x49, "J": 0x4A,
    "K": 0x4B, "L": 0x4C, "M": 0x4D, "N": 0x4E, "O": 0x4F,
    "P": 0x50, "Q": 0x51, "R": 0x52, "S": 0x53, "T": 0x54,
    "U": 0x55, "V": 0x56, "W": 0x57, "X": 0x58, "Y": 0x59,
    "Z": 0x5A, "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33,
    "4": 0x34, "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38,
    "9": 0x39,

    "Space": 0x20, "Enter": 0x0D, "Tab": 0x09,
    "Ctrl": 0x11, "Alt": 0x12, "Shift": 0x10, "CapsLock": 0x14,
    "Backspace": 0x08, "Escape": 0x1B, "Delete": 0x2E,
    "Insert": 0x2D, "Home": 0x24, "End": 0x23, "PageUp": 0x21, "PageDown": 0x22,
    "Left": 0x25, "Up": 0x26, "Right": 0x27, "Down": 0x28
}


class KeyAssignmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Przypisanie klawisza")
        self.setModal(True)
        self.resize(300, 100)

        layout = QVBoxLayout(self)
        self.label = QLabel("Naciśnij dowolny klawisz...", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.assigned_key = None

    def keyPressEvent(self, event):
        key = event.text()
        if not key:
            key = QKeySequence(event.key()).toString()
        self.assigned_key = key
        self.accept()


class GlobalHotkeyFilter(QtCore.QAbstractNativeEventFilter):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def nativeEventFilter(self, eventtype, message):
        if eventtype == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(int(message))
            if msg.message == WM_HOTKEY:
                hotkey_id = msg.wParam
                self.parent.handleGlobalHotkey(hotkey_id)
        return False, 0


class StatusFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setFixedSize(120, 50)
        self.setAttribute(
            Qt.WA_TranslucentBackground)  # Aktywuje przezroczystość tła okna, dzięki czemu można zobaczyć zawartość w nieregularnym kształcie
        # (np. z zaokrąglonymi rogami). W skrócie, tło jest renderowane jako przezroczyste, ale zawartość widżetów w oknie pozostaje widoczna.
        self.setStyleSheet("""                         
            border-radius: 10px;
            border: 1px solid #666;
        """)

        # Tworzymy dwa wiersze tekstu
        self.title_label = QLabel("Fishbot Status", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 10px;
        """)
        self.title_label.setGeometry(0, 0, 120, 25)

        self.status_label = QLabel("Nieaktywny", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            color: red;
            font-weight: bold;
            font-size: 11px;
        """)
        self.status_label.setGeometry(0, 25, 120, 25)

        # Tworzenie pustego elementu na środku dla lepszego wygladu calego qframe (tutaj jedynie aspekt wizualny, i samo obramowanie)
        self.center_element = QLabel(self)
        self.center_element.setGeometry(0, 0, 120,
                                        50)  # Element na środku ramki (większy rozmiar dla efektu "oddalenia")
        self.center_element.setStyleSheet("""
            QLabel {
                border: 1px solid #666;          /* Obramowanie */
                border-radius: 10px;             /* Zaokrąglone rogi */
                background-color: transparent;  /* Brak tła */
            }
        """)

        # Zmienne do obsługi przeciągania i rozpoznawania kliknięcia
        self.drag_start_position = QPoint()
        self.has_moved = False

    def set_status(self, active):
        if active:
            self.status_label.setText("Aktywny")
            # Kolor zależny od motywu
            if self.parent_window.toggle_button.isChecked():  # Dark mode
                color = "#00ff00"  # jasna zieleń
            else:  # Light mode
                color = "green"  # standardowa zieleń
        else:
            self.status_label.setText("Nieaktywny")
            color = "red"  # ZAWSZE czerwony

        self.status_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            font-size: 11px;
            border-radius: 10px;
            border: 1px solid #666;
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Inicjalizujemy przeciąganie tylko dla lewego przycisku myszy
            self.drag_start_position = event.globalPos()
            self.has_moved = False  # Resetujemy flagę ruchu
            event.accept()
        elif event.button() == Qt.RightButton:
            # Obsługa prawego przycisku myszy wyłącznie dla menu kontekstowego
            self.contextMenuEvent(event)

    def mouseMoveEvent(self, event):
        # Przesuwamy ramkę w czasie rzeczywistym
        if event.buttons() == Qt.LeftButton:  # Przeciąganie tylko przy wciśniętym lewym przycisku
            offset = event.globalPos() - self.drag_start_position
            if offset.manhattanLength() > 5:
                self.move(self.pos() + offset)
                self.drag_start_position = event.globalPos()  # Aktualizujemy pozycję startową
                self.has_moved = True  # Ustawiamy flagę ruchu
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.has_moved:
                # Jeśli użytkownik nie przesunął ramki, otwieramy główne okno
                self.parent().showNormal()
                self.hide()
            event.accept()

    def contextMenuEvent(self, event):
        # Tworzymy menu kontekstowe
        menu = QMenu(self)
        menu.setWindowFlags(
            menu.windowFlags() | Qt.FramelessWindowHint)  # Kluczowe! bez tych rzeczy bedzie widac rogi sa ssytemowo domyslnei stworzone w taki sposob
        menu.setAttribute(Qt.WA_TranslucentBackground)  # Kluczowe!
        menu.setAttribute(Qt.WA_NoSystemBackground)  # Kluczowe!

        exit_action = menu.addAction("Exit")

        # Zmieniamy styl menu bez tego rogi rowneiz beda jak to przeniose do stylow to nic to nie da
        menu.setStyleSheet("""
            QMenu {
                background-color: transparent; /* Całkowicie przezroczyste tło */
                padding: 0px;
                margin: 0px;
                border: none;
                  }
                          """)

        action = menu.exec_(event.globalPos())

        if action == exit_action:
            QApplication.instance().quit()  # Zamykamy całą aplikację


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Zmienne stanu
        self.dowolny1_locked = True
        self.dowolny2_locked = True
        self.program_active = False
        self.assigned_key = None
        self.assigned_key2 = None
        self.current_listening_field = None
        self.global_hotkey_list_dowolny1 = []
        self.local_hotkey_list_dowolny2 = []

        self.key_map = {
            Qt.Key_F1: "F1", Qt.Key_F2: "F2", Qt.Key_F3: "F3", Qt.Key_F4: "F4",
            Qt.Key_F5: "F5", Qt.Key_F6: "F6", Qt.Key_F7: "F7", Qt.Key_F8: "F8",
            Qt.Key_F9: "F9", Qt.Key_F10: "F10", Qt.Key_F11: "F11", Qt.Key_F12: "F12",
            Qt.Key_Left: "Left", Qt.Key_Right: "Right", Qt.Key_Up: "Up", Qt.Key_Down: "Down",
            Qt.Key_Escape: "Escape", Qt.Key_Enter: "Enter", Qt.Key_Return: "Enter",
            Qt.Key_Space: "Space", Qt.Key_Tab: "Tab", Qt.Key_Backspace: "Backspace",
            Qt.Key_Delete: "Delete", Qt.Key_Insert: "Insert", Qt.Key_Home: "Home",
            Qt.Key_End: "End", Qt.Key_PageUp: "PgUp", Qt.Key_PageDown: "PgDown",
            Qt.Key_Print: "Print", Qt.Key_Pause: "Pause", Qt.Key_Menu: "Menu",
            Qt.Key_Shift: "Shift", Qt.Key_Control: "Ctrl", Qt.Key_Alt: "Alt",
            Qt.Key_AltGr: "AltGr", Qt.Key_Meta: "Meta", Qt.Key_CapsLock: "CapsLock"
        }

        # Konfiguracja okna
        self.setObjectName("MainWindow")
        self.resize(568, 543)
        self.setWindowTitle("mt2_fishbot_v0.1")
        self.setWindowIcon(QIcon("fish.gif"))
        self.setFocusPolicy(Qt.StrongFocus)

        # Inicjalizacja interfejsu
        self.init_ui()
        self.connect_signals()
        self.setup_initial_state()
        self.move_to_top_right()

        # System tray i status frame
        self.init_system_tray()
        self.status_frame = StatusFrame(self)
        self.update_status_frame_position()
        self.status_frame.hide()

        # Global hotkey filter
        if sys.platform.startswith("win"):
            self.hotkeyFilter = GlobalHotkeyFilter(self)
            QtWidgets.QApplication.instance().installNativeEventFilter(self.hotkeyFilter)

    def init_ui(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.init_tabs()
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 568, 21))
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.set_dark_style()

    def init_tabs(self):
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 568, 543))
        self.init_fishbot_tab()
        self.init_changelog_tab()

    def init_fishbot_tab(self):
        self.fishbot_tab = QWidget()
        self.init_buttons()
        self.init_line_edits()
        self.init_labels()
        self.init_toggle_button()
        self.init_console()
        self.tabWidget.addTab(self.fishbot_tab, "Fishbot")

    def init_buttons(self):
        self.uruchamianie_b1 = QPushButton("Uruchamianie programu", self.fishbot_tab)
        self.uruchamianie_b1.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.przynete_b2 = QPushButton("Przynęta", self.fishbot_tab)
        self.przynete_b2.setGeometry(QtCore.QRect(10, 50, 131, 31))
        self.zatrzymaj_b4 = QPushButton("Zatrzymaj", self.fishbot_tab)
        self.zatrzymaj_b4.setGeometry(QtCore.QRect(10, 130, 131, 31))
        self.uruchom_b3 = QPushButton("Uruchom teraz", self.fishbot_tab)
        self.uruchom_b3.setGeometry(QtCore.QRect(10, 90, 131, 31))

    def init_line_edits(self):
        self.dowolny1_lineedit = QLineEdit(self.fishbot_tab)
        self.dowolny1_lineedit.setGeometry(QtCore.QRect(150, 10, 60, 31))
        self.dowolny1_lineedit.setStyleSheet("background-color: lightgray;")
        self.dowolny1_lineedit.setEnabled(False)
        self.dowolny1_lineedit.setAlignment(Qt.AlignCenter)
        self.dowolny1_lineedit.setPlaceholderText("...")
        self.dowolny1_lineedit_2 = QLineEdit(self.fishbot_tab)
        self.dowolny1_lineedit_2.setGeometry(QtCore.QRect(150, 50, 60, 31))
        self.dowolny1_lineedit_2.setStyleSheet("background-color: lightgray;")
        self.dowolny1_lineedit_2.setEnabled(False)
        self.dowolny1_lineedit_2.setAlignment(Qt.AlignCenter)
        self.dowolny1_lineedit_2.setPlaceholderText("...")

    def init_labels(self):
        self.przypiszznak_label1 = QLabel("Klawisz uruchamiania programu przypisany do: ", self.fishbot_tab)
        self.przypiszznak_label1.setGeometry(QtCore.QRect(220, 16, 280, 20))
        self.przypiszznak_label1_2 = QLabel("Klawisz przynęty przypisany do: ", self.fishbot_tab)
        self.przypiszznak_label1_2.setGeometry(QtCore.QRect(220, 59, 280, 21))
        self.aktywnienieaktywny_label3 = QLabel("Program aktywny/nieaktywny", self.fishbot_tab)
        self.aktywnienieaktywny_label3.setGeometry(QtCore.QRect(10, 465, 160, 20))
        self.darkmode_label4 = QLabel("Dark mode", self.fishbot_tab)
        self.darkmode_label4.setGeometry(QtCore.QRect(456, 428, 70, 50))
        self.darkmode_label4.setStyleSheet("font-weight: bold;")

    def init_toggle_button(self):
        self.toggle_button = ToggleButton(self.fishbot_tab)
        self.toggle_button.move(470, 466)
        self.toggle_button.toggled.connect(self.on_toggle_darkmod)

    def init_console(self):
        self.console_textedit = QTextEdit(self.fishbot_tab)
        self.console_textedit.setGeometry(QtCore.QRect(150, 90, 380, 350))
        self.console_textedit.setReadOnly(True)
        self.console_textedit.setPlaceholderText("Konsola...")

    def init_changelog_tab(self):
        self.changelog_tab = QWidget()
        self.changelog_label = QLabel(self.changelog_tab)
        self.changelog_label.setWordWrap(True)
        self.changelog_label.setText("""
# Buttony uruchom teraz i zatrzymaj dzialaja prawidlowo
# Edit line dziala prawidlowo
# dodano konsole + podsatwowe info-logi
# dodano nasluchiwanie jedynie przypisanych klawiszy
# dodano aktywacje programu w momencie wykrycia nacisniea klawisza przypisanego
# dodano czas do konsoli
# dodano poprawna logike w przypisywaniu klawiszy "toggle_dowolny1"
# dodano poprawna logike w  "toggle_dowolny2"
# dodano zakladke changelog
# dodano przelacznik toggle button
# dodano light & dark mode
# dodano Doddanie nad toogle buttonem napisu informujacego o tym ze jest to przelacznik do dark mode'a
# dodano Zmiana lineedit --> mozliwosc przypisania max 1 znaku + przypisanie poprzez wcisniecie na klawiaturze
# dodane blokade przy nacisnieciu przneta/uruchomienie programu dla siebie nawzajem
# poprawiono caly kod na __init__
# zrezygnowana z modulu keybord gdyz powodowal konfilkty na tle watkow przy nasluchiwaniu globalnym
# dodano pop up (jednak zrezygnowanie z nasluchiwania globalnego odebralo mozliwossc nasluchiwania przy zminimalizowanym programie)
# Rozwiazano problem z linnijki wyzej dodajac glboalne hotkeye
# dodano kontrole czy gloalny hotkey nie jest juz przypisany, dziala to tak ze mam liste przechowywanych klawiszy global hotkey
  nastepnie w momencie odpalenie qdialog odczytuje klawisze z tej listy i na czas qdialog odpisuje wszystkie hotkeye, po zamknieciu
  q dialog przywraca hotkey.
  Kolejna poprawka, lista przechowywala wiec niz 1 element i odczytywane byly wszystkie jej elementy
  Zrobilem oddzielan liste dla kazdego przycisku + odczytywanie ostatniego jej elementu, dodatkowo jest walidacja spradzajac przypisanie przyciskow do rpzycisku zarowno
  tego samego jak i przycisku drugiego
  dodatkowo podzielono przyciski na globalne i lokalne
# dodano mini okienku przy minimalizacji programu
* todo dodaie blokowania przypisania tego samego globalnego hotkeya
* todo sprawdzenie wyrównania zakladek w sensie zeby ich szerokosc dopasowywala sie do dlugosci tekstu w nich
* todo automatycznie wykrywa toogle button wiec przy uruchomieniu programu z automatu wlaczenie light mode
        """)
        self.changelog_label.setGeometry(QtCore.QRect(5, -20, 560, 530))
        self.changelog_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.changelog_label.setContentsMargins(0, 10, 0, 0)
        self.tabWidget.addTab(self.changelog_tab, "Changelog")

    def set_dark_style(self):
        dark_stylesheet = qdarkstyle.load_stylesheet()
        combined_stylesheet = dark_stylesheet + get_customstyles_dark()
        self.setStyleSheet(combined_stylesheet)

        if hasattr(self, 'aktywnienieaktywny_label3') and self.program_active:
            self.aktywnienieaktywny_label3.setStyleSheet("color: #00ff00")

        # Aktualizacja status frame jeśli istnieje i program jest aktywny
        if hasattr(self, 'status_frame') and self.program_active:
            self.status_frame.set_status(True)

    def set_light_style(self):
        light_stylesheet = qdarkstyle.load_stylesheet()
        combined_stylesheet = light_stylesheet + get_customstyles_light()
        self.setStyleSheet(combined_stylesheet)

        if hasattr(self, 'aktywnienieaktywny_label3') and self.program_active:
            self.aktywnienieaktywny_label3.setStyleSheet("color: green")

        # Aktualizacja status frame jeśli istnieje i program jest aktywny
        if hasattr(self, 'status_frame') and self.program_active:
            self.status_frame.set_status(True)

    def connect_signals(self):
        self.uruchamianie_b1.clicked.connect(self.toggle_dowolny1)
        self.przynete_b2.clicked.connect(self.toggle_dowolny2)
        self.uruchom_b3.clicked.connect(self.toggle_program_status)
        self.zatrzymaj_b4.clicked.connect(self.toggle_program_status)
        self.dowolny1_lineedit.textChanged.connect(self.clear_placeholder1)
        self.dowolny1_lineedit_2.textChanged.connect(self.clear_placeholder2)

    def init_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("fish.gif"))

        tray_menu = QMenu()
        show_action = QAction("Pokaż", self)
        show_action.triggered.connect(self.show_normal)
        quit_action = QAction("Zamknij", self)
        quit_action.triggered.connect(self.close_app)

        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_normal(self):
        self.show()
        self.status_frame.hide()
        self.activateWindow()
        self.raise_()

    def close_app(self):
        self.tray_icon.hide()
        self.status_frame.hide()
        QApplication.quit()

    def setup_initial_state(self):
        self.update_ui_for_program_status()

        if hasattr(self, 'status_frame'):
            self.status_frame.set_status(self.program_active)

    def move_to_top_right(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x_position = screen_geometry.width() - self.width()
        self.move(x_position, 0)

    def update_status_frame_position(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        self.status_frame.move(
            screen_geometry.width() - self.status_frame.width() - 10,
            screen_geometry.height() - self.status_frame.height() - 60
        )

    def log_to_console(self, message):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.console_textedit.append(f"[{current_time}] {message}")

    def on_toggle_darkmod(self, state):
        if state:
            self.log_to_console("Dark mode aktywowany")
            self.set_dark_style()
        else:
            self.log_to_console("Dark mode dezaktywowany")
            self.set_light_style()

    def unregister_all_global_hotkeys(self):
        if sys.platform.startswith("win"):
            for hotkey_id, key in enumerate(self.global_hotkey_list_dowolny1, start=1):
                vk = global_vk_map.get(key.upper(), None)
                if vk is not None:
                    ctypes.windll.user32.UnregisterHotKey(int(self.winId()), hotkey_id)
                    self.log_to_console(f"Hotkey {key} został odłączony")

    def restore_all_global_hotkeys(self):
        if sys.platform.startswith("win"):
            for hotkey_id, key in enumerate(self.global_hotkey_list_dowolny1, start=1):
                vk = global_vk_map.get(key.upper(), None)
                if vk is not None:
                    ctypes.windll.user32.RegisterHotKey(int(self.winId()), hotkey_id, 0, vk)
                    self.log_to_console(f"Przywrócono globalny hotkey: {key}")

    def toggle_dowolny1(self):
        self.unregister_all_global_hotkeys()

        dialog = KeyAssignmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            key = dialog.assigned_key.upper()

            if key == self.assigned_key:
                QMessageBox.warning(self, "Błąd", f"Klawisz {key} jest już przypisany do innego przycisku!")
                self.log_to_console(
                    f"Nastapila proba przypisania uruchamiania programu do klawisza {key} ktory jest juz przypisany do tego samego przycisku")
                self.restore_all_global_hotkeys()
                return

            last_dowolny2 = self.local_hotkey_list_dowolny2[-1] if self.local_hotkey_list_dowolny2 else None
            if key == last_dowolny2:
                QMessageBox.warning(self, "Błąd", f"Klawisz {key} jest już przypisany do innego przycisku!")
                self.log_to_console(
                    f"Nastapila proba przypisania uruchamiania programu do klawisza {key} ktory jest juz przypisany do przycisku przynety")
                self.restore_all_global_hotkeys()
                return

            if self.assigned_key and self.assigned_key in self.global_hotkey_list_dowolny1:
                self.unregisterGlobalHotkey(1, self.assigned_key)
                self.global_hotkey_list_dowolny1.remove(self.assigned_key)
            elif self.assigned_key:
                self.log_to_console(
                    f"Ostrzeżenie: Klawisz {self.assigned_key} nie znajduje się na liście globalnych hotkeyow")

            self.assigned_key = key
            self.global_hotkey_list_dowolny1.append(key)
            self.dowolny1_lineedit.setText(key)
            self.przypiszznak_label1.setText(f"Klawisz uruchamiania programu przypisany do: {key}")
            self.registerGlobalHotkey(1, key)

        self.restore_all_global_hotkeys()

    def toggle_dowolny2(self):
        self.unregister_all_global_hotkeys()

        dialog = KeyAssignmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            key = dialog.assigned_key.upper()

            if key in self.global_hotkey_list_dowolny1:
                QMessageBox.warning(self, "Błąd", f"Klawisz {key} jest już przypisany do innego przycisku!")
                self.log_to_console(
                    f"Nastapila proba przypisania przynety do klawisza {key} ktory jest juz przypisany do przycisku uruchamiania programu")
                self.restore_all_global_hotkeys()
                return

            last_dowolny2 = self.local_hotkey_list_dowolny2[-1] if self.local_hotkey_list_dowolny2 else None
            if key == last_dowolny2:
                QMessageBox.warning(self, "Błąd", f"Klawisz {key} jest już przypisany do innego przycisku!")
                self.log_to_console(
                    f"Nastapila proba przypisania przynety do klawisza {key} ktory jest juz przypisany do tego samego przycisku")
                self.restore_all_global_hotkeys()
                return

            if self.assigned_key2 in self.local_hotkey_list_dowolny2:
                self.local_hotkey_list_dowolny2.remove(self.assigned_key2)

            self.assigned_key2 = key
            self.local_hotkey_list_dowolny2.append(key)
            self.dowolny1_lineedit_2.setText(key)
            self.przypiszznak_label1_2.setText(f"Klawisz przynęty przypisany do: {key}")
            self.log_to_console(f"Klawisz przynęty {key} został przypisany lokalnie")

        self.restore_all_global_hotkeys()

    def clear_placeholder1(self):
        if self.dowolny1_lineedit.text():
            self.dowolny1_lineedit.setPlaceholderText("")

    def clear_placeholder2(self):
        if self.dowolny1_lineedit_2.text():
            self.dowolny1_lineedit_2.setPlaceholderText("")

    def toggle_program_status(self):
        self.program_active = not self.program_active
        self.update_ui_for_program_status()
        self.status_frame.set_status(self.program_active)

    def update_ui_for_program_status(self):
        if self.program_active:
            self.aktywnienieaktywny_label_text = "Status programu: AKTYWNY"
            self.zatrzymaj_b4.setEnabled(True)
            self.uruchom_b3.setEnabled(False)
            self.log_to_console("Program został uruchomiony")

            # Kolor zależny od trybu
            if self.toggle_button.isChecked():  # Dark mode
                self.aktywnienieaktywny_label_color = "#00ff00"  # jasna zieleń
            else:  # Light mode
                self.aktywnienieaktywny_label_color = "green"  # standardowa zieleń
        else:
            self.aktywnienieaktywny_label_text = "Status programu: NIEAKTYWNY"
            self.zatrzymaj_b4.setEnabled(False)
            self.uruchom_b3.setEnabled(True)
            self.log_to_console("Program został zatrzymany")
            self.aktywnienieaktywny_label_color = "red"  # ZAWSZE czerwony

        self.aktywnienieaktywny_label3.setText(self.aktywnienieaktywny_label_text)
        self.aktywnienieaktywny_label3.setStyleSheet(f"color: {self.aktywnienieaktywny_label_color};")

    def keyPressEvent(self, event):
        key_code = event.key()
        if key_code in self.key_map:
            key_string = self.key_map[key_code]
        else:
            key_string = event.text().upper()
        if not self.current_listening_field and self.assigned_key and key_string == self.assigned_key.upper():
            if self.assigned_key.upper() in global_vk_map.values():
                return
            else:
                self.log_to_console(f"Naciśnięto przypisany klawisz: {key_string}")
                self.toggle_program_status()
                return
        super().keyPressEvent(event)

    def registerGlobalHotkey(self, hotkey_id, assigned_key):
        if sys.platform.startswith("win") and assigned_key:
            vk = global_vk_map.get(assigned_key.upper(), None)
            if vk is not None:
                ctypes.windll.user32.RegisterHotKey(int(self.winId()), hotkey_id, 0, vk)
                self.log_to_console(f"Hotkey {assigned_key} został zarejestrowany")

    def unregisterGlobalHotkey(self, hotkey_id, key):
        if sys.platform.startswith("win"):
            vk = global_vk_map.get(key.upper(), None)
            if vk is not None:
                ctypes.windll.user32.UnregisterHotKey(int(self.winId()), hotkey_id)
                self.log_to_console(f"Hotkey {key} został odłączony") #to mozna wywalic w sumie albo przebudowac cala logike hotkeyi w wolnej chwili

    def handleGlobalHotkey(self, hotkey_id):
        now = datetime.datetime.now()
        if not hasattr(self, "last_hotkey_time"):
            self.last_hotkey_time = {}
        if hotkey_id in self.last_hotkey_time:
            delta_ms = (now - self.last_hotkey_time[hotkey_id]).total_seconds() * 1000
            if delta_ms < 200:
                return
        self.last_hotkey_time[hotkey_id] = now

        if hotkey_id == 1:
            self.log_to_console("Globalny hotkey (funkcja uruchamiania) naciśnięty!")
            self.toggle_program_status()
        elif hotkey_id == 2:
            self.log_to_console("Globalny hotkey (funkcja przynęty) naciśnięty!")

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            if self.isMinimized():
                self.status_frame.show()  # Pokazujemy małe okienko
            else:
                self.status_frame.hide()  # Ukrywamy małe okienko
        super().changeEvent(event)  # Przekazujemy zdarzenie dalej

    def closeEvent(self, event):
        # Upewniamy się, że zamknięcie głównego okna zamyka całą aplikację
        QApplication.instance().quit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray nie jest dostępny!")
        sys.exit(1)

    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())