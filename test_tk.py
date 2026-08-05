import tkinter

window = tkinter.Tk()
window.title("Tkinter Test")
window.geometry("400x300")

print("1. Window created")

frame = tkinter.Frame(window, bg="red", width=300, height=200)
print("2. Frame created")

frame.pack(padx=50, pady=50)

print("3. Frame packed")

label = tkinter.Label(
    frame,
    text="HELLO TKINTER",
    font=("Arial", 20),
    bg="black",
    fg="white"
)

print("4. Label created")

label.pack(padx=20, pady=20)

print("5. Label packed")

window.mainloop()