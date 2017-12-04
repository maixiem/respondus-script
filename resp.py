import time
import os.path
from datetime import date
import io
import re
import Tkinter, tkFileDialog
from Tkinter import Tk, Label, Button, StringVar, IntVar, Radiobutton, Frame, Text
import tkMessageBox

######GLOBAL DEFINTIONS######
nmask = r"\d+\.\\~"
amask = r"\\b\\ul.*\s([ABCDE])\.|(T)RUE|(F)ALSE"
possible_answers = ['A','B','C','D','E','F','T']
content = ""

#####CLASS DEFINTIONS######

class marker(object):
    def __init__(self, iterable, start, end):
        self.iterable = iterable
        self.start = start
        self.end = end
    def show_all(self):
        i = self.iterable
        s = self.start
        e = self.end
        print "[ITERABLE: %d]\n[START: %d]\n[END: %d]"%(i,s,e)

class question(object):
    def __init__(self, number, answer):
        self.number = number
        self.q_range = []
        self.answer = answer
        self.blooms = ""
        self.body = ""
    def redit(self,q_range):
        self.q_range = q_range
    def aedit(self,answer):
        self.answer = answer
    def bedit(self,blooms):
        self.blooms=blooms
    def qredit(self,q_range):
        self.q_range = q_range
    def show_all(self): #debugging
        n = self.number
        s = self.q_range
        a = self.answer
        b = self.blooms
        body = self.body
        print " _______________________________________________________________________________"
        print "|\t\t\t\tQUESTION OBJECT\t\t\t\t\t|"
        print "+-------------------------------------------------------------------------------+"
        print "| Question number: ",
        print n,
        print "\tRange of question: ",
        print s
        print "| Answer: ",
        print a,
        print "\t\t\tBloom's type: ",
        print b
        print "| Body: "
        print body
        print "+-------------------------------------------------------------------------------+\n"
    def get_question(self):
        return self.number + self.body + "\n"

class main_gui:
    def __init__(self,master):
        self.master = master
        self.body = StringVar()
        frame = Frame(master,width=300,padx=5,pady=5)
        frame.grid(columnspan='5')
        Label(master, textvariable=self.body, justify='left',wraplength=300).grid(row='0',column='0',columnspan='4',sticky='w'+'e',padx=5)
        self.prompt(master)
    def prompt(self,master):
        master.title("RESP.PY UTILITY")
        bod = "Welcome to Resp.py! This program was made to help proofread your file for importing to Respondus.\n"
        bod +="------------------------------------------------------------\n"
        bod += "[OPTIONS] \n Question number format:"
        self.var = IntVar()
        Radiobutton(self.master, text="Parentheses (ex: 1), 2), 3)...)", variable=var, value=")").grid(row='1',column='0',sticky='w',columnspan='2',padx=10,pady=5)
        Radiobutton(self.master, text="Dot (ex: 1., 2., 3. ...)", variable=var, value=".").grid(row='1',column='2',sticky='w',padx=10,pady=5)
        self.body.set(bod)

        self.browse_button = Button(master,text="Browse...", command=self.browse)
        self.browse_button.grid(row='2',column='4',sticky='w',padx=10,pady=10)

        self.close_button = Button(master,text="Exit", command=master.quit)
        self.close_button.grid(row='2',column='0',sticky='w'+'e',padx=10,pady=10)

        self.help_button = Button(master,text="Help", command=master.quit)
        self.help_button.grid(row='2',column='1',sticky='w',padx=10,pady=10)
    def browse(self):
        fp = tkFileDialog.askopenfilename(filetypes=[("Rich Text","*.rtf")])
        if fp!= '':
            fd = open(fp,'r+')
            global content
            for line in fd.readlines():
                content += line
            fd.close()
            if self.var == 'MCG':
                questions = the_rest(remove_ems(content))
                rem_low(questions)
                renum(questions)
                self.quiz = ""
                self.quiz = get_quiz(questions,self.quiz)
                self.quiz = get_answers(questions,self.quiz)
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
    def quit(self):
        self.master.protocol("WM_DELETE_WINDOW", on_closing(self.master))


def main():
    root = Tk()
    master = main_gui(root)
    root.mainloop()
def on_closing(master):
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        master.destroy()
def get_quiz(questions,quiz):
    for q in questions:
        quiz+=q.get_question()
    return quiz

