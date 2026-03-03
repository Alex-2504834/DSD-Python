import numpy
import datetime
import math
import random

quizName = "Random Math Quiz"
numberOfQuizQuestions = 10

def quizInfo():
    return f"{"Math Quiz":═^30}\nNumber of Questions: {numberOfQuizQuestions}"


def main():
    print(quizInfo())
    input("Press Enter To Start.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye :(")