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

##! so broken, math isnt mathing in my head
def heartRateMonitor():
    userAgeInput = int(input("Enter your age: "))
    userHeartInput = int(input("Enter resting heart: "))

    maxHeart = 206.9 - (0.67 * userAgeInput)
    maxHeartRate = 220 - userAgeInput

    if userHeartInput > 100:
        print("get help")
    
    if userHeartInput < 60:

    
        print("also get help",maxHeartRate)
    elif 59 > userHeartInput > 101:
        print("normal")

