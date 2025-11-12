from __future__ import annotations

import os
import time
#? REEEEEEE (Regex)
import re
import json
import pathlib

from dataclasses import dataclass, field
#? why do are these not accessable by defualt, wha the bjnfdjnb python, thought i was going insane
from typing import Dict, List, Any, Tuple, Optional

#? path to the json (full path)
bigJsonPath: str = "DSD-Python/L15/QUIZ/quiz.json"

#?Whole lot of helpers
def clearConsoleScreen() -> None:
	os.system("cls" if os.name == "nt" else "clear")

def formatBold(textString: str) -> str:
	return f"\033[1m{textString}\033[0m"

def formatUnderline(textString: str) -> str:
	return f"\033[4m{textString}\033[0m"

def formatItalic(textString: str) -> str:
	return f"\033[3m{textString}\033[0m"

def formatTextColour(textString: str, hexColour: str) -> str:
	hexColour = hexColour.lstrip("#")
	red, green, blue = (int(hexColour[i : i + 2], 16) for i in (0, 2, 4))
	return f"\x1b[38;2;{red};{green};{blue}m{textString}\033[0m"

def formatBackgroundColour(textString: str, hexColour: str) -> str:
	hexColour = hexColour.lstrip("#")
	red, green, blue = (int(hexColour[i : i + 2], 16) for i in (0, 2, 4))
	return f"\x1b[48;2;{red};{green};{blue}m{textString}\033[0m"

ansiEscapePattern = re.compile(r"\x1b\[[0-9;]*m")

def stripAnsiCodes(inputString: str) -> str:
	return ansiEscapePattern.sub("", inputString)

#?removes my weirrrrrrrrrrd markup stuff
def stripMarkupTags(inputString: str) -> str:
	inputString = re.sub(r"<(colour|bgcolour):#[0-9A-Fa-f]{6}>(.*?)(?:<>|</>)", r"\2", inputString, flags=re.DOTALL)
	inputString = re.sub(r"<(bold|underline|italic)>(.*?)</>", r"\2", inputString, flags=re.DOTALL)
	return inputString

def normaliseForComparison(inputString: str) -> str:
	return stripAnsiCodes(stripMarkupTags(inputString)).strip().lower()

def parseMarkupTags(inputText: str) -> str:
	if not isinstance(inputText, str):
		return inputText

	colourPattern = re.compile(r"<(colour|bgcolour):(#[0-9A-Fa-f]{6})>(.*?)(?:<>|</>)", flags=re.DOTALL)
	stylePattern = re.compile(r"<(bold|underline|italic)>(.*?)</>", flags=re.DOTALL)

	def replaceColourTag(match: re.Match[str]) -> str:
		tagType = match.group(1)
		hexColour = match.group(2)
		innerText = match.group(3)
		match tagType:
			case "colour":
				return formatTextColour(innerText, hexColour)
			case "bgcolour":
				return formatBackgroundColour(innerText, hexColour)
			case _:
				return innerText

	def replaceStyleTag(match: re.Match[str]) -> str:
		tagType = match.group(1)
		innerText = match.group(2)
		match tagType:
			case "bold":
				return formatBold(innerText)
			case "underline":
				return formatUnderline(innerText)
			case "italic":
				return formatItalic(innerText)
			case _:
				return innerText

	previousText: str | None = None
	formattedText: str = inputText

	while formattedText != previousText:
		previousText = formattedText
		formattedText = colourPattern.sub(replaceColourTag, formattedText)
		formattedText = stylePattern.sub(replaceStyleTag, formattedText)

	return formattedText

#?Dataclass spooooky
#?frozen=True == immutable
@dataclass(frozen=True)
class QuestionData:
	questionType: str
	questionText: str
	options: Dict[str, str]
	correctAnswers: List[str]

	#? function in a class but not like needing the self stuff, kinda weirddddddddddddddddddddddd
	@staticmethod
	def fromRaw(rawQuestion: Dict[str, Any]) -> "QuestionData":
        #? we trust validateRawQuestion() already ran, so we can index safely
		return QuestionData(
			questionType=rawQuestion["type"],
			questionText=rawQuestion["question"],
			options=dict(rawQuestion.get("options", {})),
			correctAnswers=list(rawQuestion["correctAnswers"]),
		)

	def formatted(self) -> "QuestionData":
		return QuestionData(
			questionType=self.questionType,
			questionText=parseMarkupTags(self.questionText),
			options={key: parseMarkupTags(value) for key, value in self.options.items()},
			correctAnswers=list(self.correctAnswers),
		)

