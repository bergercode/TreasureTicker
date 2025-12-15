import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, 
                             QComboBox, QHBoxLayout, QListWidget, QListWidgetItem, QTableWidget, 
                             QTableWidgetItem, QFrame, QHeaderView, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QIcon
import styles

class EarningsCounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.incomes = []  # List to store income sources
        self.total_earnings = 0.0
        self.decimal_places = 2  # Default decimal places
        self.is_dark_mode = True # Default to Dark Mode

        self.setWindowTitle("Cashflow Tracker")
        self.setGeometry(100, 100, 600, 750)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        self.init_ui()
        self.apply_theme()

        # Timer for updating earnings
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_earnings)

    def init_ui(self):
        """Initialize the UI layout with QFrame groupings."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Header Section ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Cashflow Tracker")
        title_label.setObjectName("header")
        
        self.theme_toggle_btn = QPushButton("Light Mode")
        self.theme_toggle_btn.setFixedWidth(150)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_toggle_btn)
        main_layout.addLayout(header_layout)

        # --- Controls Section ---
        controls_frame = QFrame()
        controls_frame.setObjectName("controls_frame")
        controls_layout = QVBoxLayout()
        
        # Instructions
        self.instructions_label = QLabel("Add Income Stream")
        controls_layout.addWidget(self.instructions_label)
        
        # Inputs
        input_layout = QHBoxLayout()
        self.income_name_input = QLineEdit()
        self.income_name_input.setPlaceholderText("Name (e.g. Salary)")
        
        self.income_amount_input = QLineEdit()
        self.income_amount_input.setPlaceholderText("Amount")
        self.income_amount_input.setFixedWidth(100)

        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["Hourly", "Weekly", "Fortnightly", "Monthly", "Yearly"])
        
        input_layout.addWidget(self.income_name_input)
        input_layout.addWidget(self.income_amount_input)
        input_layout.addWidget(self.frequency_combo)
        controls_layout.addLayout(input_layout)

        # Decimal Selection
        decimal_layout = QHBoxLayout()
        decimal_label = QLabel("Decimals:")
        self.decimal_combo = QComboBox()
        self.decimal_combo.addItems([str(i) for i in range(0, 10)])
        self.decimal_combo.setCurrentIndex(2)
        self.decimal_combo.currentIndexChanged.connect(self.update_decimal_places)
        self.decimal_combo.setFixedWidth(60)
        
        decimal_layout.addWidget(decimal_label)
        decimal_layout.addWidget(self.decimal_combo)
        decimal_layout.addStretch()
        controls_layout.addLayout(decimal_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_income_button = QPushButton("Incoming (+)")
        self.add_income_button.clicked.connect(lambda: self.add_stream(is_outgoing=False))
        
        self.add_outgoing_button = QPushButton("Outgoing (-)")
        self.add_outgoing_button.setObjectName("outgoing")
        self.add_outgoing_button.clicked.connect(lambda: self.add_stream(is_outgoing=True))

        self.start_button = QPushButton("Start Counter")
        self.start_button.clicked.connect(self.start_counter)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("secondary") 
        self.reset_button.clicked.connect(self.reset_counter)
        
        button_layout.addWidget(self.add_income_button)
        button_layout.addWidget(self.add_outgoing_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)
        controls_layout.addLayout(button_layout)
        
        controls_frame.setLayout(controls_layout)
        main_layout.addWidget(controls_frame)

        # --- Dashboard Section ---
        dashboard_frame = QFrame()
        dashboard_layout = QVBoxLayout()

        # Hero Earnings Label
        self.earnings_label = QLabel("$0.00")
        self.earnings_label.setAlignment(Qt.AlignCenter)
        self.earnings_label.setObjectName("hero_label")
        dashboard_layout.addWidget(self.earnings_label)

        # Income List
        list_label = QLabel("Active Streams")
        dashboard_layout.addWidget(list_label)
        
        self.income_list_widget = QListWidget()
        dashboard_layout.addWidget(self.income_list_widget)

        self.remove_income_button = QPushButton("Remove Selected")
        self.remove_income_button.setObjectName("destructive")
        self.remove_income_button.clicked.connect(self.remove_selected_income)
        dashboard_layout.addWidget(self.remove_income_button)

        # Projected Table
        self.projected_earnings_label = QLabel("Projected Earnings")
        self.projected_earnings_label.setObjectName("projected_label") 
        dashboard_layout.addWidget(self.projected_earnings_label)

        self.earnings_table = QTableWidget(5, 1)
        self.earnings_table.setHorizontalHeaderLabels(["Amount"])
        self.earnings_table.setVerticalHeaderLabels(["Per Hour", "Per Week", "Per Fortnight", "Per Month", "Per Year"])
        self.earnings_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.earnings_table.verticalHeader().setVisible(True)
        self.earnings_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.earnings_table.setSelectionMode(QTableWidget.NoSelection)
        self.earnings_table.setFocusPolicy(Qt.NoFocus)
        self.earnings_table.setFixedHeight(180) # Fixed height for compactness
        
        dashboard_layout.addWidget(self.earnings_table)

        dashboard_frame.setLayout(dashboard_layout)
        main_layout.addWidget(dashboard_frame)

        self.setLayout(main_layout)

    def apply_theme(self):
        """Apply the selected theme stylesheet."""
        if self.is_dark_mode:
            self.setStyleSheet(styles.DARK_THEME)
            self.theme_toggle_btn.setText("Light Mode")
        else:
            self.setStyleSheet(styles.LIGHT_THEME)
            self.theme_toggle_btn.setText("Dark Mode")

    def toggle_theme(self):
        """Switch between light and dark mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def update_decimal_places(self):
        """Update the number of decimal places displayed."""
        self.decimal_places = int(self.decimal_combo.currentText())
        self.update_earnings_table()

    def add_stream(self, is_outgoing=False):
        """Add an income/outgoing source with a specified name and frequency."""
        try:
            name = self.income_name_input.text().strip()
            amount = float(self.income_amount_input.text())
            frequency = self.frequency_combo.currentText()

            if not name:
                self.earnings_label.setText("Please enter a name.")
                return

            income_data = (name, amount, frequency, is_outgoing)
            self.incomes.append(income_data)

            # Display in QListWidget
            prefix = "(-)" if is_outgoing else "(+)"
            # Slightly dim outgoing in list? relying on prefix for now
            list_item_text = f"{prefix} {name}: ${amount:.2f} ({frequency})"
            list_item = QListWidgetItem(list_item_text)
            
            if is_outgoing:
                list_item.setForeground(QColor("#ff9800")) # Orange text for outgoing

            list_item.setData(Qt.UserRole, income_data)
            self.income_list_widget.addItem(list_item)

            # Clear input fields
            self.income_name_input.clear()
            self.income_amount_input.clear()
            self.earnings_label.setText("Stream added.")
            self.update_earnings_table()

        except ValueError:
            self.earnings_label.setText("Please enter a valid amount.")

    def remove_selected_income(self):
        """Remove the selected income source from the list."""
        selected_item = self.income_list_widget.currentItem()
        if selected_item:
            income_data = selected_item.data(Qt.UserRole)
            self.incomes.remove(income_data)
            self.income_list_widget.takeItem(self.income_list_widget.row(selected_item))
            self.earnings_label.setText(f"Income '{income_data[0]}' removed.")
            self.update_earnings_table()

    def start_counter(self):
        """Start the timer to update earnings based on all income sources."""
        if self.incomes:
            self.total_earnings = 0.0  # Reset earnings
            self.timer.start(1000)  # Update every second
        else:
            self.earnings_label.setText("Please add an income source first.")

    def reset_counter(self):
        """Reset the counter to zero."""
        self.total_earnings = 0.0
        self.earnings_label.setText(f"${self.total_earnings:.{self.decimal_places}f}")
        self.timer.stop()

    def update_earnings(self):
        """Update total earnings based on all income/outgoing sources."""
        increment = 0.0
        for name, amount, frequency, is_outgoing in self.incomes:
            current_inc = 0.0
            if frequency == "Hourly":
                current_inc = amount / 3600
            elif frequency == "Weekly":
                current_inc = amount / (7 * 24 * 3600)
            elif frequency == "Fortnightly":
                current_inc = amount / (14 * 24 * 3600)
            elif frequency == "Monthly":
                current_inc = amount / (30 * 24 * 3600)
            elif frequency == "Yearly":
                current_inc = amount / (365 * 24 * 3600)
            
            if is_outgoing:
                increment -= current_inc
            else:
                increment += current_inc

        self.total_earnings += increment
        self.earnings_label.setText(f"${self.total_earnings:.{self.decimal_places}f}")

    def update_earnings_table(self):
        """Update projected earnings in the table."""
        total_hourly = 0.0
        for name, amount, frequency, is_outgoing in self.incomes:
            hourly_val = 0.0
            if frequency == "Hourly": hourly_val = amount
            elif frequency == "Weekly": hourly_val = amount / (7 * 24)
            elif frequency == "Fortnightly": hourly_val = amount / (14 * 24)
            elif frequency == "Monthly": hourly_val = amount / (30 * 24)
            elif frequency == "Yearly": hourly_val = amount / (365 * 24)
            
            if is_outgoing:
                total_hourly -= hourly_val
            else:
                total_hourly += hourly_val

        projections = [
            total_hourly,
            total_hourly * 7 * 24,
            total_hourly * 14 * 24,
            total_hourly * 30 * 24,
            total_hourly * 365 * 24
        ]

        for row, value in enumerate(projections):
            # Format each projected value to 2 decimal places
            formatted_value = f"${value:.2f}"
            self.earnings_table.setItem(row, 0, QTableWidgetItem(formatted_value))

def main():
    app = QApplication(sys.argv)
    window = EarningsCounterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
