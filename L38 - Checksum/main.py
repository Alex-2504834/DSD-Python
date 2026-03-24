def main():
    userInput = input("Enter parcel code: ")
    if len(userInput) == 7:   

        lastDigit = userInput[-1:]
        restOfDigit = userInput[:-1]
        print(f"{restOfDigit = }")
        print(f"{lastDigit = }")

        checkSum = 0
        for index, value in enumerate(restOfDigit):
            checkSum = checkSum + ((index + 1) * int(value))
        print(checkSum)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye :(")