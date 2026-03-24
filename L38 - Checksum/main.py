def main():
    userInput = input("Enter parcel code: ")
    if len(userInput) == 7:   

        lastDigit = userInput[-1:]
        restOfDigit = userInput[:-1]
        print(f"{restOfDigit = }")
        print(f"{lastDigit = }")

        temp = ""
        for index, value in enumerate(restOfDigit):
            
            print(index, value)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye :(")