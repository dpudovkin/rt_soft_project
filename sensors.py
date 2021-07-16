import time
from pykafka import KafkaClient
import json
from pyspectator.processor import Cpu
import psutil


def memory():

    with open('/proc/meminfo', 'r') as mem:
        ret = {}
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                ret['total'] = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
        ret['free'] = tmp
        ret['used'] = int(ret['total']) - int(ret['free'])
    return ret


kafka_client = KafkaClient(hosts="localhost:9092")

kafka_topic  = kafka_client.topics['cpu_temp']
kafka_producer_cpu_temp = kafka_topic.get_sync_producer()

kafka_topic  = kafka_client.topics['cpu_percent']
kafka_producer_cpu_percent = kafka_topic.get_sync_producer()

kafka_topic  = kafka_client.topics['memory']
kafka_producer_memory = kafka_topic.get_sync_producer()


print("Measure source init")
cpu = Cpu(monitoring_latency=0.05)

while True:
	msg = json.dumps({"temp": cpu.temperature})
	kafka_producer_cpu_temp.produce(msg.encode('ascii'))

	mem = memory()
	msg = json.dumps({"free": mem["free"] / 1024, "used": mem["used"] / 1024})
	kafka_producer_memory.produce(msg.encode('ascii'))

	msg  = json.dumps({"percent": psutil.cpu_percent()})
	kafka_producer_cpu_percent.produce(msg.encode('ascii'))



	time.sleep(0.05)






