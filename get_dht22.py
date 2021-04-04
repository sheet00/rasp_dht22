import board
import adafruit_dht
import pymysql.cursors


def get_dht():
    # 接続したGPIOポート:22
    dhtDevice = adafruit_dht.DHT22(board.D22)

    # 測定開始
    t = dhtDevice.temperature
    h = dhtDevice.humidity

    r = {"temp": t, "hum": h}

    # print(r)
    r['temp'] = round(r['temp'], 2)
    r['hum'] = round(r['hum'] / 100, 4)

    print(r)


get_dht()
