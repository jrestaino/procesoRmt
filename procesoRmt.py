import operator
import os
import re
import json
import random
import datetime

def creoCarpetaResultados(paramDir):
    # Creo carpetas
    # Se define el nombre de la carpeta o directorio a crear
    directorio = paramDir
    try:
        os.makedirs(directorio)
    except OSError:
        print("La creación del directorio %s falló" % directorio)
        return directorio
    else:
        print("Se ha creado el directorio: %s " % directorio)
        return directorio

def isNumeric(s):
    #defino funcion para saber si es un entero en nunero a procesar
    try:
        int(s)
        return True
    except ValueError:
        return False

def eligoNumero(cantAsbr):

    numeros_enteros = range(cantAsbr)

    # Elegimos tres números enteros aleatorios de la lista
    numeros_aleatorio = random.choice(numeros_enteros)
    return numeros_aleatorio

def mergeDicAsbrOrigenes(paramListaDiccionarios, paramResultadosDir):
    returnMergeDicAsbrOrigenes = {}
    for d in paramListaDiccionarios:
        for key, value in d.items():
            #returnMergeDicAsbrOrigenes.setdefault(key, []).extend(value)
            if key not in returnMergeDicAsbrOrigenes:
                returnMergeDicAsbrOrigenes[key] = []
            mergeDicValue = list( set(returnMergeDicAsbrOrigenes[key]) | set(value) )

            '''
            # prueba
            if key == 5:
                print('valor con key 5')
                #print(value)
                print('para key: ' + str(key))
                print('len returnMergeDicAsbrOrigenes[key]: ' + str(len(returnMergeDicAsbrOrigenes[key])))
                print('len value: ' + str(len(value)))
                print('len mergeDicValue: ' + str(len(mergeDicValue)))
            '''

            returnMergeDicAsbrOrigenes[key] = mergeDicValue

    # genero los archivos de salida
    diccionarioOrigenesMergeJson = paramResultadosDir + '/diccionarioOrigenesMerge.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioOrigenesMergeJson, 'w') as archivoDiccionarioOrigenesMergeJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnMergeDicAsbrOrigenes, archivoDiccionarioOrigenesMergeJson)
    return returnMergeDicAsbrOrigenes

def armoListaAsbr(paramCantidadAsbr):
    if isNumeric(paramCantidadAsbr):
        returnListaAsbr = list(range(paramCantidadAsbr))
        return returnListaAsbr
    else:
        print('paramCantidadAsbr no es un entero')

def buscoPeers(paramAsBuscado, paramArchivoPath):

    # genero el archivo de salida
    directorioResultadosBuscoPeers = 'resultados/' + str(paramAsBuscado) + '/'
    archivoOutNombre = directorioResultadosBuscoPeers + 'out_' + str(paramAsBuscado) + '_' + paramArchivoPath + '.txt' 
    archivoOut = open(archivoOutNombre, 'w')
    archivoDump = 'archivosBgpDump/' + paramArchivoPath


    # busco los peers para un determinado ASN en un archivo preprocesado
    with open(archivoDump, 'r') as f:
        for asPath in f:
            index = 0
            asPath = asPath.rstrip('\r\n')

            asPath = asPath.replace('{','')
            asPath = asPath.replace('}','')

            asPathArray = asPath.split(' ')
            #print(asPathArray)

            for asn in asPathArray:
                if asn == str(paramAsBuscado):

                    try:
                        salidaCliente = 'peer:' + asPathArray[index+1] + ',' 'origen:' + asPathArray[-1] + '\r\n'
                        #print(salidaCliente)
                        archivoOut.write(salidaCliente)
                    except IndexError as ultimoAs:
                        pepe = 1
                    if index == 0:
                        print('prueba en ' + str(paramAsBuscado))
                    else:
                        salidaProveedor = 'peer:' + asPathArray[index-1] + ',' 'origen:' + asPathArray[1] + '\r\n'
                        #print(salidaProveedor)
                        archivoOut.write(salidaProveedor)
                else:
                    index = index + 1
        
    archivoSorted = directorioResultadosBuscoPeers + 'sorted_' + 'out_' + str(paramAsBuscado) + '_' + paramArchivoPath + '.txt'
    cmd = 'sort -u ' + archivoOutNombre + ' > ' + archivoSorted
    print(cmd)
    os.system(cmd)


def buscoPeersMenor(paramAsBuscado, paramArchivoPath):

    # genero el archivo de salida
    directorioResultadosBuscoPeers = 'resultados/' + str(paramAsBuscado) + '/'
    archivoOutNombre = directorioResultadosBuscoPeers + 'out_' + str(paramAsBuscado) + '_' + paramArchivoPath + '_distancia.txt' 
    archivoOut = open(archivoOutNombre, 'w')
    archivoDump = 'archivosBgpDump/' + paramArchivoPath
    origenesPeerDistDict = dict()
    listaDiccionarios = []

    # busco los peers para un determinado ASN en un archivo preprocesado
    with open(archivoDump, 'r') as f:
        for asPath in f:
            index = 0
            asPath = asPath.rstrip('\r\n')

            asPath = asPath.replace('{','')
            asPath = asPath.replace('}','')
            asPath = asPath.replace(',',' ')

            asPathArray = asPath.split(' ')
            #print(asPathArray)

            for asn in asPathArray:
                if asn == str(paramAsBuscado):

                    try:
                        origenCliente = asPathArray[-1]
                        peerCliente = asPathArray[index+1]
                        pos_peerCliente = asPathArray.index(peerCliente)
                        pos_origenCliente = asPathArray.index(origenCliente)
                        distanciaPeerOrigenCliente = abs(pos_peerCliente - pos_origenCliente)

                        salidaCliente = 'peer:' + peerCliente + ',' 'origen:' + origenCliente + ',' 'distancia:' + str(distanciaPeerOrigenCliente) + '\r\n'
                        archivoOut.write(salidaCliente)
                    except IndexError as ultimoAs:
                        pepe = 1
                    if index == 0:
                        print('prueba en ' + str(paramAsBuscado))
                    else:
                        origenProveedor = asPathArray[1]
                        peerProveedor = asPathArray[index-1]
                        pos_peerProveedor = asPathArray.index(peerProveedor)
                        pos_origenProveedor = asPathArray.index(origenProveedor)
                        distanciaPeerOrigenProveedor = abs(pos_peerProveedor - pos_origenProveedor)
                        salidaProveedor = 'peer:' + peerProveedor + ',' 'origen:' + origenProveedor + ',' 'distancia:' + str(distanciaPeerOrigenProveedor) + '\r\n'
                        #print(salidaProveedor)
                        archivoOut.write(salidaProveedor)
                else:
                    index = index + 1
        
    archivoSorted = directorioResultadosBuscoPeers + 'sorted_' + 'out_' + str(paramAsBuscado) + '_' + paramArchivoPath + '_distancia.txt'
    cmd = 'sort -u ' + archivoOutNombre + ' > ' + archivoSorted
    print(cmd)
    os.system(cmd)
    print(origenesPeerDistDict)


