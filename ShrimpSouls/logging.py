import os
import atexit
from datetime import datetime
LOG_FILE = os.path.join(os.path.split(__file__)[0], "../log.txt")
OUT_FILE = open(LOG_FILE, 'a')

def log(msg):
	msg = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {str(msg)}\n"
	print(msg, end="")
	OUT_FILE.write(msg)
	OUT_FILE.flush()

atexit.register(OUT_FILE.close)