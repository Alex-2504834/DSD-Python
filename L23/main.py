import csv

FILENAME = "scores.csv"
fileNames = ["name", "score"]

def addScore(username, score):
    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        
        writer.writerow([username, score])
        

def showScores():
    with open(FILENAME, newline="") as file:
        reader = csv.DictReader(file, fieldnames=fileNames)
        for row in reader:
            print(f"{row["name"]} | {row["score"]}")
        
    
def formHead():
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fileNames)
        writer.writeheader()

def main():
    formHead()
    while True:
        print("\n1. Add score")
        print("2. Show all scores")
        print("3. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            try:
                score = int(input("Enter score: "))
                if 0 <= score <= 100:
                    addScore(username, score)
                else:
                    raise ValueError
            except ValueError:
                print("Please only enter a number between 0 and 100")
                
        elif choice == "2":
            showScores()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()