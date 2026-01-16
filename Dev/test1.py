import tkinter as tk
 
    #ro ot = tk.Tk()
#root.title("TOH Schedule Maker")

# Adjust Window size
#root.geometry("1446x810")

#The name of the window
root = tk.Tk()

#Windows title (application name)
root.title("TOH Schedule Maker")

#definition
def on_clicked():
    print("Testing")

#lable
lbl = tk.Label(root, text="Lable 1")
lbl.grid(row = 0, column=0)

#Create the button
btn = tk.Button(root, text="Button 1", command=on_clicked)

#display the button
btn.grid(row = 0, column=1)

#The game loop
root.mainloop()

'''
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""  
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        root.geometry("1446x810")
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

import tkinter as tk

class schedule_maker()

root = tk.Tk()
root.title("TOH Schedule Maker")

# Adjust Window size
root.geometry("1446x810")

# Function to execute when the button is clicked
def on_button_click():
    print("Hello World")

# Create the button and add it to the window
button = tk.Button(root, text="Click Me!", command=on_button_click)
button2 = tk.Button(root,
                text="Test Button", 
                command=on_button_click,
                height= 5,
                width= 15)

button.pack(pady=20)  # Adds some padding around the button
button2.pack(side="left", padx=10, pady=5) #I can move
button2.place(x = 60, y=70)

# Run the main event loop 
root.mainloop()
'''