@dataclass(frozen=True)
class QuizEntry:
	name: str
	questions: Dict[int, QuestionData]

	@staticmethod
	def fromRaw(rawQuiz: Dict[str, Any]) -> "QuizEntry":
		questionMap: Dict[int, QuestionData] = normalizeRawQuestions(rawQuiz["questions"])
		return QuizEntry(name=rawQuiz["name"], questions=questionMap)

	def formattedName(self) -> str:
		return parseMarkupTags(self.name)

	def getFormattedQuestion(self, questionNumber: int) -> QuestionData:
		return self.questions[questionNumber].formatted()

@dataclass
class AttemptRecord:
	questionNumber: int
	userAnswers: List[str] = field(default_factory=list)
	isCorrect: bool = False

#? JSON LOADING AND STUFFFFFFFFFFFFFFFFFFFF
def validateRawQuestion(rawQuestion: Dict[str, Any], context: str = "") -> None:
	prefix = f"[{context}] " if context else ""
	if not isinstance(rawQuestion, dict):
		raise ValueError(prefix + "Question must be an object.")

	for key in ("type", "question", "correctAnswers"):
		if key not in rawQuestion:
			raise ValueError(prefix + f"Missing required key: '{key}'.")

	questionType = rawQuestion["type"]
	if questionType not in ("multiple", "direct"):
		raise ValueError(prefix + "Invalid 'type'. Must be 'multiple' or 'direct'.")

	if not isinstance(rawQuestion["question"], str):
		raise ValueError(prefix + "'question' must be a string.")

	if not isinstance(rawQuestion["correctAnswers"], list) or not rawQuestion["correctAnswers"]:
		raise ValueError(prefix + "'correctAnswers' must be a non-empty list of strings.")

	if questionType == "multiple":
		options = rawQuestion.get("options")
		if not isinstance(options, dict) or not options:
			raise ValueError(prefix + "'options' must be a non-empty object for multiple-choice.")
		for optKey, optText in options.items():
			if not isinstance(optKey, str) or not optKey:
				raise ValueError(prefix + "Option keys must be non-empty strings.")
			if not isinstance(optText, str):
				raise ValueError(prefix + f"Option '{optKey}' must be a string.")

def normalizeRawQuestions(rawQuestions: Any) -> Dict[int, QuestionData]:
	if isinstance(rawQuestions, dict):
		out: Dict[int, QuestionData] = {}
		for rawKey, rawVal in rawQuestions.items():
			try:
				num = int(rawKey)
			except Exception:
				raise ValueError(f"Question key '{rawKey}' is not an integer.")
			validateRawQuestion(rawVal, context=f"question {num}")
			out[num] = QuestionData.fromRaw(rawVal)
		return out

	if isinstance(rawQuestions, list):
		out = {}
		for idx, rawVal in enumerate(rawQuestions, start=1):
			validateRawQuestion(rawVal, context=f"question {idx}")
			out[idx] = QuestionData.fromRaw(rawVal)
		return out

	raise ValueError("The 'questions' field must be a dict or a list.")

def validateRawQuiz(rawQuiz: Dict[str, Any], context: str = "") -> None:
	prefix = f"[{context}] " if context else ""
	if not isinstance(rawQuiz, dict):
		raise ValueError(prefix + "Quiz must be an object.")
	if "name" not in rawQuiz or not isinstance(rawQuiz["name"], str) or not rawQuiz["name"].strip():
		raise ValueError(prefix + "Missing or invalid 'name'.")
	if "questions" not in rawQuiz:
		raise ValueError(prefix + "Missing 'questions' field.")

#? sluggy
def slugifyKeyFromName(name: str, existing: set[str]) -> str:
	base = normaliseForComparison(name).replace(" ", "-")
	base = re.sub(r"[^a-z0-9\-]+", "", base)
	if not base:
		base = "quiz"
	candidate = base
	i = 2
	while candidate in existing:
		candidate = f"{base}-{i}"
		i += 1
	return candidate

