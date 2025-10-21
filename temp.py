def arithmeticBasics() -> None:
    userSteps: int = 7345
    userGoal: int = 10000

    if userSteps <= userGoal:
        print(f"You have done {round((userSteps/userGoal)*100, 1)}% of your walking goal")
        print(f"You have {userGoal - userSteps} Remaining")

    else:
        print(f"you have over reached your goal of {userGoal} by {userSteps - userGoal} with {userSteps} Steps")

##!!!!! come back, math not working 
def bmiBuckets() -> None:
    userWeightKG: float = 26
    userHeightM: float = 1

    bmi: float = userWeightKG / (userHeightM ** 2)
    print(bmi)
    if  bmi >= 30:
         print("Obese")

    elif 30 <= bmi >= 25:
        print("Overweight")

    elif 25 <= bmi >= 18.5:
        print("healthy")

    elif bmi <= 18.5:
        print("Underweight")

def screentimeFlag(userDailyScreenMinutes: int, userScreenNightMinutes: int, userSteps: int) -> bool:
    if (userDailyScreenMinutes > 240 and userSteps < 5000) or userScreenNightMinutes > 60:
        return True
    return False

def hydrationStreak() -> None:
    userWater: float = 1500
    userScore: int = (userWater//250)

    userScore += ((userWater//2000)*5)

    print(f"Your score is {userScore}")

def eligibilityForFreeClass():
    userAge: int = 16
    userLowIncome: bool = False
    userLastClassDates: int = 0
