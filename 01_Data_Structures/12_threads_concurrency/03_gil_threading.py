import threading
import time

def brew_chai():
    print(f"{threading.current_thread().name} started the brewing process")
    count=0
    for _ in range(100_000_000):
        count +=1
    print(f"{threading.current_thread().name} finished the brewing process")
    

thread1=threading.Thread(target=brew_chai,name="Barista")
thread2=threading.Thread(target=brew_chai,name="Starbucks")

start=time.time()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
end = time.time()

print(f"total time taken: {end -start:.2f} secs")
