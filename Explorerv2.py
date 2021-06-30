from tkinter import *
from tkinter import messagebox
import os
import subprocess

cp = ''
cpwd= ''

root = Tk()
root.title('Gestor Linux')
owner = StringVar()
password = StringVar()
nombre = StringVar()
rmuser = StringVar()

def upLevel():
    clearListbox()
    os.chdir(os.getcwd()+'/..')
    explorerListbox.insert(END,*getLs())

def enterFolder(item):
    try:
        os.chdir(os.getcwd()+'/'+item)
        clearListbox()
        explorerListbox.insert(END,*getLs())
    except Exception as e:
        messagebox.showwarning('Imposible','No es un directorio')

def getLs():
    command = subprocess.run('ls',stdout=subprocess.PIPE)
    return command.stdout.decode('utf-8').strip().split('\n')

def getLsLa():
    command = subprocess.run(['ls','-la'],stdout=subprocess.PIPE)
    return command.stdout.decode('utf-8').strip().split('\n')

def copy(cpf, cdpad):
    global cp
    cp = cpf
    global cpwd
    cpwd = cdpad
    print (cp,cpwd)

def paste(pwd):
    print (cp,cpwd)
    if(cpwd != ''):
        if(pwd == cpwd):
            subprocess.run(['cp','-R', cpwd+'/'+cp, cpwd+'/'+cp+'-copy'])
            clearListbox()
            explorerListbox.insert(END,*getLs())
        else:
            subprocess.run(['cp','-R',cpwd+'/'+cp, pwd])
            clearListbox()
            explorerListbox.insert(END,*getLs())

def cowner(cof):
    print(cof)
    if( owner != ''):
        subprocess.run(['chown',owner.get(),cp])
    else:
        print("Inserte un usuario valido")




explorerListbox = Listbox(root)
explorerListbox.pack()
explorerListbox.insert(END,*getLs())

def clearListbox():
    explorerListbox.delete(0,END)

img = PhotoImage(file = 'btn.png')

buttonUp = Button(root,text='Subir',  image= img, command=upLevel)
buttonUp.pack()

buttonIn = Button(root,text='Entrar',  image= img, command=lambda: enterFolder(explorerListbox.get(ANCHOR)))
buttonIn.pack()

buttonCp = Button(root,text='Copiar',  image= img, command=lambda: copy(explorerListbox.get(ANCHOR), os.getcwd()))
buttonCp.pack()

buttonPs = Button(root,text='Pegar',  image= img, command=lambda: paste(os.getcwd()))
buttonPs.pack()

LabelOwner = Label(root, text='Nuevo dueño')
LabelOwner.pack()
O = Entry(root, textvariable=owner)
O.pack()

LabelUsuario = Label(root, text='Nombre del nuevo usuario')
LabelUsuario.pack()
N = Entry(root, textvariable=nombre)
N.pack()

LabelPassword = Label(root, text='Password del nuevo usuario')
LabelPassword.pack()
P = Entry(root, textvariable=password)
P.pack()

def createUser():
    if(password.get()==''):
        subprocess.run(['useradd',nombre.get()])
    else:
        subprocess.run(['useradd','-p',password.get(),nombre.get()])

buttonNewOwner = Button(root, text='Cambiar de propietario' ,  image= img, command=lambda: cowner(explorerListbox.get(ANCHOR)))
buttonNewOwner.pack()

buttonCreateUser = Button(root, text='Crear usuario' ,  image= img, command=createUser)
buttonCreateUser.pack()

belPassword = Label(root, text='usuario a eliminar')
LabelPassword.pack()
P = Entry(root, textvariable=rmuser)
P.pack()

def deleteUser():
    if (rmuser.get() != ''):
        subprocess.run(['userdel','-f',rmuser.get()])

buttonRmUser = Button(root,text='Eliminar usuario',  image= img, command=deleteUser)
buttonRmUser.pack()

root.mainloop()
