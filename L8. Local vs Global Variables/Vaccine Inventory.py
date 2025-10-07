def old():
    stock = 50

    def dispense(doses):
        stock = stock - doses
        print("Dispensed:", doses, "Remaining:", stock)
    
    def restock(amount):
        print("Before restock:", stock)
        stock = stock + amount
        print("After restock:", stock)
    
    dispense(5)
    restock(10)
    print("End of day stock:", stock)


def new():
    stock = 50

    def dispense(doses, stock):
        stock = stock - doses
        print("Dispensed:", doses, "Remaining:", stock)
        return stock

    def restock(amount, stock):
        print("Before restock:", stock)
        stock = stock + amount
        print("After restock:", stock)
        return stock

    stock = dispense(5, stock)
    stock = restock(10, stock)
    print("End of day stock:", stock)
