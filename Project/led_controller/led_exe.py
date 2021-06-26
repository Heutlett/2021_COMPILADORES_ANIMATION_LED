import serial
import time
import ast

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
#
# rules = [ [ 'PRINT',
#     [[0,1,1,0,0,1,1,0],
#      [1,0,0,0,0,0,0,1],
#      [0,0,1,0,0,1,0,0],
#      [0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0],
#      [0,1,1,1,1,1,1,0],
#      [0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0]]],
#   ['DELAY', 'seg', 2],
#   [ 'PRINT',
#     [[0, 1, 1, 0, 0, 1, 1, 0],
#      [1, 0, 0, 0, 0, 0, 0, 1],
#      [0, 1, 1, 0, 0, 1, 1, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 1, 0, 0, 0, 0, 1, 0],
#      [0, 0, 1, 1, 1, 1, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0]]],
#   ['DELAY', 'seg', 2],
#   [ 'PRINT',
#     [[0, 1, 1, 0, 0, 1, 1, 0],
#      [1, 0, 0, 0, 0, 0, 0, 1],
#      [0, 0, 1, 0, 0, 1, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 1, 0, 0, 0, 0, 1, 0],
#      [0, 0, 1, 0, 0, 1, 0, 0],
#      [0, 0, 0, 1, 1, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0]]],
#   ['DELAY', 'seg', 2]]

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
            if j:
                reslt+="1"
            else:
                reslt+="0"

    return converthex(reslt)

'''Envia una matriz por serial a Arduino'''
def send_mtrx(r):
    serialcomm.write(r.encode())
    print("SE HACE")
    time.sleep(0.5)
    print(serialcomm.readline().decode('ascii'))

def build_send(rules_):
    return "(" + build_aux(rules_,0) + ")"

def build_aux(rules_,i):
    try:
        if (rules_[i][0] == 'PRINT'):
            print("P"+trans_mtrx(rules_[i][1]))
            print("P",rules_[i][1])
            return "P"+trans_mtrx(rules_[i][1])+build_aux(rules_, i+1)
        elif (rules_[i][0] == 'DELAY'):
            print("T"+rules_[i][1]+rules_[i][2].__str__())
            return "T"+res_t(rules_[i][1])+str(rules_[i][2])+build_aux(rules_, i+1)
        else:
            return ""
    except:
        return ""

def res_t(time_):
    if time_ == 'seg':
        return "S"
    elif time_ == 'min':
        return "M"
    elif time_ == 'mil':
        return "N"

def dectohex(num):
    return f"{int(num.__str__(), 10):X}"

def converthex(b):
    print(b)
    rslt=""
    temp=""
    for i in range(16):
        for j in range(4):
            temp+=b[(i*4)+j]
            #print(temp,"\n")
        #print(temp,"\n")
        if (temp=="0000"):
            rslt+="0"
        else:
            rslt+=f"{int(temp, 2):X}"
        temp=""
    return rslt

def exe_led(rules):

    rules = ast.literal_eval(str(rules))
    print("Prueba: ",type(rules))
    time.sleep(4)
    msg=build_send(rules)
    print(msg)
    send_mtrx(msg)
    print(msg)
    serialcomm.close()



# if __name__ == '__main__':
#     time.sleep(4)
#     # send_mtrx(mtrx)
#     # time.sleep(0.8)
#     # send_mtrx(mtrx2)
#     send_mtrx(build_send(rules))
#     print(build_send(rules))
#     serialcomm.close()

