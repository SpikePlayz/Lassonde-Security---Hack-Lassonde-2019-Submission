from twilio.rest import Client
from random import randint
import json
import random
import re, uuid
from pyfiglet import Figlet
from tqdm import tqdm
import time
import requests
import os
import getpass

f = Figlet(font='doom')
print(f.renderText('Lassonde Security'))

getUserIpUrl = "https://api.ipify.org?format=json"
getUserIp = requests.get(getUserIpUrl)
json_data = getUserIp.json()
IPAddress = json_data['ip']
checkIPurl = "http://v2.api.iphub.info/ip/" + IPAddress
headers = {
    "X-Key": "NDY1NTppdHFGWTNjd2tEZlY5UTJsdUYwak1pb3JDaUZhUzVWcw=="
}
checkIP = requests.get(checkIPurl, headers=headers)
checkIPjson = checkIP.json()
if checkIPjson['block'] == 1:
    print("Our service has detected the use of a VPN or Proxy. Please disable any proxies or VPN's and try again.")
else:
    print("Your IP is " + IPAddress + " and you are using a permitted residential IP Address from ISP: " + checkIPjson['isp'] + " in " + checkIPjson['countryName'] + ".")
    while True:
        userChoice = int(input("To register a new account, enter 1. To login to an existing account, enter 2: "))
        if userChoice == None:
            print("Error! Please enter either 1 to register or 2 to login and try again.")

        elif userChoice == 1:
            username = input("Enter your username: ")
            password = getpass.getpass('Password:')
            email = input("Enter your email: ")
            phoneNum = input("Enter your phone number (ex. +10000000000): ")

            macAddress = (':'.join(re.findall('..', '%012x' % uuid.getnode()))).upper()

            def random_with_N_digits(n):
                range_start = 10**(n-1)
                range_end = (10**n)-1
                return randint(range_start, range_end)

            code = random_with_N_digits(4)

            account_sid = 'AC71fbe65bd14cca2e06241a338611b1a9'
            auth_token = '5ef64c9dce2ddcfbb2d7f7c6720d7f13'
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                 body="Your authentication code is " + str(code) + ".",
                                 from_='+19029015774',
                                 to=phoneNum
                             )

            for i in tqdm(range(100)):
                time.sleep(0.010)
            askCode = int(input("Check your phone! We sent a 4 digit code. Please enter that here: "))
            incorrectCode = True
            while incorrectCode == True:
                if askCode == code:
                    jsonData = '{"user":"' + username + '","pass":"' + password + '","email":"' + email + '","phoneNum":"' + phoneNum + '","MC":"' + macAddress + '","macChanges":0}'
                    accounts = open("accounts.txt", "r").read().split()
                    repeatedInfo = False
                    for account in accounts:
                        accounts_json = json.loads(account)
                        if accounts_json['user'] == username:
                            print("There is already an account registered under this username. Please choose another username and try again.")
                            repeatedInfo = True
                        elif accounts_json['email'] == email:
                            print("There is already an account registered with that email. Please use another email and try again.")
                            repeatedInfo = True
                    if repeatedInfo == False:
                        accountdetails = open("accounts.txt", "r").read().split()
                        with open("accounts.txt", 'a') as file:
                            file.write(jsonData + '\n')
                        print("Your number has been saved! Please login to your account.")
                        incorrectCode = False
                else:
                    print("Incorrect code inputted! Please check your 4-digit code and try again.")

        elif userChoice == 2:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            email = input("Enter your email: ")
            phoneNum = input("Enter your phone number (ex. +10000000000): ")

            macAddress = (':'.join(re.findall('..', '%012x' % uuid.getnode()))).upper()

            def random_with_N_digits(n):
                range_start = 10**(n-1)
                range_end = (10**n)-1
                return randint(range_start, range_end)

            code = random_with_N_digits(4)

            account_sid = 'AC71fbe65bd14cca2e06241a338611b1a9'
            auth_token = '5ef64c9dce2ddcfbb2d7f7c6720d7f13'
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                 body="Your authentication code is " + str(code) + ".",
                                 from_='+19029015774',
                                 to=phoneNum
                             )

            jsonData = '{"user":"' + username + '","pass":"' + password + '","email":"' + email + '","phoneNum":"' + phoneNum + '","MC":"' + macAddress + '"}'
            askForCode = True
            while askForCode == True:
                askCode = int(input("Check your phone! We sent a 4 digit code. Please enter that here: "))
                if askCode == code:
                    print("Correct code inputted! Checking database...")
                    time.sleep(2)
                    os.system('cls')
                    askForCode = False
                    accounts = open("accounts.txt", "r").read().split()
                    for account in accounts:
                        accounts_json = json.loads(account)
                        if accounts_json['user'] == username and accounts_json['MC'] == macAddress:
                            f = Figlet(font='speed')
                            print(f.renderText("Welcome " + username))
                            print("Main Menu")
                            changeMac = int(input("To change your Mac Address, enter 1. To logout, type 2."))
                            if changeMac == 1:
                                areYouSure = input("Are you sure that you want to change your Mac Address? Type Yes or No. YOU ONLY HAVE " + str(accounts_json['macChanges']) + " CHANGES LEFT!")
                                if areYouSure == "Yes":
                                    macAddress = (':'.join(re.findall('..', '%012x' % uuid.getnode()))).upper()
                                    oldMac = accounts_json['MC']
                                    accounts_json['MC'] == macAddress
                                    accounts_json['macChanges'] -= 1
                                    print("Success! Your old Mac Address " + oldMac + " has been changed to the new Mac Address " + macAddress + ".")
                                if areYouSure == "No":
                                    print("Mac Address change canceled. Returning to root menu.")
                            if changeMac == 2:
                                print("You were successfully logged out. Thanks for using LassondeSecurity.")
                        elif accounts_json['user'] == username and accounts_json['MC'] != macAddress:
                            print("We have detected a user login from another machine. Please login from the machine the account was originally created with.")
                        else:
                            print("There is no account registered on this phone number. Try registering an account and try again.")
                else:
                    print("Incorrect code inputted! Please check your 4-digit code and try again.")
