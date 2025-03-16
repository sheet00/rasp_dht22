import board
import adafruit_dht

import pymysql.cursors
import datetime
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    dht = get_dht()
    print(dht)

    if is_safe(dht):
            mysql_insert(dht)


def mysql_insert(dht):
    conn = get_connect()

    try:
        with conn.cursor() as cursor:
            sql = "insert into temperature(temp,hum) values(%s,%s);"
            cursor.execute(sql, (dht['temp'], dht['hum']))

            conn.commit()
            log('insert commit')
    finally:
        conn.close()


def mysql_select_test():
    conn = get_connect()

    try:
        with conn.cursor() as cursor:
            sql = "select * from temperature limit 100;"
            cursor.execute(sql)

            results = cursor.fetchall()
            for r in results:
                print(r)
    finally:
        conn.close()


def mysql_select_avg():
    conn = get_connect()

    try:
        with conn.cursor() as cursor:
            sql = '''
select
  avg(temp) as avg 
from
  temperature 
order by
  id desc 
limit
  60
            '''
            cursor.execute(sql)

            results = cursor.fetchall()
            for r in results:
                print(r)
    finally:
        conn.close()

    return results[0]


# 取得温度のぶれ幅検証
# 上下N度以内か判定
def is_safe(dht):
    RANGE = 12

    avg = mysql_select_avg()
    _min = avg['avg'] - RANGE
    _max = avg['avg'] + RANGE

    log('min %f' % _min )
    log('max %f' % _max)
    log('avg %f' % avg['avg'])
    log('dht %f' % dht['temp'])

    if _min <= dht['temp'] and dht['temp'] <= _max:
        log('true')
        return True
    else:
        log('false')
        return False


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
    if h is not None:
        r['temp'] = round(r['temp'], 2)
        r['hum'] = round(r['hum'] / 100, 4)
        return r


def get_connect():
    conn = pymysql.connect(host=os.environ.get('POSTGRES_HOST'),
                           user=os.environ.get('POSTGRES_USER'),
                           password=os.environ.get('POSTGRES_PASSWORD'),
                           db=os.environ.get('POSTGRES_DB'),
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

    return conn


def log(str):
    path = '/home/pi/rasp_dht22/dht.log'
    with open(path, mode='a') as f:
        f.write('\n')
        now = datetime.datetime.now()
        f.write('[%s] ' % now.strftime("%Y/%m/%d %H:%M:%S") )
        f.write(str)



main()
