import os, time

def musicList() -> None:
    def clearOutput():
        os.system("cls")

    music: list[str] = []
    running: bool = True
    currentMode: str = ""
    clearOutput()

    while running:
        print(f"Current Mode: {currentMode}")
        if currentMode == "":
            print("Entet a mode to enter: Addition (a), Removal (r), Current List (l)")
            userInput: str = input()
            if userInput == "a":
                currentMode = "add"
                clearOutput()
            elif userInput == "r":
                currentMode = "remove"
                clearOutput()
            elif userInput == "l":
                clearOutput()
                for index, songs in enumerate(music):
                    print(f"Song {index}: {songs.lstrip()}")
                    currentMode = ""
            elif userInput == "exit":
                clearOutput()
                print("Bye!")
                break
            else:
                clearOutput()
                print("Please only enter \"a\" or \"r\" or \"l\"")

        while currentMode == "add":
            clearOutput()
            print(f"Current Mode: {currentMode}")
            userInput: str = input("Enter Top 5 Songs: ")
            music: list[str] = userInput.split(",")
            for index, songs in enumerate(music):
                print(f"Song {index}: {songs.lstrip()}")
                currentMode = ""

        while currentMode == "remove":
            clearOutput()
            print(f"Current Mode: {currentMode}")
            print("Current song list:")
            for index, songs in enumerate(music):
                print(f"Song {index}: {songs.lstrip()}")

            print("Select a song number to remove: ")
            userSongInput: int = int(input(""))

            print(f"Removing {music[userSongInput]}")

            music.remove(music[userSongInput])
            currentMode = ""

def movieList() -> None:
    def clearOutput():
        os.system("cls")

    music: list[str] = []
    running: bool = True
    currentMode: str = ""
    clearOutput()

    while running:
        print(f"Current Mode: {currentMode}")
        if currentMode == "":
            print("Entet a mode to enter: Addition (a), Removal (r), Current List (l)")
            userInput: str = input().lower()
            if userInput == "a":
                currentMode = "add"
                clearOutput()
            elif userInput == "r":
                currentMode = "remove"
                clearOutput()
            elif userInput == "l":
                clearOutput()
                for index, songs in enumerate(music):
                    print(f"Movie {index}: {songs.lstrip()}")
                    currentMode = ""
            elif userInput == "exit":
                clearOutput()
                print("Bye!")
                break
            else:
                clearOutput()
                print("Please only enter \"a\" or \"r\" or \"l\"")

        while currentMode == "add":
            clearOutput()
            print(f"Current Mode: {currentMode}")
            userInput: str = input("Enter movies: ")
            music: list[str] = userInput.split(",")
            for index, songs in enumerate(music):
                print(f"Movie {index}: {songs.lstrip()}")
                currentMode = ""

        while currentMode == "remove":
            clearOutput()
            print(f"Current Mode: {currentMode}")
            print("Current movie list:")
            for index, songs in enumerate(music):
                print(f"Movie {index}: {songs.lstrip()}")

            print("Select a movie number to remove: ")
            userSongInput: int = int(input(""))

            print(f"Removing {music[userSongInput]}")

            music.remove(music[userSongInput])
            currentMode = ""

if __name__ == "__main__":
    try:
        movieList()
    except KeyboardInterrupt:
        print("\nBye")
