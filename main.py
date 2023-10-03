from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

class database:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # create toolbar and add element to the toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create status bar and add elements to the status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detect cell clicked
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
        connection = database().connect()
        result = connection.execute("select * from students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("about")
        content = """
        This app was created during the course "The Python Megha Course".
        Feel free to modify it and reuse this app.
        """
        self.setText(content)



class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Detail")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # get student name from selected area
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # get student id from the selected area
        self.student_id = main_window.table.item(index, 0).text()

        # add student name widget area
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText(student_name)
        layout.addWidget(self.student_name)

        # get course name of selected student
        course_name = main_window.table.item(index, 2).text()

        # add course select widget area
        self.course_name = QComboBox()
        course = ["Bca", "Bba", "Mca"]
        self.course_name.addItems(course)
        # assign to the edit dialog box (only the first below line)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # get mobile number of the selected student
        mobile = main_window.table.item(index, 3).text()

        # add student mobile widget area
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText(mobile)
        layout.addWidget(self.mobile)

        button = QPushButton("Update")
        layout.addWidget(button)
        button.clicked.connect(self.update_record)

        self.setLayout(layout)

    def update_record(self):
        connection = database().connect()
        cursor = connection.cursor()
        cursor.execute("update students set name = ?, course = ?, mobile = ?, where id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        # refresh the data
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Detail")

        layout = QGridLayout()

        # creating sms and the buttons
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        # add widget to the area
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        # get index and id from the selected row

        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = database().connect()
        cursor = connection.cursor()
        cursor.execute("delete from students where id = ?", (student_id, ))

        connection.commit()
        cursor.close()
        connection.close()

        # refresh the data
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Detail")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        course = ["Bca", "Bba", "Mca"]
        self.course_name.addItems(course)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        layout.addWidget(button)
        button.clicked.connect(self.add_student)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = database().connect()
        cursor = connection.cursor()
        cursor.execute("insert into students (name, course, mobile) values(?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search for student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText("Name")
        layout.addWidget(self.name_line_edit)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.name_line_edit.text()
        connection = database().connect()
        cursor = connection.cursor()
        result = cursor.execute("select * from students where name=?", (name,))
        row = list(result)[0]
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
app.exit(app.exec())
