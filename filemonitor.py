# !/usr/bin/env python
# -*- coding:UTF-8 -*-
# please use python3
# author caiqyxyx

import os
import queue
import hashlib
import time

# Constant
QUE_MAX = 999999

global q
global file_map
global file_set
global delete_q
q = queue.Queue(QUE_MAX)
delete_q = queue.Queue(QUE_MAX)
file_map = {}
file_set = set([])


def monitor(path):
    global file_set
    if os.path.isdir(path):
        new_file_set = set([])
        for root, dirs, files in os.walk(path):
            for f in files:
                new_file_set = new_file_set | set([os.path.join(root, f)])
                if hash(os.path.join(root, f)) in file_map:
                    if file_map[hash(os.path.join(root, f))] == md5(os.path.join(root, f)):
                        pass
                    else:
                        print("{0} has been modified".format(
                            os.path.join(root, f)))
                        file_map[hash(os.path.join(root, f))] = md5(
                            os.path.join(root, f))
                        q.put(os.path.join(root, f))
                else:
                    print("{0} has been added".format(os.path.join(root, f)))
                    file_map.setdefault(
                        hash(os.path.join(root, f)), md5(os.path.join(root, f)))
                    q.put(os.path.join(root, f))
        diff = file_set.difference(new_file_set)
        file_set = new_file_set
        if len(diff) > 0:
            for f in diff:
                print("{0} has been deleted".format(f))
                file_map.pop(hash(f))
                delete_q.put(f)


def md5(file):
    md5file = open(file, 'rb')
    md5_ = hashlib.md5(md5file.read()).hexdigest()
    md5file.close()
    return md5_


while True:
    monitor(r"C:\Users\c15367\Desktop\github\py-sync")
    time.sleep(5)
