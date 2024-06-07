#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 12:20:36 2022

@author: ignacioloyola
"""
# Script para detectar cambios en los archivos de una carpeta source_dir mediante
# la libreria "watchdog"
# Detecta la descarga de archivos y los guarda en carpetas, clasificandolos en
# imágen, video, audio o texto.

from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



# Definimos las carpetas donde se irán los archivos

source_dir = "/Users/ignacioloyola/Downloads"
dest_dir_audio = "/Users/ignacioloyola/Downloads/Downloaded Audios"
dest_dir_video = "/Users/ignacioloyola/Downloads/Downloaded Videos"
dest_dir_image = "/Users/ignacioloyola/Downloads/Downloaded Images"
dest_dir_documents = "/Users/ignacioloyola/Downloads/Downloaded Documents"

# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]



# agrega un numero al final de nombre para hacerlo unico
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

# Funcion para mover archivo con su actual nombre o con uno nuevo si el
# archivo existe, aplica la funcion make_unique.
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)



class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
       with scandir(source_dir) as entries:
           for entry in entries:
               name = entry.name
               self.check_audio_files(entry, name)
               self.check_video_files(entry, name)
               self.check_image_files(entry, name)
               self.check_document_files(entry, name)
               
               
    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_audio, entry, name)
                logging.info(f"Audio File {name} has been moved")
                
    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Image File {name} has been moved")
                
    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Video File {name} has been moved")
                
    def check_document_files(self, entry, name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Document File {name} has been moved")                
                
                
    
        
        
        
        
        
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

