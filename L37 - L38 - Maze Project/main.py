import os
import time
import random
import msvcrt
import shutil
from typing import TypeAlias

mazeSizeX: int = 100
mazeSizeY: int = 20

wallChars: str = "█"
playerChars: str = "☻"
goalChars: str = "G"
pathChar: str = "░"
visitedChar: str = " "

goldGradient: list[str] = [
    "#FFF4B0",
    "#FFE082",
    "#FFD54F",
    "#F4B400",
    "#C98900",
]

bigText: dict[str, list[str]] = {
    "Y": ["█   █", " █ █ ", "  █  ", "  █  ", "  █  "],
    "O": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "U": ["█   █", "█   █", "█   █", "█   █", " ███ "],
    "W": ["█   █", "█   █", "█ █ █", "██ ██", "█   █"],
    "I": ["█████", "  █  ", "  █  ", "  █  ", "█████"],
    "N": ["█   █", "██  █", "█ █ █", "█  ██", "█   █"],
    " ": ["   ", "   ", "   ", "   ", "   "],
}

Cell: TypeAlias = str
Maze: TypeAlias = list[list[Cell]]
Position: TypeAlias = tuple[int, int]
DirectionMap: TypeAlias = dict[str, Position]


def createMaze(sizeX: int, sizeY: int) -> Maze:
    width: int = sizeX * 2 + 1
    height: int = sizeY * 2 + 1

    maze: Maze = [[wallChars for _ in range(width)] for _ in range(height)]

    def carve(x: int, y: int) -> None:
        maze[y][x] = pathChar

        directions: list[Position] = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for directionX, directionY in directions:
            newX: int = x + directionX
            newY: int = y + directionY

            if 1 <= newX < width - 1 and 1 <= newY < height - 1:
                if maze[newY][newX] == wallChars:
                    wallX: int = x + directionX // 2
                    wallY: int = y + directionY // 2

                    maze[wallY][wallX] = pathChar
                    carve(newX, newY)

    carve(1, 1)

    maze[1][1] = playerChars
    maze[height - 2][width - 2] = goalChars
    return maze

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def moveCursorTopLeft() -> None:
    print("\033[H", end="")


def hideCursor() -> None:
    print("\033[?25l", end="")


def showCursor() -> None:
    print("\033[?25h", end="")


def colourText(textString: str, hexColour: str) -> str:
    hexColour = hexColour.lstrip("#")
    red, green, blue = (int(hexColour[i:i + 2], 16) for i in (0, 2, 4))
    return f"\x1b[38;2;{red};{green};{blue}m{textString}\033[0m"


def colourCell(cell: str) -> str:
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
def getMazeDisplaySize(sizeX: int, sizeY: int) -> tuple[int, int]:
    mazeWidth: int = sizeX * 2 + 1
    mazeHeight: int = sizeY * 2 + 1
    return mazeWidth, mazeHeight

def getMaxMazeSizeForTerminal() -> tuple[int, int, int, int]:
    terminalSize = shutil.get_terminal_size(fallback=(80, 24))
    terminalWidth: int = terminalSize.columns
    terminalHeight: int = terminalSize.lines

    extraLines: int = 2

    maxDisplayWidth: int = terminalWidth
    maxDisplayHeight: int = terminalHeight - extraLines

    maxSizeX: int = (maxDisplayWidth - 2) // 2
    maxSizeY: int = (maxDisplayHeight - 2) // 2

    return maxSizeX, maxSizeY, terminalWidth, terminalHeight


def askToShrinkMaze(sizeX: int, sizeY: int) -> tuple[int | None, int | None]:
    mazeWidth, mazeHeight = getMazeDisplaySize(sizeX, sizeY)
    maxSizeX, maxSizeY, terminalWidth, terminalHeight = getMaxMazeSizeForTerminal()

    extraLines: int = 2
    fits: bool = mazeWidth <= terminalWidth and (mazeHeight + extraLines) <= terminalHeight

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
            choice: str = input(colourText("Shrink maze to fit terminal? (Y/N): ", "#a9fcff")).strip().upper()

            if choice == "Y":
                return maxSizeX, maxSizeY
            if choice == "N":
                return None, None

            print("Please enter Y or N.")
    finally:
        hideCursor()


def resolveMazeSize(sizeX: int, sizeY: int) -> tuple[int | None, int | None]:
    moveCursorTopLeft()
    clear()
    return askToShrinkMaze(sizeX, sizeY)


def displayMaze(maze: Maze) -> None:
    for row in maze:
        print("".join(colourCell(cell) for cell in row))
    print()


def setPlayerPos(player: Position, maze: Maze, lastPos: Position, goalPos: Position) -> Maze:
    if lastPos == goalPos:
        maze[lastPos[1]][lastPos[0]] = goalChars
    else:
        maze[lastPos[1]][lastPos[0]] = visitedChar

    maze[player[1]][player[0]] = playerChars[0]
    return maze


