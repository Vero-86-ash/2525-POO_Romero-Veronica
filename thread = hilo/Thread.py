# Importa la biblioteca para trabajar con hilos (threads)
import threading
# Permite usar funciones de tiempo como sleep()
import time

# Función que simula una tarea ejecutada por un hilo
def tarea_hilo(identificador, delay):
    for i in range(5):  # Repite la tarea 5 veces
        print(f'Hilo {identificador}: Realizando tarea {i}')  # Muestra qué hilo y qué tarea se ejecuta
        time.sleep(delay)  # Espera un tiempo antes de continuar (simula trabajo)

# Crear 3 hilos, cada uno con diferente tiempo de espera
hilo1 = threading.Thread(target=tarea_hilo, args=(1, 1))    # Hilo 1: espera 1 segundo entre tareas
hilo2 = threading.Thread(target=tarea_hilo, args=(2, 0.8))  # Hilo 2: espera 0.8 segundos
hilo3 = threading.Thread(target=tarea_hilo, args=(3, 1.2))  # Hilo 3: espera 1.2 segundos

# Iniciar la ejecución de los 3 hilos
hilo1.start()
hilo2.start()
hilo3.start()

# Esperar a que todos los hilos terminen antes de continuar
hilo1.join()
hilo2.join()
hilo3.join()

# Mensaje final del programa principal
print('Programa principal: Todas las tareas han sido completadas.')