def buscoMenoresBuscoPeers(paramAsBuscado, paramArchivoPath):

    print('comienzo con buscoMenoresBuscoPeers')
    origenesPeerDistDict = dict()
    listaDiccionarios = []
    directorioResultadosBuscoPeers = 'resultados/' + str(paramAsBuscado) + '/'

    inArchivoSorted = directorioResultadosBuscoPeers + 'sorted_' + 'out_' + str(paramAsBuscado) + '_' + paramArchivoPath + '_distancia.txt'

    with open(inArchivoSorted, 'r') as archivoSorted:
        for line in archivoSorted:
            #print(line)
            line = line.strip()
            lineSplit = line.split(',')
            peerSplit = lineSplit[0].split(':')
            peer = peerSplit[1]
            origenSplit = lineSplit[1].split(':')
            origen = origenSplit[1]
            distanciaSplit = lineSplit[2].split(':')
            distancia = distanciaSplit[1]

            diccionario_buscado = next((d for d in listaDiccionarios if d.get('origen') == origen), None)
            if diccionario_buscado:
                #print('encontre el diccionario')
                if diccionario_buscado['distancia'] > distancia:
                    diccionario_buscado['distancia'] = distancia
                    diccionario_buscado['peer'] = [peer]
                if diccionario_buscado['distancia'] == distancia:
                    diccionario_buscado['peer'].append(peer)

            else:
                dicc = {'origen': origen, 'peer': [peer], 'distancia': distancia}
                listaDiccionarios.append(dicc)


    listaDic = directorioResultadosBuscoPeers + 'listaDic.txt' 
    nombrelistaDic = open(listaDic, 'w')
    print('escribo lista diccionarios')
    nombrelistaDic.write(str(listaDiccionarios))

    #outSorted = directorioResultadosBuscoPeers + 'sorted_' + 'out_' + str(paramAsBuscado) + '_' + paramArchivoPath + '_distancia_nuevo.txt'
    outSorted = directorioResultadosBuscoPeers + 'sorted_' + 'out_' + str(paramAsBuscado) + '_' + paramArchivoPath + '.txt'
    archivoOutSorted = open(outSorted, 'w')
    #print(listaDiccionarios)
    print('comienzo a escribir el archivo distancia nuevo')
    for dicOrigen in listaDiccionarios:
        origenArchivo = dicOrigen['origen']
        for peerArchivo in dicOrigen['peer']:
            salidaArchivo = 'peer:' + peerArchivo + ',origen:' + origenArchivo + '\r\n'
            archivoOutSorted.write(salidaArchivo)

    print('fin de buscoMenoresBuscoPeers')

def analizoArchivo(paramArchivoPath, paramAsnEstudio, paramResultadosDir):
    # Analizo el archivo sorted_out
    # devuelvo 
    #   - un diccionario con los origenes por cada peer (clave = peer, valor = lista con los origenes por allí conocidos)
    #   - una lista con todos los origenes
    #   - una lista con todos los peers

    print('comienzo analizoArchivo con: ' + paramArchivoPath + ' - ' + str(paramAsnEstudio))

    paramNombreArchivoEntrada = 'sorted_out_' + str(paramAsnEstudio) + '_' + paramArchivoPath + '.txt'

    directorioResultadosAnalizoArchivo = 'resultados/' + str(paramAsnEstudio) + '/'
    archivoEntrada = directorioResultadosAnalizoArchivo + paramNombreArchivoEntrada
    #print(archivoEntrada)
    # Abro archivo sorted peer AS Origen
    text = open(archivoEntrada, "r")

    # Creo un diccionario vacio para armar el par peer origenes por el peer
    returnDicOrigenes = dict()

    # hago una lista con todos los peers
    returnPeersTotales = []

    # hago una lista con todos los ASN posibles
    returnOrigenesTotales = []

    # analizo el archivo de entrada y separo los peers de los origenes para cargar los diccionarios
    for line in text:
        line = line.strip()
        peers = line.split(',')
        asnPeer = peers[0].split(':')
        strPeer = asnPeer[1]
        asnOrigen = peers[1].split(':')
        strOrigen = asnOrigen[1]

        # si peer y origen son numericos armo el diccionario donde la clave es el peer y una lista con cada origen es el valor
        if isNumeric(strPeer) and isNumeric(strOrigen):
            peer = int(strPeer)
            origen = int(strOrigen)

            if int(peer) not in returnDicOrigenes:
                returnDicOrigenes[peer] = []
            returnDicOrigenes[peer].append(origen)
            
            # armo una lista con todos los ASN
            if origen not in returnOrigenesTotales:
                returnOrigenesTotales.append(origen)
                
            # armo una lista con todos los peers (los peers los manejo como int para poder manejarlos como conjuntos)
            if peer not in returnPeersTotales:
                returnPeersTotales.append(int(peer))

        else:
            print('Origen: ' + str(strPeer))
            print('Peer: ' + str(strOrigen))

    # genero los archivos de salida
    diccionarioOrigenesJson = paramResultadosDir + '/diccionarioOrigenes.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioOrigenesJson, 'w') as archivoDiccionarioOrigenesJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicOrigenes, archivoDiccionarioOrigenesJson)

    peerTotales = paramResultadosDir + '/peerTotales.txt'
    with open(peerTotales, 'w') as archivoPeerTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoPeerTotales.write(str(returnPeersTotales) + ';' + str(len(returnPeersTotales)))

    origenesTotales = paramResultadosDir + '/origenesTotales.txt'
    with open(origenesTotales, 'w') as archivoOrigenesTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoOrigenesTotales.write(str(returnOrigenesTotales) + ';' + str(len(returnOrigenesTotales)))

    print('fin analizoArchivo con: ' + paramArchivoPath + ' - ' + str(paramAsnEstudio))
    return returnDicOrigenes, returnPeersTotales, returnOrigenesTotales

