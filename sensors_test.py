from pyspectator.processor import Cpu
from time import sleep
import psutil
cpu = Cpu(monitoring_latency=0.05)

def memory():
    """
    Get node total memory and memory usage
    """
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

while True:
    # print(cpu.temperature)
    import psutil
    print(str(psutil.cpu_percent()))
    mem = memory()
    print(str(mem["used"]/1024)+" "+str(mem["free"]/1024))
    sleep(1)

