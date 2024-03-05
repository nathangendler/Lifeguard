import math
import os
import requests
import json
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1wdHvDBQZh2K5U2rjHT-AxW_xl7sDGrvIe_bPLRlxASM'


def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheets = service.spreadsheets()

        TEAMNUMBERS = [
            14295, 22740, 542, 6436, 19900, 10298, 51, 19510, 14863, 359, 20824, 6282, 12675, 13277, 11770, 5218, 25,
            21936, 18253, 7767, 4348, 21380, 24433, 16234, 9887, 24079, 14996, 21325, 15091, 21980, 13303, 22030, 6372,
            21868, 14921, 15303, 24351, 20799, 49, 9040, 7832, 9247
        ]
        TEAMNAMES = [
            "Operation T.A.C.","Bot Bot","WHS Robotics","Alpha Genesis","Qualia Robotics","Brain Stormz","NerdHerd Insomniacs","VolTech","RGB 359","WEBB.exe","LeXT -- Pineapple Something","Simi Valley Robotics","Hermit Social LClub","STEAMPunks Bravo","Curiosity","Javabots","Rock N' Roll Robots","SaMoTech","BeachBots","Blueprints","RoboKnights","Beyond Robotics","Inkineers","Tekriot","CyberDragons Buttercup","Stratus","Omega Squad","Junior Knights","aztec.exe","Bread Pandas","SMES Robotics","RobTot","Patriotic Robotics","Iconic","AlphaOmega","Space Rocks","The Order","CyberDragons Westley","NerdHerd 7^2","STEAMPunks Alpha","Gear Gurus","Chromium Robotics"
        ]
        LETTERS = [chr(i).upper() for i in range(ord('a'), ord('z') + 1)]
        quotas = 0
        CATAGORIES = ["tb1", "tb2", "autoYellowPointsIndividual", "autoPurplePointsIndividual",
                      "autoPixelPoints", "autoNavPointsIndividual",
                      "autoPoints", "dcPoints", "egDronePointsIndividual", "egNavPointsIndividual",
                      "egPoints", "totalPointsNp"]
        stats = [None] * len(CATAGORIES)

        quotas = printSheets("A", "1", "Team Name", quotas, sheets)
        quotas = printSheets("B", "1", "Team Number", quotas, sheets)

        for b in range(0, len(CATAGORIES)):
            # prints catagories
            quotas = printSheets(LETTERS[b + 2], "1", CATAGORIES[b], quotas, sheets)
            print(CATAGORIES[b])

        for i, team_number in enumerate(TEAMNUMBERS):
            # gets data
            stats[:len(CATAGORIES)] = getData(TEAMNUMBERS[i])
            # prints names and numbers
            quotas = printSheets("A", (i + 2), TEAMNAMES[i], quotas, sheets)
            print(TEAMNAMES[i])
            quotas = printSheets("B", (i + 2), TEAMNUMBERS[i], quotas, sheets)
            print(TEAMNUMBERS[i])

            for a in range(len(stats)):
                # prints all stats
                quotas = printSheets(LETTERS[a + 2], (i + 2), stats[a], quotas, sheets)
                print(stats[a])


    except HttpError as error:
        print(error)


def printSheets(letLocation, numLocation, text, quotas, sheets):
    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"real!{letLocation}{numLocation}",
                           valueInputOption="USER_ENTERED", body={"values": [[f"{text}"]]}).execute()
    quotas += 1
    if quotas == 59:
        time.sleep(62)
        return 0
    else:
        return quotas


def getData(teamNumber):
    response = requests.get(f'https://api.ftcscout.org/rest/v1/teams/{teamNumber}/events/2023')
    data = response.json()
    EVENT_TOTAL = len(data)
    eventTotal = 0

    i, g = findILT(data)

    tb1 = data[i]["stats"]["tb1"]
    tb2 = data[i]["stats"]["tb2"]

    dcPoints = (data[i]["stats"]['avg']["dcPoints"] + data[g]["stats"]['avg']["dcPoints"]) / 2
    egDronePointsIndividual = (data[i]["stats"]['avg']["dronePointsIndividual"] + data[g]["stats"]['avg'][
        "dronePointsIndividual"]) / 2
    # totalPointsNp = (data[i]["stats"]['avg']["totalPointsNp"] + data[g]["stats"]['avg']["totalPointsNp"])/2
    egNavPointsIndividual = (data[i]["stats"]['avg']['egNavPointsIndividual'] + data[g]['stats']['avg'][
        'egNavPointsIndividual']) / 2
    autoPixelPoints = (data[i]["stats"]['avg']["autoPixelPoints"] + data[g]['stats']['avg']['autoPixelPoints']) / 2
    autoNavPointsIndividual = (data[i]["stats"]['avg']['autoNavPointsIndividual'] + data[g]["stats"]["avg"][
        "autoNavPointsIndividual"]) / 2
    autoYellowPointsIndividual = (data[i]["stats"]['avg']["yellowPointsIndividual"] + data[g]["stats"]["avg"][
        "yellowPointsIndividual"]) / 2
    autoPurplePointsIndividual = (data[i]["stats"]['avg']["purplePointsIndividual"] + data[g]["stats"]["avg"][
        "purplePointsIndividual"]) / 2
    autoPoints = autoYellowPointsIndividual + autoPurplePointsIndividual + autoNavPointsIndividual + autoPixelPoints
    egPoints = egDronePointsIndividual + egNavPointsIndividual
    totalPointsNp = autoPoints + egPoints + dcPoints

    return (tb1, tb2, autoYellowPointsIndividual, autoPurplePointsIndividual, autoPixelPoints,
            autoNavPointsIndividual,
            autoPoints, dcPoints, egDronePointsIndividual, egNavPointsIndividual,
            egPoints, totalPointsNp)


def findILT(data):
    EVENTORDER = ["LT", "M3", "M2", "M1", "M0"]
    events = []

    for i in range(len(data)):
        if data[i]['stats'] is not None:
            events.append(data[i]['eventCode'])
        else:
            events.append(None)


    for i in range(len(events)):
        if events[i] is not None and len(events[i]) >= 3 and events[i][-2] == "T" and events[i][-3] == "L":
            events[i] = "LT"
        else:
            events[i] = events[i][-2:] if events[i] is not None else None
    counter = 0
    ilt = 0
    m3 = 0

    for i in range(len(EVENTORDER) - 1):
        if EVENTORDER[i] in events:
            z = EVENTORDER[i]
            for g in range(len(events)):
                if counter == 2:
                    return ilt, m3
                elif events[g] == z and counter == 0:
                    ilt = g
                    counter += 1
                elif events[g] == z and counter == 1:
                    m3 = g
                    counter += 1

def getTeams(eventCode):
    response = requests.get(f'https://api.ftcscout.org/rest/v1/events/2023/{eventCode}/teams')
    data = response.json()
    teams = []
    for i in range(len(data)):
        teams.append(data[i]['teamNumber'])

    return teams


def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    main()
