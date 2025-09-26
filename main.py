# Запуск потоков для UI и для измерения

import threading
import queue

cmd   = queue.SimpleQueue()
data  = queue.SimpleQueue()
error = queue.SimpleQueue()

def thread_measurements():
	pass

def thread_ui():
	pass

tm = threading.Thread(target=thread_measurements, daemon=True)
tm.start()

tu = threading.Thread(target=thread_ui, daemon=True)
tu.start()

tm.join()
tu.join()
