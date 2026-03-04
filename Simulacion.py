import simpy
import random
import statistics
import matplotlib.pyplot as plt


RANDOM_SEED = 42
RAM_CAPACITY = 100
CPU_CAPACITY = 1
CPU_INSTRUCTIONS = 3     
INTERVAL = 10            
TOTAL_PROCESSES = 25

def proceso(env, name, ram, cpu, tiempos):

    llegada = env.now
    
    memoria = random.randint(1, 10)
    yield ram.get(memoria)

    instrucciones = random.randint(1, 10)

    while instrucciones > 0:
        with cpu.request() as req:
            yield req
            
            ejecutar = min(CPU_INSTRUCTIONS, instrucciones)
            yield env.timeout(1)
            instrucciones -= ejecutar

        if instrucciones <= 0:
            break

        opcion = random.randint(1, 21)

        if opcion == 1:
            yield env.timeout(1)
        else:
            pass

    yield ram.put(memoria)

    salida = env.now
    tiempos.append(salida - llegada)


def generador_procesos(env, total, ram, cpu, tiempos):
    for i in range(total):
        yield env.timeout(random.expovariate(1.0 / INTERVAL))
        env.process(proceso(env, f"Proceso {i}", ram, cpu, tiempos))



def correr_simulacion(total_procesos):

    random.seed(RANDOM_SEED)

    env = simpy.Environment()
    ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
    cpu = simpy.Resource(env, capacity=CPU_CAPACITY)

    tiempos = []

    env.process(generador_procesos(env, total_procesos, ram, cpu, tiempos))
    env.run()

    promedio = statistics.mean(tiempos)
    desviacion = statistics.stdev(tiempos)

    return promedio, desviacion


if __name__ == "__main__":

    procesos_lista = [25, 50, 100, 150, 200]
    promedios = []

    for n in procesos_lista:
        promedio, desviacion = correr_simulacion(n)
        print(f"Procesos: {n}")
        print(f"Tiempo promedio: {promedio:.2f}")
        print(f"Desviación estándar: {desviacion:.2f}\n")
        promedios.append(promedio)

    # Gráfica
    plt.plot(procesos_lista, promedios)
    plt.xlabel("Número de procesos")
    plt.ylabel("Tiempo promedio en el sistema")
    plt.title("Procesos vs Tiempo promedio")
    plt.show()