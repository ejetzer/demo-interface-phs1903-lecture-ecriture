#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
Démonstration de communication série.

Créé le Mon Nov 29 14:11:57 2021

@author: ejetzer
"""

import tkinter as tk
from tkinter import ttk

import serial

from serial.tools.list_ports import comports

# Sélectionner un port série (peut-être codé directement)
ports= comports()
for i, p in enumerate(ports):
    print(f'[{i}] {p!s}')

choix = int(input('Quel port?'))
port = ports[choix]
com = serial.Serial(port.device, 115200, timeout=1)
# Mauvaise pratique. Si il y a une erreur, le port peut devenir innaccessible.
# La bonne manière serait de restructure le programme et d'utiliser un bloc
# with Serial(...) as ...:
#     ...

# Objets tkinter globaux (contenants)
racine = tk.Tk()
racine.title('Démo de communication série')
cadre = tk.Frame(racine)

var_écrire: tk.StringVar = tk.StringVar(racine, 'rien')
var_lecture: tk.StringVar = tk.StringVar(racine, '')


dictionnaire = {'a': 0b00001,
                'l': 0b00010,
                'o': 0b00011,
                'r': 0b00100,
                'i': 0b00101,
                'e': 0b00110,
                'n': 0b00111}

def f(s:str) -> bytes:
    return bytes([dictionnaire[c] for c in s])

def finv(b:bytes) -> str:
    s = ''
    #for bit in b[:-1]:
    #    idx = list(dictionnaire.values()).index(bit)
    #    s = s + dictionnaire.keys()[idx]
    for a in b:
        s = s + ' ' + str(hex(a))
    return s


def lire(var=var_lecture, com=com, racine=racine):
    val = var.get()
    try:
        nouv = finv(com.read(4))
        if nouv:
            val = nouv
    except UnicodeDecodeError:
        val = var.get()

    var.set(val)

def écrire(var=var_écrire, com=com):
    val = var.get()
    print('Valeur brute: ' + val)
    print('Valeur transformée: ' + repr(f(val)))
    com.write(f(val))

entrée = ttk.Entry(cadre, textvariable=var_écrire, font=('Arial', 36))
bouton1 = ttk.Button(cadre, text='Envoyer', command=écrire)
cadran = ttk.Label(cadre, textvariable=var_lecture, font=('Arial', 36))
bouton2 = ttk.Button(cadre, text='Recevoir', command=lire)

entrée.pack(padx=10, pady=10)
bouton1.pack(padx=10, pady=10)
cadran.pack(padx=10, pady=10)
bouton2.pack(padx=10, pady=10)
cadre.pack()

racine.mainloop()

# Important:
com.close()
