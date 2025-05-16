custom_styles_dark = """ 
* {
  padding: 0px;
  margin: 0px;
  border: 0px;
  border-style: none;
  border-image: none;
  outline: 0;
}

/* specific reset for elements inside QToolBar */
QToolBar * {
  margin: 0px;
  padding: 0px;
}

QWidget {
  background-color: #19232D;
  border: 0px solid #455364;
  padding: 0px;
  color: #DFE1E2;
  selection-background-color: #346792;
  selection-color: #DFE1E2;
}

 QTabWidget::tab-bar {
  left: 5px; /* Przesuń pasek zakładek o 5 pikseli w prawo */
}

 QStatusBar { /* pasek na samym dole */
  border: 1px solid #455364;
  background: #455364;
}

 QMenuBar {
  background-color: #455364; /* pasek ktora oddzielnai od tego pierwszego an duze*/
  padding: 0px;
  border: 0px solid #19232D;
  padding-top: 1px solid #19232D;
}

 QAbstractScrollArea {
  background-color: #19232D; /* no u mnie to konsola do scrolowania - wypelnienie*/
  border: 1px solid #19232D; /* border*/
  border-radius: 4px;
  /* fix #159 */
  padding: 2px;
  /* remove min-height to fix #244 */
  color: #A37E7F; /* kolor napisowe*/
}

 QScrollBar:vertical {
  background-color: #19232D;    /* pasek konsoli pionowy do scrolowania dol gora*/
  width: 16px;
  margin: 16px 2px 16px 2px;
  border: 1px solid #455364;
  border-radius: 4px;
}

 QScrollBar::handle:vertical {
  background-color: #455364; /* pasek konsoli pionowy do scrolowania dol gora suwak*/
  border: 1px solid #455364;
  min-height: 8px;
  border-radius: 4px;
}

 QScrollBar::handle:vertical:hover {
  background-color: #346792;
  border: #346792;
  border-radius: 4px;
  min-height: 8px;
}

 QScrollBar::handle:vertical:focus {
  border: 1px solid #1A72BB;
}

QScrollBar::add-line:vertical {
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/dark/rc/arrow_down_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/dark/rc/arrow_up_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:on {
  border-image: url(":/qss_icons/dark/rc/arrow_up.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
  border-image: url(":/qss_icons/dark/rc/arrow_down.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

 QTextEdit { /* dalej ta kansola*/
  background-color: #19232D;
  color: #DFE1E2;
  border-radius: 4px;
  border: 1px solid #455364;
}

 QTextEdit:focus {
  border: 1px solid #1A72BB;
}

 QTextEdit:selected {
  background: #346792;
  color: #455364;
}

 QPushButton {
  background-color: #455364;
  color: #DFE1E2;
  border-radius: 4px;
  padding: 2px;
  outline: none;
  border: none;
}

 QPushButton:disabled {
  background-color: #455364;
  color: #788D9C;
  border-radius: 4px;
  padding: 2px;
}

 QPushButton:checked {
  background-color: #60798B;
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

 QPushButton:checked:disabled {
  background-color: #60798B;
  color: #788D9C;
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

 QPushButton:checked:selected {
  background: #60798B;
}

 QPushButton:hover {
  background-color: #54687A;
  color: #DFE1E2;
}

 QPushButton:pressed {
  background-color: #60798B;
}

 QPushButton:selected {
  background: #60798B;
  color: #DFE1E2;
}

 QPushButton::menu-indicator {
  subcontrol-origin: padding;
  subcontrol-position: bottom right;
  bottom: 4px;
}

 QLineEdit {
  background-color: #19232D;
  padding-top: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-bottom: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-left: 4px;
  padding-right: 4px;
  border-style: solid;
  border: 1px solid #455364;
  border-radius: 4px;
  color: #DFE1E2;
}

 QLineEdit:disabled {
  background-color: #19232D;
  color: #788D9C;
}

 QLineEdit:hover {
  border: 1px solid #346792;
  color: #DFE1E2;
}

 :focus {
  border: 1px solid #1A72BB;
}

 QLineEdit:selected {
  background-color: #346792;
  color: #455364;
}

 QTabWidget QWidget {
  /* Fixes #189 */
  border-radius: 4px;
}

 QTabWidget::pane {
  border: 1px solid #455364;
  border-radius: 4px;
  margin: 0px;
  /* Fixes double border inside pane with pyqt5 */
  padding: 0px;
}

 QTabBar::tab:top, QDockWidget QTabBar::tab:top {
  background-color: #455364; 
  margin-left: 2px;
  padding-left: 4px;
  padding-right: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
  min-width: 50px;
  min-height: 15px;
  border-bottom: 3px solid #455364;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

 QTabBar::tab:top:selected, QDockWidget QTabBar::tab:top:selected {
  background-color: #54687A; /* background po najkechaniu */
  border-bottom: 3px solid #259AE9;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

 QTabBar::tab:top:!selected:hover, QDockWidget QTabBar::tab:top:!selected:hover {
  border: 1px solid #1A72BB;   /* obramowanie zakladki chwile te po najechaniu kursorem */
  border-bottom: 3px solid #1A72BB;
  /* Fixes spyder-ide/spyder#9766 and #243 */
  padding-left: 3px;
  padding-right: 3px;
}

 QTabBar::tab:top:selected:disabled, QDockWidget QTabBar::tab:top:selected:disabled {
  border-bottom: 3px solid #455364;
  color: #788D9C;
  background-color: #455364;
}

 QTabBar::tab:top:!selected:disabled, QDockWidget QTabBar::tab:top:!selected:disabled {
  border-bottom: 3px solid #455364;
  color: #788D9C;
  background-color: #19232D;
}

 QTabBar::tab:top:!selected, QDockWidget QTabBar::tab:top:!selected {
  border-bottom: 2px solid #19232D; /* ta kreska jakby podswietlenie niewybranej zakladki */
  margin-top: 2px;
}

 QTabBar::tab:top:selected:disabled, QDockWidget QTabBar::tab:top:selected:disabled {
  border-bottom: 3px solid #455364;
  color: #788D9C;
  background-color: #455364;
}

QLabel {
  background-color: #19232D;
  border: 0px solid #455364;
  padding: 2px;
  margin: 0px;
  color: #DFE1E2;
}

QLabel:disabled {
  background-color: #19232D;
  border: 0px solid #455364;
  color: #788D9C;
}

QSizeGrip {
  background: transparent;
  width: 12px;
  height: 12px;
  image: url(":/qss_icons/dark/rc/window_grip.png");
}

/* content w rozwijanym menu w qframe */
QMenu::item {
  padding: 5px 10px;
  color: white;
  font-size: 10px;
  font-weight: bold;
  margin: 0px;
  border: 1px solid #666;
  border-radius: 5px;
  background-color: #18232C;
            }
/* content w rozwijanym menu w qframe po najechaniu myszką */
QMenu::item:selected {
  background-color: #1B73BB;
  color: white;
  font-weight: bold;             
  border: 1px solid #666;
  border-radius: 5px;
            }
            
"""

