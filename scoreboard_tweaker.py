import tkinter as tk
import requests
from tkinter import messagebox

boldFont = "Arial 10 bold"


class App(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.pack()
        self.master.title("BATTLESHIP Scoreboard Tweaker")
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#ececec')
        self.createStringvars()
        self.getScores()

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_separator()
        filemenu.add_command(label="Quit", command=root.destroy)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Clear High scores", command=self.clearHiScores)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        root.config(menu=menubar)

        # Header frame
        header_frame = tk.Frame(self, pady=10)
        header_frame.pack()
        tk.Label(header_frame, text="BATTLESHIP Scoreboard Tweaker", font="arial 15 bold").pack()

        # Scoreboard FRAME
        scoreboard_frame = tk.Frame(self, relief="groove", borderwidth=3)

        # Place frame
        place_frame = tk.Frame(scoreboard_frame, relief="groove",borderwidth=3, pady=5)
        tk.Label(place_frame, text="Place", font=boldFont).pack(pady=2)
        for x in range(1, 11):
            tk.Label(place_frame, text=x).pack(pady=2)
        place_frame.pack(side="left")

        # Name Frame
        name_frame = tk.Frame(scoreboard_frame, relief="groove", borderwidth=3, pady=5)
        tk.Label(name_frame, text="Name".center(16), font=boldFont).pack(pady=2)
        for x in range(0, 10):
            tk.Label(name_frame, textvariable=row[x]["PlayerName"]).pack(pady=2)
        name_frame.pack(side="left")

        # Score Frame
        score_frame = tk.Frame(scoreboard_frame, relief="groove", borderwidth=3, pady=5)
        tk.Label(score_frame, text="Score".center(16), font=boldFont).pack(pady=2)
        for x in range(0, 10):
            tk.Label(score_frame, textvariable=row[x]["Score"]).pack(pady=2)
        score_frame.pack(side="left")

        # Difficulty Frame
        difficulty_frame = tk.Frame(scoreboard_frame, relief="groove", borderwidth=3, pady=5)
        tk.Label(difficulty_frame, text="Difficulty".center(16), font=boldFont).pack(pady=2)
        for x in range(0, 10):
            tk.Label(difficulty_frame, textvariable=row[x]["Difficulty"]).pack(pady=2)
        difficulty_frame.pack(side="left")

        # Outcome Frame
        outcome_frame = tk.Frame(scoreboard_frame, relief="groove", borderwidth=3, pady=5)
        tk.Label(outcome_frame, text="Outcome".center(16), font=boldFont).pack(pady=2)
        for x in range(0, 10):
            tk.Label(outcome_frame, textvariable=row[x]["Outcome"]).pack(pady=2)
        outcome_frame.pack(side="left")

        # Turns frame
        turns_frame = tk.Frame(scoreboard_frame, relief="groove", borderwidth=3, pady=5)
        tk.Label(turns_frame, text="Turns".center(16), font=boldFont).pack(pady=2)
        for x in range(0, 10):
            tk.Label(turns_frame, textvariable=row[x]["Turns"]).pack(pady=2)
        turns_frame.pack(side="left")

        # Pack scoreboard frame
        scoreboard_frame.pack(anchor="w")

        # Insert frame
        insert_frame = tk.Frame(self, relief="groove", borderwidth=3, pady=5)
        tk.Label(insert_frame, text="Add: ", font=boldFont, width=5).pack(side="left", pady=2)
        self.nameInsert = tk.Entry(insert_frame, width=15)
        self.nameInsert.pack(side="left", padx=1)
        self.scoreInsert = tk.Entry(insert_frame, width=15)
        self.scoreInsert.pack(side="left", padx=1)
        self.difficultyInsert = tk.Entry(insert_frame, width=15)
        self.difficultyInsert.pack(side="left", padx=1)
        self.outcomeInsert = tk.Entry(insert_frame, width=15)
        self.outcomeInsert.pack(side="left", padx=1)
        self.turnsInsert = tk.Entry(insert_frame, width=15)
        self.turnsInsert.pack(side="left", padx=1)
        tk.Button(insert_frame, text="Insert", command=self.setScores).pack(padx=5)
        insert_frame.pack(anchor="w", pady=5)

        # Delete frame
        delete_frame = tk.Frame(self, relief="groove", borderwidth=3, pady=5)
        tk.Label(delete_frame, text="Delete place: ", font=boldFont).pack(side="left", pady=2)
        self.deleteInsert = tk.Entry(delete_frame, width=15)
        self.deleteInsert.pack(side="left", padx=1)
        tk.Button(delete_frame, text="Delete", command=self.deletePlace).pack(side="left", padx=5)
        delete_frame.pack(anchor="w", pady=5)

    def createStringvars(self):
        """Create a list of string variables for labels"""
        global row
        row = []
        for x in range(0, 10):
            row.append({"PlayerName": tk.StringVar(), "Score": tk.StringVar(), "Difficulty": tk.StringVar(),
                        "Outcome": tk.StringVar(), "Turns": tk.StringVar()})

    def getScores(self):
        """Get scores and update labels"""
        global high_scores
        global row
        r = requests.get("http://renki.dy.fi/battleship/getscore.php")
        high_scores = r.json()['scores']
        empty = ""

        for x in range(0, 10):
            if len(high_scores) > x:
                row[x]["PlayerName"].set(high_scores[x]['playername'])
                row[x]["Score"].set(high_scores[x]['score'])
                row[x]["Difficulty"].set(high_scores[x]['difficulty'])
                row[x]["Outcome"].set(high_scores[x]['outcome'])
                row[x]["Turns"].set(high_scores[x]['turns'])
            else:
                row[x]["PlayerName"].set(empty)
                row[x]["Score"].set(empty)
                row[x]["Difficulty"].set(empty)
                row[x]["Outcome"].set(empty)
                row[x]["Turns"].set(empty)

    def setScores(self):
        """Insert a new high score"""
        name = self.nameInsert.get()
        score = self.scoreInsert.get()
        difficulty = self.difficultyInsert.get().capitalize()
        outcome = self.outcomeInsert.get().upper()
        turns = self.turnsInsert.get().upper()

        if len(name) == 0 or len(score) == 0 or len(difficulty) == 0 or len(outcome) == 0 or len(turns) == 0:
            messagebox.showerror("Error", "Please fill each field!")
        elif outcome != "LOST" and outcome != "WON":
            messagebox.showerror("Error", "Outcome must be either LOST or WON")
        elif difficulty != "Easy" and difficulty != "Normal" and difficulty != "Impossible":
            messagebox.showerror("Error", "Difficulty must be either Easy, Normal or Impossible")
        elif not score.isdigit():
            messagebox.showerror("Error", "Check your input!\nScore must be a number.")
        elif not turns.isdigit():
            messagebox.showerror("Error", "Check your input!\nTurns must be a number.")
        else:
            requests.post("http://renki.dy.fi/battleship/addscore.php",
                          data={'playername': name, 'score': score, 'difficulty': difficulty, 'outcome': outcome,
                                'turns': turns})
            self.getScores()

    def deletePlace(self):
        """Delete one high score"""
        try:
            place = int(self.deleteInsert.get()) - 1
            playerid = high_scores[place]['id']
            requests.post("http://renki.dy.fi/battleship/deletescore.php", data={'id': playerid})
        except (IndexError, ValueError):
            if len(high_scores) == 0:
                messagebox.showerror("Error",
                                     "Error: High scores empty, unable to delete.")
            else:
                messagebox.showerror("Error", "Error: Invalid value.\nGive values between 1 and {0}".format(len(high_scores)))
        self.getScores()

    def clearHiScores(self):
        """Clear all high scores"""
        result = messagebox.askyesno("Clear High scores", "Are you sure you want to clear all high scores?")
        if result:
            for x in range(0, len(high_scores)):
                playerid = high_scores[x]['id']
                requests.post("http://renki.dy.fi/battleship/deletescore.php", data={'id': playerid})
        self.getScores()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()