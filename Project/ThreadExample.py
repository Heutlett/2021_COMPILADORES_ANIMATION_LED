import threading
import time

def contar(perro):
    '''Contar hasta cien'''
    contador = 0
    while contador<100:
        contador+=1
        time.sleep(1)
        print('Hilo:',
              threading.current_thread().getName(), contador)


def create_thread():
    hilo=threading.Thread(target=contar, kwargs={'perro': 1})
    hilo.start()


create_thread()
create_thread()

print("asdasd")