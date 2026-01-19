import pandas as pd
import csv

def taskOne():
    data = {
        "Name": ["Alex", "Jamie", "Sam"],
        "Attendance": [92, 85, 78],
        "Grade": ["B", "C", "D"]
    }

    newStudent = {
        "Name": ["Connor"],
        "Attendance": [92],
        "Grade": ["D"]
    }

    studentDataFrame = pd.DataFrame(data)
    newStudentstudentDataFrame = pd.DataFrame(newStudent)
    new = pd.concat([studentDataFrame, newStudentstudentDataFrame], ignore_index=True)

    print(new)

def taskTwo():
    csvPath = "L28 - Pandas/students.csv"
    data = pd.read_csv(csvPath)

    print(data.head)
    data.info

def taskThree():
    csvPath = "L28 - Pandas/students.csv"
    data = pd.read_csv(csvPath)
    print(f"StudentID {"|": >7} {data["StudentID"].count()}")
    print(f"Mean Attendance | {data["Attendance"].mean()}")
    print(f"Below 80% {"|": >7} {data[data["Attendance"] < 80]["Attendance"].count()}")
    print(f"At or Above 90% {"|": >1} {data[data["Attendance"] >= 80]["Attendance"].count()}")
    temp = data["Grade"].value_counts()
    print(f"Each grade {"|": >6} A: {temp["A"]} | B: {temp["B"]} | C: {temp["C"]} | D: {temp["D"]} | E: {temp["E"]}")

def taskFour():
    csvPath = "L28 - Pandas/students.csv"
    data = pd.read_csv(csvPath)
    atRisk = pd.DataFrame(data["Attendance"] < 80)
    data["atRisk"] = atRisk
    print(data)

def taskFive():
    csvPath = "L28 - Pandas/students.csv"
    data = pd.read_csv(csvPath)
    print(data.rank())

taskFive()