import time

def bytes2human(n):
    "http://code.activestate.com/recipes/578019"
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if abs(n) >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def log_memory_usage(process):
    print("Memory logging stack:\n")
    mem_info = process.memory_info()
    print(f"RSS: {bytes2human(mem_info.rss)}, VMS: {bytes2human(mem_info.vms)}")
    time.sleep(1)
