#
#laneBooking = {
#    "laneOne": {
#
#    }
#}
#
#prices = {}
#
#cafeFood = {
#    0: {"name": "temp", "price": "£2.0" }
#}
#
#currentOrders = {}

import random
import time

currentClass = {
    0: {"name": "conner", "weight": 0.5},
    1: {"name": "alex", "weight": 0.5},
    2: {"name": "kye", "weight": 0.5},
    3: {"name": "thomas", "weight": 0.5},
    4: {"name": "kieran", "weight": 0.5}
}  

nameList = [currentClass[index]["name"] for index in currentClass]
weightList = [currentClass[index]["weight"] for index in currentClass]


def weightFromName(name):        
    return [currentClass[each]["weight"] for each in currentClass if currentClass[each]["name"] == name][0]

def keyFromName(name):
    return [each for each in currentClass if currentClass[each]["name"] == name][0]

def reduceWeight(key, reduceAmount):
    if not (currentClass[key]["weight"] - reduceAmount) < 0:
        currentClass[key].update({"weight": currentClass[key]["weight"] - reduceAmount})

def getRandomStudent():
    randomStudent = random.choices(nameList, weights=weightList)[0]
    print(randomStudent)
    print(weightFromName(randomStudent))
    reduceWeight(keyFromName(randomStudent), 0.1)
    return randomStudent
#getRandomStudent()
temp = {   
    "conner": 0,
    "alex": 0,
    "kye": 0,
    "thomas": 0,
    "kieran": 0
}
while True:

    RandomStudent = getRandomStudent()
    if not (currentClass[keyFromName(RandomStudent)]["weight"]) <= 0:
        temp.update({f"{RandomStudent}": temp[RandomStudent] + 1})
    print(temp)
    time.sleep(0.01)