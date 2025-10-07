import time
import os
def calcArea() -> float:
    userInputWidth: float = float(input("Enter Width: "))
    userInputHeight: float = float(input("Enter Height: "))

    return userInputWidth * userInputHeight

def calcTime() -> None:
    userInputMinutes : float = float(input("Enter Time in minutes: "))

    print(f"{int(userInputMinutes)} minutes in hours is {int(userInputMinutes // 60)} hour", end="")

    if userInputMinutes % 60:
        print(f" and {int(userInputMinutes % 60)} minutes")



def hospital():
    userInputFirstName: str = input("Enter Patient First Name: ")
    userInputLastName: str = input("Enter Patient Last Name: ") 
    userInputAge: int = int(input("Enter Patient Age: "))
    userInputBill: float = float(input("Enter Patient Bill: "))


def passwordChecker():
    pass

def patientMenu():
    menu(patientMenuDict)



menuDict = {
    1: {
        "title": "calculate Area fo rectanagle",
        "func": calcArea,
        "sleep": 1
    },
    2: {
        "title": "Calculate Hours and minutes from minutes",
        "func": calcTime,
        "sleep": 1
    },
    3: {
        "title": "Patient Bill Calculator",
        "func": hospital,
        "sleep": 1
    },
    4: {
        "title": "Password Checker",
        "func": passwordChecker,
        "sleep": 1
    },
    5: {
        "title": "Patient Menu",
        "func": patientMenu,
        "sleep": 0
    }
}

patientMenuDict = {
    1: {
        "title": "idk",
        "func": "ill get to it",
        "sleep": 1
    },
    2: {
        "title": "idk",
        "func": "ill get to it",
        "sleep": 1
    },
    3: {
        "title": "idk",
        "func": "ill get to it",
        "sleep": 1
    }
}



def menu(menuList = menuDict):
    print("Enter the number for the option you want: ")

    #* Prints out the tiles with their option number from menuDict
    for key, value in menuList.items():
        print(f"{value["title"]}: {key}")

    try:
        userInput = int(input(""))
        userInput = int(userInput)

        #* Gets users input and calls the function from it.
        for key, value in menuList.items():
            if userInput == key:
                print(f"Going to: {value["title"]}")
                time.sleep(value["sleep"])
                os.system("cls")
                print(f"==={value["title"]}===")
                value["func"]()

        print("Enter a number from the list")

    except ValueError:
        print("Please only enter a number")
menu()




if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("Bye!")
        time.sleep(1)
        os.system("cls")
