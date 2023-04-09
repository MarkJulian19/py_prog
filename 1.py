import os
import time
start_time = time.time()
pid = os.fork()

if pid:
    for i in range(0,50000000):
        continue
else:
    for i in range(0,50000000):
        continue
print(time.time() - start_time)