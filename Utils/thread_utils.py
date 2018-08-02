#encoding:utf-8

def queue_threads_worker(q,func):
    while not q.empty():
        data = q.get()
        func(*data[0],**data[1])
        q.task_done()#任务完成，告诉q一声