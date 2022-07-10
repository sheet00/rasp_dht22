import board
import adafruit_dht
import pymysql.cursors


def get_dht():
    # 接続したGPIOポート:22
    dhtDevice = adafruit_dht.DHT22(board.D22)

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
