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
    0: {"name": "conner", "weight": 1},
    1: {"name": "alex", "weight": 2},
    2: {"name": "kye", "weight": 3},
    3: {"name": "thomas", "weight": 4},
    4: {"name": "kieran", "weight": 5}
}  

#for index in currentClass:
#    print(currentClass[index]["name"])
nameList = [currentClass[index]["name"] for index in currentClass]
weightList = [currentClass[index]["weight"] for index in currentClass]

#print(nameList)
#print(weightList)

def weightFromName(name):        
    return [currentClass[each]["weight"] for each in currentClass if currentClass[each]["name"] == name][0]

def keyFromName(name):
    return [each for each in currentClass if currentClass[each]["name"] == name][0]

def reduceWeight(key, reduceAmount):
    if (currentClass[key]["weight"] - reduceAmount) == 0:
        currentClass[key].update({"weight": currentClass[key]["weight"] - reduceAmount})

def getRandomStudent():
    randomStudent = random.choices(nameList, weights=weightList)[0]
    print(randomStudent)
    print(weightFromName(randomStudent))
    reduceWeight(keyFromName(randomStudent), 1)
#getRandomStudent()

while True:
    getRandomStudent()
    time.sleep(0.25)