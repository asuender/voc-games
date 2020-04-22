''' A simple GUI-based hangman game for learning the english vocabulary'''

import json, os, sys, tkinter, random, re
from tkinter import messagebox
from commoncodes import CommonCode

help_msg = '''A simple GUI-based hangman game for learning the english vocabulary.
            
Usage: python3 hangman.py file mode

Command line arguments:
    file    That argument should be replaced with your json file where the 
            vocabulary data is stored. See 'example.json'.
    mode    Use 0 (de->en) or 1 (en->de).'''

class Game:
    def __init__(self):
        ''' Initialize game '''
        argv = sys.argv
        argc = len(argv)
        if argc == 4:
            if any(opt in argv for opt in ("--help", "-h")): 
              print(help_msg)
              exit(0)
            else:
              raise CommonCode(5, argv[3])
        if argc < 3:
            raise CommonCode(3,argv[0],", ".join(["file", "mode"][argc-1:]))
        elif argc > 4:
            raise CommonCode(4, '', str(argc-4))
        if not os.path.exists(argv[1]):
            raise CommonCode(7, "file", argv[1], ": file not found")
        try: int(argv[2])
        except: raise CommonCode(10, "mode", argv[2])
        
        with open(argv[1], "r") as fs:
            self.data = json.load(fs)

        self.mode = int(argv[2])
        self.order = 0
        self.order_index = -1
        self.letters = []

        self.win = tkinter.Tk()
        self.win.title("Vocabulary Hangman")
        self.win.geometry("680x380")
        self.win.resizable(0, 0)
        self.win.configure(bg="lightblue")

        rFrame = tkinter.Frame(self.win, bg="lightblue")
        rFrame.grid(row=0, column=1, padx=(40, 0))
        lFrame = tkinter.Frame(self.win, bg="lightblue")
        lFrame.grid(row=0, column=0)

        self.can = tkinter.Canvas(lFrame, width=350, height=300, bg="lightblue", borderwidth=5, relief="sunken")
        self.can.pack(anchor="n")

        self.outLabel = tkinter.Label(lFrame, font="Arial 15 bold")
        self.outLabel.pack(anchor="n", pady=(20, 0))

        tkinter.Label(rFrame, text="Vocabulary", font="Arial 13 bold", fg="white", bg="red").pack()
        tkinter.Label(rFrame, text="Hangman", font="Times 35 bold", fg="darkgreen", bg="lightblue").pack()
        tkinter.Label(rFrame, text="guess here: (one letter + ENTER)").pack(pady=(20, 0))
        self.input = tkinter.Entry(rFrame)
        self.input.pack()
        self.input.bind('<Return>', self.replace_letters)
        self.hintLabel = tkinter.Label(rFrame, text="")
        self.hintLabel.pack(pady=(10, 0))

        self.rValue = tkinter.IntVar()
        self.radioRandom = tkinter.Radiobutton(rFrame, text="randomized", variable=self.rValue, value=1, command=self.change_order, bg="lightgreen")
        self.radioOrdered = tkinter.Radiobutton(rFrame, text="ordered", variable=self.rValue, value=0, command=self.change_order, bg="lightgreen")
        self.radioOrdered.pack(anchor="n", pady=(50, 0))
        self.radioRandom.pack(anchor="s")

        self.hngml =  [
            self.can.create_line(70, 300, 100, 250, fill="lightblue", width=5),
            self.can.create_line(130, 300, 100, 250, fill="lightblue", width=5),
            self.can.create_line(100, 250, 100, 80, fill="lightblue", width=5),
            self.can.create_line(100, 120, 140, 80, fill="lightblue", width=5),
            self.can.create_line(100, 80, 220, 80, fill="lightblue", width=5),
            self.can.create_line(220, 80, 220, 110, fill="lightblue", width=5),
            self.can.create_oval(205, 110, 235, 140, fill="lightblue", outline="lightblue", width=5),
            self.can.create_line(220, 140, 220, 200, fill="lightblue", width=5),
            self.can.create_line(220, 170, 200, 150, fill="lightblue", width=5),
            self.can.create_line(220, 170, 240, 150, fill="lightblue", width=5),
            self.can.create_line(220, 200, 190, 230, fill="lightblue", width=5),
            self.can.create_line(220, 200, 250, 230, fill="lightblue", width=5)
        ]
        self.hngmi = -1

        self.choose_word()

    def choose_word(self):
        ''' Choose a word from input data '''
        if self.mode == 0:
            mode="de-en"
        else: mode="en-de"
        words = list(self.data[mode].keys())
        self.hngmi=-1
        for obj in self.hngml:
            if self.can.type(obj) == 'oval':
              self.can.itemconfig(obj, outline="lightblue")
            else:
              self.can.itemconfig(obj, fill="lightblue")

        if self.order:
            self.choice = random.choice(words)
            self.order_index = words.index(self.choice)
        else:
          self.order_index+=1
          if self.order_index > len(words)-1:
            self.order_index=0
          self.choice = words[self.order_index]

        self.letters.clear()
        self.input.delete(0, 'end')

        for l in self.choice:
            if l == ' ':
              self.letters.append(" ")
            else:
              self.letters.append("_")
        
        self.outLabel["text"] = ' '.join(self.letters)
        self.hintLabel["text"] = 'Hint: %s'%self.data[mode][self.choice]

    def replace_letters(self, event):
        '''Replace fitting letters the user guessed'''
        try: uc = self.input.get()[0]
        except: return

        ucLower = uc.lower()
        cLower = self.choice.lower()
        indexl = [r.start() for r in re.finditer(ucLower, cLower)]
        if len(indexl) == 0:
            self.update_hangman()
        for i in indexl:
            self.letters[i] = self.choice[i]
        
        self.outLabel["text"] = ' '.join(self.letters)
        self.input.delete(0, 'end')

    def update_hangman(self):
        ''' update canvas when user guesses a wrong letter '''
        self.hngmi+=1
        try:
            if self.can.type(self.hngml[self.hngmi]) == 'oval':
              self.can.itemconfig(self.hngml[self.hngmi], outline="black")
            else: self.can.itemconfig(self.hngml[self.hngmi], fill="black")
        except IndexError:
            tkinter.messagebox.showerror("You lost!", "The word was '%s'"%self.choice)
            self.choose_word()

    def change_order(self):
        ''' change from randomized to ordered or reveresed '''
        self.order = self.rValue.get()

    def launch(self):
        ''' main loop of the game '''
        while(True):
            try:
                self.win.update_idletasks()
                self.win.update()

                if not '_' in self.letters:
                    tkinter.messagebox._show("You won!", "Congratulations!")
                    self.choose_word()
            except:
                break

game = Game()
game.launch()