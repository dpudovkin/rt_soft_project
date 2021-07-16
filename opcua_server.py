from kafka import KafkaConsumer # kafka-python
import json
import time
from opcua import Server
from opcua.ua import VariantType
from datetime import datetime



URL = "opc.tcp://0.0.0.0:4840"

server = Server()
server.set_endpoint(URL)

objects   = server.get_objects_node()
ns        = server.register_namespace("test_metric")

cpu_temp = objects.add_object(ns, "cpu_temp")
temp_metric = cpu_temp.add_variable(ns, "temp", 0.0, varianttype = VariantType.Double)

memory = objects.add_object(ns, "memory")
free_metric = memory.add_variable(ns, "free", 0.0, varianttype = VariantType.Double)
used_metric = memory.add_variable(ns, "used", 0.0, varianttype = VariantType.Double)

cpu_percent = objects.add_object(ns, "cpu_percent")
percent_metric = cpu_percent.add_variable(ns, "percent", 0.0, varianttype = VariantType.Double)

server.start()
     
consumer = KafkaConsumer( 
     bootstrap_servers=['localhost:9092'],
     enable_auto_commit=True)

consumer.subscribe(['cpu_temp','cpu_percent', 'memory'])

print("Converter init")

while True:

    for message in consumer:

        message_val = message.value.decode("utf-8") 
        msg_json = json.loads(message_val)

        if message.topic == 'cpu_temp':
            temp_metric.set_value(msg_json["temp"], varianttype=VariantType.Double)

        elif message.topic == 'cpu_percent':
            percent_metric.set_value(msg_json["percent"], varianttype=VariantType.Double)

        elif message.topic == 'memory':
            free_metric.set_value(msg_json["used"], varianttype=VariantType.Double)
            used_metric.set_value(msg_json["free"], varianttype=VariantType.Double)

    time.sleep(0.05)