def movePlayer(player: Position, directionX: int, directionY: int) -> Position:
    return player[0] + directionX, player[1] + directionY


def canMove(player: Position, maze: Maze, directionX: int, directionY: int) -> bool:
    newX: int = player[0] + directionX
    newY: int = player[1] + directionY
    return maze[newY][newX] != wallChars


def buildBigText(text: str) -> list[str]:
    rows: list[str] = [""] * 5

    for char in text:
        pattern: list[str] = bigText.get(char, bigText[" "])
        for i in range(5):
            rows[i] += pattern[i] + "  "

    return rows


def scaleTextRows(rows: list[str], scale: int) -> list[str]:
    scaledRows: list[str] = []

    for row in rows:
        expandedRow: str = "".join(char * scale for char in row)
        for _ in range(scale):
            scaledRows.append(expandedRow)

    return scaledRows

def drawWinBanner(maze: Maze) -> bool:
    textRows: list[str] = buildBigText("YOU WIN")

    mazeHeight: int = len(maze)
    mazeWidth: int = len(maze[0])

    targetWidth: int = int(mazeWidth * 0.6)
    baseWidth: int = max(len(row) for row in textRows)
    scale: int = max(1, targetWidth // baseWidth)

    scaledRows: list[str] = scaleTextRows(textRows, scale)
    bannerHeight: int = len(scaledRows)
    bannerWidth: int = max(len(row) for row in scaledRows)

    while (bannerWidth > mazeWidth - 2 or bannerHeight > mazeHeight - 2) and scale > 1:
        scale -= 1
        scaledRows = scaleTextRows(textRows, scale)
        bannerHeight = len(scaledRows)
        bannerWidth = max(len(row) for row in scaledRows)

    if bannerWidth > mazeWidth - 2 or bannerHeight > mazeHeight - 2:
        return False

    startY: int = (mazeHeight - bannerHeight) // 2
    startX: int = (mazeWidth - bannerWidth) // 2

    padding: int = max(1, scale)

    clearTop: int = max(1, startY - padding)
    clearBottom: int = min(mazeHeight - 1, startY + bannerHeight + padding)
    clearLeft: int = max(1, startX - padding)
    clearRight: int = min(mazeWidth - 1, startX + bannerWidth + padding)

    for y in range(clearTop, clearBottom):
        for x in range(clearLeft, clearRight):
            maze[y][x] = visitedChar

    for rowIndex, row in enumerate(scaledRows):
        colour: str = goldGradient[min(rowIndex, len(goldGradient) - 1)]
        for colIndex, char in enumerate(row):
            if char != " ":
                maze[startY + rowIndex][startX + colIndex] = colourText(char, colour)

    return True


def showWinScreen(maze: Maze) -> None:
    moveCursorTopLeft()

    if drawWinBanner(maze):
        displayMaze(maze)
    else:
        displayMaze(maze)
        print(colourText("YOU WIN", "#FFCA3A"))


def askPlayAgain() -> bool:
    showCursor()
    try:
        while True:
            choice: str = input(colourText("Play again? (Y/N): ", "#a9fcff")).strip().upper()

            if choice == "Y":
                return True
            if choice == "N":
                return False

            print("Please enter Y or N.")
    finally:
        hideCursor()


def playRound(sizeX: int, sizeY: int) -> bool:
    mazeMap: Maze = createMaze(sizeX, sizeY)
    player: Position = (1, 1)
    goalPos: Position = (len(mazeMap[0]) - 2, len(mazeMap) - 2)
    lastPos: Position = player

    directions: DirectionMap = {
        "W": (0, -1),
        "D": (1, 0),
        "S": (0, 1),
        "A": (-1, 0),
    }

    clear()

    while True:
        moveCursorTopLeft()
        mazeMap = setPlayerPos(player=player, maze=mazeMap, lastPos=lastPos, goalPos=goalPos)
        displayMaze(mazeMap)
        print("Use WASD to move. Press Q to quit.")

        playerInput: str = msvcrt.getch().decode("utf-8", errors="ignore").upper()

        if playerInput == "Q":
            return False

        if playerInput in directions:
            directionX, directionY = directions[playerInput]

            if canMove(player, mazeMap, directionX, directionY):
                lastPos = player
                player = movePlayer(player, directionX, directionY)

                if player == goalPos:
                    mazeMap = setPlayerPos(player=player, maze=mazeMap, lastPos=lastPos, goalPos=goalPos)
                    showWinScreen(mazeMap)
                    return True

        time.sleep(0)


def main() -> None:
    requestedSizeX: int = mazeSizeX
    requestedSizeY: int = mazeSizeY

    sizeX, sizeY = resolveMazeSize(requestedSizeX, requestedSizeY)

    if sizeX is None or sizeY is None:
        print("Exiting...")
        return

    while True:
        won: bool = playRound(sizeX, sizeY)

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