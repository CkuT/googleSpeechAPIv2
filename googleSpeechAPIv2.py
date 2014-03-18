#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""googleSpeechAPI
 
Usage:
  googleSpeechAPI.py APIKEY FILE

Process FILE and optionally apply correction to either left-hand side or
right-hand side.

Arguments:
  APIKEY  API Key for Google Speech
  FILE    File containing links

Options:
  -h --help                Show the help.
  -l --lang=<language>     Lang.
"""

import requests
import json
import subprocess
import os
import time
from docopt import docopt

def getTextFromGoogle(speechFile,lang='fr-fr'):
    """ Send the file to Google Speech for recognition """
    speechFile = convertToFlac(speechFile)
    payload = {
                'output': 'json', 
                'lang': lang,
                'key': arguments['APIKEY']
              }

    f = {'files': open(speechFile)}

    headers = {
                'Content-Type': 'audio/x-flac; rate=8000',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
              }

    r = requests.post('https://www.google.com/speech-api/v2/recognize', params=payload, headers=headers, files=f)
    return r

def convertToFlac(audioFile):
    """ Converts the file to flac 8khz"""
    folder, filename = os.path.split(os.path.abspath(audioFile))
    
    folder = folder
    filename = filename.split(".")[0]
    subprocess.call(["avconv", "-i", audioFile, "-ar", "8000","-y", folder + "/" + filename + ".flac"])
    return folder + "/" + filename + ".flac"

def listFolderFilesType(filePath,fileType):
    """ List files with fileType in filePath """
    return [f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath,f)) and f.endswith(".%s" % fileType)]

def writeFiles(fileName,filePath):
    """ Write list of files from a folder """
    with open(fileName, 'w') as fichier:
      for i in listFolderFilesType(filePath,"wav"):
        fichier.write(os.path.join(filePath,i) + os.linesep)

def ASRMyFile(fileWithLinks):
    """ ASR for multiple files (one per line) """
    with open(fileWithLinks, 'r') as myFile:
        for line in myFile:
            print "Fichier : %s " % line
            r = getTextFromGoogle(line.strip())
            with open(line.strip() + ".reco", 'w') as fichier:
                fichier.write(r.text.encode('utf8'))
            time.sleep(2)

if __name__ == '__main__':
    arguments = docopt(__doc__, version="0.02")
    ASRMyFile(arguments['FILE'])
    print(arguments['APIKEY'])
