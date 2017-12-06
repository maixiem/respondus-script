from header import *

class main_gui:
    def __init__(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.prompt(self.root)
        self.root.withdraw()
        self.root.mainloop()
    def prompt(self,root):
        self.main = Toplevel()
        main = self.main
        main.protocol("WM_DELETE_WINDOW",self.delete_window)
        main.title("RESP.PY UTILITY")
        Label(main,text="Welcome to Resp.py! This program was made to help with importing to Respondus.\n").grid()

        self.close_button = Button(main,text="Exit", command=self.root.quit)
        self.close_button.grid(row='4',column='0',sticky='w'+'e',padx=10,pady=10)

        self.help_button = Button(main,text="Help", command=self.root.quit)
        self.help_button.grid(row='4',column='1',sticky='w',padx=10,pady=10)

        self.mcg_button = Button(main,text="Import (McGraw-Hill rtf only)", command=self.mcg)
        self.mcg_button.grid(row='2',column='1',padx=10,pady=10)

        self.create_button = Button(main,text="New Quiz",command=create_quiz)
        self.create_button.grid(row='2',column='2',padx=10,pady=10)
    def mcg(self):
        self.quiz = mcgrawhill()
        if self.quiz:
            self.save()
        else:
            self.prompt()
    def save(self):
        f = tkFileDialog.asksaveasfilename(initialdir="/", title = "Save as", defaultextension='txt')
        if f is None:
            return 0
        elif f:
             try:
                 fd = open(f, 'w')
                 fd.write(self.quiz)
                 fd.close()
                 tkMessageBox.showinfo("Save state", "(%s) was saved successfully" % f)
                 return
             except:
                 tkMessageBox.showWarning("Save state", "Unable to save this file.")
                 return
        else:
            return 0
    def delete_window(self):
        if tkMessageBox.askyesno("Quit", "Do you want to quit?"):
            try:
                self.root.destroy()
            except:
                pass
        else:
            pass

class create_quiz:
    def __init__(self):
        self.root = Toplevel()
        
