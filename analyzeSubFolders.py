#python2
#Analyze all subfolders inside a folder

import analyzeFolder
import sys
import os

def listFoldersContainingZF(rFolder):
    """Returns a list of folders, inside rFolder, that contains Zena Files"""

    lf = []

    for (path, dirs, files) in os.walk(rFolder):
        for f in files:
            if '.zna' in f:
                lf.append(path)
                break

    #remove repeated
    lf = list(set(lf))

    return lf


if len(sys.argv)<2 :
    print('ERRO!\nUso: python2 analyzeSubFolders.py "/pasta/raiz/que/contem/outras/pastas" <format>\nOnde format = csv ou txt')
    sys.exit(0)

rootFolder = sys.argv[1]
format = sys.argv[2].lower()

folders = listFoldersContainingZF(rootFolder)

for folder in folders:
    analyzeFolder.processFolder(folder, format)

print('Resultado gerado com sucesso')


