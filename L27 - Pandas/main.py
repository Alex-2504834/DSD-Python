import matplotlib.pyplot as plot
import csv
import kagglehub 
import os
import pandas as pd

def getBasePath():
    return kagglehub.dataset_download("rohanrao/formula-1-world-championship-1950-2020")

def getCSVPath(csv):
    return f"{getBasePath()}\\{csv.removesuffix(".csv")}.csv" 
 

def printFiles(data):
    files = os.listdir(data)
    print(f"Total number of files downloaded | {len(files)}")
    for index in range(len(files)):
        print(f"{index+1: >2} | {files[index]}")

def readCSV(csv):
    return pd.read_csv(getCSVPath(csv))
    #print(csvData["driverId"])
    #print(type(csvData))

def main(dev):
    data = getBasePath()
    printFiles(data)
    drivers = readCSV("drivers.csv")
    pitStops = readCSV("pit_stops.csv")

    print((drivers["driverId"].to_numpy()))
    plot.plot((drivers["driverId"].to_numpy(), pitStops["driverId"].to_numpy()))
    plot.show()
    if dev:
        print(data)

if __name__ == "__main__":
    try:
        main(False)
    except KeyboardInterrupt:
        print("Bye :(")