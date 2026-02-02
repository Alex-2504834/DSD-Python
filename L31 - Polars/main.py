import polars as pl
from functools import cache
from pathlib import Path
import customtkinter as ctk
from typing import Dict, List, Sequence, Tuple, Any

csvPath = "L31 - Polars/pixelvault game sales.csv"

@cache
def createDataFrame(path: Path) -> pl.DataFrame:
    return pl.read_csv(source=path, null_values="")

def printColumnNames(data: pl.DataFrame) -> None:
    print("Column names:")
    for column in data.columns:
        print(column)

def checkForMissingValues(data: pl.DataFrame):
    pass

def main() -> None:
    dataFrame = createDataFrame(csvPath)

    
    #print(dataFrame.head(5))
    #print(dataFrame.tail(5))
    #print(dataFrame.describe())
    #printColumnNames(dataFrame)


    mainApp = Main()
    mainApp.mainloop()





columnDef = Tuple[str, str, int]


class virtualizedTable(ctk.CTkFrame):
    def __init__(self, master: Any, *,
        columns: Sequence[columnDef], rowHeight: int = 34,
        overscan: int = 2, maxPool: int = 30, rowPady: int = 2) -> None:
        super().__init__(master)
        self.columns: List[columnDef] = list(columns)
        self.rowHeight: int = rowHeight
        self.overscan: int = overscan
        self.maxPool: int = maxPool
        self.rowPady: int = rowPady

        self.itemsAll: List[Dict[str, str]] = []
        self.itemsView: List[Dict[str, str]] = []
        self.startIndex: int = 0

        self.poolRows: List[Dict[str, Any]] = []
        self.poolSize: int = 0

        self.poolContainer: ctk.CTkFrame
        self.scrollbar: ctk.CTkScrollbar

        self._buildUi()

    def _buildUi(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header: ctk.CTkFrame = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=6, pady=(4, 6))

        for colIdx, (_key, title, weight) in enumerate(self.columns):
            header.grid_columnconfigure(colIdx, weight=weight, uniform="cols")
            label: ctk.CTkLabel = ctk.CTkLabel(header, text=title, anchor="w")
            label.grid(row=0, column=colIdx, sticky="ew", padx=(8, 4) if colIdx < len(self.columns) - 1 else (8, 8))

        self.poolContainer = ctk.CTkFrame(self)
        self.poolContainer.grid(row=1, column=0, sticky="nsew")
        self.poolContainer.grid_columnconfigure(0, weight=1)

        self.scrollbar = ctk.CTkScrollbar(self, command=self.onScrollbar)
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(6, 4), pady=(2, 2))

        self.poolContainer.bind("<Configure>", lambda _e: self.after(10, self.rebuildPool), add=True)

    def setItems(self, items: List[Dict[str, str]]) -> None:
        self.itemsAll = list(items)
        self.itemsView = list(items)
        self.startIndex = 0
        self.rebuildPool()
        self.rebindRows()

    def visibleRowCount(self) -> int:
        return max(1, self.poolSize - self.overscan)

    def rowStride(self) -> int:
        return self.rowHeight + (self.rowPady * 2)

    def clampStartIndex(self) -> None:
        totalCount: int = len(self.itemsView)
        if totalCount <= 0:
            self.startIndex = 0
            return

        visibleCount: int = self.visibleRowCount()
        maxStartIndex: int = max(0, totalCount - visibleCount)

        if self.startIndex < 0:
            self.startIndex = 0
        elif self.startIndex > maxStartIndex:
            self.startIndex = maxStartIndex

    def rebuildPool(self) -> None:
        viewportHeight: int = max(1, int(self.poolContainer.winfo_height()))
        rowsFit: int = max(1, viewportHeight // self.rowStride())
        desiredPoolSize: int = min(rowsFit + self.overscan, self.maxPool)

        if desiredPoolSize == self.poolSize and self.poolRows:
            self.rebindRows()
            self.updateThumb()
            return

        for poolRow in self.poolRows:
            try:
                rowFrame: ctk.CTkFrame = poolRow["frame"]
                rowFrame.destroy()
            except Exception:
                pass
        self.poolRows.clear()

        for poolRowIndex in range(desiredPoolSize):
            rowFrame = ctk.CTkFrame(self.poolContainer, height=self.rowHeight)
            rowFrame.grid(row=poolRowIndex, column=0, sticky="ew", padx=4, pady=self.rowPady)
            rowFrame.grid_propagate(False)

            for colIndex, (_key, _title, weight) in enumerate(self.columns):
                rowFrame.grid_columnconfigure(colIndex, weight=weight, uniform="cols")

            varsByKey: Dict[str, ctk.StringVar] = {}
            for colIndex, (key, _title, _weight) in enumerate(self.columns):
                var: ctk.StringVar = ctk.StringVar(value="")
                varsByKey[key] = var
                label = ctk.CTkLabel(rowFrame, textvariable=var, anchor="w")
                label.grid(row=0, column=colIndex, sticky="ew", padx=(8, 4) if colIndex < len(self.columns) - 1 else (8, 8), pady=4)

            self.poolRows.append({"frame": rowFrame, "vars": varsByKey})

        self.poolSize = desiredPoolSize
        self.rebindRows()
        self.updateThumb()

    def rebindRows(self) -> None:
        if not self.poolRows:
            return

        self.clampStartIndex()

        totalCount: int = len(self.itemsView)
        for poolRowOffset, poolRow in enumerate(self.poolRows):
            dataIndex: int = self.startIndex + poolRowOffset
            varsByKey: Dict[str, ctk.StringVar] = poolRow["vars"]

            if dataIndex >= totalCount:
                for key, _title, _weight in self.columns:
                    varsByKey[key].set("")
                continue

            item: Dict[str, str] = self.itemsView[dataIndex]
            for key, _title, _weight in self.columns:
                varsByKey[key].set(item.get(key, ""))

        self.updateThumb()

    def updateThumb(self) -> None:
        totalCount: int = len(self.itemsView)
        visibleCount: int = self.visibleRowCount()

        if totalCount <= visibleCount:
            try:
                self.scrollbar.set(0.0, 1.0)
            except Exception:
                pass
            return

        firstFrac: float = self.startIndex / totalCount
        lastFrac: float = (self.startIndex + visibleCount) / totalCount
        try:
            self.scrollbar.set(firstFrac, lastFrac)
        except Exception:
            pass

    def onScrollbar(self, *args: Any) -> None:
        if not args:
            return

        op: Any = args[0]
        if op == "moveto":
            try:
                frac: float = float(args[1])
            except Exception:
                return

            totalCount: int = len(self.itemsView)
            visibleCount: int = self.visibleRowCount()
            maxStartIndex: int = max(0, totalCount - visibleCount)

            self.startIndex = int(round(frac * maxStartIndex))
            self.rebindRows()

        elif op == "scroll":
            try:
                count: int = int(args[1])
            except Exception:
                return

            what: Any = args[2] if len(args) > 2 else "units"
            step: int = self.visibleRowCount() if what == "pages" else 3

            self.startIndex += count * step
            self.rebindRows()

    def onMouseWheel(self, event: Any) -> None:
        delta: int = 0
        try:
            if getattr(event, "delta", 0):
                delta = 1 if event.delta > 0 else -1
            elif getattr(event, "num", None) == 4:
                delta = 1
            elif getattr(event, "num", None) == 5:
                delta = -1
        except Exception:
            delta = 0

        if delta != 0:
            self.startIndex -= delta * 3
            self.rebindRows()

    def scrollPages(self, pages: int) -> None:
        self.startIndex += pages * self.visibleRowCount()
        self.rebindRows()

    def scrollHome(self) -> None:
        self.startIndex = 0
        self.rebindRows()

    def scrollEnd(self) -> None:
        totalCount: int = len(self.itemsView)
        self.startIndex = max(0, totalCount - self.visibleRowCount())
        self.rebindRows()







class Main(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.title("Polars GUI")
        self.geometry("800x600")


        self.tabView: ctk.CTkTabview = ctk.CTkTabview(self)
        self.tabView.pack(expand=True, fill="both", padx=10, pady=10)
        self.tabView.add("Main")
        self.tabView.add("Other")


        self.mainTabFrame: ctk.CTkFrame = self.tabView.tab("Main")

        self.mainTable = virtualizedTable(self.mainTabFrame, columns=[
                ("sale_id", "Sale ID", 25),
                ("sale_date", "Sale Date", 25),
                ("game_title", "Game Title", 25),
                ("category", "Category", 25),
                ("platform", "Platform", 25),
                ("price", "Price", 25),
                ("quantity", "Quantity", 25),
                ("total_sale", "Total Sale", 25),
            ],
        )
        self.mainTable.pack(fill="both", expand=True, padx=12, pady=12)
        self.load(createDataFrame(csvPath))
    def load(self, dataFrame: pl.DataFrame):
        items: List[Dict[str, str]] = []

        for row in dataFrame.to_dict():
            for index, _ in enumerate(dataFrame.to_dict()[row]):
                items.append(
                    {
                        "sale_id": str(dataFrame.to_dict()["sale_id"][index] or ""),
                        "sale_date": str(dataFrame.to_dict()["sale_date"][index] or ""),
                        "game_title": str(dataFrame.to_dict()["game_title"][index] or ""),
                        "category": str(dataFrame.to_dict()["category"][index] or ""),
                        "platform": str(dataFrame.to_dict()["platform"][index] or ""),
                        "price": str(dataFrame.to_dict()["price"][index] or ""),
                        "quantity": str(dataFrame.to_dict()["quantity"][index] or ""),
                        "total_sale": str(dataFrame.to_dict()["total_sale"][index] or ""),
                    }
                )
        self.mainTable.setItems(items)

if __name__ == "__main__":
    try: 
        #pl.Config.set_tbl_rows(100)
        #pl.Config.set_tbl_cols(100)
        #pl.Config.set_fmt_float("full")
        main()
    except KeyboardInterrupt:
        print("Bye")

