import os
from typing import List, Optional

#? Optional is cool lets me like say i might want to return something.

#* works on linux now, woooo
def clearScreen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


#? got sick of the input statement
def prompt(msg: str) -> str:
    try:
        return input(msg).strip()
    except KeyboardInterrupt:
        raise KeyboardInterrupt

def parseIndex(string: str) -> Optional[int]:
    if not string.isdigit():
        return None
    index = int(string)
    return index - 1 if index >= 1 else None

def splitItems(string: str) -> List[str]:
    return [part.strip() for part in string.split(",") if part.strip()]


def runList(title: str, itemLabel: str, initial: Optional[List[str]] = None) -> None:
    items: List[str] = list(initial or [])
    commands = {
        "a": "add",
        "r": "remove",
        "l": "list",
        "c": "clear",
        "h": "help",
        "q": "quit",
    }

    helpText = (
        f"\n{title} - Commands:\n"
        "  a | add      Add one or more items (comma-separated)\n"
        "  r | remove   Remove by number (1..n) or exact name\n"
        "  l | list     Show current list\n"
        "  c | clear    Clear the screen\n"
        "  h | help     Show this help\n"
        "  q | quit     Exit\n"
    )

    while True:
        clearScreen()
        print(f"{title}\n{'-' * len(title)}")
        if items:
            print(f"Current {itemLabel}s:")
            for index, it in enumerate(items, start=1):
                print(f"  {index}. {it}")
        else:
            print(f"No {itemLabel}s yet. Use 'a' to add some")
        print("\nType a command (h for help): ", end="")

        try:
            cmdRaw = prompt("")
        except KeyboardInterrupt:
            print("\nBye!")
            break

        if not cmdRaw:
            continue

        cmd = cmdRaw.lower()
        cmd = commands.get(cmd, cmd)

        if cmd in ("q", "quit", "exit"):
            clearScreen()
            print("Bye!")
            break

        elif cmd in ("h", "help"):
            print(helpText)
            input("Press Enter to continue: ")
            continue

        elif cmd in ("l", "list"):
            input("\nPress Enter to continue: ")
            continue

        elif cmd in ("c", "clear"):
            #* we already clearing
            continue

        elif cmd in ("a", "add"):
            try:
                raw = prompt(f"Enter {itemLabel}s (comma-separated): ")
            except KeyboardInterrupt:
                print("\nCancelled")
                input("Press Enter to continue: ")
                continue

            newItems = splitItems(raw)
            if not newItems:
                print("Nothing to add")
                input("Press Enter to continue: ")
                continue

            items.extend(newItems)
            print(f"Added {len(newItems)} {itemLabel}(s)")
            input("Press Enter to continue: ")
            continue

        elif cmd in ("r", "remove"):
            if not items:
                print("List is empty : nothing to remove")
                input("Press Enter to continue: ")
                continue

            try:
                raw = prompt(f"Remove {itemLabel} by number or exact name: ")
            except KeyboardInterrupt:
                print("\nCancelled")
                input("Press Enter to continue: ")
                continue

            if not raw:
                print("Nothing entered")
                input("Press Enter to continue: ")
                continue

            index = parseIndex(raw)
            if index is not None:
                if 0 <= index < len(items):
                    removed = items.pop(index)
                    print(f"Removed: {removed}")
                else:
                    print("Invalid number")
                input("Press Enter to continue: ")
                continue

            if raw in items:
                items.remove(raw)
                print(f"Removed: {raw}")
            else:
                #? 404 :)
                print(f"'{raw}' not found")
            input("Press Enter to continue: ")
            continue

        else:
            print("Unknown command. Type 'h' for help")
            input("Press Enter to continue: ")


def musiclist() -> None:
    runList(title="Music List Manager", itemLabel="song")

def movielist() -> None:
    runList(title="Movie List Manager", itemLabel="movie")

if __name__ == "__main__":
    try:
        movielist()
    except KeyboardInterrupt:
        print("\nBye!")
