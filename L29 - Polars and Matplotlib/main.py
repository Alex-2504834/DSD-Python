import polars as pl
import matplotlib.pyplot

import time

pl.Config.set_tbl_rows(100)
pl.Config.set_fmt_float("full")

filePath ="L29 - Pandas and Matplotlib/retail_sales_1M_dataset.csv"

def createDataFrame(path) -> pl.DataFrame:
    return pl.read_csv(path) 

def getRowsFromNumber(dataFrame: pl.DataFrame, numberOfRows):
    return dataFrame.head(n=numberOfRows)

def addTotalSaleColumn(dataFrame: pl.DataFrame) -> pl.DataFrame:
    return dataFrame.with_columns((dataFrame["quantity"] * dataFrame["price"]).alias("total_sales"))

def checkForNonValues(dataFrame: pl.DataFrame) -> bool:
    """Returns True if the function finds any none values"""
    if dataFrame.select(pl.any_horizontal(pl.all().is_null().any())).item():
        return True
    else: 
        return False

def calcTotalRevenue(dataFrame: pl.DataFrame) -> (int | float):
    return dataFrame["price"].sum()

def calcTotalRevenuePerItem(dataFrame: pl.DataFrame):
    return dataFrame.group_by("product").agg(pl.col("price").sum().round(2)).sort("price")

def calcTotalRevenuePerCat(dataFrame: pl.DataFrame):
    return dataFrame.group_by("category").agg(pl.col("price").sum().round(2)).sort("price")

def main():
    data = createDataFrame(filePath)
    data = addTotalSaleColumn(data)
    if checkForNonValues(data):
        print("Found Null Values")
    else:
        print("Didnt Find Null Values")
    #print(getRowsFromNumber(data, 150))

    print("{:,.2f}".format(calcTotalRevenue(data)))
    print(calcTotalRevenuePerItem(data))
    print(calcTotalRevenuePerCat(data))
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye :(")