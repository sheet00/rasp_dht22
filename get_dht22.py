import board
import adafruit_dht
import pymysql.cursors
import time

import os
from dotenv import load_dotenv

def get_dht():
    load_dotenv()
    # .envからGPIOポートを読み込む
    gpio_port = os.environ.get('DHT22_GPIO_PORT')
    if gpio_port is None:
        print("DHT22_GPIO_PORTが.envファイルに設定されていません。")
        return None
    try:
        gpio_port = getattr(board, gpio_port)
    except AttributeError:
        print(f"無効なGPIOポート名: {gpio_port}")
        return None

    dhtDevice = adafruit_dht.DHT22(gpio_port)

    #Simple test — Adafruit CircuitPython DHT Library 1.0 documentation https://docs.circuitpython.org/projects/dht/en/latest/examples.html#id1
    is_success = False
    while is_success == False:
        try:
            #測定開始
            t = dhtDevice.temperature
            h = dhtDevice.humidity
            is_success = True

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

    r = {"temp": t, "hum": h}

    # print(r)
    r['temp'] = round(r['temp'], 2)
    r['hum'] = round(r['hum'] / 100, 4)

    print(r)


get_dht()
