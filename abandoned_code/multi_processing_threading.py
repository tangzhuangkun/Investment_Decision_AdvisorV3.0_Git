import multiprocessing
import threading
import os
import time

# demo, 多进程里嵌套多线程，且线程数量可被限制

'''
# version 1
class multiProcessingThreading:
    def __init__(self):
        pass

    def job(self, a,d):
        t1 = threading.currentThread()
        print(t1.name+"----"+str(a+d))

    def multi_threadings(self):
        process_lock.acquire()
        print("当前进程：", os.getpid(), " 父进程：", os.getppid())
        threading.Thread(target= self.job, args=(1, 1)).start()
        threading.Thread(target= self.job, args=(2, 2)).start()
        threading.Thread(target= self.job, args=(3, 4)).start()
        process_lock.release()

    def init_lock(self,l):
        global process_lock
        process_lock = l

    def main(self):
        process_lock = multiprocessing.Lock()
        print('Parent process %s.' % os.getpid())
        process_pool = multiprocessing.Pool(multiprocessing.cpu_count(), initializer=self.init_lock,
                                            initargs=(process_lock,))
        for i in range(10):
            process_pool.apply_async(self.multi_threadings)
        print('Waiting for all subprocesses done...')
        process_pool.close()
        process_pool.join()
        print('All subprocesses done.')

if __name__=='__main__':
    go = multiProcessingThreading()
    go.main()
'''

class multiProcessingThreading:
    def __init__(self):
        # 最大的计算线程数
        self.max_threading_connections = 3

    def job(self, a,d):
        # 一个测试函数

        # 线程的名称
        t1 = threading.currentThread()
        print(t1.name, end=" ")
        print(a,d)
        #print(t1.name+"----"+str(i+a+d))

    def job_with_limited_threads(self, a, d, sem):
        # 嵌套测试函数
        # 管理多线程，限制线程数量

        self.job(a,d)
        # 线程释放
        sem.release()

    def multi_threadings(self, i):
        # 多线程，限制多线程数量

        # 给进程加锁，进程同步
        process_lock.acquire()
        print("当前进程：", os.getpid(), " 父进程：", os.getppid())
        # 限制线程的最大数量
        sem = threading.Semaphore(self.max_threading_connections)
        for j in range(20):
            # 开启线程
            threading.Thread(target= self.job_with_limited_threads, args=(i, j, sem)).start()
        # 进程锁释放
        process_lock.release()

    def init_lock(self,l):
        # 设置全局变量，进程锁
        global process_lock
        process_lock = l

    def main(self):
        # 启用进程锁
        process_lock = multiprocessing.Lock()
        # 打印父进程ID
        print('Parent process %s.' % os.getpid())
        # 启用进程池，
        # initializer，每个工作进程启动时要执行的可调用对象
        # initargs：是要传给initializer的参数组。
        process_pool = multiprocessing.Pool(multiprocessing.cpu_count(), initializer=self.init_lock,
                                            initargs=(process_lock,))
        for i in range(10):
            # apply_async， 该函数用于传递不定参数，主进程会被阻塞直到函数执行结束， 是非阻塞且支持结果返回进行回调
            process_pool.apply_async(self.multi_threadings, args=(i,))
        print('Waiting for all subprocesses done...')
        process_pool.close()
        process_pool.join()
        print('All subprocesses done.')

if __name__=='__main__':
    go = multiProcessingThreading()
    go.main()