def calculoAsbr(paramCantSitios, paramResultadosDir):
    # Estimar la cantidad de ASBR que tiene el AS bajo estudio
    # a la cantidad de sitios vamos a multiplicarla de manera aleatoria por 1, 1.5 o 2
    # entrada cantidad de sitios del AS bajo estudio
    # devuelvo
    #   - cantidad de Asbr estimada

    multiplicadoresAsbr = [1, 1.5, 2]
    multiplicadorAsbr = random.choice(multiplicadoresAsbr)
    returnCantAsbr = round(multiplicadorAsbr * paramCantSitios)

    salidaArchivo = paramResultadosDir + '/cantidadAsbr.txt'
    archivoOutCantidadAsbr = open(salidaArchivo, 'w')
    archivoOutCantidadAsbr.write(str(returnCantAsbr))
    print('cantidad Asbr: ' + str(returnCantAsbr))


    return returnCantAsbr


def asignoAsbrArchivo(paramdiccionarioOrigenes, paramPeersTotales, paramResultadosDir):
    # Asigna los peers a los ASBRs en funcion de archivos de entrada donde estan los asbr y como estan asignado los peers 
    # Analizo la salida del metodo analizoArchivo, con lo cual como entrada estan la salida de este y un directorio donde esta la asignacion de los peers al asbr
    # devuelvo
    #   - un diccionario con los peers por cada asbr (clave = asbr, valor = peers por asbr)
    #   - un diccionario con los origenes por cada asbr (clave = asbr, valor = origenes por asbr)
    #   - una lista con todos los asbr

    print('comienzo asignoAsbrArchivo')

    # inicializo el numero de asbr
    asbr = 0

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Peers del mismo
    returnDicAsbrPeers = dict()

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Origen que se aprenden por el mismo
    returnDicAsbrOrigenes = dict()

    # inicializo lista con cuales son los asbrs
    returnAsbrTotales = []

    # asigno los asbr en funcion de archivos que contienen los peers por ASBR
    directorioAsbrPeersParam = 'archivosAsbrPeers/'

    for filename in os.listdir(directorioAsbrPeersParam):

        # cargo los asbr en returnAsbrTotales
        if asbr not in returnAsbrTotales:
            returnAsbrTotales.append(asbr)

        # inicializo los diccionarios para los ASBR que voy a trabajar
        if asbr not in returnDicAsbrPeers:
            returnDicAsbrPeers[asbr] = []
        if asbr not in returnDicAsbrOrigenes:
            returnDicAsbrOrigenes[asbr] = []

        # analizo los archivos en el directorio
        if os.path.isfile(os.path.join(directorioAsbrPeersParam, filename)):

            # indico cual es el asbr respecto del archivo
            equivalencia = str(asbr) + ' <-> ' + filename
            print('equivalencia ' + equivalencia)

            # abro el archivo
            with open(os.path.join(directorioAsbrPeersParam, filename), 'r') as archivoASRBPeers:

                # Cargo una lista con las lineas de los archivos casteandolas a int
                listaArchivoASBRPeers = []
                for lineArchivoASBRPeers in archivoASRBPeers:
                    if isNumeric(lineArchivoASBRPeers):
                        listaArchivoASBRPeers.append(int(lineArchivoASBRPeers.strip()))
                archivoASRBPeers.close()

                # realizo la interseccion de listas, primero las paso a conjuntos y luego uso el operador & que es la interseccion entre ambas

                # Se realiza la interseccion entre ambos conjuntos.
                interseccion = list(set(paramPeersTotales)&set(listaArchivoASBRPeers))

                print('Interseccion del archivo ' + filename)
                print('longuitud interseccion ' + str(len(interseccion)))

                # para cada ASN que se encuentra en el archivo y en los ASN encontrados previamente cargo los diccionarios returnDicAsbrPeers y returnDicAsbrOrigenes
                for j in interseccion:
                    peerAsn = int(j)
                    returnDicAsbrPeers[asbr].append(peerAsn)
                    origenAsbr_old = returnDicAsbrOrigenes[asbr]
                    origenAsbr = list( set(origenAsbr_old) | set(paramdiccionarioOrigenes[peerAsn]) )
                    returnDicAsbrOrigenes[asbr] = origenAsbr

        asbr = asbr + 1

    # genero los archivos de salida
    diccionarioAsbrPeersJson = paramResultadosDir + '/diccionarioAsbrPeers.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrPeersJson, 'w') as archivoDiccionarioAsbrPeersJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrPeers, archivoDiccionarioAsbrPeersJson)

    diccionarioAsbrOrigenesJson = paramResultadosDir + '/diccionarioAsbrOrigenes.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrOrigenesJson, 'w') as archivoDiccionarioAsbrOrigenesJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrOrigenes, archivoDiccionarioAsbrOrigenesJson)

    asbrTotales = paramResultadosDir + '/asbrTotales.txt'
    with open(asbrTotales, 'w') as archivoAsbrTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoAsbrTotales.write(str(returnAsbrTotales))

    print('fin asignoAsbrArchivo')

    return returnDicAsbrPeers, returnDicAsbrOrigenes, returnAsbrTotales