def loadBigJsonFileOnce(path: str) -> Dict[str, QuizEntry]:
	jsonPath = pathlib.Path(path)
	if not jsonPath.exists() or not jsonPath.is_file():
		#? not fatal, we just load nothing and keep the built-ins
		return {}

	try:
		with jsonPath.open("r", encoding="utf-8") as f:
			rawTop = json.load(f)
	except json.JSONDecodeError as exc:
		print(formatTextColour(f"Bad JSON in {path}: {exc}", "#ff0000"))
		return {}

	loaded: Dict[str, QuizEntry] = {}

	if isinstance(rawTop, dict):
		for key, rawQuiz in rawTop.items():
			try:
				validateRawQuiz(rawQuiz, context=f"quiz '{key}'")
				entry = QuizEntry.fromRaw(rawQuiz)
				loaded[key] = entry
			except Exception as e:
				print(formatTextColour(f"Skipping {key}: {e}", "#ff0000"))
		return loaded

	if isinstance(rawTop, list):
		existingKeys: set[str] = set()
		for index, rawQuiz in enumerate(rawTop, start=1):
			try:
				validateRawQuiz(rawQuiz, context=f"quiz index {index}")
				entry = QuizEntry.fromRaw(rawQuiz)
				autoKey = slugifyKeyFromName(entry.name, existingKeys)
				loaded[autoKey] = entry
				existingKeys.add(autoKey)
			except Exception as e:
				print(formatTextColour(f"Skipping quiz at index {index}: {e}", "#ff0000"))
		return loaded

	print(formatTextColour("JSON must be an object or an array of quizzes.", "#ff0000"))
	return {}

def mergeQuizzesInPlace(source: Dict[str, QuizEntry], target: Dict[str, QuizEntry]) -> None:
	#? merge without losing originals; auto-suffix duplicates
	existing = set(target.keys())
	for key, entry in source.items():
		if key in target:
			newKey = slugifyKeyFromName(entry.name, existing)
			target[newKey] = entry
			existing.add(newKey)
			print(formatTextColour(f"Key '{key}' exists. Added as '{newKey}'.", "#ffad33"))
		else:
			target[key] = entry
			existing.add(key)

rawQuizData: Dict[str, Dict[str, Any]] = {}

quizData: Dict[str, QuizEntry] = {key: QuizEntry.fromRaw(val) for key, val in rawQuizData.items()}

activeQuizState: Dict[str, Any] = {"currentQuizKey": "", "currentScore": 0, "currentProgress": 0}
attemptHistory: List[AttemptRecord] = []

#? this took way to long to do
def parseUserAnswerInput(inputText: str) -> List[str]:
	tokens = re.split(r"[,\s]+", inputText.strip())
	answers: List[str] = []
	for token in tokens:
		if not token:
			continue
		upper = token.upper()
		if upper not in answers:
			answers.append(upper)
	return answers

def validateAnswers(answers: List[str], validOptions: Dict[str, str]) -> Tuple[bool, List[str]]:
	filtered = [answer for answer in answers if answer in validOptions]
	return (len(filtered) == len(answers) and len(filtered) > 0, filtered)

def areAnswersCorrect(userAnswers: List[str], correctAnswers: List[str]) -> bool:
	return sorted([answer.lower() for answer in userAnswers]) == sorted([answer.lower() for answer in correctAnswers])

def printAllQuizInformation() -> None:
	for quizIndex, quizKey in enumerate(quizData.keys()):
		quizEntry = quizData[quizKey]
		displayName = quizEntry.formattedName()
		questionCount = len(quizEntry.questions)
		print(f"===  Quiz {quizIndex} ===")
		print(f"Quiz Key: {quizKey}")
		print(f"Quiz Name: {displayName}")
		print(f"Number of Questions: {questionCount}\n")

def handleQuizSelection() -> None:
	while True:
		clearConsoleScreen()
		print(formatBold(formatUnderline(formatTextColour("Select Which Quiz To Do\n", "#fcba03"))))
		printAllQuizInformation()

		userInput = input("Enter quiz number, name, or key: ").strip().lower()
		quizKeyList = list(quizData.keys())

		if userInput.isdigit():
			selectedIndex = int(userInput)
			if 0 <= selectedIndex < len(quizKeyList):
				selectedKey = quizKeyList[selectedIndex]
				activeQuizState["currentQuizKey"] = selectedKey
				print(f"\nYou selected by index: {stripAnsiCodes(quizData[selectedKey].formattedName())}")
				time.sleep(0.5)
				return
			else:
				print(formatTextColour("Invalid quiz index. Please try again.", "#ff0000"))
				time.sleep(1)
				continue

		if userInput in quizData:
			activeQuizState["currentQuizKey"] = userInput
			print(f"\nYou selected quiz by key: {stripAnsiCodes(quizData[userInput].formattedName())}")
			time.sleep(0.5)
			return

		for quizKey, quizEntry in quizData.items():
			if userInput == normaliseForComparison(quizEntry.name):
				activeQuizState["currentQuizKey"] = quizKey
				print(f"\nYou selected quiz by name: {stripAnsiCodes(quizEntry.formattedName())}")
				time.sleep(0.5)
				return

		print(formatTextColour("Invalid selection. Please try again.", "#ff0000"))
		time.sleep(1)

