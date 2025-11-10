
quiz = {"music": {
    "type": "music",
    "name": "Music Quiz",
    "questions": {
        1: {"queston": "",
            "answers": []}

}}}


def main():
    print("Welcome To The Quiz Thing\n")
    print("Select Which Quiz To Do")
    for index, quizType in enumerate(quiz):

        print(f"===Quiz {index} ===\nQuiz Name: {quiz[quizType]["name"]} \nQuiz Type: {quiz[quizType]["type"]} \nNumber of Questions: {len(quiz[quizType]["questions"])}")


main()