import tkinter as tk
from tkinter import messagebox
import math
from datetime import datetime

# ---------------- GLOBAL DATA ----------------
history = []
undo_stack = []
redo_stack = []

# Static currency rates (to INR)
currency_rates = {
    "USD": 83.0,
    "EUR": 90.0,
    "GBP": 105.0,
    "RUB": 0.90,
    "JPY": 0.55,
    "CNY": 11.5,
    "AED": 22.6,
    "CAD": 61.0,
    "AUD": 55.0,
    "SGD": 62.0
}

# ---------------- FUNCTIONS ----------------
def press(key):
    undo_stack.append(entry.get())
    entry.insert(tk.END, key)

def clear():
    entry.delete(0, tk.END)

def backspace():
    undo_stack.append(entry.get())
    entry.delete(len(entry.get())-1, tk.END)

def undo():
    if undo_stack:
        redo_stack.append(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, undo_stack.pop())

def redo():
    if redo_stack:
        entry.delete(0, tk.END)
        entry.insert(0, redo_stack.pop())

def calculate():
    try:
        expression = entry.get()
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))

        history.append({
            "expr": expression,
            "result": result,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except:
        messagebox.showerror("Error", "Invalid Expression")

def scientific(func):
    try:
        value = float(entry.get())
        result = func(value)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        messagebox.showerror("Error", "Invalid Input")

def show_history():
    hist_win = tk.Toplevel(root)
    hist_win.title("MCAL - History")

    text = tk.Text(hist_win, width=60, height=20)
    text.pack()

    for h in history:
        text.insert(tk.END, f"{h['date']} | {h['expr']} = {h['result']}\n")

def search_history():
    date = entry.get()
    result = [h for h in history if h['date'].startswith(date)]

    hist_win = tk.Toplevel(root)
    hist_win.title("Search Result")

    text = tk.Text(hist_win, width=60, height=20)
    text.pack()

    for h in result:
        text.insert(tk.END, f"{h['date']} | {h['expr']} = {h['result']}\n")

def convert_currency():
    try:
        amount = float(entry.get())
        win = tk.Toplevel(root)
        win.title("Currency Converter → INR")

        for cur, rate in currency_rates.items():
            tk.Label(win, text=f"{cur} → INR = {amount * rate:.2f}").pack()
    except:
        messagebox.showerror("Error", "Enter amount first")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("MCAL - Modern Calculator")
root.geometry("450x600")

entry = tk.Entry(root, font=("Arial", 20), bd=5, relief=tk.RIDGE, justify="right")
entry.pack(fill=tk.BOTH, padx=10, pady=10)
entry.bind("<Return>", lambda event: calculate())

btns = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    ("0", ".", "%", "+")
]

for row in btns:
    frame = tk.Frame(root)
    frame.pack()
    for b in row:
        tk.Button(frame, text=b, width=8, height=2,
                  command=lambda x=b: press(x)).pack(side=tk.LEFT)

# Control buttons
ctrl = tk.Frame(root)
ctrl.pack()
for txt, cmd in [
    ("=", calculate), ("C", clear), ("⌫", backspace),
    ("Undo", undo), ("Redo", redo)
]:
    tk.Button(ctrl, text=txt, width=8, command=cmd).pack(side=tk.LEFT)

# Scientific buttons
sci = tk.Frame(root)
sci.pack()
tk.Button(sci, text="sin", command=lambda: scientific(math.sin)).pack(side=tk.LEFT)
tk.Button(sci, text="cos", command=lambda: scientific(math.cos)).pack(side=tk.LEFT)
tk.Button(sci, text="tan", command=lambda: scientific(math.tan)).pack(side=tk.LEFT)
tk.Button(sci, text="√", command=lambda: scientific(math.sqrt)).pack(side=tk.LEFT)
tk.Button(sci, text="log", command=lambda: scientific(math.log10)).pack(side=tk.LEFT)

# Extra
extra = tk.Frame(root)
extra.pack(pady=5)
tk.Button(extra, text="History", command=show_history).pack(side=tk.LEFT)
tk.Button(extra, text="Search by Date", command=search_history).pack(side=tk.LEFT)
tk.Button(extra, text="Currency → INR", command=convert_currency).pack(side=tk.LEFT)

root.mainloop()
