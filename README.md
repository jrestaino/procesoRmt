
# Introduccion

En este repositorio se mantienden los siguientes codigos

procesoRmt.py: el cual tiene como objetivo procesar la información publica y modelar las clases
analizoResultadoInstancias.py: el cual toma la información generada por procesoRmt.py y generar estadisticas

# procesoRmt

## Configuración de la ejecución

Para la ejecución del script tiene que tener los Carriers que el mismo tiene en un archivo .json ***carriers_[asn].json***, los IXP a los cuales pertenece en un archivo .json ***ix_[asn].json***, un archivo con los datos de los datos de Ripe o RouteViews ***bgpDumpAspath_data_[fecha]_[hora]_[rrc]***, debe de tener ingresada la cantidad de Corridas en el parametro ***cantidadCorridas***, el AS que se debe de configurar en el parametro ***mainAsn*** y la cantidad de sitios en el parametro ***mainCantidadSitios*** 

### Archivos de entrada

Los nombres de los archivos deben de ser indicados en los siguientes parametros

mainArchivo = 'bgpDumpAspath_data_20220329_1600_rrc24'
diccionariosCarriers = 'carriers_6057.json'
diccionariosIxp = 'ix_6057.json'

Ejemplo de ***carriers_[asn].json***

En una misma línea

{"carriers": [6762, 12956, 2914, 1239, 174, 3356, 6461, 10429, 4230, 1299]}

Ejemplo de ***ix_[asn].json***

{"de-cix_NewYork": [42, 46, 112], "equinix_chicago": [20161, 30528, 30539], "qix_montreal": [25152, 1403, 14086, 14086], "qix_montreal": [398491, 398700, 398960, 399116, 400818], "torix": [42, 112, 376, 549, 803, 812, 819, 835, 852, 857, 1100, 1403, 1547, 1828, 2635, 2647, 2675, 2685, 3300, 3303, 3367, 3856, 4455, 4508, 5645, 5664, 5690, 5769, 6327, 6407, 6461, 6507, 6509, 6939, 7057, 7311, 7713, 7741, 7794, 7992, 8075, 10310, 10996, 11077, 11084, 11260, 11284, 11287, 11342, 11468, 11522, 11635, 11647, 11666, 400687]}

Ejemplo de bgpDumpAspath_data_[fecha]_[hora]_[rrc]

Este archivo debe de estar en la carpeta ***archivosBgpDump***

Estos archivos son un dump de los extraidos de ripe o routeviews realizado con bgpdump. Para disminuir el tiempo de ejecución es conveniente generar el bgpdump solo con las líneas de interes, que son aquellas que comienzan con AS-PATH y tienen el AS que queremos estudiar incluido. A modo de ejemplo

bgpdump data | grep ASPATH | grep 6057 > bgpDumpAspath_data_20230501_0000_rrc24

Si bien no se quiere agregar el AS a estudiar el tiempo de ejecuión no va a variar tanto y esta contemplado en el código tomar solo las líneas que lo contengan.

### Parametros a configurar en el python

cantidadCorridas = 100
mainAsn = 6057
mainCantidadSitios = 16

mainArchivo = 'bgpDumpAspath_data_20220329_1600_rrc24'
diccionariosCarriers = 'carriers_6057.json'
diccionariosIxp = 'ix_6057.json'

## Resultados

Como resultado de la ejecución se generan varios archivos, muchos de ellos con el fin de debug o analisis detallado. Los resultados estan en la carpeta **./resultados/[asn]** y los resultados de las corridas ejecutadas estará en **./resultados/[asn]/[corrida]** donde cada corrida se representa con un entero.

Dentro de cada corrida los archivos más relevantes son:

cantidadAsbr.txt: Muestra la cantidad de ASBRs estimada
resumenClases.txt: Indica la cantidad de clases y cuales son.
clasesSalida.txt: Muestra las clases y los ASNs origenes que estan dentro de ellas

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

# analizoResultadoInstancias.py

## Configuración de la ejecución

Para la configuración de este script hay que completar los parametros dentro de él, ***mainAsn*** y ***mainInstancias***. Con esto vamos a analizar todas las instancias ejecutadas y obtener números utiles para el procesamiento de la información, la cual será presentada en salida estandar del script luego de ejecutarlo.

mainAsn = 6057
mainInstancias = 124
