#python2
#Analyze one Folder of ZenaFiles

import sys
import os
import zenafile

def processEnsaio(f):
    '''Process zna file'''

    zF = zenafile.myZenaFile()

    zF.open(f)
    zF.readPackets()

    ensaio=[]   

    for i in range (1,4):
        ensaio.append(zF.getLastDataFromAddr(i))

    return ensaio

def processFolder(folder, format):
    "Process folder that contains .zna files"

    folderName = folder.split('/')[-1]

    ensaios=[]

    #Processa Ensaios
    for f in sorted(os.listdir(folder)):
        ext = f.split('.')[-1]

        if ext == 'zna':
            ensaios.append(processEnsaio(folder+'/'+f))

    #Faz Medias/Desvio
    tEnviadas = tPerdidas = tFalhasDin = float(0)
    n = float(len(ensaios))*3

    for ensaio in ensaios:
        for nodo in ensaio:
            tEnviadas += nodo['enviadas']
            tPerdidas += nodo['perdidas']
            tFalhasDin += nodo['falhasDinamicas']

    #medias    
    mEnviadas = tEnviadas/n
    mPerdidas = tPerdidas/n
    mFalhasDin = tFalhasDin/n

    #porcentagem
    pPerdas = tPerdidas/tEnviadas*100
    pDeadline = tFalhasDin/tEnviadas*100

    #desvio
    dEnviadas = dPerdidas = dFalhasDin = 0

    for ensaio in ensaios:
        for nodo in ensaio:
            dEnviadas += (nodo['enviadas']-mEnviadas)**2
            dPerdidas += (nodo['perdidas']-mPerdidas)**2
            dFalhasDin += (nodo['falhasDinamicas']-mFalhasDin)**2

    dEnviadas = (dEnviadas/(n-1))**(1/2.)
    dPerdidas = (dPerdidas/(n-1))**(1/2.)
    dFalhasDin = (dFalhasDin/(n-1))**(1/2.)


    if format=='txt':
        resultF = open(folder+'/resultado.txt', 'w')
        resultF.write('Resultado do Teste '+folderName+'\n\n')
        resultF.write('{0:^5}{1:^10}{2:^10}{3:^20}{4:^15}\n'.format('ID', 'Enviadas', 'Perdidas', 'FalhasDinamicas', 'DistanciaFalha'))

        for ensaio in ensaios:
            resultF.write('\n{0:^60}\n'.format('Ensaio '+str(ensaios.index(ensaio)+1)))
            for nodo in ensaio:
                txt = '{0:^5}{1[enviadas]:^10}{1[perdidas]:^10}{1[falhasDinamicas]:^20}{1[distanciaFalha]:^15}'.format(ensaio.index(nodo)+1, nodo)
                resultF.write(txt+'\n')

        #Imprime medias
        resultF.write('\n\n')
        resultF.write('Resultados Medios:\n')
        resultF.write('{0:^5}{1:^10.3f}{2:^10.3f}{3:^20.3f}\n\n'.format('',mEnviadas, mPerdidas, mFalhasDin))

        resultF.write('Resultados Desvios:\n')
        resultF.write('{0:^5}{1:^10.3f}{2:^10.3f}{3:^20.3f}\n\n'.format('',dEnviadas, dPerdidas, dFalhasDin))

        resultF.write('Resultado Percentual:\n')
        resultF.write('Perdas de deadline: {0:.3f}%\nFalhas dinamicas: {1:.3f}%'.format(pPerdas,pDeadline))

        #Fecha Arquivo
        resultF.close()
    else:
        resultF = open(folder+'/resultado.csv', 'w')
        resultF.write('Resultado do Teste '+folderName+'\n\n')
        resultF.write('{},{},{},{},{}\n'.format('ID', 'Enviadas', 'Perdidas', 'FalhasDinamicas', 'DistanciaFalha'))

        for ensaio in ensaios:
            resultF.write('\n{}\n'.format('Ensaio '+str(ensaios.index(ensaio)+1)))
            for nodo in ensaio:
                txt = '{0},{1[enviadas]},{1[perdidas]},{1[falhasDinamicas]},{1[distanciaFalha]}'.format(ensaio.index(nodo)+1, nodo)
                resultF.write(txt+'\n')

        #Imprime medias
        resultF.write('\n\n')
        resultF.write('Resultados Medios:\n')
        resultF.write('{0},{1:.3f},{2:.3f},{3:.3f}\n\n'.format('',mEnviadas, mPerdidas, mFalhasDin))

        resultF.write('Resultados Desvios:\n')
        resultF.write('{0},{1:.3f},{2:.3f},{3:.3f}\n\n'.format('',dEnviadas, dPerdidas, dFalhasDin))

        resultF.write('Resultado Percentual:\n')
        resultF.write('Perdas de deadline: {0:.3f}%\nFalhas dinamicas: {1:.3f}%'.format(pPerdas,pDeadline))

        #Fecha Arquivo
        resultF.close()

    print('Folder {0} completed'.format(folder))


if __name__ == '__main__':
    #Running stand-alone

    #Help
    if len(sys.argv) < 2:
        print('ERRO!\nUso: python2 analyzeFolder.py "/local/armazenado/arquivos/zena" <format>\nOnde format = csv ou txt')
        sys.exit(0)

    folder = sys.argv[1]    

    #Obtem Formato do Arquivo
    format = sys.argv[2].lower()

    processFolder(folder, format)

    print('Resultado gerado com sucesso')





