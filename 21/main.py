import random

def taskOne():
    randomNames = ["connor", "alex", "kye", "thomas", "theo", "charlie", "Nathaniel"]

    with open("temp.txt", "a") as file:

        for _ in range(1000000):
            file.write(f"{randomNames[random.randint(0, len(randomNames)-1)].capitalize()} | {random.randint(0, 10000)}\n")


    with open("temp.txt", "r") as file:
        for lines in file:
            print(lines.strip())

def taskTwo():
    try:
        if ((userNameInput := input("Enter Name: ")) != "") and ((userScoreInput := input("Enter Score: ")) != ""):
            try:
                with open("score.txt", "a") as file:
                    file.write(f"Username: {userNameInput} | Score: {userScoreInput}\n")
                    print(f"Wrote: Username: {userNameInput} | Score: {userScoreInput}")
            except PermissionError:
                print("Unable to open file")

        else:
            print("Please Enter Something")
    except KeyboardInterrupt:
        print("\n")
        with open("score.txt", "r") as file:
            for lines in file:
                print(lines.strip())

if __name__ == "__main__":
    taskTwo()