def asignoAsbrIxp(paramdiccionarioOrigenes, paramPeersTotales, paramResultadosDir, paramCantidadAsbr, paramDiccionarioIxp):
    # Asigna los peers a los ASBRs en funcion, los peers pertenecientes a un asbr se asignan al mismo asbr 
    # Analizo la salida del metodo analizoArchivo, con lo cual como entrada estan la salida de este y un directorio donde esta la asignacion de los peers al asbr
    # devuelvo
    #   - un diccionario con los peers por cada asbr (clave = asbr, valor = peers por asbr)
    #   - un diccionario con los origenes por cada asbr (clave = asbr, valor = origenes por asbr)
    #   - una lista con todos los asbr
    #   - una lista con los peers sin asignar

    print('comienzo asignoAsbrIxp')

    # inicializo el numero de asbr
    #asbr = 0

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Peers del mismo
    returnDicAsbrPeers = dict()

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Origen que se aprenden por el mismo
    returnDicAsbrOrigenes = dict()

    # inicializo lista con cuales son los asbrs
    returnAsbrTotales = []

    # inicializo la lista con los peers que faltan asignar
    returnPeersNoAsignados = []

    # inicializo la lista con los peers asignados
    returnPeersAsignados = []

    # levanto el diccionario de los ix
    with open(paramDiccionarioIxp, "r") as archivoDicIxp:
        diccionarioIxp = json.load(archivoDicIxp)


    for keyIxp, valueListIxpPeers in diccionarioIxp.items():
        interseccionIxpPeers = list(set(paramPeersTotales)&set(valueListIxpPeers))

        returnPeersAsignados = list ( set(returnPeersAsignados) | set(interseccionIxpPeers) )

        asbr = eligoNumero(paramCantidadAsbr)

        # inicializo los diccionarios para los ASBR que voy a trabajar
        if asbr not in returnDicAsbrPeers:
            returnDicAsbrPeers[asbr] = []
        if asbr not in returnDicAsbrOrigenes:
            returnDicAsbrOrigenes[asbr] = []

        for peerIxp in interseccionIxpPeers:
            # agrego el el peer al diccionario returnDicAsbrPeers
            returnDicAsbrPeers[asbr].append(peerIxp)

            # agrego al returnDicAsbrOrigenes asbr, los mismos los levanto de paramdiccionarioOrigenes con el peerIxp
            origenAsbr_old = returnDicAsbrOrigenes[asbr]
            origenAsbr = list( set(origenAsbr_old) | set(paramdiccionarioOrigenes[peerIxp]) )
            returnDicAsbrOrigenes[asbr] = origenAsbr

        # cargo los asbr en returnAsbrTotales
        if asbr not in returnAsbrTotales:
            returnAsbrTotales.append(asbr)

        '''
        # una ves que asigne a un mismo asbr todos los peers de un ixp paso a otro
        asbr = asbr + 1
        if asbr > paramCantidadAsbr:
            asbr = 0
        '''

    # me quedo con los peers no asignados
    returnPeersNoAsignados = list( set(paramPeersTotales) - set(returnPeersAsignados) )

    # genero los archivos de salida
    diccionarioAsbrPeersJson = paramResultadosDir + '/diccionarioAsbrPeersIxp.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrPeersJson, 'w') as archivoDiccionarioAsbrPeersJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrPeers, archivoDiccionarioAsbrPeersJson)

    diccionarioAsbrOrigenesJson = paramResultadosDir + '/diccionarioAsbrOrigenesIxp.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrOrigenesJson, 'w') as archivoDiccionarioAsbrOrigenesJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrOrigenes, archivoDiccionarioAsbrOrigenesJson)

    asbrTotales = paramResultadosDir + '/asbrTotalesIxp.txt'
    with open(asbrTotales, 'w') as archivoAsbrTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoAsbrTotales.write(str(returnAsbrTotales))

    peersNoAsignadosTotales = paramResultadosDir + '/asbrPeersNoAsignadosIxp.txt'
    with open(peersNoAsignadosTotales, 'w') as archivoPeersNoAsignadosTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoPeersNoAsignadosTotales.write(str(returnPeersNoAsignados) + ';' + str(len(returnPeersNoAsignados)))

    peersAsignadosTotales = paramResultadosDir + '/asbrPeersAsignadosIxp.txt'
    with open(peersAsignadosTotales, 'w') as archivoPeersAsignadosTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoPeersAsignadosTotales.write(str(returnPeersAsignados) + ';' + str(len(returnPeersAsignados)))

    print('fin asignoAsbrIxp')

    return returnDicAsbrPeers, returnDicAsbrOrigenes, returnAsbrTotales, returnPeersNoAsignados, returnPeersAsignados

def pruebaMejoresAcumulados(interseccionCarriersPeers, paramdiccionarioOrigenes, paramporcentajeAcumulado):
    # agregado para quedarnos con los carriers mas significativos
    diccionarioOrigenesCarriersLen = {}
    for carrier_for in interseccionCarriersPeers:
        diccionarioOrigenesCarriersLen[carrier_for] = len(paramdiccionarioOrigenes[carrier_for])

    print(diccionarioOrigenesCarriersLen)

    # calculo el total de los AS aprendido por los carriers
    total_origenes_carriers = sum(diccionarioOrigenesCarriersLen.values())

    # Ordenar las claves en función de sus valores de mayor a menor
    claves_ordenadas = sorted(diccionarioOrigenesCarriersLen.keys(), key=lambda clave: diccionarioOrigenesCarriersLen[clave], reverse=True)

    # Calcular el 80% del valor total
    porcentajeAcumulado = paramporcentajeAcumulado / 100
    porcentaje_seleccionado = porcentajeAcumulado * total_origenes_carriers

    # Iterar y acumular las claves hasta alcanzar el 80% del valor total
    claves_seleccionadas = []
    suma_valores = 0

    for clave in claves_ordenadas:
        suma_valores += diccionarioOrigenesCarriersLen[clave]
        claves_seleccionadas.append(clave)
        if suma_valores >= porcentaje_seleccionado:
            break

    #total_origenes_carriers = sum(len(listaOrigenes) for listaOrigenes in diccionarioOrigenesCarriers.values())
    print('Total de claves', total_origenes_carriers)
    print('75% ', porcentaje_seleccionado)
    print("Claves que representan el 75% del valor total:", claves_seleccionadas)
    cantidad_carriers_seleccionadas = len(claves_seleccionadas)
    return(cantidad_carriers_seleccionadas)


