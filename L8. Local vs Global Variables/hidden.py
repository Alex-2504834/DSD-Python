def old():
    name = "Alex"

    def change_name():
        name = "Jordan"
        print("Inside function:", name)

    change_name()
    print("Outside function:", name)

def new():
    name = "Alex"

    def change_name():
        name = "Jordan"
        print("Inside function:", name)

    change_name()
    print("Outside function:", name)
