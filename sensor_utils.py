import numpy as np
import random

WIND_DIRECTIONS = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]
WIND_TO_BITS = {d: i for i, d in enumerate(WIND_DIRECTIONS)}
BITS_TO_WIND = {i: d for d, i in WIND_TO_BITS.items()}


def generar_lectura():
    """
    Devuelve un dict con una medicion:
    {
        "temperatura": float [0,110.00],
        "humedad": int [0,100],
        "direccion_viento": str en WIND_DIRECTIONS
    }
    """

    # Temperatura: distribucion normal en [0,110]
    mean_temp = 25.0
    std_temp = 10.0
    temp = np.random.normal(loc=mean_temp, scale=std_temp)
    temp = max(0.0, min(110.0, temp))  # recortar a [0,110]
    temp = round(temp, 2)

    # Humedad relativa: normal + enteros [0,100]
    mean_hum = 60.0
    std_hum = 15.0
    hum = np.random.normal(loc=mean_hum, scale=std_hum)
    hum = int(round(max(0, min(100, hum))))

    # Direccion del viento: uniforme sobre las 8 opciones
    wind = random.choice(WIND_DIRECTIONS)

    return {"temperatura": temp, "humedad": hum, "direccion_viento": wind}


def encode_lectura(lectura):
    """
    dict -> 3 bytes
    Campos:
      temperatura (float, 2 decimales)
      humedad (int)
      direccion_viento (str)
    """

    temp = lectura["temperatura"]
    hum = lectura["humedad"]
    wind = lectura["direccion_viento"]

    temp_enc = int(round(temp * 100))

    if not (0 <= temp_enc <= 11000):
        raise ValueError("Temperatura fuera de rango")

    if not (0 <= hum <= 100):
        raise ValueError("Humedad fuera de rango")

    wind_enc = WIND_TO_BITS[wind]

    # Empaquetar en 24 bits
    value = (temp_enc << (7 + 3)) | (hum << 3) | wind_enc

    # Convertir a 3 bytes
    return value.to_bytes(3, byteorder="big")


def decode_lectura(b):
    """
    3 bytes -> dict con la misma estructura que generar_lectura()
    """
    if len(b) != 3:
        raise ValueError("Se esperaban exactamente 3 bytes")

    value = int.from_bytes(b, byteorder="big")

    wind_enc = value & 0b111  # uiltimos 3 bits
    hum = (value >> 3) & 0b1111111  # siguientes 7 bits
    temp_enc = value >> (7 + 3)  # los 14 bits superiores

    temp = temp_enc / 100.0

    wind = BITS_TO_WIND[wind_enc]

    return {"temperatura": temp, "humedad": hum, "direccion_viento": wind}
