
import tkinter as tk
import math
import re


# ============================================================
# SAFE MATHEMATICAL EXPRESSION PARSER
# ============================================================

class MathParser:

    def __init__(self, expression, mode="DEG", ans=0):
        self.expression = expression
        self.mode = mode
        self.ans = ans

        self.tokens = self.tokenize(expression)
        self.position = 0

    # --------------------------------------------------------
    # TOKENIZER
    # --------------------------------------------------------

    def tokenize(self, expression):

        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("−", "-")
        expression = expression.replace("π", "pi")
        expression = expression.replace("√", "sqrt")
        expression = expression.replace("^", "^")

        pattern = r"""
            \s*
            (
                (?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?
                |
                [A-Za-z_][A-Za-z_0-9]*
                |
                \*\*
                |
                [+\-*/^(),!%]
            )
        """

        tokens = []

        position = 0

        while position < len(expression):

            match = re.match(pattern, expression[position:], re.VERBOSE)

            if not match:
                raise ValueError(
                    f"Invalid character: '{expression[position]}'"
                )

            token = match.group(1)

            if re.fullmatch(
                r"(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?",
                token
            ):
                tokens.append(("NUMBER", float(token)))

            elif re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", token):
                tokens.append(("NAME", token.lower()))

            else:
                tokens.append((token, token))

            position += match.end()

        tokens.append(("EOF", None))

        return tokens

    # --------------------------------------------------------
    # CURRENT TOKEN
    # --------------------------------------------------------

    def current(self):
        return self.tokens[self.position]

    # --------------------------------------------------------
    # ADVANCE
    # --------------------------------------------------------

    def advance(self):
        token = self.current()
        self.position += 1
        return token

    # --------------------------------------------------------
    # MATCH
    # --------------------------------------------------------

    def match(self, token_type):

        if self.current()[0] == token_type:
            self.advance()
            return True

        return False

    # --------------------------------------------------------
    # EXPECT
    # --------------------------------------------------------

    def expect(self, token_type):

        if not self.match(token_type):
            raise ValueError(
                f"Expected '{token_type}'"
            )

    # ========================================================
    # GRAMMAR
    # ========================================================
    #
    # expression
    #     → addition
    #
    # addition
    #     → multiplication ((+ | -) multiplication)*
    #
    # multiplication
    #     → unary ((* | /) unary)*
    #
    # unary
    #     → (+ | -) unary | power
    #
    # power
    #     → postfix (^ unary)?
    #
    # postfix
    #     → primary (! | %)*
    #
    # primary
    #     → number
    #     → constant
    #     → function
    #     → ( expression )
    #
    # ========================================================

    def parse(self):

        result = self.parse_addition()

        if self.current()[0] != "EOF":
            raise ValueError(
                f"Unexpected token: {self.current()[1]}"
            )

        return result

    # --------------------------------------------------------
    # ADDITION / SUBTRACTION
    # --------------------------------------------------------

    def parse_addition(self):

        result = self.parse_multiplication()

        while True:

            if self.match("+"):
                result += self.parse_multiplication()

            elif self.match("-"):
                result -= self.parse_multiplication()

            else:
                break

        return result

    # --------------------------------------------------------
    # MULTIPLICATION / DIVISION
    # --------------------------------------------------------

    def parse_multiplication(self):

        result = self.parse_unary()

        while True:

            if self.match("*"):
                result *= self.parse_unary()

            elif self.match("/"):
                divisor = self.parse_unary()

                if divisor == 0:
                    raise ZeroDivisionError(
                        "Cannot divide by zero"
                    )

                result /= divisor

            # ------------------------------------------------
            # Implicit multiplication
            #
            # 2pi
            # 2(3+4)
            # 3sin(30)
            # ------------------------------------------------

            elif self.starts_primary():

                result *= self.parse_unary()

            else:
                break

        return result

    # --------------------------------------------------------
    # UNARY +/-
    # --------------------------------------------------------

    def parse_unary(self):

        if self.match("+"):
            return +self.parse_unary()

        if self.match("-"):
            return -self.parse_unary()

        return self.parse_power()

    # --------------------------------------------------------
    # POWER
    # --------------------------------------------------------

    def parse_power(self):

        base = self.parse_postfix()

        if self.match("^"):

            exponent = self.parse_unary()

            try:
                return base ** exponent

            except OverflowError:
                raise ValueError("Number too large")

        return base

    # --------------------------------------------------------
    # FACTORIAL / PERCENT
    # --------------------------------------------------------

    def parse_postfix(self):

        result = self.parse_primary()

        while True:

            if self.match("!"):

                if result < 0 or int(result) != result:
                    raise ValueError(
                        "Factorial requires a non-negative integer"
                    )

                if result > 170:
                    raise ValueError(
                        "Factorial result is too large"
                    )

                result = math.factorial(int(result))

            elif self.match("%"):

                result /= 100

            else:
                break

        return result

    # --------------------------------------------------------
    # PRIMARY
    # --------------------------------------------------------

    def parse_primary(self):

        token_type, value = self.current()

        # Number
        if token_type == "NUMBER":
            self.advance()
            return value

        # Name
        if token_type == "NAME":

            self.advance()

            name = value

            # Constants
            if name == "pi":
                return math.pi

            if name == "e":
                return math.e

            if name == "ans":
                return self.ans

            # Functions
            if name in {
                "sin",
                "cos",
                "tan",
                "asin",
                "acos",
                "atan",
                "log",
                "ln",
                "sqrt"
            }:

                self.expect("(")

                argument = self.parse_addition()

                self.expect(")")

                return self.apply_function(
                    name,
                    argument
                )

            raise ValueError(
                f"Unknown function or constant: {name}"
            )

        # Parentheses
        if self.match("("):

            result = self.parse_addition()

            self.expect(")")

            return result

        raise ValueError(
            f"Unexpected token: {value}"
        )

    # --------------------------------------------------------
    # PRIMARY CHECK
    # --------------------------------------------------------

    def starts_primary(self):

        token_type, value = self.current()

        if token_type in ("NUMBER", "(", "NAME"):
            return True

        return False

    # --------------------------------------------------------
    # FUNCTIONS
    # --------------------------------------------------------

    def apply_function(self, name, x):

        if name == "sqrt":

            if x < 0:
                raise ValueError(
                    "Square root requires x ≥ 0"
                )

            return math.sqrt(x)

        if name == "log":

            if x <= 0:
                raise ValueError(
                    "log requires x > 0"
                )

            return math.log10(x)

        if name == "ln":

            if x <= 0:
                raise ValueError(
                    "ln requires x > 0"
                )

            return math.log(x)

        # ----------------------------------------------------
        # Trigonometric functions
        # ----------------------------------------------------

        if name == "sin":

            if self.mode == "DEG":
                x = math.radians(x)

            return math.sin(x)

        if name == "cos":

            if self.mode == "DEG":
                x = math.radians(x)

            return math.cos(x)

        if name == "tan":

            if self.mode == "DEG":
                x = math.radians(x)

            return math.tan(x)

        # ----------------------------------------------------
        # Inverse trigonometric functions
        # ----------------------------------------------------

        if name == "asin":

            if x < -1 or x > 1:
                raise ValueError(
                    "asin domain is [-1, 1]"
                )

            result = math.asin(x)

            if self.mode == "DEG":
                return math.degrees(result)

            return result

        if name == "acos":

            if x < -1 or x > 1:
                raise ValueError(
                    "acos domain is [-1, 1]"
                )

            result = math.acos(x)

            if self.mode == "DEG":
                return math.degrees(result)

            return result

        if name == "atan":

            result = math.atan(x)

            if self.mode == "DEG":
                return math.degrees(result)

            return result

        raise ValueError(
            f"Unknown function: {name}"
        )


