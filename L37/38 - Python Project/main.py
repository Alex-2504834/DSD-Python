import os
import time
import random
import msvcrt
import shutil

mazeSizeX, mazeSizeY = 100, 20

wallChars = "█"
playerChars = "☻"
goalChars = "G"
pathChar = "░"
visitedChar = " "

goldGradient = [
    "#FFF4B0",
    "#FFE082",
    "#FFD54F",
    "#F4B400",
    "#C98900",
]

bigText = {
    "Y": ["█   █", " █ █ ", "  █  ", "  █  ", "  █  "],
    "O": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "U": ["█   █", "█   █", "█   █", "█   █", " ███ "],
    "W": ["█   █", "█   █", "█ █ █", "██ ██", "█   █"],
    "I": ["█████", "  █  ", "  █  ", "  █  ", "█████"],
    "N": ["█   █", "██  █", "█ █ █", "█  ██", "█   █"],
    " ": ["   ", "   ", "   ", "   ", "   "],
}

def createMaze(sizeX, sizeY):
    width = sizeX * 2 + 1
    height = sizeY * 2 + 1

    maze = [[wallChars for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        maze[y][x] = pathChar

        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for directionX, directionY in directions:
            newX = x + directionX
            newY = y + directionY

            if 1 <= newX < width - 1 and 1 <= newY < height - 1:
                if maze[newY][newX] == wallChars:
                    wallX = x + directionX // 2
                    wallY = y + directionY // 2

                    maze[wallY][wallX] = pathChar
                    carve(newX, newY)

    carve(1, 1)

    maze[1][1] = playerChars
    maze[height - 2][width - 2] = goalChars
    return maze

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

#?Love these codes
def moveCursorTopLeft():
    print("\033[H", end="")

def hideCursor():
    print("\033[?25l", end="")

def showCursor():
    print("\033[?25h", end="")

def colourText(textString, hexColour):
    hexColour = hexColour.lstrip("#")
    red, green, blue = (int(hexColour[i:i + 2], 16) for i in (0, 2, 4))
    return f"\x1b[38;2;{red};{green};{blue}m{textString}\033[0m"


def colourCell(cell):
    match cell:
        case c if c in wallChars:
            return colourText(cell, "#8B8B8B")
        case c if c in playerChars:
            return colourText(cell, "#9CEC9C")
        case c if c in goalChars:
            return colourText(cell, "#FFD700")
        case c if c in pathChar:
            return colourText(cell, "#757575")
        case _:
            return cell
        
def getMazeDisplaySize(sizeX, sizeY):
    mazeWidth = sizeX * 2 + 1
    mazeHeight = sizeY * 2 + 1
    return mazeWidth, mazeHeight

def getMaxMazeSizeForTerminal():
    terminalSize = shutil.get_terminal_size(fallback=(80, 24))
    terminalWidth = terminalSize.columns
    terminalHeight = terminalSize.lines

    extraLines = 2

    maxDisplayWidth = terminalWidth
    maxDisplayHeight = terminalHeight - extraLines

    maxSizeX = (maxDisplayWidth - 2) // 2
    maxSizeY = (maxDisplayHeight - 2) // 2

    return maxSizeX, maxSizeY, terminalWidth, terminalHeight


def askToShrinkMaze(sizeX, sizeY):
    mazeWidth, mazeHeight = getMazeDisplaySize(sizeX, sizeY)
    maxSizeX, maxSizeY, terminalWidth, terminalHeight = getMaxMazeSizeForTerminal()

    extraLines = 2
    fits = mazeWidth <= terminalWidth and (mazeHeight + extraLines) <= terminalHeight

    if fits:
        return sizeX, sizeY

    if maxSizeX < 1 or maxSizeY < 1:
        print(colourText("Error: Terminal is too small to display even the minimum maze.", "#ff6b6b"))
        return None, None

    print(colourText("Error: Maze is too large for your terminal.", "#ff6b6b"))
    print(f"Current maze size  | {sizeX} x {sizeY}")
    print(f"Current display    | {mazeWidth} x {mazeHeight}")
    print(f"Terminal size      | {terminalWidth} x {terminalHeight}")
    print(f"Max maze that fits | {maxSizeX} x {maxSizeY}")
    print()

    showCursor()
    try:
        while True:
            choice = input(colourText("Shrink maze to fit terminal? (Y/N): ", "#a9fcff")).strip().upper()

            if choice == "Y":
                return maxSizeX, maxSizeY
            if choice == "N":
                return None, None

            print("Please enter Y or N.")
    finally:
        hideCursor()


def resolveMazeSize(sizeX, sizeY):
    moveCursorTopLeft()
    clear()
    return askToShrinkMaze(sizeX, sizeY)


def displayMaze(maze):
    for row in maze:
        print("".join(colourCell(cell) for cell in row))
    print()


def setPlayerPos(player, maze, lastPos, goalPos):
    if lastPos == goalPos:
        maze[lastPos[1]][lastPos[0]] = goalChars
    else:
        maze[lastPos[1]][lastPos[0]] = visitedChar

    maze[player[1]][player[0]] = playerChars[0]
    return maze


def movePlayer(player, directionX, directionY):
    return (player[0] + directionX, player[1] + directionY)


def canMove(player, maze, directionX, directionY):
    newX = player[0] + directionX
    newY = player[1] + directionY
    return maze[newY][newX] != wallChars


def buildBigText(text):
    rows = [""] * 5

    for char in text:
        pattern = bigText.get(char, bigText[" "])
        for i in range(5):
            rows[i] += pattern[i] + "  "

    return rows


def scaleTextRows(rows, scale):
    scaledRows = []

    for row in rows:
        expandedRow = "".join(char * scale for char in row)
        for _ in range(scale):
            scaledRows.append(expandedRow)

    return scaledRows

#?Hm complex
def drawWinBanner(maze):
    textRows = buildBigText("YOU WIN")

    mazeHeight = len(maze)
    mazeWidth = len(maze[0])

    targetWidth = int(mazeWidth * 0.6)
    baseWidth = max(len(row) for row in textRows)
    scale = max(1, targetWidth // baseWidth)

    scaledRows = scaleTextRows(textRows, scale)
    bannerHeight = len(scaledRows)
    bannerWidth = max(len(row) for row in scaledRows)

    while (bannerWidth > mazeWidth - 2 or bannerHeight > mazeHeight - 2) and scale > 1:
        scale -= 1
        scaledRows = scaleTextRows(textRows, scale)
        bannerHeight = len(scaledRows)
        bannerWidth = max(len(row) for row in scaledRows)

    if bannerWidth > mazeWidth - 2 or bannerHeight > mazeHeight - 2:
        return False

    startY = (mazeHeight - bannerHeight) // 2
    startX = (mazeWidth - bannerWidth) // 2

    padding = max(1, scale)

    clearTop = max(1, startY - padding)
    clearBottom = min(mazeHeight - 1, startY + bannerHeight + padding)
    clearLeft = max(1, startX - padding)
    clearRight = min(mazeWidth - 1, startX + bannerWidth + padding)

    for y in range(clearTop, clearBottom):
        for x in range(clearLeft, clearRight):
            maze[y][x] = visitedChar

    for rowIndex, row in enumerate(scaledRows):
        colour = goldGradient[min(rowIndex, len(goldGradient) - 1)]
        for colIndex, char in enumerate(row):
            if char != " ":
                maze[startY + rowIndex][startX + colIndex] = colourText(char, colour)

    return True


def showWinScreen(maze):
    moveCursorTopLeft()

    if drawWinBanner(maze):
        displayMaze(maze)
    else:
        displayMaze(maze)
        print(colourText("YOU WIN", "#FFCA3A"))


def askPlayAgain():
    showCursor()
    try:
        while True:
            choice = input(colourText("Play again? (Y/N): ", "#a9fcff")).strip().upper()

            if choice == "Y":
                return True
            if choice == "N":
                return False

            print("Please enter Y or N.")
    finally:
        hideCursor()


def playRound(sizeX, sizeY):
    mazeMap = createMaze(sizeX, sizeY)
    player = (1, 1)
    goalPos = (len(mazeMap[0]) - 2, len(mazeMap) - 2)
    lastPos = player

    directions = {
        "W": (0, -1),
        "D": (1, 0),
        "S": (0, 1),
        "A": (-1, 0),
    }

    clear()

    while True:
        moveCursorTopLeft()
        maze = setPlayerPos(player=player, maze=mazeMap, lastPos=lastPos, goalPos=goalPos)
        displayMaze(maze)
        print("Use WASD to move. Press Q to quit.")

        playerInput = msvcrt.getch().decode("utf-8", errors="ignore").upper()

        if playerInput == "Q":
            return False

        if playerInput in directions:
            directionX, directionY = directions[playerInput]

            if canMove(player, maze, directionX, directionY):
                lastPos = player
                player = movePlayer(player, directionX, directionY)

                if player == goalPos:
                    maze = setPlayerPos(player=player, maze=mazeMap, lastPos=lastPos, goalPos=goalPos)
                    showWinScreen(maze)
                    return True

        time.sleep(0)


def main() -> None:
    requestedSizeX = mazeSizeX
    requestedSizeY = mazeSizeY

    sizeX, sizeY = resolveMazeSize(requestedSizeX, requestedSizeY)

    if sizeX is None or sizeY is None:
        print("Exiting...")
        return

    while True:
        won = playRound(sizeX, sizeY)

        if not won:
            print(colourText("Exiting...", "#ff6b6b"))
            break

        if not askPlayAgain():
            print(colourText("Exiting...", "#ff6b6b"))
            break

        sizeX, sizeY = resolveMazeSize(requestedSizeX, requestedSizeY)

        if sizeX is None or sizeY is None:
            print(colourText("Exiting...", "#ff6b6b"))
            break


if __name__ == "__main__":
    try:
        hideCursor()
        main()
    except KeyboardInterrupt:
        print("\nBye :(")
    finally:
        showCursor()