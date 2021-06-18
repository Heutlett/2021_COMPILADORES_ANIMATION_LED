import tkinter
from tkinter import *
from tkinter import scrolledtext
from CopiaSemanticAdrian import compile_program  # CAMBIAR CAMBIAR CAMBIAR CAMBIAR



class Ide(Frame):



    def __init__(self):
        super().__init__(bg="#333")
        self.initUI()

    def initUI(self):

        self.contador = 1

        self.master.title("IDE")
        self.pack(fill=BOTH, expand=1)

        self.labelOutput = Label(self.master, text="Output")
        self.labelOutput.place(x=90, y=573)

        self.labelLoad = Label(self.master, text="    Nombre del archivo a cargar  ")
        self.labelLoad.place(x=281, y=100)

        self.entryLoad = Entry(self.master, width=28)
        self.entryLoad.place(x=281, y=130)

        self.buttonLoad = Button(self.master, text="Load", command=self.loadFunction, width=25, height=5)
        self.buttonLoad.place(x=90, y=65)

        self.buttonCompile = Button(self.master, text="Compile", command=self.compileFunction, width=25, height=5)
        self.buttonCompile.place(x=560, y=65)

        self.labelCompile = Label(self.master, text="Nombre del archivo a compilar")
        self.labelCompile.place(x=760, y=100)

        self.entryCompile = Entry(self.master, width=28)
        self.entryCompile.place(x=760, y=130)

        self.buttonCompileRun = Button(self.master, text="Compile and run",
                                       command=self.compileAndRunFunction, width=25, height=5)
        self.buttonCompileRun.place(x=1010, y=65)

        def viewall(*args):
            txtInput.yview(*args)
            txtLineCount.yview(*args)

        # scrollbar = Scrollbar(self.master, orient=VERTICAL)
        # scrollbar.place(x=0,y=0)
        # scrollbar.config(command=viewall)

        txtInput = scrolledtext.ScrolledText(self.master, undo=True, width=120, height=20)  # 120 20
        txtInput['font'] = ('consolas', '12')
        txtInput.place(x=90, y=180)
        # self.txtInput.vbar
        self.inputTxt = txtInput

        #self.inputTxt.bind("<B1-Leave>", lambda event: "break")

        txtInput.vbar.bind_all("<MouseWheel>", self._on_mousewheel)
        txtInput.vbar.config(command=viewall)

        txtLineCount = Text(self.master, undo=True, width=7,
                            height=20)
        txtLineCount['font'] = ('consolas', '12')
        txtLineCount.place(x=15, y=180)

        self.lineCountTxt = txtLineCount

        #self.txtInput.bind("<B1-Leave>", lambda event: "break")

        txtLineCount.configure(state=NORMAL)
        i = 1
        for x in range(0, 200):
            txtInput.insert(INSERT, "\n")
            txtLineCount.insert(INSERT, str(i))
            txtLineCount.insert(INSERT, "\n")
            i = i + 1
        txtLineCount.configure(state=DISABLED)

        # self.txtLineCount.vbar.set()

        # self.txtInput.vbar.config(command=self.txtLineCount.yview)

        self.txtOutput = scrolledtext.ScrolledText(self.master, undo=True, width=120, height=5, state=DISABLED)
        self.txtOutput['font'] = ('consolas', '12')
        self.txtOutput.place(x=90, y=600)

        self.insertTextOutput("")

    def _on_mousewheel(self, event):

        self.lineCountTxt.yview_moveto(self.inputTxt.yview()[0])




    def loadFunction(self):
        self.clearTextOutput()
        self.insertTextOutput("loading program...\n\n")

        nombre_archivo = self.entryLoad.get()

        if nombre_archivo == "":
            self.insertTextOutput("No se ha podido cargar el programa porque no se ha insertado el nombre del archivo")
            return

        nombre_archivo = "./saved/" + nombre_archivo + ".txt"

        try:
            with open(nombre_archivo, "r") as file:

                texto = ""

                for linea in file.readlines():
                    texto = texto + linea

                self.inputTxt.insert("1.0", texto)
                file.close()
                self.insertTextOutput("El programa se ha cargado correctamente!\n\n")


        except Exception:
            self.insertTextOutput("Error: no existe un archivo con el nombre ingresado\n\n")


    def compileFunction(self):
        self.clearTextOutput()
        self.insertTextOutput("compiling program...\n\n")

        nombre_archivo = self.entryCompile.get()

        if nombre_archivo == "":
            self.insertTextOutput("No se ha podido compilar el programa porque no se ha insertado el nombre del archivo")
            return

        nombre_archivo = "./saved/" + nombre_archivo + ".txt"

        file = open(nombre_archivo, "w")

        file.write(self.inputTxt.get("1.0", tkinter.END))

        file.close()



        errors = compile_program(self.inputTxt.get("1.0", tkinter.END))
        if len(errors) == 0:
            self.insertTextOutput("El codigo se ha compilado correctamente sin errores")
        else:
            self.insertTextOutput("ERRORES ENCONTADOS, NO SE PUDO COMPILAR CORRECTAMENTE:\n")
            self.insertTextOutput(str(errors))



    def compileAndRunFunction(self):
        self.clearTextOutput()
        self.insertTextOutput("compiling and running program...\n\n")

        texto = self.inputTxt.get("1.0", tkinter.END)

        vacio = True

        for i in texto:
            if i != "\n" and i != "" and i != " ":
                vacio = False

        if vacio:
            self.insertTextOutput("Error: no se ha podido compilar porque el programa esta vacio\n\n")



    def insertTextOutput(self, text):
        self.txtOutput.configure(state=NORMAL)
        self.txtOutput.insert(INSERT, text)
        self.txtOutput.configure(state=DISABLED)

    def clearTextOutput(self):
        self.txtOutput.configure(state=NORMAL)
        self.txtOutput.delete('1.0', END)
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
    #print(x, y)



if __name__ == '__main__':
    main()
