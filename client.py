import time
from opcua import Client
from datetime import datetime
from influxdb import InfluxDBClient
import json


db_client = InfluxDBClient(host='localhost', port=8086)
db_client.create_database('opc')
db_client.switch_database('opc')


URL = "opc.tcp://localhost:4840"
 
if __name__ == "__main__":
    client = Client(URL)
    client.connect()
     
    percent = client.get_node("ns=2;i=7")
    temp = client.get_node("ns=2;i=2")
    free = client.get_node("ns=2;i=4")
    used = client.get_node("ns=2;i=5")
     
    print("Client loop init")

    while True:

      p = percent.get_value()
      json_body = [{
              "measurement": "cpu_load",
              "fields": {
                  "percent": p
              }}]

      db_client.write_points(json_body)





      t = temp.get_value()
      json_body = [{
              "measurement": "cpu_temperature",
              "fields": {
                  "temp": t
              }}]

      db_client.write_points(json_body)





      f = free.get_value()
      u = used.get_value()
      json_body = [{
              "measurement": "memory",
              "fields": {
                  "free": f,
                  "used": u
              }}]
      db_client.write_points(json_body)




      time.sleep(0.05)
