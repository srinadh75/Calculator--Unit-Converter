import tkinter as tk
from tkinter import ttk, messagebox
from math import sin, cos, tan, log, sqrt, pi, e
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class ScientificCalculator:

    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("800x600")
        self.theme = "dark"
        self.history = []
        self.history_file = "calc_history.txt"

        self.expression = ""
        self.input_text = tk.StringVar()

        self.tab_control = ttk.Notebook(self.root)
        self.calc_tab = tk.Frame(self.tab_control, bg="#1e1e1e")
        self.graph_tab = tk.Frame(self.tab_control, bg="#1e1e1e")

        self.tab_control.add(self.calc_tab, text='Calculator')
        self.tab_control.add(self.graph_tab, text='Graph Plotter')
        self.tab_control.pack(expand=True, fill='both')

        self.create_main_layout()
        self.create_buttons()
        self.create_graph_tab()
        self.update_theme()
        self.load_history()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_main_layout(self):
        self.entry = tk.Entry(self.calc_tab, textvariable=self.input_text, font=('Consolas', 20),
                              bd=0, justify='right')
        self.entry.pack(fill='x', ipady=20, padx=10, pady=(10, 0))
        self.entry.bind("<KeyPress>", self.key_input)

        self.content_frame = tk.Frame(self.calc_tab)
        self.content_frame.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self.content_frame)
        self.button_frame.pack(side='left', expand=True, fill='both')

        self.history_frame = tk.Frame(self.content_frame, width=200)
        self.history_frame.pack(side='right', fill='y')

        self.history_label = tk.Label(self.history_frame, text="History", font=('Arial', 12, 'bold'))
        self.history_label.pack(pady=(10, 0))

        self.history_listbox = tk.Listbox(self.history_frame, font=('Consolas', 12))
        self.history_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.history_listbox.bind("<Double-Button-1>", self.copy_result)

        self.theme_btn = tk.Button(self.history_frame, text="🌙 Toggle Theme", command=self.toggle_theme)
        self.theme_btn.pack(pady=5)

        self.unit_btn = tk.Button(self.history_frame, text="🔄 Unit Converter", command=self.open_unit_converter)
        self.unit_btn.pack(pady=5)

    def create_graph_tab(self):
        label = tk.Label(self.graph_tab, text="Enter function of x (e.g., sin(x), x**2 + 2*x):")
        label.pack(pady=10)

        self.graph_expr = tk.Entry(self.graph_tab, font=('Consolas', 14))
        self.graph_expr.pack(fill='x', padx=20)

        plot_btn = tk.Button(self.graph_tab, text="Plot Graph", command=self.plot_graph)
        plot_btn.pack(pady=10)

        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def plot_graph(self):
        expr = self.graph_expr.get()
        try:
            x = np.linspace(-10, 10, 400)
            y = eval(expr, {"x": x, "sin": np.sin, "cos": np.cos, "tan": np.tan,
                            "log": np.log10, "sqrt": np.sqrt, "pi": pi, "e": e,
                            "abs": abs, "round": round, "exp": np.exp})
            self.ax.clear()
            self.ax.plot(x, y)
            self.ax.set_title(f"y = {expr}")
            self.ax.grid(True)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Plot Error", f"Invalid function: {e}")

    def press(self, value):
        self.expression += str(value)
        self.input_text.set(self.expression)

    def clear(self):
        self.expression = ""
        self.input_text.set("")

    def evaluate(self):
        try:
            result = eval(self.expression, {"__builtins__": None}, {
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "log": np.log10, "ln": np.log, "sqrt": np.sqrt,
                "pi": pi, "e": e, "abs": abs, "round": round
            })
            result = str(result)
            record = f"{self.expression} = {result}"
            self.history.append(record)
            self.history_listbox.insert(tk.END, record)
            self.expression = result
            self.input_text.set(result)
        except:
            self.input_text.set("Error")
            self.expression = ""

    def key_input(self, event):
        char = event.char
        key = event.keysym

        if key == "Return":
            self.evaluate()
        elif key == "Escape":
            self.clear()
        elif key == "BackSpace":
            self.expression = self.expression[:-1]
            self.input_text.set(self.expression)
        elif char in "0123456789.+-*/()":
            self.press(char)
        elif char.isalpha():
            self.press(char)
        return "break"

    def copy_result(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            text = self.history_listbox.get(selection[0])
            result = text.split("=")[-1].strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.root.update()
            messagebox.showinfo("Copied", f"Copied to clipboard: {result}")

    def create_buttons(self):
        buttons = [
            ['7', '8', '9', '/', 'sin'],
            ['4', '5', '6', '*', 'cos'],
            ['1', '2', '3', '-', 'tan'],
            ['0', '.', 'sqrt', '+', '='],
            ['(', ')', 'log', 'ln', 'C']
        ]

        for r, row in enumerate(buttons):
            for c, btn in enumerate(row):
                cmd = (
                    self.evaluate if btn == '=' else
                    self.clear if btn == 'C' else
                    lambda x=btn: self.press(x)
                )
                tk.Button(self.button_frame, text=btn, font=('Arial', 14),
                          command=cmd).grid(row=r, column=c, sticky='nsew', padx=2, pady=2)

        for i in range(len(buttons)):
            self.button_frame.rowconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.columnconfigure(i, weight=1)

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.update_theme()

    def update_theme(self):
        dark = self.theme == "dark"
        bg = "#1e1e1e" if dark else "#f0f0f0"
        fg = "white" if dark else "black"
        entry_bg = "#2e2e2e" if dark else "white"
        btn_bg = "#333" if dark else "#ddd"
        btn_active = "#444" if dark else "#ccc"

        self.root.configure(bg=bg)
        self.calc_tab.configure(bg=bg)
        self.graph_tab.configure(bg=bg)
        self.content_frame.configure(bg=bg)
        self.button_frame.configure(bg=bg)
        self.history_frame.configure(bg=bg)
        self.entry.configure(bg=entry_bg, fg=fg, insertbackground=fg)

        self.history_label.configure(bg=bg, fg=fg)
        self.history_listbox.configure(bg=entry_bg, fg=fg)
        self.theme_btn.configure(bg=btn_bg, fg=fg, activebackground=btn_active)
        self.unit_btn.configure(bg=btn_bg, fg=fg, activebackground=btn_active)

        for widget in self.button_frame.winfo_children():
            widget.configure(bg=btn_bg, fg=fg, activebackground=btn_active, relief='flat')

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                for line in file:
                    record = line.strip()
                    self.history.append(record)
                    self.history_listbox.insert(tk.END, record)

    def save_history(self):
        with open(self.history_file, 'w') as file:
            for item in self.history:
                file.write(item + '\n')

    def on_closing(self):
        self.save_history()
        self.root.destroy()

    def open_unit_converter(self):
        def convert():
            category = category_var.get()
            try:
                value = float(entry_value.get())
                if category == "Length":
                    result = f"{value:.2f} m = {value * 3.28084:.2f} ft\n" \
                             f"{value * 100:.2f} cm = {value * 39.3701:.2f} in"
                elif category == "Weight":
                    result = f"{value:.2f} kg = {value * 2.20462:.2f} lb\n" \
                             f"{value * 1000:.2f} g = {value * 35.274:.2f} oz"
                elif category == "Temperature":
                    fahrenheit = (value * 9 / 5) + 32
                    kelvin = value + 273.15
                    result = f"{value:.2f} °C = {fahrenheit:.2f} °F\n{value:.2f} °C = {kelvin:.2f} K"
                elif category == "Speed":
                    result = f"{value:.2f} km/h = {value / 1.609:.2f} mph"
                elif category == "Area":
                    result = f"{value:.2f} sq m = {value * 10.764:.2f} sq ft"
                else:
                    result = "Select a category"
                label_result.config(text=result)
            except ValueError:
                label_result.config(text="Invalid input")

        dark = self.theme == "dark"
        bg = "#1e1e1e" if dark else "#f9f9f9"
        fg = "white" if dark else "#000000"
        entry_bg = "#2e2e2e" if dark else "#ffffff"
        btn_bg = "#444444" if dark else "#cccccc"
        active_bg = "#555555" if dark else "#bbbbbb"

        top = tk.Toplevel(self.root)
        top.title("All-in-One Unit Converter")
        top.geometry("380x270")
        top.configure(bg=bg)

        tk.Label(top, text="Select Category:", bg=bg, fg=fg, font=('Arial', 11)).pack(pady=(10, 5))
        category_var = tk.StringVar(value="Length")
        categories = ["Length", "Weight", "Temperature", "Speed", "Area"]
        category_menu = ttk.Combobox(top, textvariable=category_var, values=categories, state='readonly')
        category_menu.pack(pady=5)

        tk.Label(top, text="Enter Value:", bg=bg, fg=fg, font=('Arial', 11)).pack(pady=(10, 5))
        entry_value = tk.Entry(top, bg=entry_bg, fg=fg, insertbackground=fg, font=('Consolas', 12), relief='flat')
        entry_value.pack(pady=5)

        tk.Button(top, text="Convert", command=convert, bg=btn_bg, fg=fg,
                  activebackground=active_bg, font=('Arial', 12), relief='flat').pack(pady=15)

        label_result = tk.Label(top, text="", justify="left", bg=bg, fg=fg, font=('Consolas', 11))
        label_result.pack(pady=(5, 10))

if __name__ == "__main__":
    root = tk.Tk()
    ScientificCalculator(root)
    root.mainloop()
