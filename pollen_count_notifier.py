#THIS PROGRAM WILL GRAB THE POLLEN COUNT FOR TODAY AND SEND A TEXT
#MESSAGE IF THE POLLEN COUNT IS > 1500, WHICH IS NOTED TO BE EXTREME

import requests, schedule, time             #LIBRARY TO RETREIVE DATA FROM THE WEB
from lxml import html                       #LIBRARY FOR PARSING HTML
from twilio.rest import Client              #TWILIO API!!
from datetime import date                   #USE DATETIME TO PRINT TODAYS DATE


print('The Pollen Count is checked at 8am')

def send_sms():         #FUNTION THAT WILL GRAB THE POLLEN COUNT FOR TODAY AND SEND AN SMS IF IT IS EXTREME

    today = date.today()                #GRAB DATE
    d = today.strftime("%m/%d/%y")      #FORMAT DATE

    extreme_pollen_count = 1500         #THE WEBSITE CATEGORIZES A POLLEN COUNT OF 1500 OR GREATER AS EXTREME

    r = requests.get('http://www.atlantaallergy.com/pollen_counts')     #RETREIVE HTML WEBPAGE

    tree = html.fromstring(r.content)                                   #USE LXML TO FORMAT PAGE INTO SEARCHABLE HTML TREE

    pollen_count = tree.xpath('//html/body/div[5]/div/div/div/div/div[1]/div/div[2]/div/p[1]/strong/span')  #USE LXML TO FIND XPATH LOCATION OF DATA

    for x in pollen_count:                          #ITERATE THROUGH THE RETRIEVED LIST TO SET NEW VARIABLE
        todays_pollen_count = int(x.text.strip())   #SET NEW VARIABLE AS AN INTEGER AND STRIP ALL EXTRA SPACE

    if todays_pollen_count >= extreme_pollen_count:         #WILL SEND SMS IF POLLEN COUNT IS GREATER THAN 1500

        #TWILIO
        account_sid = "AC8985f47b608f5031a88032b517fb923c"
        auth_token  = "XXXXXXXXX"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+14048632171",
            from_="+18189622834",
            body="Today's Pollen Count is: " + str(todays_pollen_count) + ". It is Extreme")

        print()
        print('Date: ' + d)
        print('The pollen count is extreme. You have been notified via SMS that the pollen count is: ' + str(todays_pollen_count))
        print('Message SID is: ' + message.sid)
        print()
        print('The pollen count will be checked again at 8am')

        return todays_pollen_count
    else:
        print()
        print('The pollen count is: ' + str(todays_pollen_count) + '. It is not Extreme and you will not be notified')
        print()
        print('The pollen count will be checked again at 8am')


schedule.every().day.at("08:00").do(send_sms)       #SCHEDULER MODULE WILL RUN SEMD_SMS FUNCTION ONLY AT THE SPECIFIED TIME

while True:                     #WHILE LOOP LETS PROGRAM RUN IN THE BACKGROUND WAITING FOR SPECIFIED TIME
    schedule.run_pending()      #USES NEARLY ZERO CPU RESOURCES WHILE ITERATING THROUGH WHILE LOOP ONCE A SECOND
    time.sleep(1)
