import requests
import bs4
from datetime import date
import sqlite3

try:
    today = date.today()
    todays_date = today.strftime("%d/%m/%Y")
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    weekday = days[today.weekday()]
    print(weekday, todays_date)
    conn = sqlite3.connect('gym1.db')
    c = conn.cursor()
    print("setup successful")
except:
    print("setup unsuccessful")

def connection():
    s = requests.Session()
    try:
        r1 = s.get("https://bookings.bs7gym.co.uk")
        print("connected to BS7Gym 1")
    except:
        print("connection error 1")
    soup = bs4.BeautifulSoup(r1.text, "html.parser")
    ev = soup.find("input", id="__EVENTVALIDATION")
    vs = soup.find("input", id="__VIEWSTATE")

    login_data = {
        "__EVENTTARGET": "ctl00$mainContent$Login1$LoginImageButton",
        "__VIEWSTATE": vs["value"],
        "__EVENTVALIDATION": ev["value"],
        "ctl00$errorPrompt": "",
        "ctl00$mainContent$Login1$UserName": "julianpbill@gmail.com",
        "ctl00$mainContent$Login1$Password": "qmAin1"
    }
    s.post("https://bookings.bs7gym.co.uk/login.aspx", data=login_data)

    try:
        r2 = s.get("https://bookings.bs7gym.co.uk/Bookings/BookSession.aspx")
        print("connected to BS7Gym 2")
    except:
        print("connection error 2")

    soup2 = bs4.BeautifulSoup(r2.text, "html.parser")
    ev2 = soup2.find("input", id="__EVENTVALIDATION")
    vs2 = soup2.find("input", id="__VIEWSTATE")

    date_data = {
        "__EVENTTARGET": "ctl00$mainContent$SessionDatePicker",
        "__VIEWSTATE": vs2["value"],
        "__EVENTVALIDATION": ev2["value"],
        "ctl00$errorPrompt": "",
        "ctl00$mainContent$SessionDatePicker": todays_date
    }
    try:
        r = s.post("https://bookings.bs7gym.co.uk/Bookings/BookSession.aspx", data=date_data)
        print("connected to BS7Gym 3")
    except:
        print("connection error 3")    

    try:
        f = open("booking.html", "w")
        print("opened booking.html")
    except:
        print("failed to open booking.html")
    
    try:
        f.write(r.text)
        print("write to booking.html successful")
    except:
        print("failed to write to booking.html")
    f.close()

def scrape_input():
    with open('booking.html') as html:
        soup = bs4.BeautifulSoup(html , 'html.parser')
        for div in soup.find_all('div', class_='timeSlot'):
            s2 = div.find_all('div', class_='time hidden')
            s3 = div.find_all('div', class_='spaces hidden')
            for x, y in zip(s2, s3):
                timeslot = x.text.strip()
                spaces = int("".join(z for z in y.text if z.isdigit()))
                datetime = timeslot + todays_date
                print(timeslot, spaces)

                try:
                    c.execute("INSERT INTO gymnew1 (date, time, datetime, weekday, spaces) VALUES (?,?,?,?,?)", (todays_date, timeslot, str(datetime), weekday, spaces))
                except:
                    c.execute("UPDATE gymnew1 SET spaces = ? WHERE datetime = ?;", (spaces, str(datetime)))
                
                conn.commit()

def main():
    connection()
    scrape_input()
    conn.close()

if __name__ == "__main__":
    main()