# ============================================================
# SCIENTIFIC CALCULATOR GUI
# ============================================================

class ScientificCalculator:

    def __init__(self, window):

        self.window = window

        self.window.title(
            "Scientific Calculator"
        )

        self.window.geometry(
            "720x700"
        )

        self.window.resizable(
            False,
            False
        )

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        self.expression = ""
        self.answer = 0
        self.mode = "DEG"
        self.history = []

        # ----------------------------------------------------
        # Colors
        # ----------------------------------------------------

        self.bg_color = "#202124"
        self.display_color = "#303134"
        self.number_color = "#3c4043"
        self.operator_color = "#5f6368"
        self.function_color = "#4b4f52"
        self.equal_color = "#1a73e8"
        self.special_color = "#7b1fa2"

        self.window.configure(
            bg=self.bg_color
        )

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        self.display = tk.Entry(
            window,
            font=("Arial", 28),
            bg=self.display_color,
            fg="white",
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
        # Mode
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
            padx=20,
            pady=(0, 5)
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        buttons = [

            ("DEG", 2, 0),
            ("(", 2, 1),
            (")", 2, 2),
            ("⌫", 2, 3),
            ("C", 2, 4),
            ("÷", 2, 5),

            ("sin", 3, 0),
            ("cos", 3, 1),
            ("tan", 3, 2),
            ("7", 3, 3),
            ("8", 3, 4),
            ("9", 3, 5),

            ("asin", 4, 0),
            ("acos", 4, 1),
            ("atan", 4, 2),
            ("4", 4, 3),
            ("5", 4, 4),
            ("6", 4, 5),

            ("log", 5, 0),
            ("ln", 5, 1),
            ("√", 5, 2),
            ("1", 5, 3),
            ("2", 5, 4),
            ("3", 5, 5),

            ("x²", 6, 0),
            ("xʸ", 6, 1),
            ("!", 6, 2),
            ("0", 6, 3),
            (".", 6, 4),
            ("=", 6, 5),

            ("π", 7, 0),
            ("e", 7, 1),
            ("EXP", 7, 2),
            ("ANS", 7, 3),
            ("+", 7, 4),
            ("−", 7, 5),

            ("×", 8, 0),
            ("%", 8, 1),
            ("±", 8, 2),
            ("History", 8, 3),
            ("Clear History", 8, 4),
            ("Exit", 8, 5)
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
                command=lambda value=text:
                self.button_click(value)
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
        # Keyboard
        # ----------------------------------------------------

        self.window.bind(
            "<Return>",
            lambda event: self.calculate()
        )

        self.window.bind(
            "<Escape>",
            lambda event: self.clear()
        )

    # ========================================================
    # BUTTON COLORS
    # ========================================================

    def get_button_color(self, text):

        if text == "=":
            return self.equal_color

        if text in [
            "+",
            "−",
            "×",
            "÷",
            "%",
            "xʸ"
        ]:
            return self.operator_color

        if text in [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "log",
            "ln",
            "√",
            "x²",
            "!",
            "π",
            "e",
            "EXP",
            "ANS",
            "DEG"
        ]:
            return self.function_color

        if text in [
            "C",
            "⌫",
            "Exit",
            "History",
            "Clear History"
        ]:
            return self.special_color

        return self.number_color

    # ========================================================
    # BUTTON HANDLER
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

        elif value in [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "log",
            "ln"
        ]:
            self.expression += value + "("
            self.update_display()

        elif value == "√":
            self.expression += "sqrt("
            self.update_display()

        elif value == "x²":
            self.expression += "^2"
            self.update_display()

        elif value == "xʸ":
            self.expression += "^"
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
            # Scientific notation.
            # Example: 1 EXP 6 → 1e6
            self.expression += "e"
            self.update_display()

        elif value == "ANS":
            self.expression += "ans"
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
                self.expression = (
                    "-(" + self.expression + ")"
                )
            else:
                self.expression = "-"

            self.update_display()

        elif value == "%":
            self.expression += "%"
            self.update_display()

        else:
            self.expression += value
            self.update_display()

    # ========================================================
    # DISPLAY
    # ========================================================

    def update_display(self):

        self.display.delete(
            0,
            tk.END
        )

        display_expression = (
            self.expression
            .replace("pi", "π")
            .replace("sqrt", "√")
            .replace("ans", "ANS")
        )

        self.display.insert(
            0,
            display_expression
        )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):

        self.expression = ""

        self.display.delete(
            0,
            tk.END
        )

    # ========================================================
    # BACKSPACE
    # ========================================================

    def backspace(self):

        if not self.expression:
            return

        # Remove complete function names
        # rather than one character at a time.

        functions = [
            "sqrt(",
            "asin(",
            "acos(",
            "atan(",
            "sin(",
            "cos(",
            "tan(",
            "log(",
            "ln("
        ]

        for function in functions:

            if self.expression.endswith(function):

                self.expression = (
                    self.expression[:-len(function)]
                )

                self.update_display()
                return

        if self.expression.endswith("ans"):
            self.expression = self.expression[:-3]

        elif self.expression.endswith("pi"):
            self.expression = self.expression[:-2]

        else:
            self.expression = self.expression[:-1]

        self.update_display()

    # ========================================================
    # DEG / RAD
    # ========================================================

    def toggle_mode(self):

        if self.mode == "DEG":
            self.mode = "RAD"
        else:
            self.mode = "DEG"

        self.mode_label.config(
            text=self.mode
        )

    # ========================================================
    # CALCULATE
    # ========================================================

    def calculate(self):

        if not self.expression:
            return

        original_expression = (
            self.display.get()
        )

        try:

            parser = MathParser(
                self.expression,
                self.mode,
                self.answer
            )

            result = parser.parse()

            if not math.isfinite(result):
                raise ValueError(
                    "Result is not finite"
                )

            # ------------------------------------------------
            # Formatting
            # ------------------------------------------------

            if abs(result) < 1e-15:
                result = 0

            if result.is_integer():
                result = int(result)

            else:
                result = round(
                    result,
                    12
                )

            self.answer = result

            self.history.append(
                f"{original_expression} = {result}"
            )

            self.expression = str(result)

            self.update_display()

        except ZeroDivisionError as error:

            self.show_error(
                str(error)
            )

        except ValueError as error:

            self.show_error(
                str(error)
            )

        except OverflowError:

            self.show_error(
                "Number too large"
            )

        except Exception as error:

            self.show_error(
                f"Error: {error}"
            )

    # ========================================================
    # ERROR
    # ========================================================

    def show_error(self, message):

        self.expression = ""

        self.display.delete(
            0,
            tk.END
        )

        self.display.insert(
            0,
            message
        )

    # ========================================================
    # HISTORY
    # ========================================================

    def show_history(self):

        history_window = tk.Toplevel(
            self.window
        )

        history_window.title(
            "Calculation History"
        )

        history_window.geometry(
            "500x400"
        )

        history_window.configure(
            bg=self.bg_color
        )

        listbox = tk.Listbox(
            history_window,
            font=("Arial", 13),
            bg=self.display_color,
            fg="white",
            selectbackground=self.equal_color
        )

        listbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        if self.history:

            for calculation in self.history:

                listbox.insert(
                    tk.END,
                    calculation
                )

        else:

            listbox.insert(
                tk.END,
                "No calculations yet."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    window = tk.Tk()

    calculator = ScientificCalculator(
        window
    )

    window.mainloop()

