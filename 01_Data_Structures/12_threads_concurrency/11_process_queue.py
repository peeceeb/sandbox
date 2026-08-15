from multiprocessing import Process, Queue, Value


def prepare_chai(queue):
    queue.put("Masala Chai is ready")

counter= Value('i',0)
  

queue=Queue()

if __name__=="__main__":
    p=Process(target=prepare_chai,args=(queue,))
    p.start()
    p.join()
    print(queue.get())


