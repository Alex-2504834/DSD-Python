import os
import time
import random

mazeSizeX, mazeSizeY = 10, 10

mazeMap = [
    ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"],
    ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
    ]



def clear() -> None:
	os.system("cls" if os.name == "nt" else "clear")

def displayMaze(maze):
    for walls in maze:
        for keys, cells in enumerate(walls):
            if keys == 0:
                print("")
            print(cells, end="")
    print("\n")

def setPlayerPos(player, map, lastPos):
    map[lastPos[1]][lastPos[0]] = "."
    map[player[1]][player[0]] = "P"
    return map

def temp(player, x, y):
    #?[1] = X [0] = Y
    return (player[0] + x, player[1] + y)


def main() -> None:
    player = (1,1)
    lastPos = player
    running=True
    while running:
        maze = setPlayerPos(player=player, map=mazeMap, lastPos=lastPos)
        displayMaze(maze)
        playerInput = input("Enter direction (N, E, S, W): ").upper().strip()
        match playerInput:
            case "N":
                if mazeMap[player[1]-1][player[0]] == "#":
                    continue
                lastPos = player
                player = temp(player, 0, -1)

            case "E":
                if mazeMap[player[1]][player[0]+1] == "#":
                    continue
                lastPos = player
                player = temp(player, 1, 0)

            case "S":
                if mazeMap[player[1]+1][player[0]] == "#":
                    continue
                lastPos = player
                player = temp(player, 0, 1)

            case "W":
                if mazeMap[player[1]][player[0]-1] == "#":
                    continue
                lastPos = player
                player = temp(player, -1, 0)
            case _:
                pass

        time.sleep(0.2)
        clear()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye :(")