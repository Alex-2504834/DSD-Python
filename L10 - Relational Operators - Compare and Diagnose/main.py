def highTempCheck(temp):
    if temp > 37.5:
        return True
    return False

def lowOxygen(oxygen):
    if oxygen < 92:
        return True
    return False

def heartRateNormal(heartRate):
    if heartRate <= heartRate <= 100:
        return True
    return False


def main():
    userInputOxygen = input("Enter Oxgyen Level: ")
    userInputTemp = input("Enter Temperatue: ")
    userInputHeart = input("Enter Heart Rate: ")
    try: 
        if highTempCheck(float(userInputTemp)):
            print("You have a high temp")

        elif lowOxygen(float(userInputOxygen)):
            print("you have a low oxgygen level")

        elif heartRateNormal(float(userInputHeart)):
            print("You have a normal heart rate")

        else: 
            pass

    except ValueError:
        print("Please Only Enter A Number")



main()
