import threading
import time

def contar():
    '''Contar hasta cien'''
    contador = 0
    while contador<100:
        contador+=1
        time.sleep(1)
        print('Hilo:',
              threading.current_thread().getName(), contador)


hilo1 = threading.Thread(target=contar)
hilo2 = threading.Thread(target=contar)
hilo1.start()
hilo2.start()
print("asdasd")