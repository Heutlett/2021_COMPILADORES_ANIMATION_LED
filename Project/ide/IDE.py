from tkinter import *
from tkinter import scrolledtext

class Ide(Frame):

    def __init__(self):
        super().__init__(bg="#333")
        self.initUI()


    def initUI(self):

        self.master.title("IDE")
        self.pack(fill=BOTH, expand=1)

        self.labelOutput = Label(self.master, text="Output")
        self.labelOutput.place(x=90, y=573)

        self.buttonLoad = Button(self.master, text="Load", command=self.loadFunction, width=25, height=5)
        self.buttonLoad.place(x=90,y=65)

        self.buttonCompile = Button(self.master, text="Compile", command=self.compileFunction, width=25, height=5)
        self.buttonCompile.place(x=560,y=65)

        self.buttonCompileRun = Button(self.master, text="Compile and run",
                                       command=self.compileAndRunFunction, width=25, height=5)
        self.buttonCompileRun.place(x=1010,y=65)

        def viewall(*args):
            txtInput.yview(*args)
            txtLineCount.yview(*args)

        #scrollbar = Scrollbar(self.master, orient=VERTICAL)
        #scrollbar.place(x=0,y=0)
        #scrollbar.config(command=viewall)

        txtInput = scrolledtext.ScrolledText(self.master, undo=True, width=120, height=20)  # 120 20
        txtInput['font'] = ('consolas', '12')
        txtInput.place(x=90,y=180)
        #self.txtInput.vbar

        txtInput.vbar.config(command=viewall)

        txtLineCount = Text(self.master, undo=True, width=7,
                                                      height=20)
        txtLineCount['font'] = ('consolas', '12')
        txtLineCount.place(x=15,y=180)

        txtLineCount.configure(state=NORMAL)
        i = 0
        for x in range(0,1000):
            txtInput.insert(INSERT, "\n")
            txtLineCount.insert(INSERT, str(i))
            txtLineCount.insert(INSERT, "\n")
            i = i+1
        txtLineCount.configure(state=DISABLED)


        #self.txtLineCount.vbar.set()

        #self.txtInput.vbar.config(command=self.txtLineCount.yview)


        self.txtOutput = scrolledtext.ScrolledText(self.master, undo=True, width=120, height=5, state=DISABLED)
        self.txtOutput['font'] = ('consolas', '12')
        self.txtOutput.place(x=90, y=600)

        self.insertTextOutput("SE HA COMPILADO CORRECTAMENTE EL CODIGO")


    def loadFunction(self):
        print("loading program")
        self.txtLineCount.vbar.set(self.txtInput.vbar.get()[0],self.txtInput.vbar.get()[1])
        self.update()
        print(self.txtInput.vbar.get()[1])

    def compileFunction(self):
        print("compiling program")

    def compileAndRunFunction(self):
        print("compiling and running program")

    def insertTextOutput(self, text):
        self.txtOutput.configure(state=NORMAL)
        self.txtOutput.insert(INSERT, text)
        self.txtOutput.configure(state=DISABLED)

    def insertLineNumber(self):
        pass

def main():

    root = Tk()
    root.geometry("1300x730+100+10")
    root.bind("<Button 1>", getorigin)
    IDE = Ide()
    root.mainloop()



def getorigin(eventorigin):
    global x, y
    x = eventorigin.x
    y = eventorigin.y
    print(x, y)



if __name__ == '__main__':
    main()