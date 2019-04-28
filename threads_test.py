from multiprocessing import Process, Queue, Manager
import threading
from random import random
from time import sleep

class foo(object):
    def __init__(self,d):
        self.d = d
        self.digested = False

def func(runtime):
    while True:
        if runtime['obj'].digested == False:
            print('Handel obj.')
            runtime['digested'] = True
        else:
            pass
    
if __name__ == '__main__':
    with Manager() as mgr:
        runtime = mgr.dict()
        runtime['a'] = {'val1':1, 'val2':2}
        runtime['bool'] = True
        runtime['obj'] = foo({'val':1})
        runtime['digested'] = False
        is_first_loop = True
        p = Process(target = func, args = (runtime, ))

        while True:
            runtime['a']['val1'] = "changed"
            runtime['bool'] = not runtime['bool']
            runtime['obj'] = foo({'val':random()})
            runtime['digested'] = False
            if is_first_loop:
                p.start()
                is_first_loop = 0
            if runtime['digested'] == True:
                print(runtime, runtime['obj'].d, runtime['obj'])
