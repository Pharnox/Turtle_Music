import turtle
import winsound
import re
import math

turtlesAtPlay = []
turtlesOfThePast = []
turtlesInTransit = []
wiggles = 0
f0 = 440
a = 2.0**(1.0/12.0) # Twelth root of 2
noteSteps = ["Ab", "A", "A#", "Bb", "B", "B#", "Cb", "C", "C#", "Db", "D", "D#", "Eb", "E", "E#", "Fb", "F", "F#", "Gb", "G", "G#"]
posNotes = [ "F5","E5","D5","C5","B4","A4","G4","F4","E4","D4","C4","B3","A3","G3","F3","E3","D3","C3","B2","A2","G2"]
stepValues = [0, 1, 2, 2, 3, 4, 3, 4, 5, 5, 6, 7, 7, 8, 9, 8, 9, 10, 10, 11, 12]

turtle.setup(1000, 800)

class MyTurtle(turtle.Turtle) :

	note = ''
	duration = 'quarter'

	def __init__(self,**args) :
		turtle.Turtle.__init__(self,**args)

	def callPlay(self, x, y) :
		PlayNotes(GetNotes(turtlesAtPlay), GetDurations(turtlesAtPlay))

	def ClearNotes(self, x, y) :
		for i in turtlesAtPlay :
			i.ht()
		del turtlesAtPlay[:]
		global wiggles
		wiggles = 0

	def CopyTurtles(self, x, y) :
		del turtlesOfThePast[:]
		for i in turtlesAtPlay :
			turtlesOfThePast.append(i)

	def SwapTurtles(self, x, y) :
		#Copy Current turtles to storage then clear current
		for i in turtlesAtPlay :
			turtlesInTransit.append(i)
			i.ht()
		del turtlesAtPlay[:]
		#Copy Past turtles to current then clear past
		for i in turtlesOfThePast :
			turtlesAtPlay.append(i)
		del turtlesOfThePast[:]
		for i in turtlesAtPlay :
			i.st()
		#Copy Storage turtles to past then clear storage
		for i in turtlesInTransit :
			turtlesOfThePast.append(i)
		del turtlesInTransit[:]

	def changeDur(self, x, y) :
		if (self.duration == "eighth"):
			self.duration = "quarter"
			self.shapesize(0.4, 0.4)
		elif (self.duration == "quarter"):
			self.duration = "half"
			self.fillcolor("white")
		elif (self.duration == "half"):
			self.duration = "whole"
			self.shapesize(0.4, 0.6)
		elif (self.duration == "whole"):
			self.duration = "eighth"
			self.fillcolor("black")
			self.shapesize(0.6, 0.4)

	def wiggle(self, x, y) :
		global wiggles
		if (self.fillcolor() == "red"):
			self.fillcolor("black")
		else:
			self.fillcolor("red")

		y = self.ycor()
		y = int(5 * round(float(y)/5))

		print self.note

		makeNewNote(wiggles, (y-300), self.note)
		wiggles = wiggles + 1

def GetNoteFreq(note) :

  #note -match '([A-G#b]{1,2})(\d+)' | out-null
  matches = re.match("([A-G#b]{1,2})(\d+)", note)

  octave = int(matches.group(2))
  x = noteSteps.index(matches.group(1))

  if (stepValues[x] > 3):
    octave+=-1

  stepVal = int(stepValues[x])

  steps = octave * 12 + stepVal;
  n = steps - 49

  freq = f0 * (a**n)
  print freq

  freqU = (math.ceil(freq/10))*10
  print freqU
  freqD = (math.floor(freq/10))*10
  print freqD
  
  if (math.fabs(freqU-freq) < math.fabs(freqD-freq)) :
  	freq = freqU
  else :
  	freq = freqD

  freq = int(freq)

  return freq;

def GetNoteDuration(duration):
  if (duration == "quarter"):
    note = 500
  elif (duration == "half"):
    note = 1000
  elif (duration == "whole"):
    note = 2000
  elif (duration == "eighth"):
    note = 250
  else:
    note = 500
  
  return note

def Beep(freq, dur):
  print freq
  print dur
  winsound.Beep(freq, dur)

