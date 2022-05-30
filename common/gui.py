from typing import List, Optional

from threading import Thread

from tkinter import Tk, RIGHT, BOTH, RAISED, CENTER, IntVar, LEFT, Canvas
from tkinter.ttk import Frame, Button, Style, Scale, Label
from PIL import ImageTk, Image
from time import sleep

class AnimationThead(Thread):
    variable: IntVar
    running: bool = True
    rate: int = 1

    min: int
    max: int

    def __init__(self, variable: IntVar, min: int, max: int, interval: float = 1.2):
        super().__init__()
        self.variable = variable
        self.interval = interval

        self.min = min
        self.max = max
    
    def run(self):
        while True:
            sleep(self.interval)
            value = self.variable.get()

            if value == self.max:
                self.rate = -1
            
            if value == self.min:
                self.rate = 1

            if self.running:
                self.variable.set(value+self.rate)


class SolutionDisplay(Frame):
    N: int
    W: int
    H: int

    solutions: Optional[List[str]]
    images: List[Image.Image]

    scroll_var: IntVar
    animation_thread: Thread

    #Labels
    progress_label: Label
    action_label: Label 

    def __init__(self, solutions: Optional[List[str]], images: List[Image.Image]):
        super().__init__()

        self.solutions = solutions
        self.images = [*map(ImageTk.PhotoImage, images)]

        self.W = self.images[0].width()
        self.H = self.images[0].height()

        self.animation_thread = None

        if self.solutions is not None:
            self.N = len(self.solutions)
        else:
            self.N = len(self.images)

        self.initUI()
    
    def toggle_animation(self, *args):
        if self.animation_thread is None:
            self.animation_thread = AnimationThead(self.scroll_var, 1, self.N)
            self.animation_thread.start()
        elif self.animation_thread is not None:
            self.animation_thread.running ^= True    
    
    def change_step(self, n):
        self.progress_label.config(text=f"{n}/{self.N}")

        if self.solutions is not None:
            self.action_label.config(text=str(self.solutions[n-1]))

        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        self.canvas.config(image=self.images[n-1])
        pass

    def trace_scroll(self, *args):
        val = self.scroll_var.get()
        self.change_step(val)

    def initUI(self):

        self.master.title("Buttons")
        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.canvas = canvas = Label(frame)
        canvas.pack(expand=1, anchor=CENTER)

        self.pack(fill=BOTH, expand=True)

        self.scroll_var = scroll_var = IntVar(value=1)
        scroll_var.trace('w', self.trace_scroll)

        animate_button = Button(self, text="Animate")
        animate_button.pack(side=RIGHT, padx=5, pady=5)

        scale = Scale(self, variable = scroll_var, from_=1, to=self.N)
        scale.pack(anchor=CENTER, padx=5, pady=5, fill="both")

        self.progress_label = progress_label = Label(self, text="1/10")
        progress_label.pack(side=LEFT, padx=5, pady=5, fill="none")

        self.action_label = action_label = Label(self, text="")
        action_label.pack(anchor=CENTER, padx=5, pady=5, fill="both")

        # Add animate button handler
        animate_button.bind('<Button-1>', self.toggle_animation)

        scroll_var.set(1)