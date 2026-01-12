import matplotlib.pyplot as plot
import csv
import kagglehub 

data = kagglehub.dataset_download("mexwell/busiest-airports-of-europe")
dataset = "Busiest-European-Airports-2016"

with open(f"{data}/{dataset}.csv", "r") as csvFile:
    dataCSV = csv.DictReader(csvFile)
    for row in dataCSV:
        print(row["Airport"])
        print(int(row["Passengers2016"]))
        plot.barh(row["Airport"].strip("Airpot"),(int(row["Passengers2016"])))
        plot.tick_params(axis='y', pad=8, labelsize=8)
        plot.xlabel("Airports")
        plot.ylabel("Number of passengers in 2016")
        plot.title(dataset)
    plot.show()