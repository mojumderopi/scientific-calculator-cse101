import tkinter as tk
import math


# ============================================================
# SCIENTIFIC CALCULATOR
# ============================================================

class ScientificCalculator:

    def __init__(self, window):

        self.window = window
        self.window.title("Scientific Calculator")
        self.window.geometry("700x650")
        self.window.resizable(False, False)

        # ----------------------------------------------------
        # Calculator state
        # ----------------------------------------------------

        self.expression = ""
        self.answer = 0
        self.mode = "DEG"

        # ----------------------------------------------------
        # Colors
        # ----------------------------------------------------

        self.bg_color = "#202124"
        self.display_color = "#303134"
        self.number_color = "#3c4043"
        self.operator_color = "#5f6368"
        self.function_color = "#4b4f52"
        self.equal_color = "#1a73e8"
        self.text_color = "white"

        self.window.configure(bg=self.bg_color)

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        self.display = tk.Entry(
            window,
            font=("Arial", 28),
            bg=self.display_color,
            fg=self.text_color,
            insertbackground="white",
            justify="right",
            relief="flat",
            bd=10
        )

        self.display.grid(
            row=0,
            column=0,
            columnspan=6,
            padx=10,
            pady=(15, 5),
            sticky="nsew"
        )

        # ----------------------------------------------------
        # Mode label
        # ----------------------------------------------------

        self.mode_label = tk.Label(
            window,
            text="DEG",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg="white"
        )

        self.mode_label.grid(
            row=1,
            column=0,
            columnspan=6,
            sticky="e",
            padx=20
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        buttons = [

            # Row 1
            ("DEG", 2, 0),
            ("(", 2, 1),
            (")", 2, 2),
            ("⌫", 2, 3),
            ("C", 2, 4),
            ("÷", 2, 5),

            # Row 2
            ("sin", 3, 0),
            ("cos", 3, 1),
            ("tan", 3, 2),
            ("7", 3, 3),
            ("8", 3, 4),
            ("9", 3, 5),

            # Row 3
            ("asin", 4, 0),
            ("acos", 4, 1),
            ("atan", 4, 2),
            ("4", 4, 3),
            ("5", 4, 4),
            ("6", 4, 5),

            # Row 4
            ("log", 5, 0),
            ("ln", 5, 1),
            ("√", 5, 2),
            ("1", 5, 3),
            ("2", 5, 4),
            ("3", 5, 5),

            # Row 5
            ("x²", 6, 0),
            ("xʸ", 6, 1),
            ("!", 6, 2),
            ("0", 6, 3),
            (".", 6, 4),
            ("=", 6, 5),

            # Row 6
            ("π", 7, 0),
            ("e", 7, 1),
            ("EXP", 7, 2),
            ("ANS", 7, 3),
            ("+", 7, 4),
            ("−", 7, 5),

            # Row 7
            ("×", 8, 0),
            ("%", 8, 1),
            ("±", 8, 2),
            ("History", 8, 3),
            ("Clear History", 8, 4),
            ("Exit", 8, 5),
        ]

        for text, row, column in buttons:

            button = tk.Button(
                window,
                text=text,
                font=("Arial", 13, "bold"),
                fg="white",
                bg=self.get_button_color(text),
                activebackground="#777777",
                activeforeground="white",
                relief="flat",
                bd=0,
                command=lambda value=text: self.button_click(value)
            )

            button.grid(
                row=row,
                column=column,
                padx=4,
                pady=4,
                ipadx=5,
                ipady=10,
                sticky="nsew"
            )

        # ----------------------------------------------------
        # History window
        # ----------------------------------------------------

        self.history = []

        # ----------------------------------------------------
        # Keyboard
        # ----------------------------------------------------

        self.window.bind("<Return>", lambda event: self.calculate())
        self.window.bind("<Escape>", lambda event: self.clear())

    # ========================================================
    # Button colors
    # ========================================================

    def get_button_color(self, text):

        if text == "=":
            return self.equal_color

        if text in ["+", "−", "×", "÷", "%", "xʸ"]:
            return self.operator_color

        if text in [
            "sin", "cos", "tan",
            "asin", "acos", "atan",
            "log", "ln", "√",
            "x²", "!", "π", "e",
            "EXP", "ANS", "DEG"
        ]:
            return self.function_color

        if text in ["C", "⌫", "Exit", "History", "Clear History"]:
            return "#7b1fa2"

        return self.number_color

    # ========================================================
    # Button handler
    # ========================================================

    def button_click(self, value):

        if value == "=":
            self.calculate()

        elif value == "C":
            self.clear()

        elif value == "⌫":
            self.backspace()

        elif value == "Exit":
            self.window.destroy()

        elif value == "DEG":
            self.toggle_mode()

        elif value == "History":
            self.show_history()

        elif value == "Clear History":
            self.history.clear()

        elif value == "sin":
            self.insert_function("sin(")

        elif value == "cos":
            self.insert_function("cos(")

        elif value == "tan":
            self.insert_function("tan(")

        elif value == "asin":
            self.insert_function("asin(")

        elif value == "acos":
            self.insert_function("acos(")

        elif value == "atan":
            self.insert_function("atan(")

        elif value == "log":
            self.insert_function("log(")

        elif value == "ln":
            self.insert_function("ln(")

        elif value == "√":
            self.insert_function("sqrt(")

        elif value == "x²":
            self.expression += "**2"
            self.update_display()

        elif value == "xʸ":
            self.expression += "**"
            self.update_display()

        elif value == "!":
            self.expression += "!"
            self.update_display()

        elif value == "π":
            self.expression += "pi"
            self.update_display()

        elif value == "e":
            self.expression += "e"
            self.update_display()

        elif value == "EXP":
            self.expression += "e**"
            self.update_display()

        elif value == "ANS":
            self.expression += str(self.answer)
            self.update_display()

        elif value == "×":
            self.expression += "*"
            self.update_display()

        elif value == "÷":
            self.expression += "/"
            self.update_display()

        elif value == "−":
            self.expression += "-"
            self.update_display()

        elif value == "±":
            if self.expression:
                self.expression = f"-({self.expression})"
            else:
                self.expression = "-"

            self.update_display()

        elif value == "%":
            self.expression += "/100"
            self.update_display()

        else:
            self.expression += value
            self.update_display()

    # ========================================================
    # Insert function
    # ========================================================

    def insert_function(self, function):

        self.expression += function
        self.update_display()

    # ========================================================
    # Update display
    # ========================================================

    def update_display(self):

        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    # ========================================================
    # Clear
    # ========================================================

    def clear(self):

        self.expression = ""
        self.display.delete(0, tk.END)

    # ========================================================
    # Backspace
    # ========================================================

    def backspace(self):

        self.expression = self.expression[:-1]
        self.update_display()

    # ========================================================
    # Toggle DEG/RAD
    # ========================================================

    def toggle_mode(self):

        if self.mode == "DEG":
            self.mode = "RAD"
        else:
            self.mode = "DEG"

        self.mode_label.config(text=self.mode)

    # ========================================================
    # Factorial
    # ========================================================

    def factorial(self, x):

        if x < 0 or int(x) != x:
            raise ValueError("Factorial requires a non-negative integer")

        return math.factorial(int(x))

    # ========================================================
    # Trigonometric functions
    # ========================================================

    def sin(self, x):

        if self.mode == "DEG":
            x = math.radians(x)

        return math.sin(x)

    def cos(self, x):

        if self.mode == "DEG":
            x = math.radians(x)

        return math.cos(x)

    def tan(self, x):

        if self.mode == "DEG":
            x = math.radians(x)

        return math.tan(x)

    # ========================================================
    # Inverse trigonometric functions
    # ========================================================

    def asin(self, x):

        result = math.asin(x)

        if self.mode == "DEG":
            return math.degrees(result)

        return result

    def acos(self, x):

        result = math.acos(x)

        if self.mode == "DEG":
            return math.degrees(result)

        return result

    def atan(self, x):

        result = math.atan(x)

        if self.mode == "DEG":
            return math.degrees(result)

        return result

    # ========================================================
    # Calculate
    # ========================================================

    def calculate(self):

        if not self.expression:
            return

        original_expression = self.expression

        try:

            expression = self.expression

            # ------------------------------------------------
            # Convert factorial
            # Example:
            # 5! → factorial(5)
            # ------------------------------------------------

            while "!" in expression:

                position = expression.find("!")

                left = position - 1

                if left < 0:
                    raise ValueError("Invalid factorial")

                if expression[left] == ")":

                    depth = 1
                    left -= 1

                    while left >= 0 and depth > 0:

                        if expression[left] == ")":
                            depth += 1

                        elif expression[left] == "(":
                            depth -= 1

                        left -= 1

                    operand = expression[left + 1:position]

                else:

                    start = left

                    while start >= 0 and (
                        expression[start].isdigit()
                        or expression[start] == "."
                    ):
                        start -= 1

                    operand = expression[start + 1:position]

                expression = (
                    expression[:left + 1]
                    + f"factorial({operand})"
                    + expression[position + 1:]
                )

            # ------------------------------------------------
            # Allowed functions
            # ------------------------------------------------

            allowed = {
                "sin": self.sin,
                "cos": self.cos,
                "tan": self.tan,
                "asin": self.asin,
                "acos": self.acos,
                "atan": self.atan,
                "log": math.log10,
                "ln": math.log,
                "sqrt": math.sqrt,
                "factorial": self.factorial,
                "pi": math.pi,
                "e": math.e
            }

            # ------------------------------------------------
            # Evaluate
            # ------------------------------------------------

            result = eval(
                expression,
                {"__builtins__": {}},
                allowed
            )

            # ------------------------------------------------
            # Format result
            # ------------------------------------------------

            if isinstance(result, float):

                if result.is_integer():
                    result = int(result)

                else:
                    result = round(result, 12)

            self.answer = result

            self.history.append(
                f"{original_expression} = {result}"
            )

            self.expression = str(result)
            self.update_display()

        except ZeroDivisionError:

            self.display_error("Cannot divide by zero")

        except ValueError as error:

            self.display_error(str(error))

        except Exception:

            self.display_error("Invalid expression")

    # ========================================================
    # Error display
    # ========================================================

    def display_error(self, message):

        self.expression = ""
        self.display.delete(0, tk.END)
        self.display.insert(0, message)

    # ========================================================
    # History
    # ========================================================

    def show_history(self):

        history_window = tk.Toplevel(self.window)

        history_window.title("Calculation History")
        history_window.geometry("450x400")

        history_window.configure(bg=self.bg_color)

        listbox = tk.Listbox(
            history_window,
            font=("Arial", 13),
            bg=self.display_color,
            fg="white",
            selectbackground="#1a73e8"
        )

        listbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        if self.history:

            for item in self.history:
                listbox.insert(tk.END, item)

        else:

            listbox.insert(
                tk.END,
                "No calculations yet."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    window = tk.Tk()

    calculator = ScientificCalculator(window)

    window.mainloop()