#def elijoCarriers(paramCantAsbr, paramDiccionarioCarriers, paramPeersTotales):
def elijoCarriers(paramdiccionarioOrigenes, paramPeersTotales, paramResultadosDir, paramCantidadAsbr, paramDiccionarioCarriers):

    # asigno los Carriers a diferentes ASBRs
    # entradas
    #   - Cantidad de ASBRs
    #   - Archivo con los carriers
    # Salida
    #   - diccionario donde la llave es el asbr y las claves los ASN de los carriers

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Peers del mismo
    returnDicAsbrPeers = dict()

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Origen que se aprenden por el mismo
    returnDicAsbrOrigenes = dict()

    # inicializo lista con cuales son los asbrs
    returnAsbrCarriers = []

    # inicializo la lista con los peers que faltan asignar
    returnPeersNoAsignados = []

    # inicializo la lista con los peers asignados
    returnPeersAsignados = []


    # levanto el diccionario de los Carriers
    with open(paramDiccionarioCarriers, "r") as archivoDicCarriers:
        diccionarioCarriers = json.load(archivoDicCarriers)
    carriers = diccionarioCarriers['carriers']
    interseccionCarriersPeers = list(set(paramPeersTotales)&set(carriers))
    returnPeersAsignados = interseccionCarriersPeers
    cantCarriers = len(interseccionCarriersPeers)

    ####### Inicio codigo para obtener el 75% de los carriers con mas clases
    print('cantidad de ASBR que tienen Carriers: ', cantCarriers)
    porcentaje_acumulado = 75
    cantCarriers= pruebaMejoresAcumulados(interseccionCarriersPeers, paramdiccionarioOrigenes, porcentaje_acumulado)
    print('cantidad de ASBR que representan el ' + str(porcentaje_acumulado) + ' ' + str(cantCarriers))
    ####### Fin codigo para obtener el 75% de los carriers con mas clases


    # me quedo con los peers no asignados
    returnPeersNoAsignados = list( set(paramPeersTotales) - set(returnPeersAsignados) )
    #print(carriers)

    # obtengo la cantidad de ASBR pasibles de tener una conexión con un Carrier
    multiplicadores = [1, 0.75, 0.5]
    #multiplicadores = [0.3, 0.3, 0.3]
    multiplicador = random.choice(multiplicadores)
    print('Multiplicador: ' + str(multiplicador))
    cantAsbrCarriers = round(multiplicador * cantCarriers)
    print('cantAsbrCarriers: ' + str(cantAsbrCarriers))

    # Selecciono los ASBR que pueden tener una conexion con un carrier
    numeros_enteros = range(paramCantidadAsbr)
    returnAsbrCarriers = random.sample(numeros_enteros, cantAsbrCarriers)
    print('asbrCarriers' +  str(returnAsbrCarriers))

    for carrier in interseccionCarriersPeers:

        # realizo la estimacion de la cantidad de conexiones del Carrier
        # supongo una conexion con igual peso de 1 o 2
        # si la aleatoreadad me da que el asbr es el mismo dejo una sola conexion
        conexionesPosibles = [1, 2]
        cantidadConexionesCarrier = random.choice(conexionesPosibles)
        asbrCarrierPrevio = -1
        for conexion in range(cantidadConexionesCarrier):

            asbrCarrier = random.choice(returnAsbrCarriers)
            if asbrCarrierPrevio != asbrCarrier:
                print('conexion carrier: ' + str(carrier) + ' conexion: ' + str(conexion) + ' asbr: ' + str(asbrCarrier))

                # inicializo los diccionarios para los ASBR que voy a trabajar
                if asbrCarrier not in returnDicAsbrPeers:
                    returnDicAsbrPeers[asbrCarrier] = []
                #if asbrCarrier not in returnDicAsbrPeers:
                #    returnDicAsbrPeers[asbrCarrier] = []
                if asbrCarrier not in returnDicAsbrOrigenes:
                    returnDicAsbrOrigenes[asbrCarrier] = []

                returnDicAsbrPeers[asbrCarrier].append(carrier)
                #print(str(carrier) + ' -> ' + str(asbrCarrier))
                asbrCarrierPrevio = asbrCarrier

        # agrego al returnDicAsbrOrigenes asbr, los mismos los levanto de paramdiccionarioOrigenes con el peerIxp
        origenAsbr_old = returnDicAsbrOrigenes[asbrCarrier]
        origenAsbr = list( set(origenAsbr_old) | set(paramdiccionarioOrigenes[carrier]) )
        returnDicAsbrOrigenes[asbrCarrier] = origenAsbr

    # genero los archivos de salida
    diccionarioAsbrPeersJson = paramResultadosDir + '/diccionarioAsbrPeersCarriers.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrPeersJson, 'w') as archivoDiccionarioAsbrPeersJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrPeers, archivoDiccionarioAsbrPeersJson)

    diccionarioAsbrOrigenesJson = paramResultadosDir + '/diccionarioAsbrOrigenesCarriers.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrOrigenesJson, 'w') as archivoDiccionarioAsbrOrigenesJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrOrigenes, archivoDiccionarioAsbrOrigenesJson)

    asbrTotales = paramResultadosDir + '/asbrTotalesCarriers.txt'
    with open(asbrTotales, 'w') as archivoAsbrTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoAsbrTotales.write(str(returnAsbrCarriers))

    peersNoAsignadosTotales = paramResultadosDir + '/asbrPeersNoAsignadosCarriers.txt'
    with open(peersNoAsignadosTotales, 'w') as archivoPeersNoAsignadosTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoPeersNoAsignadosTotales.write(str(returnPeersNoAsignados) + ';' + str(len(returnPeersNoAsignados)))

    peersAsignadosTotales = paramResultadosDir + '/asbrPeersAsignadosCarriers.txt'
    with open(peersAsignadosTotales, 'w') as archivoPeersAsignadosTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoPeersAsignadosTotales.write(str(returnPeersAsignados) + ';' + str(len(returnPeersAsignados)))


    #return returnDicAsbrCarriers
    return returnDicAsbrPeers, returnDicAsbrOrigenes, returnAsbrCarriers, returnPeersNoAsignados, returnPeersAsignados



