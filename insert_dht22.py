import board
import adafruit_dht

import pymysql.cursors
import datetime
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    log("-------")
    dht = get_dht()
    print(f"{dht=}")

    if validate_temperature_range(dht):
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
                print(f"mysql_select_avg {r=}")
    finally:
        conn.close()

    return results[0]


# 取得温度のぶれ幅検証
# 上下N度以内か判定
def validate_temperature_range(dht):
    RANGE = 12

    avg = mysql_select_avg()
    _min = avg['avg'] - RANGE
    _max = avg['avg'] + RANGE

    log("[上下N度以内か判定]")
    log('直近のavg %f' % avg['avg'])
    log('insert許可 min %f' % _min )
    log('insert許可 max %f' % _max)
    log('取得したtemp %f' % dht['temp'])

    is_valid = False
    if _min <= dht['temp'] and dht['temp'] <= _max:
        is_valid = True

    log(f'insert許可 {is_valid=}')

def get_dht():
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
            print(f"{error.args[0]=}")
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
    conn = pymysql.connect(host=os.environ.get('MYSQL_HOST'),
                           user=os.environ.get('MYSQL_USER'),
                           password=os.environ.get('MYSQL_PASSWORD'),
                           db=os.environ.get('MYSQL_DB'),
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
