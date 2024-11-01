import tkinter as tk
from tkinter import ttk
import random

# It is the main class to handle the Joke Teller app functionality, all the function are in this class.
class JokeTeller:
    def __init__(self, root):
        # In this fucntion we intialize the variables the screen size and calling the setup ui function.
        self.root = root
        self.root.title("Joke Teller")
        self.root.geometry(f"800x600+{(root.winfo_screenwidth()-600)//2}+{(root.winfo_screenheight()-400)//2}")
        self.root.configure(bg="#E8F4F8")
        
        # Initialize main variables
        self.current_punchline = ""
        self.jokes = [line.strip().split('?') for line in open("randomJokes.txt", "r") if '?' in line]
        self.waiting_for_joke = True  # Check if user is ready for a new joke
        
        self.setup_ui()

    def setup_ui(self):
        # This function is a centeral frame to hold widgets.
        main_frame = tk.Frame(self.root, bg="#E8F4F8")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add labels for app title, change its font color and anyother customization is done here.
        for widget in [
            (tk.Label, {"text": "🎭 Joke Teller 🎭", "font": ("Helvetica", 24, "bold"), "bg": "#E8F4F8", "fg": "#2C3E50"}, {"pady": (0, 30)}),
            (tk.Label, {"text": "Ready to hear a joke? Type 'Alexa, tell me a joke' below!", "font": ("Helvetica", 16), "bg": "#E8F4F8", "fg": "#34495E", "wraplength": 700, "height": 3}, {"pady": (0, 20)}),
            (tk.Label, {"text": "", "font": ("Helvetica", 16, "italic"), "bg": "#E8F4F8", "fg": "#E74C3C", "wraplength": 700, "height": 3}, {"pady": (0, 30)})
        ]:
            w = widget[0](main_frame, **widget[1])
            w.pack(**widget[2])
            # Store references for setup and punchline labels
            if widget[1]["text"] == "Ready to hear a joke? Type 'Alexa, tell me a joke' below!":
                self.setup_label = w
            elif widget[1]["text"] == "":
                self.punchline_label = w

        self.command_entry = tk.Entry(main_frame, font=("Helvetica", 14), width=30)
        self.command_entry.pack(pady=(0, 20))
        self.command_var = tk.StringVar()
        self.command_entry.config(textvariable=self.command_var)
        self.command_var.trace_add("write", self.handle_alexa_command)

        # Creating frame and buttons for joke control options
        button_frame = tk.Frame(main_frame, bg="#E8F4F8")
        button_frame.pack(pady=(0, 20))

        # Configs for buttons to control joke actions
        button_configs = [
            ("Tell me a joke! 😊", self.display_new_joke, "#3498DB", tk.DISABLED),
            ("Reveal Punchline! 🎯", self.reveal_punchline, "#2ECC71", tk.DISABLED),
            ("Quit 👋", self.root.quit, "#E74C3C", tk.NORMAL)
        ]

        # Creating buttons and seting up commands
        for text, command, bg, state in button_configs:
            btn = tk.Button(button_frame if text != "Quit 👋" else main_frame, 
                          text=text, command=command, font=("Helvetica", 12, "bold"), 
                          bg=bg, fg="white", width=15 if text != "Quit 👋" else 10, 
                          state=state, relief=tk.RAISED, cursor="hand2")
            if text == "Reveal Punchline! 🎯":
                self.reveal_button = btn
            elif text == "Tell me a joke! 😊":
                self.tell_joke_button = btn
            btn.pack(side=tk.LEFT if text != "Quit 👋" else tk.TOP, padx=10 if text != "Quit 👋" else 0, pady=(20, 0) if text == "Quit 👋" else 0)

    # this function is used to handle the Alexa command from user input.
    def handle_alexa_command(self, *args):
        if not self.waiting_for_joke: 
            return

        command = self.command_var.get().strip().lower()
        if command in ["alexa tell me a joke", "alexa, tell me a joke"]:
            self.tell_joke_button.config(state=tk.NORMAL)
            self.setup_label.config(text="Great! Now click 'Tell me a joke!' button")
        else:
            # Disable button if command isn't recognized
            self.tell_joke_button.config(state=tk.DISABLED)
            self.setup_label.config(text="Please enter 'Alexa, tell me a joke' to hear a joke!")
            self.punchline_label.config(text="")

    # if the user asks for another joke this function will be called.
    def display_new_joke(self):
        if self.jokes:
            self.waiting_for_joke = False
            # Randomly select a joke setup and punchline
            setup, punchline = random.choice(self.jokes)
            self.setup_label.config(text=setup + '?')
            self.punchline_label.config(text="")
            self.current_punchline = punchline
            self.reveal_button.config(state=tk.NORMAL)
            self.tell_joke_button.config(state=tk.DISABLED)
            self.command_var.set("") 
            self.command_entry.focus() 
        else:
            self.setup_label.config(text="Error: No jokes loaded from file!")

    # this function reveals the punchline when the button of reveal punchline is clicked and the function is called.
    def reveal_punchline(self):
        self.punchline_label.config(text=self.current_punchline)
        self.reveal_button.config(state=tk.DISABLED)
        self.setup_label.config(text="Type 'Alexa, tell me a joke' for another joke!")
        self.current_punchline = ""
        self.waiting_for_joke = True 

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeTeller(root)
    root.mainloop()
