import multiprocessing as mp
import threading
import time

# Definir la duración de ejecución (en segundos)
execution_time = 13

# Crear un bloqueo (lock) para sincronización
lock = threading.Lock()

def monitor_sensor(sensor_id, stop_event, result_counter):
    start_time = time.time()
    while not stop_event.is_set():
        with lock:  # Sincronización para asegurar acceso exclusivo a la sección crítica
            # Simulación de lectura de datos de un sensor
            temperature = 25.0 + sensor_id
            humidity = 50.0 + sensor_id
            result_counter[sensor_id] += 1  # Incrementar el contador de resultados
            print(f"Sensor {sensor_id} - Temp: {temperature}, Hum: {humidity}")
        time.sleep(1)
        # Verificar si se ha excedido el tiempo de ejecución
        if time.time() - start_time > execution_time:
            stop_event.set()

if __name__ == "__main__":
    sensor_ids = [1, 2, 3]
    stop_event = mp.Event()

    # Ejemplo de Multiprocessing
    print("Multiprocessing Example")
    manager = mp.Manager()
    result_counter_mp = manager.dict({sid: 0 for sid in sensor_ids})
    processes = [mp.Process(target=monitor_sensor, args=(sid, stop_event, result_counter_mp)) for sid in sensor_ids]
    
    start_time_mp = time.time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    end_time_mp = time.time()
    
    print(f"Multiprocessing Execution Time: {end_time_mp - start_time_mp:.2f} seconds")
    for sid in sensor_ids:
        print(f"Sensor {sid} - Readings: {result_counter_mp[sid]}")

    stop_event.clear()  # Reiniciar el evento de detención

    # Ejemplo de Multithreading
    print("Multithreading Example")
    result_counter_th = {sid: 0 for sid in sensor_ids}
    threads = [threading.Thread(target=monitor_sensor, args=(sid, stop_event, result_counter_th)) for sid in sensor_ids]
    
    start_time_th = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time_th = time.time()
    
    print(f"Multithreading Execution Time: {end_time_th - start_time_th:.2f} seconds")
    for sid in sensor_ids:
        print(f"Sensor {sid} - Readings: {result_counter_th[sid]}")

    stop_event.clear()  # Reiniciar el evento de detención

    # Benchmarking
    def sequential_monitoring(sensor_ids, stop_event, result_counter):
        start_time = time.time()
        while not stop_event.is_set():
            for sensor_id in sensor_ids:
                with lock:  # Sincronización para asegurar acceso exclusivo a la sección crítica
                    temperature = 25.0 + sensor_id
                    humidity = 50.0 + sensor_id
                    result_counter[sensor_id] += 1  # Incrementar el contador de resultados
                    print(f"Sensor {sensor_id} - Temp: {temperature}, Hum: {humidity}")
                time.sleep(1)
            if time.time() - start_time > execution_time:
                stop_event.set()

    print("Benchmarking Sequential Execution")
    result_counter_seq = {sid: 0 for sid in sensor_ids}
    stop_event.clear()
    start_time_seq = time.time()
    sequential_monitoring(sensor_ids, stop_event, result_counter_seq)
    end_time_seq = time.time()
    
    print(f"Sequential Execution Time: {end_time_seq - start_time_seq:.2f} seconds")
    for sid in sensor_ids:
        print(f"Sensor {sid} - Readings: {result_counter_seq[sid]}")

    print("Benchmarking Parallel Execution")
    result_counter_th_bench = {sid: 0 for sid in sensor_ids}
    stop_event.clear()
    start_time_par = time.time()
    threads = [threading.Thread(target=monitor_sensor, args=(sid, stop_event, result_counter_th_bench)) for sid in sensor_ids]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time_par = time.time()
    
    print(f"Parallel Execution Time: {end_time_par - start_time_par:.2f} seconds")
    for sid in sensor_ids:
        print(f"Sensor {sid} - Readings: {result_counter_th_bench[sid]}")
