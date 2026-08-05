
import tkinter


#python creating window using tkinter module
window = tkinter.Tk() # this to create the window 
window.title("test tiltle name tai lung")# giving title to the window
window.resizable(True, True)# making the window resizable
##window.mainloop() # for the window to run until user closes it

# we need a frame to put the widgets in it, so we will create a frame and put it in the window
frame = tkinter.Frame(
    window,
    bg="red",
    width=300,
    height=200
)
frame.pack(padx=50, pady=50)
frame.pack()# we are creating a frame and putting it in the window
label = tkinter.Label(
    frame,
    text="This is a label",
    font=("Arial", 12),
    bg="black",
    fg="white"
) # we are creating a label and putting it in the frame
#label.pack(padx=20, pady=20)# we are packing the label in the frame
label.pack()
window.mainloop()