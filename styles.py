
# Modern Dark Theme
DARK_THEME = """
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
}

/* Headings & Labels */
QLabel {
    color: #e0e0e0;
}
QLabel#header {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 10px;
}
QLabel#hero_label {
    font-size: 28px;
    font-weight: bold;
    color: #4caf50; /* Green accent for money */
    padding: 10px;
}
QLabel#projected_label {
    font-size: 16px;
    font-weight: bold;
    color: #64b5f6; /* Blue accent */
    margin-top: 15px;
}

/* Inputs */
QLineEdit, QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #3e3e3e;
    border-radius: 6px;
    padding: 8px;
    color: #ffffff;
    selection-background-color: #007acc;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #007acc;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}

/* Buttons */
QPushButton {
    background-color: #007acc;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #005f9e;
}
QPushButton:pressed {
    background-color: #004475;
}
QPushButton#secondary {
    background-color: #3e3e3e;
    color: #cccccc;
}
QPushButton#secondary:hover {
    background-color: #4e4e4e;
}
QPushButton#destructive {
    background-color: #d32f2f;
}
QPushButton#destructive:hover {
    background-color: #b71c1c;
}
QPushButton#outgoing {
    background-color: #ff9800;
    color: white;
}
QPushButton#outgoing:hover {
    background-color: #f57c00;
}

/* List & Table */
QListWidget, QTableWidget {
    background-color: #252526;
    border: 1px solid #3e3e3e;
    border-radius: 6px;
    gridline-color: #3e3e3e;
    alternate-background-color: #2d2d2d;
}
QHeaderView::section {
    background-color: #3e3e3e;
    color: #ffffff;
    padding: 5px;
    border: none;
    border-right: 1px solid #2d2d2d;
}
QTableWidget::item {
    padding: 5px;
}
/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #1e1e1e;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #424242;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# Modern Light Theme
LIGHT_THEME = """
QWidget {
    background-color: #f5f5f7;
    color: #333333;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 14px;
}

/* Headings & Labels */
QLabel {
    color: #333333;
}
QLabel#header {
    font-size: 18px;
    font-weight: bold;
    color: #000000;
    margin-bottom: 10px;
}
QLabel#hero_label {
    font-size: 28px;
    font-weight: bold;
    color: #2e7d32; /* Darker green for contrast */
    padding: 10px;
}
QLabel#projected_label {
    font-size: 16px;
    font-weight: bold;
    color: #1976d2; /* Darker blue */
    margin-top: 15px;
}

/* Inputs */
QLineEdit, QComboBox {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 8px;
    color: #333333;
    selection-background-color: #4a90e2;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #4a90e2;
}

/* Buttons */
QPushButton {
    background-color: #4a90e2;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #357abd;
}
QPushButton:pressed {
    background-color: #2a629c;
}
QPushButton#secondary {
    background-color: #e0e0e0;
    color: #333333;
}
QPushButton#secondary:hover {
    background-color: #d0d0d0;
}
QPushButton#destructive {
    background-color: #e53935;
}
QPushButton#destructive:hover {
    background-color: #d32f2f;
}
QPushButton#outgoing {
    background-color: #ff9800; /* Orange for outgoing */
    color: white;
}
QPushButton#outgoing:hover {
    background-color: #fb8c00;
}

/* List & Table */
QListWidget, QTableWidget {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    gridline-color: #e0e0e0;
    alternate-background-color: #f9f9f9;
}
QHeaderView::section {
    background-color: #e0e0e0;
    color: #333333;
    padding: 5px;
    border: none;
    border-right: 1px solid #d0d0d0;
}
QTableWidget::item {
    padding: 5px;
}
"""
