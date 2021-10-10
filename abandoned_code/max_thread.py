import threading
import time

sem = threading.Semaphore(4)  # 限制线程的最大数量为4个


def gothread():
    with sem:  # 锁定线程的最大数量
        for i in range(8):
            print(threading.current_thread().name, i)
            time.sleep(0.2)


for i in range(5):
    threading.Thread(target=gothread).start()