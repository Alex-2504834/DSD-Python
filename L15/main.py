import time, os

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

arcades = { 
    "arcade1": {"name": "Arcade 1", "category": "???","status": "working"},
    "arcade2": {"name": "Arcade 2", "category": "???","status": "working"},
    "arcade3": {"name": "Arcade 3", "category": "???","status": "working"},
    "arcade4": {"name": "Arcade 4", "category": "???","status": "working"},
    "arcade5": {"name": "Arcade 5", "category": "???","status": "working"},
    "arcade6": {"name": "Arcade 6", "category": "???","status": "working"}
}

def listArcades():
    print("Key | Name | Category | Status")
    for arcade in arcades:
        print(f"{arcade} {arcades[arcade]["name"]} | {arcades[arcade]["category"]} | {arcades[arcade]["status"]}")

#! Very Very Cursed 
def editArcade():
    listArcades()
    if (userInput := input("Enter a key of the arcade to edit: ")) in arcades:
        clearScreen()
        print(f"Editing {userInput}")
        if (userInputEditType := input("Edit (n)ame, (c)ategory or (s)tatus: ")) in ("n", "name"):
            if (userInputName := input(f"Editing {arcades[userInput]["name"]}'s name | Enter a name: ")) != "":
                oldData = arcades[userInput]
                arcades[userInput] = {"name": userInputName, "category": oldData["category"], "status": oldData["status"]}
        
            else:
                print("Name cant be empty")

        elif userInputEditType in ("c", "category"):
            if (userInputCategory := input(f"Editing {arcades[userInput]["name"]}'s category | Enter a category: ")) != "":
                oldData = arcades[userInput]
                arcades[userInput] = {"name": oldData["name"], "category": userInputCategory, "status": oldData["status"]}

            else:
                print("Category cant be empty")

        elif userInputEditType in ("s", "status"):
            if (userInputStatus := input(f"Editing {arcades[userInput]["name"]}'s Status | Enter a status: ")) != "":
                oldData = arcades[userInput]
                arcades[userInput] = {"name": oldData["name"], "category": oldData["category"], "status": userInputStatus}
            else:
                print("Status cant be empty")
    else: 
        print(f"Unable to fine {userInput}")

def main ():
    while True:
        print("==Arcade==")
        listArcades()

        if (userInput := input("(e)dit | (l)ist | (exit): ")) in ("e", "edit"):
            clearScreen()
            editArcade()

        elif userInput in ("l", "list"):
            clearScreen()
            listArcades()

        elif userInput in ("exit"):
            clearScreen()
            print("Bye")
            time.sleep(1)
            clearScreen()
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clearScreen()
        print("Bye")
        time.sleep(1)
        clearScreen()