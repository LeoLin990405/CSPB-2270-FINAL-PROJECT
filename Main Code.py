#!/usr/bin/env python
# coding: utf-8

# In[11]:


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import random

# Constants
COLOR_PALETTE = ["#FFAAAA", "#AAAAFF", "#AAFFAA", "#FFAFAF", "#AFAFFF", "#AFFFAF"]
COMPLETION_COLORS = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f"]
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 400
DEFAULT_NUMBER_COUNT = 20
DEFAULT_MIN_VALUE = 10
DEFAULT_MAX_VALUE = 999
SORT_DELAY = 150  # Initial delay between each sorting operation in milliseconds

def get_digit(number, exp):
    return (number // (10 ** exp)) % 10

def get_max_digit_length(numbers):
    return max((len(str(num)) for num in numbers), default=0)

class RadixSort:
    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.digits = get_max_digit_length(visualizer.numbers)
        self.paused = False
        self.current_exp = 0

    def lsd_radix_sort_step(self):
        if self.paused or self.current_exp >= self.digits:
            self.visualizer.update_status("LSD Radix Sort completed.")
            self.visualizer.complete_animation()
            return
        self.counting_sort(self.current_exp)
        self.current_exp += 1
        self.visualizer.master.after(self.visualizer.sort_delay, self.lsd_radix_sort_step)

    def msd_radix_sort_step(self):
        generator = self.msd_sort(self.visualizer.numbers, self.digits - 1)
        self.process_sort(generator, [])

    def msd_sort(self, numbers, digit):
        if digit < 0:
            yield numbers
        else:
            buckets = [[] for _ in range(10)]
            for number in numbers:
                idx = get_digit(number, digit)
                buckets[idx].append(number)
            result = []
            for bucket in buckets:
                if bucket:
                    for sorted_bucket in self.msd_sort(bucket, digit - 1):
                        result.extend(sorted_bucket)
                        yield result

    def process_sort(self, generator, result):
        if self.paused:
            return
        try:
            next_result = next(generator)
            self.visualizer.numbers[:] = next_result
            self.visualizer.draw_numbers()
            self.visualizer.master.after(self.visualizer.sort_delay, lambda: self.process_sort(generator, next_result))
        except StopIteration:
            self.visualizer.update_status("MSD Radix Sort completed.")
            self.visualizer.complete_animation()

    def counting_sort(self, exp):
        output = [0] * len(self.visualizer.numbers)
        count = [0] * 10
        for number in self.visualizer.numbers:
            index = get_digit(number, exp)
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(len(self.visualizer.numbers) - 1, -1, -1):
            number = self.visualizer.numbers[i]
            index = get_digit(number, exp)
            output[count[index] - 1] = number
            count[index] -= 1
        self.visualizer.numbers[:] = output
        self.visualizer.draw_numbers()

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.visualizer.update_status("Resuming sort...")
            self.lsd_radix_sort_step()  # Continue sorting where paused

class SortingVisualizer:
    def __init__(self, master):
        self.master = master
        self.numbers = []
        self.sort_delay = SORT_DELAY
        self.current_sort = None
        self.setup_ui()
        self.setup_sidebar()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.master, width=DEFAULT_WINDOW_WIDTH, height=DEFAULT_WINDOW_HEIGHT, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame = ttk.Frame(self.master)
        frame.pack(fill=tk.X, side=tk.TOP)
        ttk.Button(frame, text="Generate", command=self.generate_numbers).pack(side=tk.LEFT)
        ttk.Button(frame, text="Start LSD Sort", command=lambda: self.start_sort('LSD')).pack(side=tk.LEFT)
        ttk.Button(frame, text="Start MSD Sort", command=lambda: self.start_sort('MSD')).pack(side=tk.LEFT)
        ttk.Button(frame, text="Pause/Resume", command=self.toggle_pause).pack(side=tk.LEFT)
        self.status_label = ttk.Label(self.master, text="Ready to sort!", font=("Helvetica", 10))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def setup_sidebar(self):
        self.sidebar = ttk.Frame(self.master, width=200)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.info_text = scrolledtext.ScrolledText(self.sidebar, font=("Helvetica", 10), height=10)
        self.info_text.pack(pady=20, padx=10)
        self.update_info("Instructions:\n1. Generate numbers\n2. Choose a sort type\n3. Use pause/resume as needed.")

    def update_info(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED)

    def generate_numbers(self):
        self.numbers = [random.randint(DEFAULT_MIN_VALUE, DEFAULT_MAX_VALUE) for _ in range(DEFAULT_NUMBER_COUNT)]
        self.draw_numbers()
        self.update_status("Ready to sort!")

    def draw_numbers(self):
        self.canvas.delete("all")
        bar_width = DEFAULT_WINDOW_WIDTH / len(self.numbers)
        max_height = max(self.numbers, default=1)
        for i, num in enumerate(self.numbers):
            x0 = i * bar_width
            y0 = DEFAULT_WINDOW_HEIGHT - (num / max_height * DEFAULT_WINDOW_HEIGHT)
            x1 = x0 + bar_width
            y1 = DEFAULT_WINDOW_HEIGHT
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=COLOR_PALETTE[i % len(COLOR_PALETTE)])
            self.canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(num), font=("Helvetica", 10), fill="black")

    def complete_animation(self):
        for i, num in enumerate(self.numbers):
            color = COMPLETION_COLORS[i % len(COMPLETION_COLORS)]
            self.master.after(100 * i, lambda i=i, color=color: self.highlight_bar(i, color))

    def highlight_bar(self, index, color):
        bar_width = DEFAULT_WINDOW_WIDTH / len(self.numbers)
        num = self.numbers[index]
        x0 = index * bar_width
        y0 = DEFAULT_WINDOW_HEIGHT - (num / max(self.numbers, default=1) * DEFAULT_WINDOW_HEIGHT)
        x1 = x0 + bar_width
        y1 = DEFAULT_WINDOW_HEIGHT
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    def update_status(self, message):
        self.status_label.config(text=message)

    def start_sort(self, sort_type):
        if sort_type == 'LSD':
            self.current_sort = RadixSort(self)
            self.current_sort.lsd_radix_sort_step()
        elif sort_type == 'MSD':
            self.current_sort = RadixSort(self)
            self.current_sort.msd_radix_sort_step()

    def toggle_pause(self):
        if self.current_sort:
            self.current_sort.toggle_pause()

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()


# In[7]:





# In[10]:





# In[2]:





# In[5]:





# In[6]:





# In[9]:





# In[15]:





# In[17]:





# In[24]:





# In[27]:





# In[28]:





# In[29]:





# In[ ]:




