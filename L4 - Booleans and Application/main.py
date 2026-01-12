import csv


path: str = "exam.csv"
def getExamData(path, firstName, lastName) -> str:
    try: 
        with open(path, newline="") as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                if row["firstName"].lower() in (firstName.lower()) and row["lastName"].lower() in (lastName.lower()):
                    if {row["passed"]}: 
                        return(f"Student: {row["firstName"]} {row["lastName"]} got a score of: {row["testScore"]} and passed")
                    else: 
                        return(f"Student: {row["firstName"]} {row["lastName"]} got a score of: {row["testScore"]} and failed")
                else: 
                    return(f"Student: {firstName} {lastName} not found")

    except FileNotFoundError:
        print(f"File {path} not found")


firstName: str = input("Enter First Name: ")
lastName: str = input("Enter Last Name: ")
print(getExamData(path, firstName, lastName))
