import time
import random
from kafka import KafkaProducer
from sensor_utils import generar_lectura, encode_lectura

TOPIC = "22155"


def main():
    producer = KafkaProducer(bootstrap_servers=["iot.redesuvg.cloud:9092"])

    print(f"[3 BYTES] Enviando datos al topic '{TOPIC}'... Ctrl+C para salir.")

    try:
        while True:
            lectura = generar_lectura()
            payload = encode_lectura(lectura)

            print("Lectura original:", lectura, "-> bytes:", payload)

            producer.send(TOPIC, value=payload)
            producer.flush()

            delay = random.randint(15, 30)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nDeteniendo producer...")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
