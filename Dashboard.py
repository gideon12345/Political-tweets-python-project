import numpy as np
import matplotlib.pyplot as plt
import dbconn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

class DashboardWindow(QWidget):
    def __init__(self, username,first_name,last_name):
        super().__init__()

        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 1000, 600)

        main_layout = QHBoxLayout()

        # Sidebar
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)  # Set spacing to 0
        sidebar_widget.setLayout(sidebar_layout)


        # Sidebar items
        sidebar_items = ["Dashboard", "Data Analyzed", "Reports"]
        for item in sidebar_items:
            item_label = QLabel(item)
            item_label.setStyleSheet("font-size: 16px; color: #555; padding: 10px 20px; border-bottom: 1px solid #ddd;")
            sidebar_layout.addWidget(item_label)

        # main_layout.addWidget(sidebar_widget)

        # Main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)

        welcome_label = QLabel(f"Welcome, {first_name+' '+last_name}!")
        welcome_label.setStyleSheet("font-size: 24px; color: #333; margin-bottom: 20px;")
        content_layout.addWidget(welcome_label)

        # Add graph
        graph_widget = QWidget()
        graph_layout = QVBoxLayout()
        graph_widget.setLayout(graph_layout)

        # x = np.linspace(0, 10, 100)
        # y = np.sin(x)
        # Assuming you have two lists of data: x_data and y_data

        #Get the candidates data 
        conn =dbconn.connect_to_database()
        cursor =conn.cursor()

        cursor.execute("SELECT word,count FROM analysis_details where analysis_id =1")

        analysis_data =cursor.fetchall()

        data_dict = {}

        #conn.commit()

        if analysis_data:
            for row in analysis_data:
                    word, count = row
                    data_dict[word] = count
                    analysis_data_list =dict(analysis_data)
                    keys =list(data_dict.keys())
                    values =list(data_dict.values())
                    print(data_dict)
                    y_data = values
                    x_data = keys
        else:
            y_data = [1, 0.2, 3, 1.4, 5]
            x_data = ["Ruto", "Isaac", "Raila", "kalonzo", "test"]


        
        
        # Replace x and y with your data
        cursor.close()
        conn.close()
        x = x_data
        y = y_data

        

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title("Kenyan Political Tweets Analysis graph")
        ax.set_xlabel("Presidential Candidates")
        ax.set_ylabel("Famous Scale")

        canvas = FigureCanvas(fig)
        graph_layout.addWidget(canvas)

        content_layout.addWidget(graph_widget)

        # Add pie chart
        pie_chart_widget = QWidget()
        pie_chart_layout = QVBoxLayout()
        pie_chart_widget.setLayout(pie_chart_layout)

        print("The labels of the pie chart",keys)

        total_sum = sum(values)
        # Calculate the percentage of each element relative to the total sum
        percentages = [(x / total_sum) * 100 for x in values]

        labels = keys
        sizes = percentages
        explode = (0.1,) * len(keys)

        #fig1, ax1 = plt.subplots()
        fig1, ax1 = plt.subplots(figsize=(10, 10))  # Adjust the size as needed
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title("Popular candidates Pie Chart")

        canvas = FigureCanvas(fig1)
        pie_chart_layout.addWidget(canvas)

        content_layout.addWidget(pie_chart_widget)

        main_layout.addWidget(content_widget)

        self.setLayout(main_layout)