def GetDurations(noteTurtles):
	durations = [None] * len(noteTurtles)
	for i in range(len(noteTurtles)):
		durations[i] = noteTurtles[i].duration
		print durations[i]
	return durations

def GetNotes(noteTurtles):
	notes = [None] * len(noteTurtles)
	for i in range(len(noteTurtles)):
		notes[i] = noteTurtles[i].note
		print notes[i]
	return notes

def PlayNotes(notes, durations):
	for i in range(len(notes)):
		Beep(GetNoteFreq(notes[i]), GetNoteDuration(durations[i]))

def makeStaff(h):
	staffTurtle.showturtle()
	for num in range(11):
		staffTurtle.penup()
		staffTurtle.setheading(0)
		staffTurtle.setpos((-400), (h - (num * 10)))
		if (num != 5):
			staffTurtle.pendown()
			staffTurtle.setheading(0)
			staffTurtle.forward(800)

	staffTurtle.penup()
	staffTurtle.setpos(-380, (h-15))
	staffTurtle.shape('TrebleClef2.gif')
	staffTurtle.stamp()
	staffTurtle.hideturtle()
	staffTurtle.shape('BassClef2.gif')
	staffTurtle.setpos(-380, (h-85))
	staffTurtle.showturtle()
	staffTurtle.stamp()
	staffTurtle.shape('turtle')
	staffTurtle.hideturtle()

def makeNewNote(numNote, h, nNote):
	s = -350
	scale = 800.0/60.0
	turtlesAtPlay.append(MyTurtle())
	turtlesAtPlay[numNote].note = nNote
	turtlesAtPlay[numNote].duration = "eighth"
	turtlesAtPlay[numNote].speed(4)
	turtlesAtPlay[numNote].penup()
	turtlesAtPlay[numNote].shape('circle')
	turtlesAtPlay[numNote].shapesize(0.6, 0.4)
	turtlesAtPlay[numNote].setpos((s + (numNote * scale)), (h + 100))
	turtlesAtPlay[numNote].onclick(turtlesAtPlay[numNote].changeDur)


def populateNotes(h):
	s = -350
	scale = 800.0/40.0
	noteTurtles = []
	for num in range(21):
		noteTurtles.append(MyTurtle())
		noteTurtles[num].note = posNotes[num]
		noteTurtles[num].speed(4)
		noteTurtles[num].penup()
		noteTurtles[num].shape('circle')
		noteTurtles[num].shapesize(0.4, 0.4)
		noteTurtles[num].setpos((s + (num * scale)), (h - (num * 5)))
		noteTurtles[num].onclick(noteTurtles[num].wiggle)

# End of Definitions

staffTurtle = MyTurtle()
staffTurtle.speed(6)
staffTurtle.shape('turtle')
staffTurtle.hideturtle()
turtle.register_shape('TrebleClef2.gif')
turtle.register_shape('BassClef2.gif')

makeStaff(300)
populateNotes(300)
makeStaff(100)

staffTurtle.shape('square')
staffTurtle.setpos(-250, -200)
staffTurtle.write("Play")
staffTurtle.setpos(-250, -250)
staffTurtle.onclick(staffTurtle.callPlay)
staffTurtle.showturtle()

clearTurtle = MyTurtle()
clearTurtle.onclick(clearTurtle.ClearNotes)
clearTurtle.shape('square')
clearTurtle.pu()
clearTurtle.setpos(-200, -200)
clearTurtle.write("Clear")
clearTurtle.setpos(-200, -250)

copyTurtle = MyTurtle()
copyTurtle.onclick(copyTurtle.CopyTurtles)
copyTurtle.shape('square')
copyTurtle.pu()
copyTurtle.setpos(-150, -200)
copyTurtle.write("Copy")
copyTurtle.setpos(-150, -250)

swapTurtle = MyTurtle()
swapTurtle.onclick(swapTurtle.SwapTurtles)
swapTurtle.shape('square')
swapTurtle.pu()
swapTurtle.setpos(-100, -200)
swapTurtle.write("Swap")
swapTurtle.setpos(-100, -250)

turtle.mainloop()