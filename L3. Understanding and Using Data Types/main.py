def average():
    numberList: list = []

    print("Enter a score and hit enter, finish by typing f")
    def score():
        userInput = input()
        try:
            int(userInput)
            numberList.append(int(userInput))
        except:
            pass
        if userInput in ("f"):
            length: int = len(numberList)
            addedNumbers: float = 0
            for numbers in numberList:
                addedNumbers += numbers
            print(f"Entered a total of: {numberList} scores")
            try: 
                final: float = addedNumbers / length
                print(f"Average: {final}")
            except ZeroDivisionError:
                score()

        else:
            score()

def nameAnswer() -> bool:
    userFirstName: str = input("Enter first name: ")
    print(f"You Entered: {userFirstName}")
    userLastName: str = input("Enter last name: ")
    print(f"You Entered: {userFirstName}")
    userFullName: str = userFirstName + userLastName

    if len(userFullName) >= 20:
        print("Please Enter a name less then 20 chars long")
        print(f"Like: {userFullName[:20]}")
        return False
    else: 
        print(f"Your user name is: {userFullName}")

if __name__ == "__main__":
    try:
        #average()
        nameAnswer()
    except KeyboardInterrupt:
        print("Bye! :(")
