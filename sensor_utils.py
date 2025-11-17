import numpy as np
import random

WIND_DIRECTIONS = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]


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
