import pandas as pl 
from pathlib import Path
from functools import cache
import matplotlib.pyplot as plt

path: Path = "L33 - Polars Once AGAIN!/amazon_sales_dataset.csv"

@cache
def getDataFrame(path) -> pl.DataFrame:
    return pl.read_csv(path)

def main(path):
    data = getDataFrame(path)
    
    #print(data.head(5))
    #print(data.info())

    print(f"Total Sales: £{round(data["total_revenue"].sum(), 2):,}")
    print(f"Average Sales: £{round(data["total_revenue"].mean(), 2):,}")

    productByCategory = data.groupby("product_category")["total_revenue"].sum().sort_values()
    #plt.bar(productByCategory.index, productByCategory)
    #plt.show()

    salesByRegion = data.groupby("customer_region")["total_revenue"].sum().sort_values()
    plt.bar(salesByRegion.index, salesByRegion)
    plt.show()
if __name__ == "__main__":
    try: 
        main(path)

    except KeyboardInterrupt:
        print("Bye") 

