def taskOne():
    DOB = "05/12/2006"
    patientFirstName = "Alex"
    patientLastName = "Greenwood"
    patientHeight = "???"

    print(f"\033[1mPatient Info\033[0m\nPatient Name: {patientFirstName} {patientLastName}\nPatient Height: {patientHeight}\nPatient DOB: {DOB}")

def BMI():
    userInputHeight = input("Enter Your Height: ")
    userInputWeight = input("Enter Your Weight: ")
    try: 
        ##! math not mathing?
        bmi = (float(userInputWeight) / (float(userInputHeight) ** 2))

        if bmi >= 40:
            print(f"Your body mass index is: {bmi} which puts you in the \033[0;31mMorbidly Obese\033[0m group")
        elif 30 <= bmi >= 39.9:
            print(f"Your body mass index is: {bmi} which puts you in the \033[0;33mObese\033[0m group")
        elif 25 <= bmi >= 29.9:
            print(f"Your body mass index is: {bmi} which puts you in the \033[1;33mOver Weight\033[0m group")
        elif 18.5 <= bmi >= 24.9:
            print(f"Your body mass index is: {bmi} which puts you in the \033[0;32mNormal Weight\033[0m group")
        elif bmi <= 18.5:
            print(f"Your body mass index is: {bmi} which puts you in the \033[0;36mUnder Weight\033[0m group")

        else:
            print(f"Your body mass index is: {bmi} which puts you in the \033[0;31mUnknown\033[0m group. Your BMI might be too high or low")

                    
    except ValueError or TypeError:
        print(f"\033[31mEnter A Numbers\033[0m")


def dosage():
    import os
    MAXDOSAGE = 5
    currentDosage = 0
    alive = True
    while alive:
        os.system("cls")
        print(f"Patients current dosage is: {currentDosage}")
        userInput = input("Give the patient a dose? (y/n): ")

        if userInput.lower() == ("y"):
            currentDosage += 1
            print(f"You gave them a dose, their current amount is: {currentDosage}" )
        elif userInput.lower() == ("n"):
            break
        else: 
            pass
        if currentDosage == 5:
            print(f"\033[0;31mPatient has reached their max dose.\033[0m")
        if currentDosage > 5:
            print(f"\033[0;31mPatient is over the max dose......\033[0m")
            alive = False


def menu():
    import time
    import os
    menu = True

    while menu:
        os.system("cls")
        userinput = int(input("Select which task to run\n1: TaskOne\n2: BMI\n3: dosage\n4: exit\nEnter A Number: "))
        if userinput == 1:
            print("Running: taskOne()")
            time.sleep(1)
            os.system("cls")
            taskOne()
            menu = False

        elif userinput == 2:
            print("Running: BMI()")
            time.sleep(1)
            os.system("cls")
            BMI()
            menu = False

        elif userinput == 3:
            print("Running: dosage()")
            time.sleep(1)
            os.system("cls")
            dosage()
            menu = False

        elif userinput == 4:
            print("Bye!")
            time.sleep(1)
            os.system("cls")
            menu = False
        else: 
            os.system("cls")
            print("Please enter a number from 1 - 4")
            time.sleep(1)
            

if __name__ == "__main__":
    try:
        menu()
    except:
        print("Something went wrong")