def asignoAsbrCarriers(paramdiccionarioOrigenes, paramPeersTotales, paramResultadosDir, paramCantidadAsbr, paramDiccionarioCarriers):
    # Asigna los peers a los ASBRs en funcion, los peers pertenecientes a un asbr se asignan al mismo asbr 
    # Analizo la salida del metodo analizoArchivo, con lo cual como entrada estan la salida de este y un directorio donde esta la asignacion de los peers al asbr
    # devuelvo
    #   - un diccionario con los peers por cada asbr (clave = asbr, valor = peers por asbr)
    #   - un diccionario con los origenes por cada asbr (clave = asbr, valor = origenes por asbr)
    #   - una lista con todos los asbr
    #   - una lista con los peers sin asignar

    print('comienzo asignoAsbrCarriers')

    # inicializo el numero de asbr
    #asbr = 5

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Peers del mismo
    returnDicAsbrPeers = dict()

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Origen que se aprenden por el mismo
    returnDicAsbrOrigenes = dict()

    # inicializo lista con cuales son los asbrs
    returnAsbrTotales = []

    # inicializo la lista con los peers que faltan asignar
    returnPeersNoAsignados = []

    # inicializo la lista con los peers asignados
    returnPeersAsignados = []

    # levanto el diccionario de los ix
    with open(paramDiccionarioCarriers, "r") as archivoDicCarriers:
        diccionarioCarriers = json.load(archivoDicCarriers)


    for keyCarriers, valueListCarriersPeers in diccionarioCarriers.items():
        interseccionCarriersPeers = list(set(paramPeersTotales)&set(valueListCarriersPeers))

        returnPeersAsignados = list ( set(returnPeersAsignados) | set(interseccionCarriersPeers) )

        # eligo un asbr
        asbr = eligoNumero(paramCantidadAsbr)

        # inicializo los diccionarios para los ASBR que voy a trabajar
        if asbr not in returnDicAsbrPeers:
            returnDicAsbrPeers[asbr] = []
        if asbr not in returnDicAsbrOrigenes:
            returnDicAsbrOrigenes[asbr] = []

        for peerCarriers in interseccionCarriersPeers:
            # agrego el el peer al diccionario returnDicAsbrPeers
            returnDicAsbrPeers[asbr].append(peerCarriers)

            # agrego al returnDicAsbrOrigenes asbr, los mismos los levanto de paramdiccionarioOrigenes con el peerIxp
            origenAsbr_old = returnDicAsbrOrigenes[asbr]
            origenAsbr = list( set(origenAsbr_old) | set(paramdiccionarioOrigenes[peerCarriers]) )
            returnDicAsbrOrigenes[asbr] = origenAsbr

        # cargo los asbr en returnAsbrTotales
        if asbr not in returnAsbrTotales:
            returnAsbrTotales.append(asbr)

        '''
        # una ves que asigne a un mismo asbr todos los peers de un ixp paso a otro
        asbr = asbr + 1
        if asbr > paramCantidadAsbr:
            asbr = 0
        '''

    # me quedo con los peers no asignados
    returnPeersNoAsignados = list( set(paramPeersTotales) - set(returnPeersAsignados) )

    # genero los archivos de salida
    diccionarioAsbrPeersJson = paramResultadosDir + '/diccionarioAsbrPeersCarriers.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrPeersJson, 'w') as archivoDiccionarioAsbrPeersJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrPeers, archivoDiccionarioAsbrPeersJson)

    diccionarioAsbrOrigenesJson = paramResultadosDir + '/diccionarioAsbrOrigenesCarriers.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrOrigenesJson, 'w') as archivoDiccionarioAsbrOrigenesJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrOrigenes, archivoDiccionarioAsbrOrigenesJson)

    asbrTotales = paramResultadosDir + '/asbrTotalesCarriers.txt'
    with open(asbrTotales, 'w') as archivoAsbrTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoAsbrTotales.write(str(returnAsbrTotales))

    peersNoAsignadosTotales = paramResultadosDir + '/asbrPeersNoAsignadosCarriers.txt'
    with open(peersNoAsignadosTotales, 'w') as archivoPeersNoAsignadosTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoPeersNoAsignadosTotales.write(str(returnPeersNoAsignados) + ';' + str(len(returnPeersNoAsignados)))

    peersAsignadosTotales = paramResultadosDir + '/asbrPeersAsignadosCarriers.txt'
    with open(peersAsignadosTotales, 'w') as archivoPeersAsignadosTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoPeersAsignadosTotales.write(str(returnPeersAsignados) + ';' + str(len(returnPeersAsignados)))

    print('fin asignoAsbrCarriers')

    return returnDicAsbrPeers, returnDicAsbrOrigenes, returnAsbrTotales, returnPeersNoAsignados, returnPeersAsignados


