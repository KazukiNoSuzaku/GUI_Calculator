import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("320x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        # Current expression
        self.current = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")

        # Create display
        self.create_display()

        # Create buttons
        self.create_buttons()

        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)

    def create_display(self):
        display_frame = tk.Frame(self.root, bg="#2c3e50")
        display_frame.pack(pady=20, padx=10, fill=tk.BOTH)

        display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 32),
            bg="#34495e",
            fg="black",
            justify=tk.RIGHT,
            bd=0,
            insertbackground="white"
        )
        display.pack(fill=tk.BOTH, ipady=10)
        display.config(state='readonly')

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Button layout
        buttons = [
            ['C', '⌫', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        colors = {
            'number': {'bg': '#34495e', 'fg': 'white'},
            'operator': {'bg': '#e67e22', 'fg': 'white'},
            'special': {'bg': "#041b1d", 'fg': 'white'},
            'equal': {'bg': '#27ae60', 'fg': 'white'}
        }

        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                if text == '':
                    continue

                # Determine button color
                if text in ['C', '⌫', '%']:
                    color = colors['special']
                elif text in ['÷', '×', '-', '+']:
                    color = colors['operator']
                elif text == '=':
                    color = colors['equal']
                else:
                    color = colors['number']

                # Create button
                btn = tk.Button(
                    button_frame,
                    text=text,
                    font=('Arial', 18, 'bold'),
                    bg=color['bg'],
                    fg=color['fg'],
                    activebackground=color['bg'],
                    activeforeground=color['fg'],
                    bd=0,
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=lambda t=text: self.on_button_click(t)
                )

                # Grid placement
                if text == '0':
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, sticky="nsew", padx=2, pady=2)
                elif text == '=':
                    btn.grid(row=row_idx, column=col_idx+1, sticky="nsew", padx=2, pady=2)
                else:
                    btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)

        # Configure grid weights
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.current = ""
            self.display_var.set("0")
        elif char == '⌫':
            self.current = self.current[:-1]
            self.display_var.set(self.current if self.current else "0")
        elif char == '=':
            self.calculate()
        elif char == '×':
            self.current += '*'
            self.display_var.set(self.current)
        elif char == '÷':
            self.current += '/'
            self.display_var.set(self.current)
        else:
            self.current += char
            self.display_var.set(self.current)

    def on_key_press(self, event):
        key = event.char
        keys_map = {
            '\r': '=',
            '\x08': '⌫',
            '\x1b': 'C',
            'x': '*',
            'X': '*'
        }

        if key in '0123456789.+-*/%=':
            self.on_button_click(key if key not in '*/' else ('×' if key == '*' else '÷'))
        elif key == '\r' or event.keysym == 'Return':
            self.calculate()
        elif key == '\x08' or event.keysym == 'BackSpace':
            self.on_button_click('⌫')
        elif key == '\x1b' or event.keysym == 'Escape':
            self.on_button_click('C')

    def calculate(self):
        try:
            if self.current:
                result = eval(self.current)
                self.display_var.set(str(result))
                self.current = str(result)
        except Exception:
            self.display_var.set("Error")
            self.current = ""

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()