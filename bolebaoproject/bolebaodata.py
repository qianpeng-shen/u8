#执行删除数据
from data import fun
import time
import threading
def fun1():
    for i in range(20000):
        fun()
for i in range(10):
    t = threading.Thread(target=fun1())
    t.start()

time.sleep(4)
t.join()