def runQuiz() -> None:
	clearConsoleScreen()
	quizKey = activeQuizState["currentQuizKey"]
	if not quizKey:
		print("No quiz selected.")
		return

	quizEntry = quizData[quizKey]
	print(formatBold(formatUnderline(formatTextColour(f"Current Quiz: {quizEntry.formattedName()}\n", "#fcba03"))))

	activeQuizState["currentScore"] = 0
	attemptHistory.clear()

	for questionNumber in sorted(quizEntry.questions.keys()):
		question = quizEntry.questions[questionNumber]
		formatted = question.formatted()

		print(formatBold(f"Question {questionNumber}:"))
		print(formatted.questionText)

		if question.questionType == "multiple":
			for key, value in formatted.options.items():
				print(f"  {key}. {value}")
			if len(question.correctAnswers) > 1:
				print(formatItalic("(Multiple answers allowed | separate with commas or spaces)"))

			while True:
				userInput = input("\nYour answer: ").strip()
				parsed = parseUserAnswerInput(userInput)
				isValid, filtered = validateAnswers(parsed, question.options)
				if not isValid:
					print(formatTextColour("Please enter valid letter(s) from the options above.", "#ffad33"))
					continue
				break

			isCorrect = areAnswersCorrect(filtered, question.correctAnswers)
			attemptHistory.append(AttemptRecord(questionNumber, filtered, isCorrect))

		elif question.questionType == "direct":
			while True:
				userInput = input("\nYour one-word answer: ").strip()
				if not userInput:
					print(formatTextColour("Answer cannot be blank.", "#ffad33"))
					continue
				if " " in userInput.strip():
					print(formatTextColour("Please enter only one word.", "#ffad33"))
					continue
				break

			normalizedAnswer = userInput.strip().lower()
			isCorrect = normalizedAnswer in [ans.lower() for ans in question.correctAnswers]
			attemptHistory.append(AttemptRecord(questionNumber, [userInput], isCorrect))

		print(formatTextColour("Answer recorded.\n", "#00b3ff"))
		time.sleep(0.3)

	activeQuizState["currentScore"] = sum(1 for record in attemptHistory if record.isCorrect)
	showQuizSummary(quizEntry)

def showQuizSummary(quizEntry: QuizEntry) -> None:
	clearConsoleScreen()
	totalQuestions = len(quizEntry.questions)
	score = activeQuizState["currentScore"]
	print(formatBold(formatUnderline("Quiz Summary")))
	print(f"Score: {score}/{totalQuestions}\n")

	for record in attemptHistory:
		question = quizEntry.questions[record.questionNumber]
		formatted = quizEntry.getFormattedQuestion(record.questionNumber)

		userAnswers = ", ".join(record.userAnswers)
		correctAnswers = ", ".join(question.correctAnswers)
		status = formatTextColour("Correct", "#00d26a") if record.isCorrect else formatTextColour("Incorrect", "#ff4d4d")

		print(formatBold(f"Question {record.questionNumber}:"))
		print(formatted.questionText)
		print(f"Your answer: {userAnswers}")
		print(f"Correct answer(s): {correctAnswers}")
		print(status)
		print("-" * 35)

	input("\nPress Enter to exit: ")

def main() -> None:
	clearConsoleScreen()
	#? try to load the 1 big json lol (if it exists)
	loaded = loadBigJsonFileOnce(bigJsonPath)
	if loaded:
		mergeQuizzesInPlace(loaded, quizData)
		print(formatTextColour(f"Loaded {len(loaded)} quiz(es) from {bigJsonPath}", "#00d26a"))
		time.sleep(0.7)
	else:
		print(formatBold((formatTextColour("No JSON loaded", "#ff0000"))))
		return

	print(formatBold(formatUnderline(formatTextColour("Welcome To The Quiz Thing\n", "#fcba03"))))
	printAllQuizInformation()
	handleQuizSelection()
	runQuiz()

if __name__ == "__main__":
	main()
