import threading

file_lock = threading.Lock()
    
def open_write_and_close(message):
    file_lock.acquire()
    file = open('web_log.txt', 'a')
    file.write(message)
    file.flush()
    file.close()
    file_lock.release()