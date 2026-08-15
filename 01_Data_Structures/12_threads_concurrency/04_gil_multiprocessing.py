from multiprocessing import Process
import time

def crunch_number():
    print(f"Started the count process")
    count=0
    for _ in range(100_000_000):
        count+=1
    print(f"End the count process")


if __name__=="__main__": #without main it will throw an error 
    # An attempt has been made to start a new process before the current process has finished its bootstrapping phase.
    # Basically its saying I dont know what is the entry point of your program where to start it
    # In muulti - processing you need to be careful as you are overwriting your mutex.
    start = time.time()
    p1= Process(target=crunch_number)
    p2= Process(target=crunch_number)

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    end=time.time()

    print(f"Total time with multi-processing : {end - start:.2f} seconds")