def asignoAsbrDefault(paramDiccionarioOrigenes, paramPeers, paramResultadosDir, paramCantidadAsbr, paramRedundancia):
    # Asigna los peers a los ASBR que no han sido asignados aun
    # Para la asignacion se ordena en funcion de los ASBR que tengan mas origenes y los asigna
    # entradas
    #   - paramDiccionarioOrigenes: diccionario con los origenes en función
    #   - paramPeers: lista con todos los peers
    #   - paramResultadosPeersDir: directorio donde se dejan los archivos de salida
    #   - paramCantidadAsbr: cantidad de ASBRs de la red a simular
    #   - paramReundancia: con un entero reviso si le asigno los peers a mas de un asbr
    # devuelvo
    #   - un diccionario con los peers por cada asbr (clave = asbr, valor = peers por asbr)
    #   - un diccionario con los origenes por cada asbr (clave = asbr, valor = origenes por asbr)
    #   - una lista con todos los asbr

    print('comienzo asignoAsbrDefault')

    # inicializo el numero de asbr
    #asbr = 0
    #asbr = 5

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Peers del mismo
    returnDicAsbrPeers = dict()

    # inicializo diccionario el cual tiene como clave el ASBR y valores los AS Origen que se aprenden por el mismo
    returnDicAsbrOrigenes = dict()

    # inicializo lista con cuales son los asbrs
    returnAsbrTotales = []

    # genero un diccionario con todos los origenes ordenados por peer ordenados por cantidad
    sortedDiccionarioOrigenes = dict(sorted(paramDiccionarioOrigenes.items(), key=lambda x: len(x[1]), reverse=True))

    # recorro el diccionario ordenado y voy asignando los peers a los asbr
    for keyPeer, valueListOrigen in sortedDiccionarioOrigenes.items():

        # elijo el asbr
        asbr = eligoNumero(paramCantidadAsbr)

        # verifico si el el peer indicado en keyPeer falta asignar
        if keyPeer in paramPeers:
            # ingreso a la lista de asbr el asbr en caso de no estar
            if asbr not in returnAsbrTotales:
                returnAsbrTotales.append(asbr)
                
            # inicializo los diccionarios para los ASBR que voy a trabajar
            if asbr not in returnDicAsbrPeers:
                returnDicAsbrPeers[asbr] = []
            if asbr not in returnDicAsbrOrigenes:
                returnDicAsbrOrigenes[asbr] = []
            
            returnDicAsbrPeers[asbr].append(keyPeer)
            #returnDicAsbrOrigenes[asbr].append(valueListOrigen)
            origenAsbr_old = returnDicAsbrOrigenes[asbr]

            #print('asbr_old')
            #print(origenAsbr_old)
            #print('valueListOrigen')
            #print(valueListOrigen)

            origenAsbr = list( set(origenAsbr_old) | set(valueListOrigen) )
            returnDicAsbrOrigenes[asbr] = origenAsbr

            '''
            if paramRedundancia != 0:
                
                for redundanciaJ in range(paramRedundancia):
                    asbrBackup = asbr + redundanciaJ + 1

                    print('------------- asbr -------------')
                    print(asbr)
                    print('------------- asbrBkp -------------')
                    print(asbrBackup)

                    # si con el bkp supero la cantidad de asbr lo inicializo
                    if asbrBackup > paramCantidadAsbr:
                        asbrBackup = paramCantidadAsbr - 1
                        print('entro al if y dejo asbrBackup en')
                        print(asbrBackup)
                    
                    if asbrBackup not in returnDicAsbrPeers:
                        returnDicAsbrPeers[asbrBackup] = []
                    if asbrBackup not in returnDicAsbrOrigenes:
                        returnDicAsbrOrigenes[asbrBackup] = []
                    
                    returnDicAsbrPeers[asbrBackup].append(keyPeer)

                    origenAsbr_old = returnDicAsbrOrigenes[asbr]
                    #print('asbr_old')
                    #print(origenAsbr_old)
                    #print('valueListOrigen')
                    #print(valueListOrigen)
                    origenAsbr = list( set(origenAsbr_old) | set(valueListOrigen) )
                    returnDicAsbrOrigenes[asbrBackup] = origenAsbr
            '''
        '''
        # incremento la cantidad de los asbr
        asbr = asbr + 1
        if asbr > paramCantidadAsbr:
            asbr = 0
        '''

    # genero los archivos de salida
    diccionarioAsbrPeersJson = paramResultadosDir + '/diccionarioAsbrPeersDefault.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrPeersJson, 'w') as archivoDiccionarioAsbrPeersJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrPeers, archivoDiccionarioAsbrPeersJson)

    diccionarioAsbrOrigenesJson = paramResultadosDir + '/diccionarioAsbrOrigenesDefault.json'
    # Abrir el archivo en modo escritura
    with open(diccionarioAsbrOrigenesJson, 'w') as archivoDiccionarioAsbrOrigenesJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(returnDicAsbrOrigenes, archivoDiccionarioAsbrOrigenesJson)

    asbrTotales = paramResultadosDir + '/asbrTotalesDefault.txt'
    with open(asbrTotales, 'w') as archivoAsbrTotales:
        # Escribir el diccionario en el archivo en formato JSON
        archivoAsbrTotales.write(str(returnAsbrTotales))

    print('fin asignoAsbrDefault')

    return returnDicAsbrPeers, returnDicAsbrOrigenes, returnAsbrTotales



def calculoClases(paramdiccionarioOrigenes, paramOrigenesTotales, paramAsbrTotales, paramResultadosDir):
    # Calcula las clases en función de los Origenes y del diccionario con todos los origenes en funcion de los Asbr
    # devuelvo
    #   - un diccionario con los peers por cada asbr (clave = asbr, valor = peers por asbr)
    #   - un diccionario con los origenes por cada asbr (clave = asbr, valor = origenes por asbr)
    #   - una lista con todos los asbr

    print('comienzo calculoClases')

    # diccionario donde la clave son los origenes y los valores las clases
    clasesOrigenDiccionario = dict()
    # Lista con todas las clases
    clasesList = []
    # diccionario donde la clave es la clase y el valor el origen
    clasesClaseDiccionario = dict()

    # recorro todos los posibles origenes
    for origen in paramOrigenesTotales:
        clase = ''
        # para cada origen recorro los asbr y verfico si en el diccionario origenes esta el Origen correspondiente
        for asbr in paramAsbrTotales:
            try:
                if origen in paramdiccionarioOrigenes[asbr]:
                    clase = clase + str(asbr) + '_'
            except KeyError:
                print('no existe en paramdiccionarioOrigenes para el asbr: ' + str(asbr))
        if clase not in clasesList:
            clasesList.append(clase)
        
        clasesOrigenDiccionario[origen] = clase
        #salidaClaseOrigen = clase + ':' + origen

    # genero los archivos de salida
    clasesOrigenDiccionarioJson = paramResultadosDir + '/clasesOrigenDiccionario.json'

    # Abrir el archivo en modo escritura
    with open(clasesOrigenDiccionarioJson, 'w') as archivoDiccionarioClasesOrigenJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(clasesOrigenDiccionario, archivoDiccionarioClasesOrigenJson)



    salidaResumenClases = str(len(clasesList)) + ':' + str(clasesList)
    #print('salidaResumenClases')
    #print(salidaResumenClases)
    resumenClases = paramResultadosDir + '/resumenClases.txt'
    archivoResumenClases = open(resumenClases, 'w')
    archivoResumenClases.write(salidaResumenClases)

    salida = paramResultadosDir + '/clasesSalida.txt'
    archivoSalida = open(salida, 'w')


    #test = paramResultadosDir + '/test.txt'
    #archivoTest = open(test, 'w')

    # recorro las clases y armo un diccionario donde la clave es la clase y el valor son los origenes
    for claseI in clasesList:
        for origen in paramOrigenesTotales:
            #print('clasesOrigenDiccionario[origen]')
            #print(clasesOrigenDiccionario[origen])
            '''
            archivoTest.write('clasesOrigenDiccionario[origen]: ')
            archivoTest.write(clasesOrigenDiccionario[origen])
            archivoTest.write('\r\n')
            archivoTest.write('claseI: ')
            archivoTest.write(claseI)
            archivoTest.write('\r\n')
            archivoTest.write('--------------------\r\n')
            '''
            
            if claseI == clasesOrigenDiccionario[origen]:
                #print('entro al if')
                #print('claseI :' + claseI)
                if clasesClaseDiccionario.get(claseI) is not None:
                    clasesClaseDiccionario[claseI].append(origen)
                else:
                    clasesClaseDiccionario[claseI] = [origen]


        salidaClaseClase = claseI + ';' + str(clasesClaseDiccionario[claseI]) + ';' + str(len(clasesClaseDiccionario[claseI])) + '\r\n'
        archivoSalida.write(salidaClaseClase)

    # genero los archivos de salida
    clasesClaseDiccionarioJson = paramResultadosDir + '/clasesClaseDiccionario.json'

    # Abrir el archivo en modo escritura
    with open(clasesClaseDiccionarioJson, 'w') as archivoDiccionarioClasesClaseJson:
        # Escribir el diccionario en el archivo en formato JSON
        json.dump(clasesClaseDiccionario, archivoDiccionarioClasesClaseJson)

    print('fin calculoClases')


