#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 21:47:03 2022

@author: ignacioloyola
"""

import PyPDF2
import os

merger = PyPDF2.PdfFileMerger()

for file in os.listdir(os.curdir): #enlista los elementos de current directory
    if file.endswith(".pdf"):
        merger.append(file)             #Agrega el file 2 a la cola del primero      
    merger.write("combinedDocs.pdf")    #escribe el nuevo documento combinado
