import requests
from bs4 import BeautifulSoup
from datetime import date
from pathlib import Path
import sqlite3

today = date.today()
todays_date = today.strftime("%d/%m/%Y")
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
weekday = days[today.weekday()]
print(weekday, todays_date)
db_file = Path(__file__).parent.joinpath('gym1.db')
conn = sqlite3.connect(db_file)
c = conn.cursor()

def connection():
    s = requests.Session()
    r1 = s.get("https://bookings.bs7gym.co.uk")
    soup = BeautifulSoup(r1.text, "html.parser")
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

    r2 = s.get("https://bookings.bs7gym.co.uk/Bookings/BookSession.aspx")
    soup2 = BeautifulSoup(r2.text, "html.parser")
    ev2 = soup2.find("input", id="__EVENTVALIDATION")
    vs2 = soup2.find("input", id="__VIEWSTATE")

    date_data = {
        "__EVENTTARGET": "ctl00$mainContent$SessionDatePicker",
        "__VIEWSTATE": vs2["value"],
        "__EVENTVALIDATION": ev2["value"],
        "ctl00$errorPrompt": "",
        "ctl00$mainContent$SessionDatePicker": todays_date
    }
    r = s.post("https://bookings.bs7gym.co.uk/Bookings/BookSession.aspx", data=date_data)
    return r.text


def scrape_input(html):
    soup = BeautifulSoup(html , 'html.parser')
    for div in soup.find_all('div', class_='timeSlot'):
        s2 = div.find_all('div', class_='time hidden')
        s3 = div.find_all('div', class_='spaces hidden')
        for x, y in zip(s2, s3):
            timeslot = x.text.strip()
            spaces = int("".join(z for z in y.text if z.isdigit()))
            if spaces == 0:
                continue
            datetime = timeslot + todays_date
            print(timeslot, spaces)

            try:
                c.execute("INSERT INTO gymnew1 (date, time, datetime, weekday, spaces) VALUES (?,?,?,?,?)", (todays_date, timeslot, str(datetime), weekday, spaces))
            except:
                c.execute("UPDATE gymnew1 SET spaces = ? WHERE datetime = ?;", (spaces, str(datetime)))
            
            conn.commit()

def main():
    text = connection()
    scrape_input(text)
    conn.close()

if __name__ == "__main__":
    main()