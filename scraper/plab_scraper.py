from selenium import webdriver
import datetime
import json
import sqlite3
import requests
import urllib.request
from selenium.webdriver.remote.webelement import WebElement

today_index = datetime.datetime.today().weekday()

driver = webdriver.Firefox(executable_path=r'geckodriver')

# user_pref = input("Let us know which place you are interested in: ")
user_pref = "용산"


def getSessions(url,location):
#Loop to go through all days
    driver.get(url)

    day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    return_dict = {}

    session_string = ""

    for day in range(1,8):
        #no need to click smth for the first day(default) but have to do it for any other day
        if day > 1:
            link_key = "#tab > a:nth-child("+str(day)+") > div"
            new_link = driver.find_element_by_css_selector(link_key)
            new_link.click()

        css_key = "#day"+str(day)+" > ul"
        sessions_new_day = driver.find_elements_by_css_selector(css_key)

        session_string+='<<'+day_list[(today_index+day-1)%7]+'>>'
        # session_string+='\n'

        sessions_text_day = []
        for item in sessions_new_day:
            sessions_text_day.append(item.text.split('\n'))

        # print('<<'+day_list[(today_index+day-1)%7]+'>>')

        # print(sessions_text_day)
        count = 0
        tracker = 0
        for sessions in sessions_text_day[0]:
            #this is a horrible way to code but for now we can check that every time 2019 comes, it is a new session
            if "2019년" in sessions:
                tracker += 1

            if user_pref in sessions:
                #count-1 is to get the time since that is always the element that comes right before the placeholder
                # print("And the time is: " + sessions_text_day[0][count - 1])
                status_key = "#day"+str(day)+ "> ul > li:nth-child(" + str(tracker) + ") > div > div.listRight"
                session_status = driver.find_elements_by_css_selector(status_key)
                # print(session_status.get_attribute('text'))

                return_dict.update({day_list[(today_index+day-1)%7] : sessions_text_day[0][count - 1]})

                session_string += sessions_text_day[0][count - 1]
                for item in session_status:
                    #below is also not a good way of coding but for now we only want to return the status without details
                    if "원" not in item.text:
                        tmp_add = "--" + str(item.text)
                        session_string += tmp_add.rstrip()
                    # session_str += '---'
                # session_string+='\n'
            count += 1

        # session_string+= "--------------------------------"

    return session_string

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

    fulfillment_string = "{\"fulfillmentText\": "


    fulfillment_string += jsonStr
    # jsonFormat = jsonStr
    # print(type(jsonFormat))

    r = requests.post(url=url,json=jsonFormat)
    print("response from database server:", r.text)


def main():
    # database = "/Users/jhn/Desktop/plab_football_chatbot/flask/pythonsqlite.db"
    #
    # conn = create_connection(database)
    #
    # with conn:
    #     loc_1 = (user_pref)
    #     session_1 = ("session_string")
    #     time_id = create_sessions(conn,[loc_1,session_1])

    jsonstr = getSessions("http://www.plabfootball.com/",user_pref)
    print(jsonstr)
    send(jsonstr)



if __name__ == '__main__':
    main()
