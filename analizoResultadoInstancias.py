import heapq
import numpy as np


def isNumeric(s):
    #defino funcion para saber si es un entero en nunero a procesar
    try:
        int(s)
        return True
    except ValueError:
        return False

def analizoResultados(paramAsn, paramResultadosDir, paramInstancias):

        print('comienzo analisoResultados')
        cantidClasesdict = dict()
        distribucionClasesDict = dict()

        for instancia in range(paramInstancias):
            # analizo la cantidad de clases de cada instancia
            resumenClases = paramResultadosDir + '/' + str(instancia) + '/resumenClases.txt'
            with open(resumenClases, 'r') as archivoresumenClases:
                for j in archivoresumenClases:
                    cantidadClasesArray = j.split(':')
                    cantidadClases = cantidadClasesArray[0]
                    if isNumeric(cantidadClases):
                        cantidClasesdict[instancia] = int(cantidadClases)
            
            # analizo el porcentaje de origenes cubiertos por las que tienen las diez que mas tienen
            distribucionClasesInstanciaDict = dict()
            clasesSalida = paramResultadosDir + '/' + str(instancia) + '/clasesSalida.txt'
            with open(clasesSalida, 'r') as archivorclasesSalida:
                for i in archivorclasesSalida:
                    clasesSalidaArray = i.split(';')
                    cantidadOrigenes = clasesSalidaArray[2]
                    clase = clasesSalidaArray[0]
                    if isNumeric(cantidadOrigenes):
                        distribucionClasesInstanciaDict[clase] = int(cantidadOrigenes)
                
                mayores = heapq.nlargest(10, distribucionClasesInstanciaDict.values())
                totalOrigenes = sum(distribucionClasesInstanciaDict.values())
                acumuladoOrigenes = 0
                for z in mayores:
                    acumuladoOrigenes = acumuladoOrigenes + 100*z/totalOrigenes
                distribucionClasesDict[instancia] = acumuladoOrigenes


                #print(str(mayores))




        print('--------------- Cantidad de clases ---------------')
        print(str(cantidClasesdict))
        #print(list(cantidClasesdict.values()))
        # Obtener el promedio
        promedio = sum(cantidClasesdict.values()) / len(cantidClasesdict)
        print("El promedio es:", promedio)

        # Obtener el valor máximo
        maximo = max(cantidClasesdict.values())
        print("El valor máximo es:", maximo)

        # Obtener el valor mínimo
        minimo = min(cantidClasesdict.values())
        print("El valor mínimo es:", minimo)

        # Obtener la desviacion estandar
        st_dev = np.std(list(cantidClasesdict.values()))
        print("La desviacion estandar es: ", st_dev)

        # Error del 10% de la muestra
        err10 = 0.1 * promedio
        print("Error del 10%", err10)

        # Intervalo de confianza al 10%
        intervalo_inferior_10 = promedio - err10
        intervalo_superior_10 = promedio + err10
        print("limite inferior al 10%", intervalo_inferior_10)
        print("limite superior al 10%", intervalo_superior_10)

        # Cantidad de muestras necesarias al 10%
        Znc10 = 1.645
        n10 = ((Znc10 * st_dev)/err10) ** 2
        print("Canntidad de muestras al 10%: ", n10)
        

        # Error del 5% de la muestra
        err5 = 0.05 * promedio
        print("Error del 5%", err5)

        # Intervalo de confianza al 5%
        intervalo_inferior_5 = promedio - err5
        intervalo_superior_5 = promedio + err5
        print("limite inferior al 5%", intervalo_inferior_5)
        print("limite superior al 5%", intervalo_superior_5)

        # Cantidad de muestras necesarias al 5%
        Znc5 = 1.960
        n5 = ((Znc5 * st_dev)/err5) ** 2
        print("Canntidad de muestras al 5%: ", n5)


        print('--------------- Acumulado 10 primeras clases ---------------')
        print(str(distribucionClasesDict))
        # Obtener el promedio
        promedio = sum(distribucionClasesDict.values()) / len(distribucionClasesDict)
        print("El promedio es:", promedio)

        # Obtener el valor máximo
        maximo = max(distribucionClasesDict.values())
        print("El valor máximo es:", maximo)

        # Obtener el valor mínimo
        minimo = min(distribucionClasesDict.values())
        print("El valor mínimo es:", minimo)

        # Obtener la desviacion estandar
        st_dev_distClases = np.std(list(distribucionClasesDict.values()))
        print("La desviacion estandar es: ", st_dev_distClases)

        # Error del 10% de la muestra
        err_distClases_10 = 0.1 * promedio
        print("Error del 10%", err_distClases_10)

        # Intervalo de confianza al 10%
        intervalo_inferior_distClases_10 = promedio - err_distClases_10
        intervalo_superior_distClases_10 = promedio + err_distClases_10
        print("limite inferior al 10%", intervalo_inferior_distClases_10)
        print("limite superior al 10%", intervalo_superior_distClases_10)

        # Cantidad de muestras necesarias al 10%
        Znc10 = 1.645
        n10 = ((Znc10 * st_dev_distClases)/err_distClases_10) ** 2
        print("Canntidad de muestras al 10%: ", n10)
        

        # Error del 5% de la muestra
        err_distClases_5 = 0.05 * promedio
        print("Error del 5%", err_distClases_5)

        # Intervalo de confianza al 5%
        intervalo_inferior_distClases_5 = promedio - err_distClases_5
        intervalo_superior_distClases_5 = promedio + err_distClases_5
        print("limite inferior al 5%", intervalo_inferior_distClases_5)
        print("limite superior al 5%", intervalo_superior_distClases_5)

        # Cantidad de muestras necesarias al 5%
        Znc5 = 1.960
        n5 = ((Znc5 * st_dev_distClases)/err_distClases_5) ** 2
        print("Canntidad de muestras al 5%: ", n5)




mainAsn = 6057
mainCarpeta = 'resultados/' + str(mainAsn)
#mainCarpeta = 'resultados/' + str(mainAsn) + '_20230824'
#mainCarpeta = 'resultados/' + str(mainAsn) + '_500'
mainInstancias = 124

analizoResultados(mainAsn, mainCarpeta, mainInstancias)






