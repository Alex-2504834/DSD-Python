def old():
    total_mg = 0
    
    def record_dose(mg):
        total_mg = total_mg + mg
        print("Recorded dose:", mg, "mg. Total today:", total_mg, "mg")
    
    record_dose(250)
    record_dose(250)
    print("Final total:", total_mg)

def new():
    total_mg = 0

    def record_dose(mg):
        print("Recorded dose:", mg, "mg. Total today:", total_mg, "mg")
        return total_mg + mg

    total_mg = record_dose(250)
    total_mg = record_dose(250)
    print("Final total:", total_mg)
