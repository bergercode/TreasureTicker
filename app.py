import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPalette

class EarningsCounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.incomes = []  # List to store income sources with their names, frequencies, and amounts
        self.total_earnings = 0.0
        self.decimal_places = 2  # Default decimal places

        # Set up the GUI elements
        self.setWindowTitle("Multi-Source Earnings Tracker")
        self.setGeometry(100, 100, 500, 600)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        # Set color theme
        self.set_color_theme()

        # Title and Instruction Label
        self.instructions_label = QLabel("Enter an income name, amount, and select frequency:")
        self.instructions_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")

        # Input fields for income name and amount, and frequency selection
        self.income_name_input = QLineEdit()
        self.income_name_input.setPlaceholderText("Income name (e.g., Salary)")
        
        self.income_amount_input = QLineEdit()
        self.income_amount_input.setPlaceholderText("Income amount (e.g., 500)")

        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["Hourly", "Weekly", "Fortnightly", "Monthly", "Yearly"])

        # Buttons
        self.add_income_button = QPushButton("Add Income")
        self.start_button = QPushButton("Start Counter")
        self.reset_button = QPushButton("Reset Counter")
        
        self.earnings_label = QLabel("Total Earnings: $0.00")
        self.earnings_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Decimal places selection
        self.decimal_combo = QComboBox()
        self.decimal_combo.addItems([str(i) for i in range(0, 10)])  # Options from 0 to 9 decimal places
        self.decimal_combo.setCurrentIndex(2)  # Default to 2 decimal places
        self.decimal_combo.currentIndexChanged.connect(self.update_decimal_places)

        # Income list widget
        self.income_list_widget = QListWidget()
        self.remove_income_button = QPushButton("Remove Selected Income")

        # Projected earnings table with styled row headers
        self.earnings_table = QTableWidget(5, 1)  # Only 1 column for Projected Earnings
        self.earnings_table.setHorizontalHeaderLabels(["Projected Earnings"])
        self.earnings_table.setVerticalHeaderLabels(["Per Hour", "Per Week", "Per Fortnight", "Per Month", "Per Year"])
        self.earnings_table.horizontalHeader().setStretchLastSection(True)
        self.earnings_table.verticalHeader().setVisible(True)
        self.earnings_table.verticalHeader().setStyleSheet("font-weight: bold; color: #4a90e2; font-size: 12px;")  # Style row headers

        # Projected Earnings Label
        self.projected_earnings_label = QLabel("Projected Earnings:")
        self.projected_earnings_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #4a90e2; margin-top: 15px;")

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.instructions_label)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.income_name_input)
        input_layout.addWidget(self.income_amount_input)
        input_layout.addWidget(self.frequency_combo)
        layout.addLayout(input_layout)

        layout.addWidget(QLabel("Select Decimal Places for Display:"))
        layout.addWidget(self.decimal_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_income_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.income_list_widget)
        layout.addWidget(self.remove_income_button)
        layout.addWidget(self.earnings_label)
        
        # Add the styled "Projected Earnings" label and the table
        layout.addWidget(self.projected_earnings_label)
        layout.addWidget(self.earnings_table)

        self.setLayout(layout)

        # Connect buttons
        self.add_income_button.clicked.connect(self.add_income)
        self.remove_income_button.clicked.connect(self.remove_selected_income)
        self.start_button.clicked.connect(self.start_counter)
        self.reset_button.clicked.connect(self.reset_counter)

        # Style buttons for visibility
        button_style = "background-color: #4a90e2; color: #ffffff; font-weight: bold; padding: 6px; border-radius: 4px;"
        self.add_income_button.setStyleSheet(button_style)
        self.start_button.setStyleSheet(button_style)
        self.reset_button.setStyleSheet(button_style)
        self.remove_income_button.setStyleSheet(button_style)

        # Timer for updating earnings
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_earnings)

    def set_color_theme(self):
        """Apply a professional color theme to the application."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f0f0f5"))
        palette.setColor(QPalette.WindowText, QColor("#2f2f2f"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#e1e1e1"))
        palette.setColor(QPalette.ToolTipBase, QColor("#f0f0f5"))
        palette.setColor(QPalette.ToolTipText, QColor("#2f2f2f"))
        palette.setColor(QPalette.Text, QColor("#2f2f2f"))
        palette.setColor(QPalette.Button, QColor("#4a90e2"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.Highlight, QColor("#4a90e2"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)

    def update_decimal_places(self):
        """Update the number of decimal places displayed."""
        self.decimal_places = int(self.decimal_combo.currentText())
        self.update_earnings_table()

    def add_income(self):
        """Add an income source with a specified name and frequency."""
        try:
            name = self.income_name_input.text().strip()
            amount = float(self.income_amount_input.text())
            frequency = self.frequency_combo.currentText()

            if not name:
                self.earnings_label.setText("Please enter an income name.")
                return

            income_data = (name, amount, frequency)
            self.incomes.append(income_data)

            # Display income in QListWidget with name, amount, and frequency
            list_item_text = f"{name}: ${amount:.2f} ({frequency})"
            list_item = QListWidgetItem(list_item_text)
            list_item.setData(Qt.UserRole, income_data)
            self.income_list_widget.addItem(list_item)

            # Clear input fields
            self.income_name_input.clear()
            self.income_amount_input.clear()
            self.earnings_label.setText("Income added.")
            self.update_earnings_table()

        except ValueError:
            self.earnings_label.setText("Please enter a valid income amount.")

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
        self.earnings_label.setText(f"Total Earnings: ${self.total_earnings:.{self.decimal_places}f}")
        self.timer.stop()

    def update_earnings(self):
        """Update total earnings based on all income sources and their frequencies."""
        increment = 0.0
        for name, amount, frequency in self.incomes:
            if frequency == "Hourly":
                increment += amount / 3600
            elif frequency == "Weekly":
                increment += amount / (7 * 24 * 3600)
            elif frequency == "Fortnightly":
                increment += amount / (14 * 24 * 3600)
            elif frequency == "Monthly":
                increment += amount / (30 * 24 * 3600)
            elif frequency == "Yearly":
                increment += amount / (365 * 24 * 3600)

        self.total_earnings += increment
        self.earnings_label.setText(f"Total Earnings: ${self.total_earnings:.{self.decimal_places}f}")

    def update_earnings_table(self):
        """Update projected earnings in the table based on income sources."""
        total_hourly = sum(amount if frequency == "Hourly" else
                           amount / (7 * 24) if frequency == "Weekly" else
                           amount / (14 * 24) if frequency == "Fortnightly" else
                           amount / (30 * 24) if frequency == "Monthly" else
                           amount / (365 * 24) for name, amount, frequency in self.incomes)

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
