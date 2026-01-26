import polars as pl
from pathlib import Path
import matplotlib.pyplot as plot


def createDataFrame(path: Path) -> pl.DataFrame:
    return pl.read_csv(path, null_values="")

def checkForNonValues(dataFrame: pl.DataFrame) -> bool:
    """Returns True if the function finds any none values"""
    if dataFrame.select(pl.any_horizontal(pl.all().is_null().any())).item():
        return True
    else: 
        return False

def averageLEGOPrice(dataFrame: pl.DataFrame) -> float:
    return dataFrame["list_price"].mean()

def maxLEGOPrice(dataFrame: pl.DataFrame) -> float:
    return dataFrame["list_price"].max()

def formHistogram(dataFrame: pl.DataFrame) -> None:
    plot.hist(dataFrame["list_price"])
    plot.xlabel("Price")
    plot.ylabel("Lego Sets")
    plot.show()

def formScatter(dataFrame: pl.DataFrame) -> None:
    plot.scatter(dataFrame["piece_count"], dataFrame["list_price"])
    plot.xlabel("Piece Count")
    plot.ylabel("Lego Price")
    plot.show()

def formBar(dataFrame: pl.DataFrame) -> None:
    data = dataFrame.group_by("theme_name").agg(pl.col("star_rating").mean().fill_null(value=0)).sort("star_rating", descending=True).head(10)
    fig, ax = plot.subplots()
    ax.bar(data["theme_name"], data["star_rating"])
    ax.tick_params(axis='x', labelrotation=90)

    plot.xlabel("Theme Name")
    plot.ylabel("Star Rating")
    plot.show()

def main() -> None:
    csvData = createDataFrame("L30 - Polars and Matplotlib/lego_sets.csv")
    print(csvData.head(10))
    print(checkForNonValues(csvData))
    print(f"Average Lego Price is: {averageLEGOPrice(csvData):.2f}")
    print(f"Maximum Lego Price is: {maxLEGOPrice(csvData)}")
    formHistogram(csvData)
    formScatter(csvData)
    formBar(csvData)
    
if __name__ == "__main__":
    try:
        pl.Config.set_tbl_rows(100)
        pl.Config.set_fmt_float("full")
        main()
    except KeyboardInterrupt:
        print("Bye")