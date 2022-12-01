import time

def recebe_senha(ser):
    ser.flush()
    ser.read(3)

    for x in range(3):
        time.sleep(3)
        saida = ser.read(100).decode("utf-8")
        saida_limpa = ''.join((x for x in saida if x.isdigit()))
        print(saida_limpa)
        
def abre_cofre(ser):
    ser.write('a'.encode('utf-8'))
    recebe_senha(ser)

def fecha_cofre(ser):
    ser.write('f'.encode('utf-8'))

def nova_senha(ser):
    ser.write('n'.encode('utf-8'))
    recebe_senha(ser)
    