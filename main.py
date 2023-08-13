import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}




class Event:
    def scrape(self, url):
        """Get the source code from the URL"""
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        """only take the event name from the source code"""
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        """send email"""
        host = "smtp.gmail.com"
        port = 465

        username = "jac4code@gmail.com"
        password = "lwjziqvjkpfhhkem"

        receiver = "jac4code@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)


class Database:

    """
    What is init?
    Init is a special method, this method is executed when you
    create an instance of the class
    eg. when you run
    database = Database(database_path="data.db")
    this method is called on the background

    What is self?
    Self is a variable that hold the instance inside the class
    ed. self.connection
    means that you are pointing to the connection inside the class
    """
    def __init__(self, database_path):
        """Established connection to the database, by making a connection object"""
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted):
        """get the event and stores in the database"""
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        """return the existing data in data DB and return the rows"""
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",(band, city, date))
        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    while True:
        """create an event instance by call ing that class"""
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database(database_path="data.db")
            row = database.read(extracted)
            if not row:
                email = Email()
                database.store(extracted)
                email.send(message="Hey,new event was found!")
        time.sleep(2)