def get_customstyles_dark():
    return custom_styles_dark

################################################################################################################################################

custom_styles_light = """ 

* {
  padding: 0px;
  margin: 0px;
  border: 0px;
  border-style: none;
  border-image: none;
  outline: 0;
}

/* specific reset for elements inside QToolBar */
QToolBar * {
  margin: 0px;
  padding: 0px;
}

QWidget { /* UWAGA NA DZIEDZICZENIE I SELEKTORY CSS */
  background-color: #F0F0F0;
  border: 0px solid #455364;
  padding: 0px;
  color: #DFE1E2;
  selection-background-color: #346792;
  selection-color: #DFE1E2;
}

 QTabWidget QWidget { /* UWAGA NA DZIEDZICZENIE I SELEKTORY CSS */
  /* Fixes #189 */
  border-radius: 4px;
  background-color: transparent;
}

 QTabWidget::pane { /*  POZOSTALE TLO CALEJ ZAKLADKI */
  border-radius: 4px;
  border: 1px solid #E6E6E6;
  border-bottom: 1px solid #828283;
  margin: 0px;
  padding: 0px;
  background-color: #F9F8F8;
}

QWidget::item:selected {
  background-color: #D1D1D0;
}

 QTabWidget::tab-bar {
  left: 5px; /* Przesuń pasek zakładek o 5 pikseli w prawo */
}

 QTabBar::tab {
  font-weight: normal;
  color: #000000;
}

 QStatusBar { /* pasek na samym dole pasek dolny*/
  border: 1px solid #EBEAEB;
  background: #EBEAEB;
}

 QMenuBar {
  background-color: #f9f8f8; /* pasek ktora oddziela od tego pierwszego an duze*/
  padding: 0px;
  border: 0px solid #19232D;
  padding-top: 1px solid #19232D;
}

 QAbstractScrollArea {
  background-color: #F30E0E; /* no u mnie to changelog - wypelnienie*/
  border: 1px solid #D1D1D0; /* border*/
  border-radius: 4px;
  /* fix #159 */
  padding: 2px;
  /* remove min-height to fix #244 */
  color: #000000; /* kolor napisowe*/
}

 QScrollBar:vertical {
  background-color: #F9F8F8;    /* pasek konsoli pionowy do scrolowania dol gora a raczej jego tlo*/
  width: 16px;
  margin: 16px 2px 16px 2px;
  border: 1px solid #455364;
  border-radius: 4px;
}

 QScrollBar::handle:vertical {
  background-color: #BFDDF7; /* pasek konsoli pionowy do scrolowania dol gora suwak*/
  border: 1px solid #BFDDF7; 
  min-height: 8px;
  border-radius: 4px;
}

 QScrollBar::handle:vertical:hover {
  background-color: #75CFF7; /* jak najade kursorem na suwak to zmienia koloru*/
  border: #346792;
  border-radius: 4px;
  min-height: 8px;
}

 QScrollBar::handle:vertical:focus {
  border: 1px solid #1A72BB;
}

QScrollBar::add-line:vertical { /* Strzałka do scrolowania dół */
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/dark/rc/arrow_down_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical { /* Strzałka do scrolowania góra */
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/dark/rc/arrow_up_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:on { /* Strzałka do scrolowania po najechaniu kursorem góra */
  border-image: url(":/qss_icons/dark/rc/arrow_up_focus.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on { /* Strzałka do scrolowania po najechaniu kursorem dół */
  border-image: url(":/qss_icons/dark/rc/arrow_down_focus.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

 QTextEdit { /* dalej ta konsola*/
  background-color: #FEFEFF;
  color: #000000;
  border-radius: 4px;
  border: 1px solid #E6E6E6;
  border-bottom: 1px solid #828283;
}

 QTextEdit:focus {
  border: 1px solid #1A72BB;
}

 QTextEdit:selected {
  background: #346792;
  color: #455364;
}

 QPushButton {
  background-color: #f9f8f8;
  color: #000000;
  border: 1px solid #D1D1D0;
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

 QPushButton:disabled {
  background-color: #f9f8f8;
  color: #787979;
  border: 1px solid #E9E9E9;
  border-radius: 4px;
  padding: 2px;
}

 QPushButton:checked {
  background-color: #60798B;
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

 QPushButton:checked:disabled {
  background-color: #60798B;
  color: #788D9C;
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

 QPushButton:checked:selected {
  background: #60798B;
}

 QPushButton:hover {
  background-color: #E0EEF9;
  border: 1px solid #0079D5;
  border-radius: 4px;
  color: #000000
}

 QPushButton:pressed {
  background-color: #CCE5F6;
}

 QPushButton:selected {
  background: #60798B;
  color: #DFE1E2;
}

 QPushButton::menu-indicator {
  subcontrol-origin: padding;
  subcontrol-position: bottom right;
  bottom: 4px;
}

 QLineEdit {
  background-color: #19232D;
  padding-top: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-bottom: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-left: 4px;
  padding-right: 4px;
  border-style: solid;
  border: 1px solid #455364;
  border-radius: 4px;
  color: #000000;
}

 QLineEdit:disabled {
  background-color: #19232D;
  color: #lightgrey;
}

 QLineEdit:hover {
  border: 1px solid #346792;
  color: #DFE1E2;
}

/* :focus {
  border: 1px solid #B5416B;
} */

 QLineEdit:selected {
  background-color: #346792;
  color: #455364;
}

 QTabBar::tab:top, QDockWidget QTabBar::tab:top {
  background-color: #F3F2F3; /* --> TŁO ZAKLADKI KTORA AKTUALNIE NIE JEST WYBRANA */
  margin-left: 2px;
  padding-left: 4px;
  padding-right: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
  min-width: 50px;
  min-height: 15px;
  border: 1px solid #E4E4E5;
  border-bottom: 3px solid #455364;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

 QTabBar::tab:top:!selected, QDockWidget QTabBar::tab:top:!selected {
  border-bottom: 2px solid #F9F8F8; /* ta kreska jakby podswietlenie nmiewybranejk zakladki */
  margin-top: 2px;
}

 QTabBar::tab:top:selected, QDockWidget QTabBar::tab:top:selected {
  background-color: #DEEDF8; /*  TŁO ZAKLADKI KTORA AKTUALNIE JEST WYBRANA */
  border-bottom: 3px solid #259AE9;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

 QTabBar::tab:top:!selected:hover, QDockWidget QTabBar::tab:top:!selected:hover {
  border: 1px solid #1A72BB;   /* obramowanie zakladki chwile te po najechaniu kursorem */
  border-bottom: 3px solid #1A72BB;
  /* Fixes spyder-ide/spyder#9766 and #243 */
  padding-left: 3px;
  padding-right: 3px;
}

 QTabBar::tab:top:selected:disabled, QDockWidget QTabBar::tab:top:selected:disabled {
  border-bottom: 3px solid #455364;
  color: #788D9C;
  background-color: #455364;
}

 QTabBar::tab:top:!selected:disabled, QDockWidget QTabBar::tab:top:!selected:disabled {
  border-bottom: 3px solid #455364;
  color: #788D9C;
  background-color: #19232D;
}

 QTabBar::tab:top:selected:disabled, QDockWidget QTabBar::tab:top:selected:disabled {
  border-bottom: 3px solid #455364;
  color: #788D9C;
  background-color: #455364;
}

QLabel {
  padding: 2px;
  margin: 0px;
  color: #000000;
}

QLabel:disabled {
  color: #788D9C;
}

QSizeGrip {
  background: transparent;
  width: 12px;
  height: 12px;
  image: url(":/qss_icons/dark/rc/window_grip_disabled.png");
}

QMenu::item {
  padding: 5px 10px;
  color: black;
  font-size: 10px;
  font-weight: bold;
  margin: 0px;
  border: 1px solid #858A8F;
  border-radius: 5px;
  background-color: #F0F1F1;
            }

QMenu::item:selected {
  background-color: #BFDCF6;
  color: black;
  font-weight: bold;             
  border: 1px solid #858A8F;
  border-radius: 5px;
            }

"""

def get_customstyles_light():
    return custom_styles_light

