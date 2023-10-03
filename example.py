from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton

import sys
from datetime import date, datetime


class AgeCalculator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        # create widget
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        birth_date_label = QLabel("Date of birth MM/DD/YYYY:")
        self.birth_date_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # add widget to the grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(birth_date_label, 1, 0)
        grid.addWidget(self.birth_date_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        current_year = date.today().year
        date_of_birth = self.birth_date_line_edit.text()
        year_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y")
        year_of_birth = year_of_birth.date().year
        age = current_year - year_of_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old.")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
app.exit(app.exec())
