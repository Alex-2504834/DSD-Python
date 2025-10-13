from tkinter import *

windowWidth, windowHeight = 800, 600



window = Tk()
window.title("Fitness Tracker App")
window.geometry(f"{windowWidth}x{windowHeight}")

#? Calorie burn fields
calorieBurnFrame = Frame(window,bg="lightgreen")
caloriesPerMinuteLabel = Label(calorieBurnFrame, text="Calories Per Minute: ")
caloriesPerMinuteEntry = Entry(calorieBurnFrame, width=5)

workoutLabel        = Label(calorieBurnFrame, text="Workout Time: ")
workoutHoursLabel   = Label(calorieBurnFrame, text="Hours: ")
workoutMinutesLabel = Label(calorieBurnFrame, text="Minutes: ")
workoutSecondsLabel = Label(calorieBurnFrame, text="Seconds: ")

workoutHoursEntry   = Entry(calorieBurnFrame, width=5)
workoutMinutesEntry = Entry(calorieBurnFrame, width=5)
workoutSecondsEntry = Entry(calorieBurnFrame, width=5)

caloriesPerMinuteLabel.grid(row=0, column=0, padx=10, pady=10)
caloriesPerMinuteEntry.grid(row=0, column=1, padx=10, pady=10)

workoutLabel       .grid(row=1, column=0, padx=5, pady=10)
workoutHoursLabel  .grid(row=1, column=1, padx=5, pady=10)
workoutMinutesLabel.grid(row=1, column=3, padx=5, pady=10)
workoutSecondsLabel.grid(row=1, column=5, padx=5, pady=10)

workoutHoursEntry  .grid(row=1, column=2, padx=5, pady=10)
workoutMinutesEntry.grid(row=1, column=4, padx=5, pady=10)
workoutSecondsEntry.grid(row=1, column=6, padx=5, pady=10)


calorieBurnFrame.grid(row=1, column=0, padx=10, pady=10)

#? Step converison
stepsFrame = Frame(window)

stepsLabel      = Label(stepsFrame, text="Number of steps")
stepsEntry      = Entry(stepsFrame)
stepsOuputLabel = Label(stepsFrame, text="")

stepsLabel     .grid(row=0, column=0, padx=10, pady=10)
stepsEntry     .grid(row=0, column=1, padx=10, pady=10)
stepsOuputLabel.grid(row=0, column=2, padx=10, pady=10)

stepsFrame.grid(row=2, column=0, padx=10, pady=10)

#? medication timing

medTimingFrame = Frame(window)

medTimingLabel        = Label(medTimingFrame, text="Enter Total Minutes: ")
medItmingEntry        = Entry(medTimingFrame)
medTimingHoursLabel   = Label(medTimingFrame, text="")
medTimingMinutesLabel = Label(medTimingFrame, text="")

medTimingLabel       .grid(row=0, column=0, padx=10, pady=10)
medItmingEntry       .grid(row=0, column=1, padx=10, pady=10)
medTimingHoursLabel  .grid(row=0, column=2, padx=10, pady=10)
medTimingMinutesLabel.grid(row=0, column=3, padx=10, pady=10)


medTimingFrame.grid(row=3, column=0, padx=10, pady=10)
window.mainloop()
