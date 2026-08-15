from multiprocessing import Process
import time

def brew_chai(name):
    print(f"{name} start of chai brewing")
    time.sleep(3)
    print(f"{name} start of chai brewing")

if __name__ =="__main__":
    chai_makers= [
        Process(target=brew_chai, args=(f"Chai Makers #{i+1}", )) 
        for i in range(3)
        ]
    
#1 Start all the process
for p in chai_makers:
    p.start()


#wait for all to complete
for p in chai_makers:
    p.join()

print("All Chai Served")