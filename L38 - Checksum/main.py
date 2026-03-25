def main():
    userInput = input("Enter parcel code: ")
    if len(userInput) == 7:   
        try:
            lastDigit = userInput[-1:]
            restOfDigit = userInput[:-1]
            checkSum = 0
            for index, value in enumerate(restOfDigit):
                checkSum = checkSum + ((index + 1) * int(value))

            if (checkSum % 10) == int(lastDigit):
                print("Is Valid")
            else:
                print("Is Not Valid")
        except ValueError:
            print("Please Enter A Number!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye :(")