def medicine():
    try:
        userAge: int = int(input("Enter Age: "))
        userWeight: float = float(input("Enter Weight in kg: "))

        if userAge >= 12 and userWeight >= 40:
            print("Safe")
        else: 
            print("Not Safe")
    except ValueError:
        print("Please only enter a number for the age, or a float for the weight")

def fitnessAcces():
    try: 
        userAge: int = int(input("Enter Age: "))
        userHasMedicalClearance: str = str(input("Please enter True Or False: if you have a Medical Clearance: "))

        if userAge >= 18 and userHasMedicalClearance.lower() in ("t"):
            print("You can enter Intensive Zone")
        else: 
            print("You cant enter the Intensive Zone")

    except ValueError:
        print("Please only enter a number for the age, or a true or false for the clearnace")

def sleepTrack():
    try:
        userHeartRate: int = int(input("Enter Heart Rate: "))
        userAsleep: str = str(input("User Asleep: "))

        if not userAsleep in ("y") and userHeartRate > 100:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        else: 
            pass

    except ValueError:
        print("Please enter a number for an age, and a string if user is asleep")

def menu():
    pass

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("BYE!")
