# CPU and RAM monitoring

The development allows using Grafana to monitor the temperature and load of the processor, as well as the amount of used RAM.
Based on: Kafka + OPC UA + InfluxDB + Graphana

## Instruction

Run three scripts sequentially in different terminals

```bash
python3 sensor.py
python3 opcua.py
python3 client.py
```

## Screenshots

### OPC UA client
![alt text](https://github.com/p134d/rt_soft_project/blob/main/screenshots/opcua_client.png?raw=true)

### CPU dashboards
![alt text](https://github.com/p134d/rt_soft_project/blob/main/screenshots/cpu_dashboard.png?raw=true)

### Memory dashboard
![alt text](https://github.com/p134d/rt_soft_project/blob/main/screenshots/memory_usage_dashboard.png?raw=true)
