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

def lire(var=var_lecture, com=com, racine=racine):
    val = var.get()
    try:
        nouv = str(com.read_until('\n'), encoding='utf-8').strip()
        if nouv:
            val = nouv
    except UnicodeDecodeError:
        val = var.get()

    var.set(val)

def écrire(var=var_écrire, com=com):
    val = var.get()
    com.write(bytes(val, encoding='utf-8'))

var_écrire.trace('w', écrire)
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
