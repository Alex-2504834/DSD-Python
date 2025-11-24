import datetime
import json
from pathlib import Path
from dataclasses import dataclass

jsonPath = Path("19\\loans.json")

@dataclass
class Colour:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    def custom(self, hexColour):
        hexColour = hexColour.lstrip("#")
        red, green, blue = (int(hexColour[i : i + 2], 16) for i in (0, 2, 4))
        return f"\x1b[38;2;{red};{green};{blue}m"


def loadDataFromDisk(filePath: Path) -> dict[int, dict[str, str]]:
    with filePath.open("r", encoding="utf-8") as jsonFile:
        rawData = json.load(jsonFile)

    dataDict = {}

    for index in rawData:
        dataDict[int(index)] = {"student_name": rawData[index]["student_name"],
                                "student_id": rawData[index]["student_id"],
                                "device_type": rawData[index]["device_type"],
                                "device_id": rawData[index]["device_id"],
                                "date_out": rawData[index]["date_out"],
                                "due_back": rawData[index]["due_back"],
                                "returned": rawData[index]["returned"]}

    return dataDict

def saveDataToDisk(filePath: Path, data):
    try:
        with filePath.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except Exception as error:
        print(error)


def addToJsonData(jsonData, data):
    jsonData[list(jsonData.keys())[-1] + 1] = data

def updateJsonData(jsonData, data, loanID):
    try:
        jsonData[loanID]
        jsonData[loanID] = data
    except:
        print(f"{Colour.RED}That loan ID doesnt exist{Colour.END}")

jsonData = loadDataFromDisk(jsonPath)


temp = {
        "student_name": "Alex",
        "student_id": "S12345",
        "device_type": "Laptop",
        "device_id": "L-001",
        "date_out": "2025-11-24",
        "due_back": "2025-12-01",
        "returned": "False"
    }


updateJsonData(jsonData, temp, 5)

addToJsonData(jsonData, temp)

saveDataToDisk(jsonPath, jsonData)
print(loadDataFromDisk(jsonPath))