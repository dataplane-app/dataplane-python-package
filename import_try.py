from datetime import datetime

start  = datetime.now()

from dataplane import hello

duration = datetime.now() - start

hello()

print(duration)
