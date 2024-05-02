import sys
import mysql.connector
import dbconn
import hashlib
from sqlalchemy import create_engine
from Dashboard import DashboardWindow
import registration
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(600, 250, 500, 250)
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("font-size: 20px; color: #333333;")
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("font-size: 20px; padding: 10px; border: 2px solid #555555; border-radius: 5px; background-color: #eeeeee;")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("font-size: 20px; color: #333333;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("font-size: 20px; padding: 10px; border: 2px solid #555555; border-radius: 5px; background-color: #eeeeee;")
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("font-size: 20px; padding: 10px; background-color: blue; color: white; border: none; border-radius: 6px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        #add register button
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("font-size: 20px; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 6px;")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        self.close()
        self.register_window =registration.RegistrationWindow()
        self.register_window.show()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        password = hashlib.sha1(password.encode()).hexdigest()

        # conn = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="",
        #     database="kenyan_tweets"
        #     )
        conn =dbconn.connect_to_database()
        cursor =conn.cursor()
        #query = "SELECT * FROM users"
        #result =cursor.execute(query)

        # Secure way of executing the query using parameters to avoid SQL injection
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Fetch the first row, assuming usernames are unique
        user = cursor.fetchone()
        if user:
            users =list(user)
            print("This is user Data :",users)
            first_name =users[1]
            last_name =users[2]
            print(first_name)
            print(last_name)

        
    

        # Here you would typically check the username and password against a database or some other storage
        # For demonstration purposes, let's just use a hardcoded check
        if user:
            QMessageBox.information(self, "Login Successful", "Welcome, {}".format(first_name +"  "+ last_name))
            self.close()
            self.dashboard_window =DashboardWindow(username,first_name,last_name)
            self.dashboard_window.show()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
