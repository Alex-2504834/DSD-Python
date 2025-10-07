def old():
    total_patients = 0

    def add_patient():
        global total_patients
        total_patients += 1
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        print("Patient added:", name)
    
    def view_total():
        print("Total patients:", total_patients)


def new():
    total_patients = 0

    def add_patient(total_patients):
        total_patients += 1
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        print("Patient added:", name)
        return total_patients

    def view_total():
        print("Total patients:", total_patients)

    total_patients = add_patient(total_patients)
    view_total()