import threading

def create_threads(iplist, function):
    threads = []
    for ip in iplist:
        th = threading.Thread(target = function, args = (ip,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()