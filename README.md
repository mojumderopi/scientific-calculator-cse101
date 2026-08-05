# Scientific Calculator (CSE101)

A simple scientific calculator implemented in Python — a student project for CSE101. This repository contains multiple implementations and small test scripts implementing a GUI-based and CLI-capable scientific calculator.

## Features

- Basic arithmetic: add, subtract, multiply, divide
- Scientific functions: trigonometry, logarithms, exponentiation (implemented in the included scripts)
- Simple Tkinter-based GUI (included example windows and test scripts)

## Requirements

- Python 3.8 or newer
- Tkinter (usually included with standard Python distributions)

No external packages are required by the repository as provided. If you add dependencies, list them in a requirements.txt file.

## Files

- `scientifc_calculator.py` — Primary calculator implementation (note: filename contains a typo `scientifc`). Run this to start the main calculator application.
- `sci-calc-two.py` — Alternate implementation or iteration of the calculator.
- `window_code.py` — Helper code for Tkinter window setup and layout used by the GUI apps.
- `test_tk.py` — Small test script that demonstrates or tests the Tkinter GUI.

## Usage

To run the main calculator (if the script is executable as a script):

```bash
python scientifc_calculator.py
```

Or run the alternate implementation:

```bash
python "sci-calc-two.py"
```

If you encounter any Tkinter-related errors, ensure Tkinter is available for your Python installation. On some Linux distributions you may need to install a system package (for example: `sudo apt install python3-tk`).

## Contributing

Contributions, bug reports, and improvements are welcome. Suggested workflows:

- Open an issue describing the change or bug.
- Fork the repository and create a feature branch.
- Submit a Pull Request with a clear description and tests where applicable.

Please add a `requirements.txt` if you introduce external Python dependencies.

## Notes

- Consider renaming `scientifc_calculator.py` to `scientific_calculator.py` to fix the filename typo; if you do, update any imports or documentation that reference the current name.
- If you'd like a packaged installation or command-line entry point, add a setup.py/pyproject.toml and a requirements file.

## License

No license file is included in this repository. 
