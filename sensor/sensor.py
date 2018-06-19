import pymysql
from time import sleep


def get_temperature(id):
    fo = open('/sys/bus/w1/devices/' + id + '/w1_slave', 'r')
    fo.readline()
    line = fo.readline()
    temperature = line[29:34]
    return int(temperature)/1000


slave_id = "28-05169391c6ff"

conn = pymysql.connect(user='sensor', password='sensor', host='127.0.0.1', database='smartfreezer')
cursor = conn.cursor()

try:
    while True:
        sql = 'insert into temperature (temp) values (%s)'
        temp = (get_temperature(slave_id))
        temp -= 40
        print(temp)
        print(type(temp))
        cursor.execute(sql, str(temp))
        conn.commit()
        sleep(60)
except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()
