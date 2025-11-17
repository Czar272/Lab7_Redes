import json
import time
import random
from kafka import KafkaProducer
from sensor_utils import generar_lectura

TOPIC = "22155"


def main():
    producer = KafkaProducer(
        bootstrap_servers=["iot.redesuvg.cloud:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    print(f"Enviando datos al topic '{TOPIC}'...")

    try:
        while True:
            lectura = generar_lectura()
            print("Enviando:", lectura)

            producer.send(TOPIC, value=lectura)
            producer.flush()

            delay = random.randint(5, 10)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nDeteniendo producer...")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
