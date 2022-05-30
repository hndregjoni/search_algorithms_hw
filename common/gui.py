from tkinter import filedialog
from typing import List, Optional

from threading import Thread, Event

from tkinter import BOTTOM, Tk, RIGHT, BOTH, RAISED, CENTER, IntVar, LEFT, Canvas, E
from tkinter.filedialog import FileDialog
from tkinter.ttk import Frame, Button, Style, Scale, Label
from PIL import ImageTk, Image
from time import sleep


class AnimationThead(Thread):
    variable: IntVar
    running: bool = False
    rate: int = 1

    min: int
    max: int

    quit_event: Event

    def __init__(self, variable: IntVar, min: int, max: int, interval: float = 1.5):
        super().__init__()
        self.variable = variable
        self.interval = interval

        self.min = min
        self.max = max

        self.quit_event = Event()
    
    def run(self):
        try:
            while not self.quit_event.is_set():
                sleep(self.interval)
                value = self.variable.get()

                if value == self.max:
                    self.rate = -1
                
                if value == self.min:
                    self.rate = 1

                if self.running:
                    self.variable.set(value+self.rate)
        except Exception:
            pass


class SolutionDisplay(Frame):
    N: int
    W: int
    H: int

    animation_thread: AnimationThead

    solutions: Optional[List[str]]
    images: List[Image.Image]

    scroll_var: IntVar

    #Labels
    progress_label: Label
    action_label: Label 

    animate_button: Button

    def __init__(self, solutions: Optional[List[str]], images: List[Image.Image]):
        super().__init__()

        self.solutions = solutions
        self._pil_images = images
        self.images = [*map(ImageTk.PhotoImage, images)]

        self.W = self.images[0].width()
        self.H = self.images[0].height()

        self.animation_thread = None

        if self.solutions is not None:
            self.N = len(self.solutions)
        else:
            self.N = len(self.images)

        self.initUI()
    
    def quit(self):
        if self.animation_thread is not None:
            self.animation_thread.quit_event.set()
    
    def toggle_animation(self, *args):
        if self.animation_thread is None:
            self.animation_thread = AnimationThead(self.scroll_var, 1, self.N)
            self.animation_thread.start()

        if self.animation_thread is not None:
            val = self.animation_thread.running
            val ^= True
            self.animation_thread.running = val

            if val:
                self.animate_button.config(text="Stop")
            else:
                self.animate_button.config(text="Animate")
            
    def save(self, *action):
        curr = self.scroll_var.get()
        path = filedialog.asksaveasfilename(filetypes=[("PNG", ".png"), ("JPEG", ".jpg")])
        if path is not None and len(path) > 0:
            self._pil_images[curr-1].save(path)
    
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
    
    def speed_event(self, change):
        def callback(*args):
            if self.animation_thread is None:
                return

            interval = self.animation_thread.interval
            interval = max(min(interval + change*0.2, 3), .2)
            self.animation_thread.interval = interval
        
        return callback
    
    def next_event(self, step):
        def callback(*args):
            st = self.scroll_var.get()
            st += step
            self.scroll_var.set(st)
        
        return callback

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

        buttons_frame = Frame(self, borderwidth=1)
        buttons_frame.pack(side=RIGHT)
        #Down
        down_button = Button(buttons_frame, text="🠗", width=2)
        down_button.grid(row=0, column=0, padx=5, pady=5)
        down_button.bind('<Button-1>', self.speed_event(-1))
        #Animate
        self.animate_button = animate_button = Button(buttons_frame, text="Animate")
        animate_button.grid(row=0, column=1, sticky='news', padx=5, pady=5)
        #Up
        up_button = Button(buttons_frame, text="🠕", width=2)
        up_button.grid(row=0, column=2, padx=5, pady=5)
        up_button.bind('<Button-1>', self.speed_event(-1))
        #Left
        left_button = Button(buttons_frame, text="🠔", width=2)
        left_button.grid(row=1, column=0, padx=5, pady=5)
        left_button.bind('<Button-1>', self.next_event(-1))
        #Save
        save_button = Button(buttons_frame, text="Save")
        save_button.grid(row=1, column=1, sticky='news', padx=5, pady=5)
        save_button.bind('<Button-1>', self.save)
        #Right
        right_button = Button(buttons_frame, text="🠖", width=2)
        right_button.grid(row=1, column=2, padx=5, pady=5)
        right_button.bind('<Button-1>', self.next_event(1))

        scale = Scale(self, variable = scroll_var, from_=1, to=self.N)
        scale.pack(anchor=CENTER, padx=5, pady=5, fill="both")

        self.progress_label = progress_label = Label(self, text="1/10")
        progress_label.pack(side=LEFT, padx=5, pady=5, fill="none")

        self.action_label = action_label = Label(self, text="")
        action_label.pack(anchor=CENTER, padx=5, pady=5, fill="both")

        # Add animate button handler
        animate_button.bind('<Button-1>', self.toggle_animation)

        scroll_var.set(1)