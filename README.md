# procesoRmt

## Introduccion

En este repositorio se mantienden los siguientes codigos

procesoRmt.py: el cual tiene como objetivo procesar la información publica y modelar las clases
analizoResultadoInstancias.py: el cual toma la información generada por procesoRmt.py y generar estadisticas

## Estructura de los datos obtenidos y procesados

```bash
.
├── archivosAsbrPeers
│   └── asn_conectados__[asbr]_[fecha].txt
├── bgpDumpAspath_data_[fecha]_[hora]_[rrc]
├── carriers_[asn].json
├── ix_[asn].json
└── resultado
    └── [asn]
        ├── sorted_out_[asn]_bgpDumpAspath_[archivo a estudiar].txt
        ├── out_[asn]_bgpDumpAspath_[archivo a estudiar].txt
        ├── peersTotales.txt
        ├── diccionarioOrigenes.json
        ├── origenesTotales.txt
        └── [corrida]
           ├── cantidadAsbr.txt
           ├── diccionarioAsbrPeersCarriers.json
           ├── diccionarioAsbrOrigenesCarriers.json
           ├── asbrTotalesCarriers.txt
           ├── asbrPeersNoAsignadosCarriers.txt
           ├── asbrPeersAsignadosCarriers.txt
           ├── diccionarioAsbrPeersIxp.json
           ├── diccionarioAsbrOrigenesIxp.json
           ├── asbrTotalesIxp.txt
           ├── asbrPeersNoAsignadosIxp.txt
           ├── asbrPeersAsignadosIxp.txt
           ├── diccionarioAsbrPeersDefault.json
           ├── diccionarioAsbrOrigenesDefault.json
           ├── asbrTotalesDefault.txt
           ├── diccionarioOrigenesMerge.json
           ├── clasesOrigenDiccionario.json
           ├── clasesClaseDiccionario.json
           ├── resumenClases.txt
           └── clasesSalida.txt
```

## Codigo de procesoRmt.py

### buscoPeers

    - Objetivo: Procesar el archivo de ruteo publico buscando los peers del AS bajo estudio
    -- Entrada:
        --- Archivo con información de ruteo
        --- As bajo estudio
    -- Salida:
        --- Archivo sorted_out_[asn]_bgpDumpAspath_[archivo a estudiar].txt

### analizoArchivo

    - Analizo el archivo sorted_out generado en buscoPeers
    -- Entrada:
        --- Archivo sorted_out_[asn]_bgpDumpAspath_[archivo a estudiar].txt generado en buscoPeers
    -- Salida:
       --- un diccionario con los origenes por cada peer (clave = peer, valor = lista con los origenes por allí conocidos)
       --- una lista con todos los origenes
       --- una lista con todos los peers

### calculoAsbr

    - Objetivo: Estimar la cantidad de ASBR que tiene el AS bajo estudio a la cantidad de sitios vamos a multiplicarla de manera aleatoria por 1, 1.5 o 2
    -- Entrada:
        --- Cantidad de sitios del AS bajo estudio
    -- Devuelve:
        --- Cantidad de Asbr estimada

### elijoCarriers

    - Objetivo: Asignar los Carriers a diferentes ASBRs
    -- Entradas:
        --- Cantidad de ASBRs (obtenida de calculoAsbr)
        --- Archivo con los carriers
    -- Devuelve
        --- Diccionario donde la llave es el asbr y las claves los ASN de los carriers

### asignoAsbrIxp

    - Objetivo: Asigna los peers pertenecientes a un IXP a los ASBRs
    -- Entradas:
        --- Cantidad de ASBRs (obtenida de calculoAsbr)
        --- Archivo con los carriers
    -- Devuelve
        --- Diccionario donde la llave es el asbr y las claves los ASN de los Peers pertenecientes a un IXP

### asignoAsbrDefault

    - Objetivo: Asigna los peers a los ASBR que no han sido asignados aun, para la asignacion se ordena en funcion de los ASBR que tengan mas origenes y los asigna
    -- Entradas:
        --- paramDiccionarioOrigenes: diccionario con los origenes
        --- paramPeers: lista con todos los peers
        --- paramResultadosPeersDir: directorio donde se dejan los archivos de salida
        --- paramCantidadAsbr: cantidad de ASBRs de la red a simular
        --- paramReundancia: con un entero reviso si le asigno los peers a mas de un asbr
    Devuelve
        --- un diccionario con los peers por cada asbr (clave = asbr, valor = peers por asbr)
        --- un diccionario con los origenes por cada asbr (clave = asbr, valor = origenes por asbr)
        --- una lista con todos los asbr

### mergeDicAsbrOrigenes

    - Objetivo: Realizar un merge de los diccionarios obtenidos en asignoAsbrDefault, asignoAsbrIxp y elijoCarriers
    -- Entradas:
        --- Lista con los tres diccionarios
    -- Devuelve:
        --- Un único diccionario con los resultados de los tres

### armoListaAsbr

    - Objetivo: Obtener una lista con los ASBR
    -- Entradas:
        --- Cantidad de ASBR
    -- Devuelve:
        --- Lista con números de todos los ASBRs

### calculoClases

    - Objetivo: Calcula las clases en función de los Origenes y del diccionario con todos los origenes en funcion de los Asbr
    -- Entradas:
        --- Diccionario obtenido en mergeDicAsbrOrigenes
        --- Diccionario con todos los ASN Origen
        --- Diccionario con ASBRs Totales
    -- Devuelve
       --- Diccionario con los peers por cada asbr (clave = asbr, valor = peers por asbr)
       --- Diccionario con los origenes por cada asbr (clave = asbr, valor = origenes por asbr)
       --- Lista con todos los asbr