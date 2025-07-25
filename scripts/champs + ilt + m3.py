import math
import os
import requests
import json
import csv


def main():
    TEAMNUMBERS = [
        14295, 22740, 542, 6436, 19900, 10298, 51, 19510, 14863, 359, 20824, 6282, 12675, 13277, 11770, 5218, 25,
        21936, 18253, 7767, 4348, 21380, 24433, 16234, 9887, 24079, 14996, 21325, 15091, 21980, 13303, 22030, 6372,
        21868, 14921, 15303, 24351, 20799, 49, 9040, 7832, 9247
    ]
    TEAMNAMES = [
        "Operation T.A.C.", "Bot Bot", "WHS Robotics", "Alpha Genesis", "Qualia Robotics", "Brain Stormz",
        "NerdHerd Insomniacs", "VolTech", "RGB 359", "WEBB.exe", "LeXT -- Pineapple Something", "Simi Valley Robotics",
        "Hermit Social LClub", "STEAMPunks Bravo", "Curiosity", "Javabots", "Rock N' Roll Robots", "SaMoTech",
        "BeachBots", "Blueprints", "RoboKnights", "Beyond Robotics", "Inkineers", "Tekriot", "CyberDragons Buttercup",
        "Stratus", "Omega Squad", "Junior Knights", "aztec.exe", "Bread Pandas", "SMES Robotics", "RobTot",
        "Patriotic Robotics", "Iconic", "AlphaOmega", "Space Rocks", "The Order", "CyberDragons Westley",
        "NerdHerd 7^2", "STEAMPunks Alpha", "Gear Gurus", "Chromium Robotics"
    ]
    CATAGORIES = ["tb1", "tb2", "autoYellowPointsIndividual", "autoPurplePointsIndividual",
                  "autoPixelPoints", "autoNavPointsIndividual",
                  "autoPoints", "dcPoints", "egDronePointsIndividual", "egNavPointsIndividual",
                  "egPoints", "totalPointsNp"]
    stats = []

    with open('../csvs/champs + ilt + m3.csv', mode='w') as csvfile:
        fieldnames = []
        fieldnames.append("Team Name")
        fieldnames.append("Team Number")
        for term in CATAGORIES:
            fieldnames.append(term)
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for i, team_number in enumerate(TEAMNUMBERS):
            stats = []
            stats.append(f"{TEAMNAMES[i]}")
            stats.append(f"{TEAMNUMBERS[i]}")
            stats[2:((len(CATAGORIES)) + 2)] = getData(TEAMNUMBERS[i])
            writer.writerow(stats)
            print(f"team {i + 1} done")

def getData(teamNumber):
    print("before data api")
    response = requests.get(f'https://api.ftcscout.org/rest/v1/teams/{teamNumber}/events/2023')
    data = response.json()
    print("before ilt")
    i, g, h = findILT(data)

    tb1 = data[i]["stats"]["tb1"]
    tb2 = data[i]["stats"]["tb2"]

    dcPoints = (data[i]["stats"]['avg']["dcPoints"] + data[g]["stats"]['avg']["dcPoints"] + data[h]["stats"]['avg']["dcPoints"]) / 3
    egDronePointsIndividual = (data[i]["stats"]['avg']["dronePointsIndividual"] + data[g]["stats"]['avg'][
        "dronePointsIndividual"] + data[h]["stats"]['avg'][
        "dronePointsIndividual"]) / 3
    # totalPointsNp = (data[i]["stats"]['avg']["totalPointsNp"] + data[g]["stats"]['avg']["totalPointsNp"])/2
    egNavPointsIndividual = (data[i]["stats"]['avg']['egNavPointsIndividual'] + data[g]['stats']['avg'][
        'egNavPointsIndividual'] + data[h]['stats']['avg'][
        'egNavPointsIndividual']) / 3
    autoPixelPoints = (data[i]["stats"]['avg']["autoPixelPoints"] + data[g]['stats']['avg']['autoPixelPoints'] + data[h]['stats']['avg']['autoPixelPoints']) / 3
    autoNavPointsIndividual = (data[i]["stats"]['avg']['autoNavPointsIndividual'] + data[g]["stats"]["avg"][
        "autoNavPointsIndividual"] + data[h]["stats"]["avg"][
        "autoNavPointsIndividual"]) / 3
    autoYellowPointsIndividual = (data[i]["stats"]['avg']["yellowPointsIndividual"] + data[g]["stats"]["avg"][
        "yellowPointsIndividual"] + data[h]["stats"]["avg"][
        "yellowPointsIndividual"]) / 3
    autoPurplePointsIndividual = (data[i]["stats"]['avg']["purplePointsIndividual"] + data[g]["stats"]["avg"][
        "purplePointsIndividual"] + data[h]["stats"]["avg"][
        "purplePointsIndividual"]) / 3
    autoPoints = autoYellowPointsIndividual + autoPurplePointsIndividual + autoNavPointsIndividual + autoPixelPoints

    egPoints = egDronePointsIndividual + egNavPointsIndividual
    totalPointsNp = autoPoints + egPoints + (dcPoints/4)

    return (tb1, tb2, autoYellowPointsIndividual, autoPurplePointsIndividual, autoPixelPoints,
            autoNavPointsIndividual,
            autoPoints, dcPoints, egDronePointsIndividual, egNavPointsIndividual,
            egPoints, totalPointsNp)


def findILT(data):
    EVENTORDER = ["MP", "LT", "M3", "M2", "M1", "M0"]
    events = []

    for i in range(len(data)):
        if data[i]['stats'] is not None:
            events.append(data[i]['eventCode'])
        else:
            events.append(None)

    for i in range(len(events)):
        if events[i] is not None and len(events[i]) >= 2 and events[i][-2] == "T" and events[i][-3] == "L":
            events[i] = "LT"
        elif events[i] is not None and len(events[i]) >= 2 and events[i][-2] == "P" and events[i][-3] == "M":
            events[i] = "MP"
        else:
            events[i] = events[i][-2:] if events[i] is not None else None
    counter = 0
    ilt = 0
    m3 = 0
    mp = 0
    for i in range(len(EVENTORDER) - 1):
        if EVENTORDER[i] in events:
            z = EVENTORDER[i]
            for g in range(len(events)):
                if counter == 3:
                    return mp, ilt, m3
                elif events[g] == z and counter == 0:
                    mp = g
                    counter += 1
                elif events[g] == z and counter == 1:
                    ilt = g
                    counter += 1
                elif events[g] == z and counter == 2:
                    m3 = g
                    counter += 1


def getTeams(eventCode):
    response = requests.get(f'https://api.ftcscout.org/rest/v1/events/2023/{eventCode}/teams')
    data = response.json()
    teams = []
    for i in range(len(data)):
        teams.append(data[i]['teamNumber'])

    return teams



if __name__ == "__main__":
    main()