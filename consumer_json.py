import json
from collections import deque
from kafka import KafkaConsumer
import matplotlib.pyplot as plt

TOPIC = "22155"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=["iot.redesuvg.cloud:9092"],
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="grupo-lab7",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    # Guardamos historia de lecturas
    temps = []
    hums = []
    winds = []

    # Configuracion inicial de la grafica
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle("Estacion Meteorologica - Lab 7")

    for msg in consumer:
        data = msg.value
        print("Recibido:", data)

        temps.append(data["temperatura"])
        hums.append(data["humedad"])
        winds.append(data["direccion_viento"])

        if len(temps) > 50:
            temps.pop(0)
            hums.pop(0)
            winds.pop(0)

        # Actualizar grafica
        ax1.clear()
        ax2.clear()

        ax1.plot(temps, marker="o")
        ax1.set_ylabel("Temperatura (°C)")

        ax2.plot(hums, marker="o")
        ax2.set_ylabel("Humedad (%)")
        ax2.set_xlabel("Muestras")

        plt.pause(0.01)


if __name__ == "__main__":
    main()
