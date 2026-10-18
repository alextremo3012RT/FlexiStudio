"""Identidad visual Flexi / Red Graphite, sin imágenes externas ni archivos de fuente."""
COLOR_ROJO = '#F00432'
COLOR_ROJO_CLARO = '#FF687A'
COLOR_FONDO = '#0E0F11'
COLOR_PANEL = '#18191C'
COLOR_LINEA = '#303135'
COLOR_TEXTO = '#F5F5F6'
COLOR_MUTED = '#999BA2'

ESTILO = r'''
* { font-family: 'Segoe UI', 'Inter', 'Arial'; font-size: 12px; color: #E9E9EB; }
QMainWindow, QDialog, QWidget#appBackground { background-color: #0E0F11; }
QWidget#sideBar { background-color: #151518; border-right: 1px solid #292A2E; }
QWidget#topBar { background-color: #111114; border-bottom: 1px solid #2A2B2E; }
QWidget#centralPanel { background-color: #0E0F11; }
QWidget#loginLeft { background-color: #19191C; border-right: 1px solid #343438; }
QWidget#loginRight { background-color: #0E0F11; }
QLabel#logo { color: #F00432; font-size: 44px; font-weight: 900; letter-spacing: -2px; }
QLabel#logoSmall { color: #F00432; font-size: 28px; font-weight: 900; }
QLabel#brandTitle { color: #F6F6F7; font-size: 35px; font-weight: 800; }
QLabel#pageTitle { color: #F5F5F7; font-size: 28px; font-weight: 800; }
QLabel#sectionTitle { color: #F5F5F7; font-size: 17px; font-weight: 700; }
QLabel#caption { color: #8D8F96; font-size: 11px; }
QLabel#muted { color: #A0A1A7; font-size: 12px; }
QLabel#sectionLabel { color: #FF687A; font-size: 11px; font-weight: 800; letter-spacing: 1px; }
QLabel#kpi { color: #F8F8F8; font-size: 35px; font-weight: 800; }
QLabel#kpiLabel { color: #A2A2A7; font-size: 12px; font-weight: 600; }
QFrame#surface, QWidget#surface, QWidget#kpiCard { background-color: #1A1A1E; border: 1px solid #343438; border-radius: 14px; }
QFrame#redSurface { background: #330E17; border: 1px solid #852037; border-radius: 14px; }
QLabel#pill { background: #37131B; border: 1px solid #712033; padding: 5px 11px; border-radius: 9px; color: #FF7387; font-weight: 700; }
QPushButton { background: #29292E; border: 1px solid #43434A; padding: 10px 17px; border-radius: 9px; color: #F4F4F6; font-weight: 650; }
QPushButton:hover { background: #38383F; border-color: #6B6B73; }
QPushButton:pressed { background: #19191C; }
QPushButton:disabled { color: #6C6C72; background: #202024; border-color: #303036; }
QPushButton#primary { background: #E6002B; border: 1px solid #E6002B; color: white; font-weight: 800; }
QPushButton#primary:hover { background: #FF1744; }
QPushButton#danger { background: #46121E; border-color: #9C1D39; color: #FF8293; }
QPushButton#danger:hover { background: #691B2D; }
QPushButton#nav { text-align: left; background: transparent; border: 1px solid transparent; border-radius: 10px; padding: 13px 15px; color: #A6A6AC; font-size: 13px; }
QPushButton#nav:hover { background: #27272C; color: white; }
QPushButton#nav:checked { background: #36121C; color: #FF6680; border-left: 3px solid #EF0032; border-top: 1px solid #501C29; border-right: 1px solid #501C29; border-bottom: 1px solid #501C29; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QPlainTextEdit { background: #202024; color: #F5F5F5; border: 1px solid #4A4A51; border-radius: 8px; padding: 9px 11px; selection-background-color: #B5002B; min-height: 20px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus { border: 1px solid #FF4966; }
QLineEdit::placeholder { color: #74757C; }
QComboBox QAbstractItemView { background: #252529; color: white; selection-background-color: #831A32; border: 1px solid #414149; padding: 6px; }
QCheckBox { spacing: 9px; }
QCheckBox::indicator { width: 18px; height: 18px; }
QTableView { background-color: #19191D; alternate-background-color: #212125; border: 1px solid #34343A; border-radius: 10px; gridline-color: #303036; selection-background-color: #6E1C31; selection-color: white; }
QTableView::item { padding: 7px; border: none; }
QHeaderView::section { color: #B9BAC1; background: #28282E; padding: 11px 10px; border: none; border-right: 1px solid #34343A; font-weight: bold; }
QTableCornerButton::section { background: #28282E; border: none; }
QScrollBar:vertical { background: #18181B; width: 10px; margin: 1px; }
QScrollBar::handle:vertical { background: #505056; border-radius: 4px; min-height: 25px; }
QScrollBar:horizontal { background: #18181B; height: 10px; }
QScrollBar::handle:horizontal { background: #505056; border-radius: 4px; min-width: 25px; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0px; height: 0px; }
QTreeWidget { background: #1B1B1F; border: 1px solid #3A3A40; border-radius: 9px; alternate-background-color: #25252B; }
QTreeWidget::item { padding: 8px; }
QTreeWidget::item:selected { background: #63172E; }
QDialog { background: #151518; }
QMessageBox { background: #17171B; }
QToolTip { background: #28282D; color: white; border: 1px solid #4D4D54; padding: 8px; }
QStatusBar { background: #17171A; color: #A1A1A7; border-top: 1px solid #333337; }
'''
