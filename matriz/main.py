import serial
import time

serialcomm = serial.Serial('COM6',9600)
serialcomm.timeout = 1
response = False

mtrx = [ [0,1,1,0,0,1,1,0],
         [1,0,0,0,0,0,0,1],
         [0,0,1,0,0,1,0,0],
         [0,0,0,0,0,0,0,0],
         [0,1,0,0,0,0,1,0],
         [0,0,1,0,0,1,0,0],
         [0,0,0,1,1,0,0,0],
         [0,0,0,0,0,0,0,0]]

mtrx2 = [[0,1,1,0,0,1,1,0],
         [1,0,0,0,0,0,0,1],
         [0,1,1,0,0,1,1,0],
         [0,0,0,0,0,0,0,0],
         [0,1,0,0,0,0,1,0],
         [0,0,1,1,1,1,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

mtrx3 = [[0,1,1,0,0,1,1,0],
         [1,0,0,0,0,0,0,1],
         [0,0,1,0,0,1,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,1,1,1,1,1,1,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

rules = [ [ 'PRINT',
    [[0,1,1,0,0,1,1,0],
     [1,0,0,0,0,0,0,1],
     [0,0,1,0,0,1,0,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0],
     [0,1,1,1,1,1,1,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0]]],
  ['DELAY', 'seg', 2],
  [ 'PRINT',
    [[0, 1, 1, 0, 0, 1, 1, 0],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [0, 1, 1, 0, 0, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 1, 0],
     [0, 0, 1, 1, 1, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0]]],
  ['DELAY', 'seg', 2],
  [ 'PRINT',
    [[0, 1, 1, 0, 0, 1, 1, 0],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [0, 0, 1, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 1, 0],
     [0, 0, 1, 0, 0, 1, 0, 0],
     [0, 0, 0, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0]]],
  ['DELAY', 'seg', 2]]

#mtrx_send = "1111111111111111111111111111111111111111111111111111111111111111"

'''Apaga o enciende un punto de la matriz'''
def c_led(x,y,S):
    if S==True:
        for i in mtrx:
            i[y][x]=1

    elif S==False:
        for i in mtrx:
            i[y][x]=0

'''Transforma una matriz a un string'''
def trans_mtrx(m):
    reslt=""
    for i in m:
        for j in i:
            reslt+=j.__str__()

    return reslt

'''Envia una matriz por serial a Arduino'''
def send_mtrx(m):
    serialcomm.write(trans_mtrx(m).encode())
    time.sleep(0.5)
    #print(serialcomm.readline().decode('ascii'))


if __name__ == '__main__':
    time.sleep(3)
    send_mtrx(mtrx)
    time.sleep(0.8)
    send_mtrx(mtrx2)
    time.sleep(0.8)
    send_mtrx(mtrx3)
    serialcomm.close()

