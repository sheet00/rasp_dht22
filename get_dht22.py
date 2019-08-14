import Adafruit_DHT as DHT
import pymysql.cursors


def get_dht():
    # センサーの種類
    SENSOR_TYPE = DHT.DHT22

    # 接続したGPIOポート
    DHT_GPIO = 22

    # 測定開始
    h, t = DHT.read_retry(SENSOR_TYPE, DHT_GPIO)

    r = {"temp": t, "hum": h}
    # print(r)

    r['temp'] = round(r['temp'], 2)
    r['hum'] = round(r['hum'] / 100, 4)

    print(r)


get_dht()
