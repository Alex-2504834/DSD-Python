
def taskOne() -> None:
    energy: list[str] = ["null energy", "tired", "normal", "chaotic", "god like energy"]
    userName: list[str] = ["Conner", "Alex", "Thomas", "Kye", "Mark"]
    stepCount: list[int] = [1200, 1500, 3000, 3141, 4000]


    def printList(listInput: list[str] | list[int]) -> None:
        print(listInput)

    def section(listInput: list[str] | list[int]) -> None:
        print(f"Start: {listInput[0]} | Middle: {listInput[len(listInput) // 2]} | End {listInput[-1]}")

    def add(listInput: list[str] | list[int], valueToAdd) -> None:
        listInput.append(valueToAdd)


    def main() -> None:
        printList(energy)
        section(energy)
        add(energy, "???")

        printList(userName)
        section(userName)
        add(userName, "Kieran")

        printList(stepCount)
        section(stepCount)
        add(stepCount, 5000)

    main()


def taskTwo() -> None:
    screenTimes: list[int] = [120, 95, 140, 160, 80, 100, 200]

    def printLastThreeDays() -> None:
        print(screenTimes[-3:])

    def average():
        print(sum(screenTimes[0:3])/3)

    def replace():
        temp = screenTimes[-1] = 300
        print(temp)

    def minMax():
        print(f"Min: {min(screenTimes)} | Max: {max(screenTimes)}")

    def main():
        printLastThreeDays()
        average()
        replace()
        minMax()

    main()

def taskThree():
    pass

def taskFour():
    import os
    notifications = [34, 28, 55, 40, 60, 22, 18]

    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")


    def printInfo():
        print("═══Notifications Stats═══")
        print(f"Highest Day: {max(notifications)}\nLowest Day: {min(notifications)}")
        print(f"Average: {sum(notifications)/len(notifications)}")
    
    def getUserInput():
        if (userInput := input("Enter A new Value: ")) == "exit":
            return True

        if userInput != "":
            try: 
                int(userInput)
                notifications.append(int(userInput))

            except ValueError:
                print("Please Only Enter A Number.")


    def main():
        running = True
        while running:
            clear()
            printInfo()
            if getUserInput():
                running = False

    main()


if __name__ == "__main__":
    taskFour()