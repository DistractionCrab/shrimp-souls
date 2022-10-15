import atexit

OUT_FILE = open("D:\\Documents\\Programming\\shrimp-souls\\log.txt", 'a')

def log(msg):
	OUT_FILE.write(msg + "\n")

def close():
	OUT_FILE.flush()
	OUT_FILE.close()

atexit.register(close)