##### Main

cantidadCorridas = 100

### corrida Antel
mainArchivo = 'bgpDumpAspath_data_20220329_1600_rrc24'
mainAsn = 6057
diccionariosCarriers = 'carriers_6057.json'
diccionariosIxp = 'ix_6057.json'
mainCantidadSitios = 16
#mainCantidadAsbr = 80
'''
### corrida Telus
#mainArchivo = 'bgpDumpAspath_data_20230501_0000_rrc24'
#mainAsn = 852
#diccionariosCarriers = 'carriers_852.json'
#diccionariosIxp = 'ix_852.json'
#mainCantidadSitios = 4
###
'''

print('comienzo analisis del asn:' + str(mainAsn) + ' archivo:' + mainArchivo +  '\r\n')

# creo la carpeta resultados/6057 dentro del directorio de trabajo
mainCarpeta = 'resultados/' + str(mainAsn)
mainDirResultados = creoCarpetaResultados(mainCarpeta)
# Busco los peers y armo el archivo (si corro buscoPeers me quedo con todos)
buscoPeers(mainAsn, mainArchivo)
# Busco los peers y armo el archivo (si corro buscoPeersMenor y buscoMenoresBuscoPeers me quedo solo con los ASN mas proximos al AS que estoy estudiando)
#buscoPeersMenor(mainAsn, mainArchivo)
#buscoMenoresBuscoPeers(mainAsn, mainArchivo)

# analizo el archivo y genero el diccionario de los origenes por peer y las listas de peers y origenes
mainDicOrigenes, mainPeersTotales, mainOrigenesTotales = analizoArchivo(mainArchivo, mainAsn, mainDirResultados)



for corrida in range(cantidadCorridas):

    hora_actual = datetime.datetime.now().time()
    print("La corrida " + str(corrida) + ' comienza a ', hora_actual)


    mainCarpetaInstancia = 'resultados/' + str(mainAsn) + '/' + str(corrida)
    mainDirResultados = creoCarpetaResultados(mainCarpetaInstancia)
    print('comienzo la corrida, los resultados quedaran en ' + mainDirResultados)

    mainCantidadAsbr = calculoAsbr(mainCantidadSitios, mainDirResultados)

    ## analizo el archivo y genero el diccionario de los origenes por peer y las listas de peers y origenes
    #mainDicOrigenes, mainPeersTotales, mainOrigenesTotales = analizoArchivo(mainArchivo, mainAsn, mainDirResultados)

    # asigno a los ASBRs a los diferentes peers con eso armo un diccionario con los peers por asbr y otro con los origenes por asbr, ademas devuelvo la cantidad de asbrs totales
    #mainDicAsbrPeers, mainDicAsbrOrigenes, mainAsbrTotales = asignoAsbrArchivo(mainDicOrigenes, mainPeersTotales, mainDirResultados)

    # asigno a los ASBRs a los peers pertenecientes a los carriers, 
    #mainDicAsbrPeersCarriers, mainDicAsbrOrigenesCarriers, mainAsbrTotalesCarriers, mainPeersNoAsignadosCarriers, mainPeersAsignadosCarriers = asignoAsbrCarriers(mainDicOrigenes, mainPeersTotales, mainDirResultados, mainCantidadAsbr, diccionariosCarriers)
    mainDicAsbrPeersCarriers, mainDicAsbrOrigenesCarriers, mainAsbrTotalesCarriers, mainPeersNoAsignadosCarriers, mainPeersAsignadosCarriers = elijoCarriers(mainDicOrigenes, mainPeersTotales, mainDirResultados, mainCantidadAsbr, diccionariosCarriers)

    # asigno a los ASBRs a los peers pertenecientes a los ixp, 
    mainDicAsbrPeersIxp, mainDicAsbrOrigenesIxp, mainAsbrTotalesIxp, mainPeersNoAsignadosIxp, mainPeersAsignadosIxp = asignoAsbrIxp(mainDicOrigenes, mainPeersTotales, mainDirResultados, mainCantidadAsbr, diccionariosIxp)

    # veo los peers ya asignados
    peersAsignados = list ( set(mainPeersAsignadosCarriers) | set(mainPeersAsignadosIxp) )
    peersPorAsignar = list ( set(mainPeersTotales) - set(peersAsignados) )

    #print('peers por asignar: ' + str(peersPorAsignar))

    # asigno a los ASBRs a los diferentes peers con eso armo un diccionario con los peers por asbr y otro con los origenes por asbr, ademas devuelvo la cantidad de asbrs totales
    mainDicAsbrPeersDefault, mainDicAsbrOrigenesDefault, mainAsbrTotalesDefault = asignoAsbrDefault(mainDicOrigenes, peersPorAsignar, mainDirResultados, mainCantidadAsbr, 2)

    # realizo el merge entre los diccionarios dicAsbrOrigenes
    #diccionariosMerge = [mainDicAsbrPeersIxp, mainDicAsbrPeersDefault]
    # test
    #print('mainDicAsbrOrigenesCarriers[5]: ' + str(len(mainDicAsbrOrigenesCarriers[5])))
    #print('mainDicAsbrOrigenesIxp[5]' + str(len(mainDicAsbrOrigenesIxp[5])))
    #print('mainDicAsbrOrigenesDefault[5]: ' + str(len(mainDicAsbrOrigenesDefault[5])))

    diccionariosMerge = [mainDicAsbrOrigenesCarriers, mainDicAsbrOrigenesIxp, mainDicAsbrOrigenesDefault]
    mainDicAsbrOrigenesMerge = mergeDicAsbrOrigenes(diccionariosMerge, mainDirResultados)

    # armo la lista de los de los asbr
    mainAsbrTotales = armoListaAsbr(mainCantidadAsbr)

    # calculo las clases
    #calculoClases(mainDicAsbrOrigenes, mainOrigenesTotales, mainAsbrTotales, mainDirResultados)
    calculoClases(mainDicAsbrOrigenesMerge, mainOrigenesTotales, mainAsbrTotales, mainDirResultados)

