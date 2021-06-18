import tkinter
from tkinter import *
from tkinter import scrolledtext
from SemanticAdrianCopia import compile_program  # CAMBIAR CAMBIAR CAMBIAR CAMBIAR
import os
import ast
# from led_controller import led_exe
# from led_controller.led_exe import exe_led

user_color = '#aa9787' #Café
change_color='#b0dfc2' #lila
front_color = '#9c2c51' #Vino
admin_color = '#8ca5b4' #Verde oscuro

bg_color ='#d2ce9c' #Beige oscuro
entry_color = '#e0d8b0' #Beige Claro
label_color='#2b2a29' #Gris oscuro
light='light gray'
admin_color=admin_color
body_color=light

class Ide(Frame):



    def __init__(self):
        super().__init__(bg=admin_color)
        self.initUI()

    def initUI(self):

        self.load_img = self.CargarImg('load.png')
        self.compile_img = self.CargarImg('compile.png')
        self.run_img = self.CargarImg('run.png')

        self.contadorLineas = 20

        self.master.title("IDE")
        self.pack(fill=BOTH, expand=1)


        fontList = ('century gothic', 16, 'italic', 'bold')
        self.labelLoad = Label(self.master,  text='Open...', bg=admin_color, fg = label_color, font=fontList)
        self.labelCompile = Label(self.master, text='Compile',bg=admin_color, fg = label_color, font=fontList)
        self.entryLoad = Entry(self.master, width=28)
        self.entryCompile = Entry(self.master, width=28)

        self.buttonLoad = Button(self.master, image=self.load_img, command=self.loadFunction, bg= admin_color,
                                 relief="ridge", cursor="hand2", activebackground=admin_color, bd='0' )
        self.buttonCompile = Button(self.master, image=self.compile_img, command=self.compileFunction,  bg= admin_color,
                                 relief="ridge", cursor="hand2", activebackground=admin_color, bd='0' )
        self.buttonCompileRun = Button(self.master,  image=self.run_img, command=self.compileAndRunFunction, bg= admin_color,
                                 relief="ridge", cursor="hand2", activebackground=admin_color, bd='0' )

        self.labelCompileRun  = Label(self.master,  text='Compile\n&\nRun', bg=admin_color, fg = label_color, font=fontList)

        self.labelOutput = Label(self.master, text="Output", bg=admin_color, fg = label_color, font=('century gothic', 20, 'italic', 'bold'))


        self.buttonLoad.place(x=40, y=23)
        self.labelLoad.place(x=154, y=45)
        self.entryLoad.place(x=154, y=80)

        self.labelCompile.place(x=619, y=45)


        self.entryCompile.place(x=619, y=80)
        self.buttonCompile.place(x=500, y=23)
        self.buttonCompileRun.place(x=960, y=23)
        self.labelCompileRun.place(x=1073, y=35)


        self.labelOutput.place(x=90, y=550)



        def viewall(*args):
            txtInput.yview(*args)
            txtLineCount.yview(*args)

        # scrollbar = Scrollbar(self.master, orient=VERTICAL)
        # scrollbar.place(x=0,y=0)
        # scrollbar.config(command=viewall)

        txtInput = scrolledtext.ScrolledText(self.master, font = fontList, bg= body_color, undo=True, width=120, height=20)  # 120 20
        txtInput['font'] = ('consolas', '12')
        txtInput.place(x=90, y=150)
        # self.txtInput.vbar
        self.inputTxt = txtInput

        #self.inputTxt.bind("<B1-Leave>", lambda event: "break")

        txtInput.vbar.bind_all("<MouseWheel>", self._on_mousewheel)
        txtInput.bind_all('<Return>', self._on_enter)

        txtInput.vbar.config(command=viewall)

        txtLineCount = Text(self.master, font = fontList, undo=True, width=7, height=20, bg= body_color)
        txtLineCount['font'] = ('consolas', '12')
        txtLineCount.place(x=15, y=150)

        self.lineCountTxt = txtLineCount

        #self.txtInput.bind("<B1-Leave>", lambda event: "break")

        txtLineCount.configure(state=NORMAL)
        i = 1
        for x in range(0, self.contadorLineas):
            txtInput.insert(INSERT, "\n")
            txtLineCount.insert(INSERT, str(i))
            txtLineCount.insert(INSERT, "\n")
            i = i + 1
        txtLineCount.configure(state=DISABLED)

        # self.txtLineCount.vbar.set()

        # self.txtInput.vbar.config(command=self.txtLineCount.yview)

        self.txtOutput = scrolledtext.ScrolledText(self.master, font = ("Times New Roman",15),
                                                   undo=True, bg= body_color, width=120, height=5, state=DISABLED)
        self.txtOutput['font'] = ('consolas', '12')
        self.txtOutput.place(x=90, y=600)

        self.insertTextOutput("")

    #                       ________________________
    # __________/Función para cargar imágenes
    def CargarImg(self, nombre):
        ruta = os.path.join('imgsound', nombre)
        imagen = PhotoImage(file=ruta)
        return imagen

    def _on_enter(self, event):
        self.crear_linea()

    def crear_lineas(self, count):
        for i in range(count):
            self.crear_linea()

    def crear_linea(self):
        self.lineCountTxt.configure(state=NORMAL)
        self.contadorLineas += 1
        self.inputTxt.insert(END, "\n")
        self.lineCountTxt.insert(END, str(self.contadorLineas))
        self.lineCountTxt.insert(END, "\n")
        self.lineCountTxt.configure(state=DISABLED)




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

                data = file.readlines()

                for linea in data:
                    texto = texto + linea


                self.inputTxt.insert("1.0", texto)
                file.close()

                self.contadorLineas = data.count("\n")
                self.crear_lineas(self.contadorLineas)

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
        self.compileFunction()
        self.crear_linea()
        self.clearTextOutput()
        self.insertTextOutput("compiling and running program...\n\n")

        texto = self.inputTxt.get("1.0", tkinter.END)

        vacio = True

        for i in texto:
            if i != "\n" and i != "" and i != " ":
                vacio = False

        if vacio:
            self.insertTextOutput("Error: no se ha podido compilar porque el programa esta vacio\n\n")
            return

        file = open("ArduinoCompiledOutput.txt", "r")
        content = file.readlines()
        content = ast.literal_eval(content[0])

        if len(content) > 0:
            print("se ha enviado")
            print(content)
            #exe_led(content)
            self.insertTextOutput("El programa se ha enviado correctamente al controlador\n\n")
            return
        else:
            self.insertTextOutput("Error, no se podido correr porque hay errores en la compilacion\n\n")
            return




    def insertTextOutput(self, text):
        self.txtOutput.configure(state=NORMAL)
        self.txtOutput.insert(INSERT, text)
        self.txtOutput.configure(state=DISABLED)

    def clearTextOutput(self):
        self.txtOutput.configure(state=NORMAL)
        self.txtOutput.delete('1.0', END)
        self.txtOutput.configure(state=DISABLED)
        self.contadorLineas = 20

    def insertLineNumber(self):
        pass


def main():
    root = Tk()
    root.geometry("1210x730+100+10")
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
