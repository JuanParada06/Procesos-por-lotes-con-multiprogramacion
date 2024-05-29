import os
import time
import random
import msvcrt

lista_lotes = []
lotes = []
proc_terminados = []
pausa = False
numeros_generados = []
interrumpidos = []
numeros1 = []
numeros2 = []

class Proceso:
    def __init__(self):
        self.operacion = ""
        self.numero1 = 0
        self.numero2 = 0
        self.tiempo_maximo = 0
        self.id_programa = 0
        self.resultado_operacion = 0
        self.cadena_operacion = ""
        self.porcentaje = 0
        self.BanderaError = False
        self.tiempoRestante = 0
        self.tiempofaltante = 0

def funcionOperacion(operador, proceso):
    proceso.numero1 = random.randint(1, 100)
    proceso.numero2 = random.randint(1, 100)
    if operador == "/":
        while proceso.numero2 == 0:
            proceso.numero2 = random.randint(1, 100)
    proceso.cadena_operacion = '{}{}{}'.format(proceso.numero1, operador, proceso.numero2)
    numeros_generados.append((operador, proceso.numero1, operador, proceso.numero2))
    numeros1.append(proceso.numero1)
    numeros2.append(proceso.numero2)

def porcentaje(operador, proceso):
    proceso.numero1 = random.randint(1, 100)
    proceso.numero2 = random.randint(1, 100)
    while proceso.numero2 == 0:
        proceso.numero2 = random.randint(1, 100)
    proceso.porcentaje = (proceso.numero1 / proceso.numero2) * 10
    numeros_generados.append((operador, proceso.numero1, operador, proceso.numero2))
    numeros1.append(proceso.numero1)
    numeros2.append(proceso.numero2)

def main():
    global pausa
    while True:
        dato = input("Ingrese la cantidad de procesos a realizar: ")
        if dato.isdigit():
            cantidad = int(dato)
            break
        else:
            print("INGRESA UN DIGITO")

    for _ in range(cantidad):
        proceso = Proceso()

        print('\n---------Proceso {}---------'.format(len(lotes) + 1))

        while True:
            opcion = random.randint(1, 5)
            if opcion == 1:
                proceso.operacion = '+'
            elif opcion == 2:
                proceso.operacion = '-'
            elif opcion == 3:
                proceso.operacion = '*'
            elif opcion == 4:
                proceso.operacion = '/'
            elif opcion == 5:
                proceso.operacion = '%'

            if proceso.operacion in ['+', '-', '*', '/', '%']:
                if proceso.operacion == '%':
                    a = random.randint(1, 2)
                    if a == 2:
                        porcentaje(proceso.operacion, proceso)
                        proceso.resultado_operacion = proceso.porcentaje
                        break
                    else:
                        funcionOperacion(proceso.operacion, proceso)
                        proceso.resultado_operacion = eval(proceso.cadena_operacion)
                        break
                else:
                    funcionOperacion(proceso.operacion, proceso)
                    proceso.resultado_operacion = eval(proceso.cadena_operacion)
                    break
            else:
                print("Operacion invalida")

        while True:
            proceso.tiempo_maximo = random.randint(6,18)
            if proceso.tiempo_maximo > 0:
                break
            else:
                print("El tiempo debe ser mayor a 0, ingréselo de nuevo")

        while True:
            proceso.id_programa = random.randint(1, 10)

            if proceso.id_programa in [p.id_programa for p in lotes]:
                print("El ID ingresado ya ha sido utilizado")
            else:
                lotes.append(proceso)
                break

    for i in range(0, len(lotes), 5):
        lista_lotes.append(lotes[i:i + 5])

    contador_global = 0

    for i, lote in enumerate(lista_lotes):
        num_proc = len(lote)
        cont = 1
        while cont <= num_proc: 
            if lote:
                proceso = lote[0]
            proceso.tiempoRestante = proceso.tiempo_maximo
            proceso.tiempoRestante -=proceso.tiempofaltante
            while proceso.tiempoRestante >= 0:
                os.system("cls" if os.name == "nt" else "clear")
                if msvcrt.kbhit():
                    tecla = msvcrt.getch().decode()
                    if tecla == 'p':
                        pausa = True
                    if tecla == 'e':
                        proceso.BanderaError = True
                        proceso.resultado_operacion = "ERROR"
                        proceso.tiempoRestante = 0
                    if tecla == 'i':
                        proceso.tiempofaltante=proceso.tiempo_maximo - proceso.tiempoRestante 
                        prosc = proceso
                        lote.append(prosc)
                        lote.remove(proceso)
                        break

                print('----Cantidad de lotes pendientes---')
                print(len(lista_lotes) - (i + 1))

                print('---------Lote en Ejecución---------')
                for proces in lote[1:]:
                    if proces.tiempoRestante:
                        proces.tiempoRestante=proces.tiempo_maximo
                    print('ID: {}, TM: {}, TR: {}'.format(proces.id_programa,proces.tiempo_maximo,(proces.tiempo_maximo-proces.tiempofaltante)), end=' |')

                print('\n-------Proceso en Ejecución--------')
                if proceso.tiempoRestante == 0:
                    print("Operacion: \nTME:  \nId:  \nTiempo trascurrido: \nTiempo restante: ")
                else: 
                    print("Operacion: {} \nTME: {} \nId: {} \nTiempo trascurrido: {} \nTiempo restante: {}".format(proceso.operacion, proceso.tiempo_maximo, proceso.id_programa,contador_global, proceso.tiempoRestante))

                if proceso.tiempoRestante == 0 and proceso.BanderaError == False:
                    proc_terminados.append([proceso.id_programa, proceso.numero1,  proceso.operacion, proceso.numero2,proceso.resultado_operacion,  i + 1])
                elif proceso.BanderaError == True:
                    proceso.resultado_operacion = "ERROR"
                    proc_terminados.append([proceso.id_programa, proceso.numero1,  proceso.operacion, proceso.numero2,proceso.resultado_operacion, i + 1])
                
                if proceso.tiempoRestante == 0:
                    if lote:
                        lote.pop(0)
                    cont +=1

                print('--------Procesos Terminados--------')

                if proc_terminados:
                    for proces in proc_terminados:
                        print(f"id: {proces[0]} operacion: {proces[1]} {proces[2]} {proces[3]} Resultado = {proces[4]} Lote -> {proces[5]}")
        

                if pausa:
                    print("Presione 'c' para continuar.")
                    while pausa:
                        if msvcrt.kbhit():
                            tecla = msvcrt.getch().decode()
                            if tecla == 'c':
                                pausa = False
                                print("Programa reanudado.")
                                break
            
                proceso.tiempoRestante -= 1
                contador_global += 1
                time.sleep(1)

        




if __name__ == "__main__":
    os.system("cls")
    main()
