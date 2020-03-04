import tkinter
import webbrowser
window=tkinter.Tk()
window.title("nakg")
window.geometry("640x400+100+100")
window.resizable(False, False)
btn=tkinter.Button(window,text="b",command=lambda _=None: webbrowser.open("info.html",new=0,autoraise=True))
btn.pack()
window.mainloop()