def rem_low(questions):
    for q in questions:
        if q.blooms == '1':
            questions.remove(q)
    return questions

def renum(questions):
    i = 1
    for q in questions:
        q.number = str(i) + ". "
        i+=1
def remove_ems(content):
    markers = mark_finder()
    start = 1
    while start < len(markers):
        x = start
        while x > 0 and markers[x-1].start > markers[x].start:
            markers.insert(x,markers.pop(x-1))
            x = x-1
        start += 1

    delete = []
    for m in range(0,len(markers)-1): #starting from the end of content, delete questions that are not multiple choice or TF
        key = markers[m].iterable
        next_key = markers[m+1].iterable
        if key == 0 and next_key == 0:
            pass
        if key == 0 and next_key == 1:
            markers[m].end = markers[m+1].start-1

    for m in markers:
        if m.iterable == 0:
            delete.append(m.start)
            delete.append(m.end)

    if len(delete) !=0:
        content = content[:delete[0]] + content[delete[len(delete)-1]:]
        return content
    else:
        return content

def the_rest(content):
    global possible_naswers
    global nmask
    global amask

    numbers = []
    numbers = [num.group(0)[:len(num.group(0))-2] for num in re.finditer(nmask,content)]

    starts = []
    for m in re.finditer(nmask,content):
        starts.append(m.start())

    answers = []
    for ans in re.finditer(amask, content):
        check = [ans.group(i) for i in range(1,4)]
        for c in check:
            if c in possible_answers:
                answers+=c

    questions = []
    tmp = [answers,numbers]

    for x in range(0,len(numbers)):
        q_obj = question(tmp[1][x],tmp[0][x])
        if(x+1<len(starts)):
            q_obj.qredit([starts[x],starts[x+1]-1])
            q_obj.body = get_body_mc(content[starts[x]:starts[x+1]-1])
            q_obj.blooms = blooms_finder(content[starts[x]:starts[x+1]-1])
        else:
            q_obj.qredit([starts[x],len(content)])
            q_obj.body = get_body_mc(content[starts[x]:])
            q_obj.blooms = blooms_finder(content[starts[x]:])
        questions.append(q_obj)

    return questions

def blooms_finder(content):
    result = re.search(r"\s*B\s*l\s*oom\s*'s:\s(\d)\.",content)
    return result.group(1)

def get_body_mc(rtf):
    result = re.split(r"\d+\.|\\\\|\\[a-z0-9]+|\\\\~\\n|\n|B\s*loom's.+|}{|\s{|\s}|\s*\\\\~|{\s*|\s*}",rtf)
    result = filter(lambda i: i!=' ' and '\\~' and ' \\~',filter(None, result))
    result = map(lambda i: i.strip(r"\\\\~ "), result)
    result = " ".join(result)
    result = mc_returns(result)
    if re.search(r"True / False",result):
        result = result[:re.search(r"True / False",result).start()]
    if re.search(r"TRUE|FALSE", result):
        result = result[:re.search(r"TRUE|FALSE", result).start()]+ "\nA. True\nB. False"
    return result

def mc_returns(rtf):
    letters = [r"A\.",r"B\.",r"C\.",r"D\.",r"E\."]
    for l in letters:
        result = re.search(l,rtf)
        if result:
            newline = result.start()
            rtf = rtf[:newline] + "\n" + rtf[newline:]
        else:
            pass
    return rtf
def get_answers(questions,quiz):
    quiz += "Answers:\n"
    for q in questions:
        quiz+= q.number + q.answer + "\n"
    return quiz

def mark_finder(): #finds the matching section header in the given content and appends it to an array as an object
    markers = []
    for m in re.finditer(r"Multiple Choice Questions", content):
        markers.append(marker(1, m.start(), m.end()))
    for m in re.finditer(r"True / False Questions", content):
        markers.append(marker(1, m.start(), m.end()))
    for m in re.finditer(r"Essay Questions", content):
        markers.append(marker(0, m.start(), m.end()))
    for m in re.finditer(r"Matching Questions", content):
        markers.append(marker(0, m.start(), m.end()))
    for m in re.finditer(r"Short Answer Questions", content):
        markers.append(marker(0, m.start(), m.end()))
    return markers

if __name__ == "__main__":
    main()
