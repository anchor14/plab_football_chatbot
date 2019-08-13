from selenium import webdriver
import datetime
import json
import sqlite3
import requests
import urllib.request
from selenium.webdriver.remote.webelement import WebElement

today_index = datetime.datetime.today().weekday()

# Using Selenium's webdriver to open the page

driver = webdriver.Firefox(executable_path=r'geckodriver')
driver.get("http://www.plabfootball.com/")


# user_pref = input("Let us know which place you are interested in: ")
user_pref = "용산"

day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

return_dict = {}
session_string = ""

#Loop to go through all days
for day in range(1,8):
    #no need to click smth for the first day(default) but have to do it for any other day
    if day > 1:
        link_key = "#tab > a:nth-child("+str(day)+") > div"
        new_link = driver.find_element_by_css_selector(link_key)
        new_link.click()

    css_key = "#day"+str(day)+" > ul"
    sessions_new_day = driver.find_elements_by_css_selector(css_key)


    sessions_text_day = []
    for item in sessions_new_day:
        sessions_text_day.append(item.text.split('\n'))

    session_string+='<<'+day_list[(today_index+day-1)%7]+'>>'
    session_string+='\n'
    print('<<'+day_list[(today_index+day-1)%7]+'>>')

    # print(sessions_text_day)
    count = 0
    tracker = 0
    for sessions in sessions_text_day[0]:
        if "2019년" in sessions:
            tracker += 1

        if user_pref in sessions:
            #count-1 is to get the time since that is always the element that comes right before the placeholder
            print("And the time is: " + sessions_text_day[0][count - 1])
#day1 > ul > li:nth-child(1) > div > div.listRight
            status_key = "#day"+str(day)+ "> ul > li:nth-child(" + str(tracker) + ") > div > div.listRight"
            session_status = driver.find_elements_by_css_selector(status_key)
            # print(session_status.get_attribute('text'))
            for item in session_status:
                print(item.text)

            return_dict.update({day_list[(today_index+day-1)%7] : sessions_text_day[0][count - 1]})
            session_string += sessions_text_day[0][count - 1]
            session_string+='\n'
        count += 1

    print('------------------------------------------')

# newjson = json.dumps(return_dict)

# print('session string:')
# print(session_string)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_sessions(conn, time):

    # time = (user_pref,new_json)
    sql = '''INSERT INTO times(Loc,Sessions)
    VALUES(?,?)'''

    cur = conn.cursor()
    cur.execute(sql,time)

    return cur.lastrowid

def send(jsonStr):
    print("sending data: ", jsonStr, "\n======")
    # write code to send jsonStr to DB server here...

    url = "http://127.0.0.1:5000/postJson"
    # jsonStr = json.dumps(json.loads(jsonStr))
    r = requests.post(url=url, json=json.dumps(jsonStr))
    print("response from database server:", r.json)


def main():
    database = "/Users/jhn/Desktop/plab_football_bot/flask/pythonsqlite.db"

    conn = create_connection(database)

    with conn:
        loc_1 = (user_pref)
        session_1 = (session_string)
        time_id = create_sessions(conn,[loc_1,session_1])

    # send(json.dumps(return_dict))


if __name__ == '__main__':
    main()
