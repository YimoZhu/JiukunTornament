from multiprocessing import Process, Queue, Manager
import os, time, random
from time import sleep

def proc1(mgr):
    while True:
        mgr['val'] += 1
        mgr['val'] -= 1

if __name__ == '__main__':
    with Manager() as mgr:
        d = mgr.dict()
        d['val'] = 0
        p1 = Process(target = proc1, args = (d,))
        p2 = Process(target = proc1, args = (d,))
        p1.start()
        p2.start()
        while True:
            print(d['val'])