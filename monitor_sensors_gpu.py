from numba import cuda
import numpy as np
import time

# Definir la duración de ejecución (en segundos)
execution_time = 10

# Función que se ejecutará en la GPU
@cuda.jit
def monitor_sensors_gpu(temperatures, humidities):
    idx = cuda.grid(1)
    if idx < temperatures.size:
        temperatures[idx] = 25.0 + idx
        humidities[idx] = 50.0 + idx

def main():
    num_sensors = 3
    temperatures = np.zeros(num_sensors, dtype=np.float32)
    humidities = np.zeros(num_sensors, dtype=np.float32)

    # Copiar datos a la memoria de la GPU
    temperatures_gpu = cuda.to_device(temperatures)
    humidities_gpu = cuda.to_device(humidities)

    start_time = time.time()
    while time.time() - start_time < execution_time:
        # Llamar a la función de la GPU
        monitor_sensors_gpu[num_sensors, 1](temperatures_gpu, humidities_gpu)

        # Copiar resultados de vuelta a la CPU
        temperatures_gpu.copy_to_host(temperatures)
        humidities_gpu.copy_to_host(humidities)

        for i in range(num_sensors):
            print(f"Sensor {i} - Temp: {temperatures[i]}, Hum: {humidities[i]}")
        time.sleep(1)

if __name__ == "__main__":
    main()
