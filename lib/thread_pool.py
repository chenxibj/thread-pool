import concurrent.futures
from time import sleep
from threading import Thread

class ThreadPoolError(Exception):
    pass

class ThreadPool():
    def __init__(self):
        print("ThreadPool")
        self.threads = []

    def addTask(self, func, *args):
        self.task = func
        print(self.task)
        self.args = args

    def setMaxWorkers(self, num):
        self.max_workers = num

    def runTaskPerParm(self, parms):
        # We can use a with statement to ensure threads are cleaned up promptly
        print(self.task)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for parm in parms:
                print("runTaskPerParm %s" % parm)
                self.threads.append(executor.submit(self.task, **parm))

    def runTaskPerNum(self, total_task_num):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for i in range(total_task_num):
                print(self.args)
                self.threads.append(executor.submit(self.task, *self.args))

    def cancelTask(self):
        # status = [x.running() for x in self.threads]
        # print("before cancel status" % status)
        for t in self.threads:
            t.cancel()
            # print(t.cancelled())
        # status = [x.cancelled() for x in self.threads]
        print("after cancel status %s" % self.threads)

if __name__ == "__main__":
    pass
    # ==================test========================================
    # class Test():
    #     def __init__(self, index):
    #         print("test class sleep")
    #         sleep(8)
    #         print("class test %s" % index)
    #
    def load_url(index, str):
        if str == "error":
            raise ThreadPoolError
        sleep(1)
        print("this task is %s %s" % (index, str))

    # ==========================================================
    # pool.addTask(Test, 33)
    test_parms = [{"index":1, "str":"cccc"},
                  {"index": 2, "str":"ddddd"},
                  {"index":3, "str":"error"}]
    pool = ThreadPool()
    pool.setMaxWorkers(10)
    pool.addTask(load_url, 33)
    pool.runTaskPerParm(test_parms)
    sleep(1)
    # obj = Thread(target=pool.runTaskPerNum, args=[2])
    # obj.start()
    print(pool.threads)
    # pool.deploy_id = 1
    # running_deploy[deploy_id] = pool
    # pool = ThreadPool()
    # pool.setMaxWorkers(1)
    # pool.addTask(load_url, 33, "ssss")
    # deploy_id = 2
    # running_deploy[deploy_id] = pool
    # print running_deploy
    # pool.setMaxWorkers(10)

    # obj1 = Thread(target=running_deploy[2].runTaskPerNum, args=[2])
    # obj1.start()
    # sleep(1)
    # print("start cancel")
    # pool.cancelTask()
    # print("cancel done")
    # print running_deploy[1].threads
    # print running_deploy[2].threads
    # print("wait for join")
    # obj.join()
    # sleep(1)
    # print("cancel")
    # pool.cancelTask()
