from threading import Semaphore

"""
Barrier class using semaphores, that will block threads
until N threads are arrived at the barrier.

This class is used to synchronize the starting of the threads, because
it may happen that, when starting the threads by iterating over the list of threads,
some threads have finished their work before all threads have been started.

This code is gotten from here: https://stackoverflow.com/questions/26622745/implementing-barrier-in-python2-7
as it's a clean, simple and efficient solution to our problem
"""


class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.acquire()
        self.count = self.count + 1
        self.mutex.release()
        if self.count == self.n:
            self.barrier.release()
        self.barrier.acquire()
        self.barrier.release()
