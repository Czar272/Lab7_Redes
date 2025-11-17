from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from sensor_utils import decode_lectura

TOPIC = "22155"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=["iot.redesuvg.cloud:9092"],
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="grupo-lab7-bytes",
        # no usamos value_deserializer, trabajamos con bytes crudos
    )

    temps = []
    hums = []
    winds = []

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle("Estacion Meteorologica - Payload 3 bytes")

    for msg in consumer:
        raw = msg.value  # bytes
        data = decode_lectura(raw)  # dict

        print("Bytes recibidos:", raw, "-> decodificado:", data)

        temps.append(data["temperatura"])
        hums.append(data["humedad"])
        winds.append(data["direccion_viento"])

        if len(temps) > 50:
            temps.pop(0)
            hums.pop(0)
            winds.pop(0)

        ax1.clear()
        ax2.clear()

        ax1.plot(temps, marker="o")
        ax1.set_ylabel("Temp (°C)")

        ax2.plot(hums, marker="o")
        ax2.set_ylabel("Humedad (%)")
        ax2.set_xlabel("Muestras")

        plt.pause(0.01)


if __name__ == "__main__":
    main()
