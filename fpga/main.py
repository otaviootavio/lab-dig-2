import tkinter as tk
from tkinter import ttk, IntVar
import serial
import time
from functools import partial
### Firebase
from firebase_admin import db, firestore, credentials, initialize_app
import json
import datetime
########

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("700x500")
        self.title('ULAVault')
        self.resizable(0, 0)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)        
        
        self.is_open_txt = 'Fechado'
        
        self.set_con()
        self.create_widget()
        self.setup_firebase()
        
    def set_con(self):
        self.ser = serial.Serial('COM5', 
                    115200, 
                    timeout=0, 
                    bytesize=serial.SEVENBITS, 
                    stopbits=serial.STOPBITS_TWO, 
                    parity=serial.PARITY_EVEN) 
        
    def setup_firebase(self):
        self.cred_obj = credentials.Certificate('labdig-2-f58c4ecf792d.json')
        self.default_app = initialize_app(self.cred_obj, {'databaseURL':'https://labdig-2.firebaseio.com'})
        self.db = firestore.client()
    
    def firebase_open(self):
        self.db.collection(u'estado').add({
            u'estado': u'Aberto',
            u'datastamp': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })

    def firebase_closed(self):
        self.db.collection(u'estado').add({
            u'estado': u'Fechado',
            u'datastamp': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })

    def firebase_bloqueado(self):
        self.db.collection(u'estado').add({
            u'estado': u'Bloqueado',
            u'datastamp': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })
    
    def firebase_wrong_password(self):
        self.db.collection(u'estado').add({
            u'estado': u'Fechado',
            u'comentario': u'Senha incorreta!',
            u'datastamp': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })
    
    def firebase_new_password(self):
        self.db.collection(u'estado').add({
            u'estado': u'Aberto',
            u'comentário': u'Nova senha criada.',
            u'datastamp': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        })


    def create_widget(self):
        font_size = 50
        pad_size = 5
        
        self.text_1 = ttk.Label(self, text="", font=("Arial", font_size))
        self.text_1.grid(row = 3, column = 0, padx=5, pady=5)
        
        self.text_2 = ttk.Label(self, text="", font=("Arial", font_size))
        self.text_2.grid(row = 3, column = 1, padx=5, pady=5)

        self.text_3 = ttk.Label(self, text="", font=("Arial", font_size))
        self.text_3.grid(row = 3, column = 2, padx=5, pady=5)
        
        fecha_cofre_func = partial(self.fecha_cofre, self.ser)
        abre_cofre_func = partial(self.abre_cofre, self.ser)
        nova_senha_func = partial(self.nova_senha, self.ser)
        
        self.botao_1 = ttk.Button(self, text = "Abrir", command = abre_cofre_func)
        self.botao_1.grid(row = 5, column = 0, padx=pad_size, pady=pad_size)
        
        self.botao_2 = ttk.Button(self, text = "Fechar", command = fecha_cofre_func)
        self.botao_2.grid(row = 5, column = 1, padx=pad_size, pady=pad_size)
        
        self.botao_3 = ttk.Button(self, text = "Nova senha", command = nova_senha_func)
        self.botao_3.grid(row = 5, column = 2, padx=pad_size, pady=pad_size)
        
        self.text_4 = ttk.Label(self, text="", font=("Arial", font_size))
        self.text_4.grid(row = 5, column = 3, padx=pad_size, pady=pad_size)
        
        self.is_open = ttk.Label(self, text="Fechado", font=("Arial", font_size))
        self.is_open.grid(row = 6, column = 1, padx=pad_size, pady=pad_size)
        
        self.status = '0'
        
        col_count, row_count = self.grid_size()

        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=50)

        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=50)
    
    def abre_cofre(self, ser):
        ser.write(b'a')
        time.sleep(0.02)
        if self.status == '0':    
            self.recebe_senha(ser)    

    def fecha_cofre(self, ser):
        ser.flush()
        ser.write(b'f')
        time.sleep(0.02)
        ### update visual to closed or open
        text = ser.read(100).decode('utf-8')
        ser.flush()
        print("Fecha cofre")
        print(text)
        print("######")
        
        if text == '0':
            self.status = '0'
            self.is_open.config(text = 'Fechado' )
            self.is_open_text = 'Fechado'
            self.firebase_closed()
        ## elif text == '1':
        ##     self.status = '1'
        ##     self.is_open.config(text = 'Aberto' )
        ##     self.is_open_text = 'Aberto'
        ## elif text == '2':
        ##     self.status = '2'
        ##     self.is_open.config(text = 'Bloqueado' )
        ##     self.is_open_text = 'Bloqueado'
        
    def nova_senha(self, ser):
        ser.write('n'.encode('utf-8'))
        self.firebase_new_password()
        if self.status == '1':    
            self.recebe_senha(ser)
        
    def recebe_senha(self, ser):
        ser.flush()
        ser.read(1)
        self.after(3010, lambda: self.recebe_senha_1(ser))
        
    def recebe_senha_1(self, ser):
        ser.flush()
        saida_1 =  ser.read(3).decode("utf-8")
        saida_limpa_1 = ''.join((x for x in saida_1 if x.isdigit()))
        self.text_1.config(text = saida_limpa_1 )
        self.after(3010, lambda: self.recebe_senha_2(ser))
        
    def recebe_senha_2(self, ser):
        ser.flush()
        saida_2 = ser.read(3).decode("utf-8")
        saida_limpa_2 = ''.join((x for x in saida_2 if x.isdigit()))
        self.text_2.config(text = saida_limpa_2 )
        self.after(3010, lambda: self.recebe_senha_3(ser))
                   
    def recebe_senha_3(self, ser):
        ser.flush()
        saida_3 = ser.read(3).decode("utf-8")
        saida_limpa_3 = ''.join((x for x in saida_3 if x.isdigit()))
        self.text_3.config(text = saida_limpa_3 )
        
        ### update visual to closed or open
        text = ser.read(1).decode('utf-8')
        print("Ultima leitura")
        print(text)
        
        if text == '0':
            self.status = '0'
            self.is_open.config(text = 'Fechado' )
            self.is_open_text = 'Fechado'
            self.firebase_wrong_password()
        elif text == '1':
            self.status = '1'
            self.is_open.config(text = 'Aberto' )
            self.is_open_text = 'Aberto'
            self.firebase_open()
        else:
            self.status = '2'
            self.is_open.config(text = 'Bloqueado' )
            self.is_open_text = 'Bloqueado'
            self.firebase_bloqueado()
            self.after(3010, self.limpar)
            self.blocked(ser)
            return
        
        self.after(3010, self.limpar)
        
    def limpar(self):
        self.text_1.config(text = '' )
        self.text_2.config(text = '' )
        self.text_3.config(text = '' )
        
    def wait_time(self, time):
        var = IntVar()
        self.after(time, var.set, 1)
        print("waiting...")
        self.wait_variable(var)
    
    def blocked(self, ser):
        x = ser.read(1).decode('utf-8')
        if x == '1':
            self.status = '1'
            self.is_open.config(text = 'Aberto' )
            self.is_open_text = 'Aberto'
        else:
            self.after(1000, lambda: self.blocked(ser))

if __name__ == "__main__":
    app = App()
    app.mainloop()