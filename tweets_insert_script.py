import csv
import mysql.connector

def read_csv(filename, encoding='utf-8'):
    data = []
    with open(filename, 'r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def save_to_mysql(data, host, user, password, database, table):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        for row in data:
            columns = ', '.join(row.keys())
            values = ', '.join(['%s'] * len(row))
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(query, list(row.values()))

        connection.commit()
        print("Data inserted successfully!")

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    filename = 'kenya_political_tweets.csv'
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'kenyan_tweets'
    table = 'tweets'

    data = read_csv(filename)
    save_to_mysql(data, host, user, password, database, table)
