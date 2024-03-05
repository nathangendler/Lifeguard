import requests
import json



autoPoints = []
egPoints = []
dcPoints = []
totalPointsNp = []
dronePointsIndividual = []

avg_autoPoints = 0
avg_egPoints = 0
avg_dcPoints = 0
avg_totalPointsNp = 0
avg_dronePointsIndividual = 0


teamnumber = 21936

response = requests.get(f'https://api.ftcscout.org/rest/v1/teams/{teamnumber}/events/2023')
data = response.json()

EVENTAMOUNT = len(data)

tb1 = data[0]["stats"]["tb1"]
tb2 = data[0]["stats"]["tb2"]

ilt_autoPoints = data[0]["stats"]['avg']["autoPoints"]
ilt_egPoints = data[0]["stats"]['avg']["egPoints"]
ilt_dcPoints = data[0]["stats"]['avg']["dcPoints"]
ilt_dronePointsIndividual = data[0]["stats"]['avg']["dronePointsIndividual"]
ilt_totalPointsNp = data[0]["stats"]['avg']["totalPointsNp"]
ilt_autoYellowPointsIndividual = 0
ilt_autoPurplePointsIndividual = 0



for i in range(EVENTAMOUNT):
    autoPoints.append(data[i]['stats']['avg']['autoPoints'])
    egPoints.append(data[i]['stats']['avg']['egPoints'])
    dcPoints.append(data[i]['stats']['avg']['dcPoints'])
    totalPointsNp.append(data[i]['stats']['avg']['totalPointsNp'])
    dronePointsIndividual.append(data[i]['stats']['avg']['dronePointsIndividual'])
    avg_autoPoints += autoPoints[i]
    avg_egPoints += egPoints[i]
    avg_dcPoints += dcPoints[i]
    avg_totalPointsNp += totalPointsNp[i]
    avg_dronePointsIndividual += dronePointsIndividual[i]


avg_autoPoints /= EVENTAMOUNT
avg_egPoints /= EVENTAMOUNT
avg_dcPoints /= EVENTAMOUNT
avg_totalPointsNp /= EVENTAMOUNT
avg_dronePointsIndividual /= EVENTAMOUNT


print(f"Team {teamnumber}")
print("-------------------")
print(f"Average Auto Points: {avg_autoPoints}")
print(f"Average End Game Points: {avg_egPoints}")
print(f"Average TeleOp Points: {avg_dcPoints}")
print(f"Average Total Points: {avg_totalPointsNp}")
print(f"Average Individual Drone Points: {avg_dronePointsIndividual}")
print("-------------------")
print(f"ILT Auto Points: {ilt_autoPoints}")
print(f"ILT End Game Points: {ilt_egPoints}")
print(f"ILT TeleOp Points: {ilt_dcPoints}")
print(f"ILT Total Points: {ilt_totalPointsNp}")
print(f"ILT Individual Drone Points: {ilt_dronePointsIndividual}")





