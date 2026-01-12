import os, time

gameList: list[list] = [
    ["Minecraft", "", ""],
    ["Grand Theft Auto V","", ""],
    ["Wii Sports", "", ""],
    ["Mario Kart", "", ""],
    ["Red Dead Redemption", "", ""]
    ]


def printGameList(gameList: list[list] = gameList) -> None:
    print("Game Number | Game Name | Favourite | Playing")
    for gameListindex, games in enumerate(gameList):
            print(f"Game {gameListindex}: {games[0]}", end="")
            print(f" {games[1]}", end="")
            print(f" {games[2]}")

def printControlInfo() -> None:
    print("Type (a)dd to add more games | (r)emove to remove more games | (e)dit to edit more games")

def clearScreen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def addGameList():
    printGameList()
    if (userinput := input("Enter a game to add: ")) != "": 
        gameList.append([userinput, "", ""])

def removeGameList():
    printGameList()
    if (userinput := input("Enter a game to remove: ")) != "": 
        for gameListindex, games in enumerate(gameList):
             if games[0] == userinput:
                  
                gameList.pop(gameListindex)

def editGameList():
    printGameList()
    if (userinput := input("Enter a game to edit: ")) != "": 
        for games in gameList:
            if games[0] == userinput:
                print(f"Editing {games[0]}")
                print("Type (p)laying to add to playing | (f)avourite to add to favourite")
                userinput = input() 
                if userinput in ("p", "playing"):
                    for game in gameList:
                        game[1] = ""
                    games[1] = "Playing"

                if userinput in ("f", "favourite"):
                    games[2] = "Favourite"

currentMode: str = ""

while True:
      clearScreen()
      printGameList()
      printControlInfo()
      if currentMode == "":
            userinput = input().lower()
            if userinput in ("a", "add"):
                clearScreen()
                addGameList()
                
            elif userinput in ("r", "remove"):
                clearScreen()
                removeGameList()
                

            elif userinput in ("e", "edit"):
                clearScreen()
                editGameList()
                