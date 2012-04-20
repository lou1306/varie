#!/usr/bin/env python2
# -*- coding: utf-8 -*-


## Virgin Radio Log
## ©2012 Luca Di Stefano
## lou1306.tumblr.com
##
##     This program is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.
##
##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.
##
##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
## Il programma controlla il brano attualmente in esecuzione su Virgin Radio e
## salva le informazioni (data, ora, titolo, artista) su un file di testo ('songs.txt').
##
import urllib
import re
import datetime
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

def fetch_song():
    # Inviamo la richiesta
    f = urllib.urlopen("http://virginradioitaly.s.widget.ldrhub.com/new/api/now_playing/virginradioitaly/")
    # Salviamo la risposta in una stringa s
    s = f.read()
    f.close()

    # Stringhe di esempio
    #s = 'jQuery15109967182718683034_1334405218381({"now_playing":{"id":"10805604","title":"ORANGE CRUSH","artist":"R.E.M.","seconds_left":102}});'
    # s = 'jQuery15109967182718683034_1334405218381({"now_playing":null});'

    # Controlliamo se c'è una canzone in esecuzione
    now = re.search(r'now_playing":(.*)}', s).group(1)
    if now != "null":
        # Estrazione delle informazioni sulla canzone
        info =  re.search('"title":"(.*)","artist":"(.*)",',now)
        data = info.group(1) + " ### "+ info.group(2)
        # Maiuscola per la prima lettera di ogni parola
        data = ' '.join(word.capitalize() for word in data.split())
        #Rimuove le backslah (in "AC\/DC", ad esempio)
        data =  data.replace('\/', '/')
        # lettura dal file
        try:
            f = open("songs.txt", "r")
        except IOError as e:
            # se songs.txt non esiste, viene creato
            f = open("songs.txt", "w")
            f.close()
            f = open("songs.txt", "r")
        songs = f.readlines()
        f.close()

        if len(songs) > 0:
            # prev = ultima canzone salvata
            prev= songs[-1]
            prev = prev.strip()
        else:
            prev = ""
        if data != prev:
            f = open("songs.txt", "a")
            now = datetime.datetime.now()
            f.write(now.strftime("%Y-%m-%d %H:%M")+"\n"+data+"\n")
            f.close()

# La funzione viene eseguita ogni 60 secondi
lc = LoopingCall(fetch_song)
lc.start(60)
reactor.run()
