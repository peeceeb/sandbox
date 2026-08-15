import threading
import time

def take_order():
    for i in range(1,4):
        print(f"Taking order in {i}")
        time.sleep(1)

def brew_chai():
    for i in range(1,4):
        print(f"Brewing chai for #{i}")
        time.sleep(2)

order_thread=threading.Thread(target=take_order)
brew_thread=threading.Thread(target=brew_chai)

order_thread.start()
brew_thread.start()

#wait for both to finish
order_thread.join()
brew_thread.join()

print(f"All orders taken and chai is brewed")
