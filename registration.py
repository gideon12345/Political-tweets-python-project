import sys
import sqlite3
import random
import string
import hashlib
import dbconn
import Login
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Registration")
        self.resize(500, 300)

        self.layout = QVBoxLayout()

        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()
        self.first_name_input.setObjectName("input")

        self.last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()
        self.last_name_input.setObjectName("input")

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setObjectName("input")

        self.register_button = QPushButton("Register")
        self.register_button.setObjectName("register_button")
        self.register_button.clicked.connect(self.register_user)

        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("login_button")
        self.login_button.clicked.connect(self.login_user)

        self.layout.addWidget(self.first_name_label)
        self.layout.addWidget(self.first_name_input)
        self.layout.addWidget(self.last_name_label)
        self.layout.addWidget(self.last_name_input)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.login_button)
        self.layout.addStretch(1)

        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                margin-bottom: 5px;
            }

            QLineEdit, QPushButton {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            #input {
                background-color: #f9f9f9;
            }

            QPushButton#register_button {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }

            QPushButton#register_button:hover {
                background-color: #45a049;
            }
                           
            QPushButton#login_button {
                background-color: blue;
                color: white;
                border: none;
                border-radius: 5px;
            }

            QPushButton#login_button:hover {
                background-color: blue;
            }
        """)

        self.setLayout(self.layout)

    def login_user(self):
        self.close()
        self.login_user=Login.LoginWindow()
        self.login_user.show()


    def register_user(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()

        # Generate a random password (for demonstration purposes only)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        print(password)

        # Save user data to SQLite database
        connection = dbconn.connect_to_database()
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), password VARCHAR(255), date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

        # Insert user data into the table
        cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, hashed_password))
        #insert into the pgen
        cursor.execute("INSERT INTO pgen (username, password) VALUES (%s, %s)", (email,password))
        # Commit changes and close connection
        connection.commit()
        connection.close()

        #Clos the window 
        self.close()
        self.registration_window =RegistrationWindow()
        self.registration_window.show()

        print("User Data Saved to Database:")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Email: {email}")
        print(f"Password: {password}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())
