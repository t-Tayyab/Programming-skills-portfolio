import tkinter as tk
from tkinter import ttk, messagebox
import random

"""All function are defined in the class named mathquiz. This class contain total of 8 functions """
class MathQuiz:
    # In this function we setup the variables and call the displaymenu fucntion to start the quiz with difficulty selection.
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Quiz state variables
        self.current_score = 0
        self.current_question = 0
        self.attempts_remaining = 2
        self.difficulty = 1
        self.current_answer = 0
        self.question_values = {'num1': 0, 'num2': 0, 'operation': '+'}
        
        # UI elements
        self.score_label = None
        self.question_label = None
        self.question_num_label = None
        self.answer_var = None
        self.answer_entry = None
        
        # Start with menu
        self.displayMenu()
    
    def displayMenu(self):
        # In this function it displays the difficulty level menu at the beginning of the quiz.
        # Using for loop it clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Creating header
        header = ttk.Label(
            self.root,
            text="Math Quiz",
            font=('Arial', 16, 'bold'),
            padding=20
        )
        header.pack()
        
        # Creating difficulty selection 
        diff_frame = ttk.LabelFrame(
            self.root,
            text="Select Difficulty",
            padding=20
        )
        diff_frame.pack(padx=20, pady=20, fill="x")
        
        # Creating difficulty buttons
        difficulties = [
            ("Easy - Single Digits", 1),
            ("Medium - Double Digits", 2),
            ("Hard - Triple Digits", 3)
        ]
        
        for text, value in difficulties:
            ttk.Button(
                diff_frame,
                text=text,
                command=lambda v=value: self.start_quiz(v),
                padding=10
            ).pack(fill="x", pady=5)
    
    def randomInt(self):
        # In this function it determines the values used in each question based on difficulty using the if statement.
        if self.difficulty == 1:
            max_val = 9
        elif self.difficulty == 2:
            max_val = 99
        else:
            max_val = 999
        
        num1 = random.randint(0, max_val)
        num2 = random.randint(0, max_val)
        
        # this if statemennt is used if there is any equation in which subtraction dose not result in negative numbers
        if self.question_values['operation'] == '-' and num2 > num1:
            num1, num2 = num2, num1
            
        self.question_values['num1'] = num1
        self.question_values['num2'] = num2
        
        # Calculate correct answer
        self.current_answer = num1 + num2 if self.question_values['operation'] == '+' else num1 - num2
    
    def decideOperation(self):
        """Function that randomly decides whether the problem is addition or subtraction."""
        self.question_values['operation'] = random.choice(['+', '-'])
        return self.question_values['operation']
    
    def displayProblem(self):
        """Function that displays the question and accepts user answer."""
        self.current_question += 1
        if self.current_question > 10:
            self.displayResults()
            return
        
        # Generate new problem
        self.decideOperation()
        self.randomInt()
        
        # Update labels
        self.question_num_label.config(text=f"Question {self.current_question}/10")
        self.question_label.config(
            text=f"{self.question_values['num1']} {self.question_values['operation']} "
                f"{self.question_values['num2']} = "
        )
        
        # Reset entry and focus
        self.answer_var.set("")
        self.answer_entry.focus()
    
    def isCorrect(self):
        # Using try block and nested if statements this function checks whether the user's answer was correct.
        try:
            user_answer = int(self.answer_var.get())
            
            if user_answer == self.current_answer:
                points = 10 if self.attempts_remaining == 2 else 5
                self.current_score += points
                self.score_label.config(text=f"Score: {self.current_score}")
                messagebox.showinfo("Correct!", f"You earned {points} points!")
                self.attempts_remaining = 2
                self.displayProblem()
            else:
                self.attempts_remaining -= 1
                if self.attempts_remaining > 0:
                    messagebox.showwarning("Incorrect", "Try again!")
                    self.answer_var.set("")
                    self.answer_entry.focus()
                else:
                    messagebox.showinfo("Incorrect", f"The correct answer was {self.current_answer}")
                    self.attempts_remaining = 2
                    self.displayProblem()
                    
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            self.answer_var.set("")
            self.answer_entry.focus()
    
    def displayResults(self):
        # in this function it uses for loop to display outputs of the user's final score and rank.
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Calculate rank
        rank = "A+" if self.current_score >= 90 else (
               "A" if self.current_score >= 80 else (
               "B" if self.current_score >= 70 else (
               "C" if self.current_score >= 60 else "D")))
        
        # Display results
        ttk.Label(
            self.root,
            text="Quiz Complete!",
            font=('Arial', 16, 'bold'),
            padding=20
        ).pack()
        
        ttk.Label(
            self.root,
            text=f"Final Score: {self.current_score}/100",
            font=('Arial', 14),
            padding=10
        ).pack()
        
        ttk.Label(
            self.root,
            text=f"Rank: {rank}",
            font=('Arial', 14),
            padding=10
        ).pack()
        
        # Add buttons
        ttk.Button(
            self.root,
            text="Play Again",
            command=self.displayMenu,
            padding=10
        ).pack(pady=20)
        
        ttk.Button(
            self.root,
            text="Quit",
            command=self.root.quit,
            padding=10
        ).pack()
    
    def start_quiz(self, difficulty):
        #in this function after the difficulty fucntion is finnished it display the quiz interface and start first question.
        self.difficulty = difficulty
        self.current_score = 0
        self.current_question = 0
        self.attempts_remaining = 2
        
        # Clear and create new interface
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create quiz interface elements
        self.score_label = ttk.Label(
            self.root,
            text="Score: 0",
            font=('Arial', 12),
            padding=10
        )
        self.score_label.pack()
        
        self.question_num_label = ttk.Label(
            self.root,
            text="Question 1/10",
            font=('Arial', 12),
            padding=10
        )
        self.question_num_label.pack()
        
        self.question_label = ttk.Label(
            self.root,
            text="",
            font=('Arial', 14),
            padding=20
        )
        self.question_label.pack()
        
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(
            self.root,
            textvariable=self.answer_var,
            justify='center',
            font=('Arial', 14)
        )
        self.answer_entry.pack(pady=20)
        
        submit_button = ttk.Button(
            self.root,
            text="Submit",
            command=self.isCorrect,
            padding=10
        )
        submit_button.pack(pady=10)
        
        self.answer_entry.bind('<Return>', lambda e: self.isCorrect())
        
        # Start first question
        self.displayProblem()

root = tk.Tk()
app = MathQuiz(root)
root.mainloop()