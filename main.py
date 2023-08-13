import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

"""Established connection to the database"""
connection = sqlite3.connect("data.db")

def scrape(url):
    """Get the source code from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    """only take the event name from the source code"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
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


def store(extracted):
    """get the event and stores in the database"""
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    """return the existing data in data DB and return the rows"""
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",(band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="Hey,new event was found!")
        time.sleep(2)


