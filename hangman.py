''' A simple GUI-based hangman game for learning the english vocabulary'''

import json, os, sys, tkinter, random, re
from commoncodes import CommonCode


class Game:
    def __init__(self):
        argv = sys.argv
        argc = len(argv)
        if argc < 2:
            raise CommonCode(3, argv[0], "file")
        elif argv[1] in ("-h", "h", "help", "--help", "-help"):
            help_msg = '''
            A simple GUI-based hangman game for learning the english vocabulary.
            
            Command line arguments:
                file    That argument should be replaced with your json file where the 
                        vocabulary data is stored. See 'example.json'.
            '''
            print(help_msg)
            exit(0)
        
        with open(argv[1], "r") as fs:
             self.data = json.load(fs)

        self.letters = []

        self.win = tkinter.Tk()
        self.win.title("Vocabulary Hangman")
        self.win.geometry("500x500")
        #self.win.resizable(0, 0)
        self.win.configure(bg="lightblue")
        self.can = tkinter.Canvas(self.win, width=350, height=300, bg="lightblue", borderwidth=5, relief="sunken")
        self.can.grid(row=0, column=0)
        rFrame = tkinter.Frame(self.win, bg="lightblue")
        rFrame.grid(row=0, column=1)
        tkinter.Label(rFrame, text="Vocabulary", font="Arial 13 bold", fg="white", bg="red").pack()
        tkinter.Label(rFrame, text="Hangman", font="Times 35 bold", fg="darkgreen", bg="lightblue").pack()
        self.input = tkinter.Entry(rFrame)
        self.input.pack()
        self.input.bind('<Return>', self.replace_letters)
        self.outLabel = tkinter.Label(self.win, font="Arial 20 bold")
        self.outLabel.grid(row=1, column=0)

        self.choose_word()

    def choose_word(self):
        self.choice = random.choice(list(self.data.keys()))
        print(self.choice)
        for l in self.choice:
            if l == ' ':
                self.letters.append(" ")
            else:
                self.letters.append("_")
        self.outLabel["text"] = ''.join(self.letters)

    def replace_letters(self, event):
        #replace correct letters
        uc = self.input.get()
        for c in uc:
            for i in [r.start() for r in re.finditer(c, self.choice)]:
                self.letters[i] = c
        self.outLabel["text"] = ''.join(self.letters)

    def launch(self):
        self.win.mainloop()

        while(self.win.state == 'normal'):
            pass

game = Game()
game.launch()