import os
import time

def labUnitConverter():
    GLUCOSE_CONVERSION = 18
    CHOLESTRROL_CONVERSION = 38.67

    userTestTypeInput = input("Enter Test Type | Glucose(mmol/L) or Cholesterol(mg/dL) | (g/c): ")
    userValueInput = float(input("Enter Value: "))
    userUnitInput = int(input("Enter Units | mg/dL or mmol/L | (1/2): "))
    
    #? mmol/L to mg/dL
    if userTestTypeInput == "g" and userUnitInput == 1:
        print(f"{userValueInput / GLUCOSE_CONVERSION} mmol/L")

    elif userTestTypeInput == "g" and userUnitInput == 2:
        print(f"{userValueInput * GLUCOSE_CONVERSION} mg/dL")

    #? mg/dL to mmol/L
    if userTestTypeInput == "c" and userUnitInput == 1:
        print(f"{userValueInput / CHOLESTRROL_CONVERSION} mmol/L")

    elif userTestTypeInput == "c" and userUnitInput == 2:
        print(f"{userValueInput * CHOLESTRROL_CONVERSION} mg/dL")

def average():
    MAX_FEVER = 45
    MIN_FEVER = 30
    numberList: list = []

    print("Enter the temperature, finish by typing f")
    running = True
    while running:
        userInput = input()
        try:
            if float(userInput) < MIN_FEVER:
                print(f"Entered {userInput} but this is too low: (30) | value rejected")
            elif float(userInput) > MAX_FEVER:
                print(f"Entered {userInput} but this is too high: (45) | value rejected")
            else:
                numberList.append(float(userInput))
        except:
            pass
        if userInput in ("f"):
            length: int = len(numberList)
            addedNumbers: float = 0
            for numbers in numberList:
                addedNumbers += numbers
            print(f"Entered a total of: {len(numberList)} temperature")
            try: 
                final: float = addedNumbers / length
                print(f"The average temperature is: {round(final, 2)}")
                running = False
            except ZeroDivisionError:
                print("Divded by 0")
                running = False


def heartRateMonitor():
    userAgeInput = int(input("Enter your age: "))
    userHeartInput = int(input("Enter resting heart: "))

    ##* https://www.ncbi.nlm.nih.gov/books/NBK593193/table/ch1survey.T.normal_heart_rate_by_age/

    heartRateRanges = {
        "toddler": {"min": 80, "max": 130},
        "preschool": {"min": 80, "max": 110},
        "schoolAge": {"min": 70, "max": 100},
        "adolescents": {"min": 60, "max": 100}
     }
    heartRateRanges = {
        "Toddler":     { "age": {"min": 1, "max": 3},   "heartRate": {"min": 80, "max": 130}},
        "Preschool":   { "age": {"min": 4, "max": 5},   "heartRate": {"min": 80, "max": 110}},
        "School Age":  { "age": {"min": 6, "max": 12},  "heartRate": {"min": 70, "max": 100}},
        "Adolescents": { "age": {"min": 13, "max": 18}, "heartRate": {"min": 60, "max": 100}}
     }

    maxHeart = 206.9 - (0.67 * userAgeInput)


    for group, age in heartRateRanges.items():
        if userAgeInput in range(age["age"]["min"], age["age"]["max"] + 1):
            if userHeartInput >= age["heartRate"]["min"] and userHeartInput <= age["heartRate"]["max"]:
                print(f"Your age group is: {group}\nYour heart rate is: {userHeartInput}\nWhich is in the normal range of {age["heartRate"]["min"]} - {age["heartRate"]["max"]}")
           
            elif userHeartInput <= age["heartRate"]["min"]: 
                print(f"Your age group is: {group}\nYour heart rate is: {userHeartInput}\nWhich is to \033[0;36mlow\033[0m for your age: ({age["heartRate"]["min"]} - {age["heartRate"]["max"]})")  

            elif userHeartInput >= age["heartRate"]["max"]:
                print(f"Your age group is: {group}\nYour heart rate is: {userHeartInput}\nWhich is to \033[0;31mhigh\033[0m for your age: ({age["heartRate"]["min"]} - {age["heartRate"]["max"]})")  



def printMenu():
    print("\n==Patient Health Monitoring System==")
    print("Lab Results Converter: 1\nAverage Temperature Tracker: 2\nHeart Rate Monitor: 3\nPatient Hydration Tracker: 4")

def  menu():
    os.system("cls")
    running = True
    
    while running:
        try: 
            printMenu()
            userInput = input("Enter a number from the list: ")
            userInput = int(userInput)
        except ValueError:
            print("\033[0;31mPlease only enter a number from the list\033[0m")
            time.sleep(1)
            printMenu()
            os.system("cls")

        if userInput == 1:
            print("Going to Lab Results Converter")
            time.sleep(1)
            os.system("cls")
            running == False
            labUnitConverter()

        elif userInput == 2:
            print("Going to Average Temperature Tracker")
            time.sleep(1)
            os.system("cls")
            running == False
            average()

        elif userInput == 3:
            print("Going to Heart Rate Monitor")
            time.sleep(1)
            os.system("cls")
            running == False
            heartRateMonitor()




if __name__ == "__main__":
    try: 
        menu()
    except KeyboardInterrupt:
        os.system("cls")
        print("Bye: :(")
        time.sleep(1)
        os.system("cls")
