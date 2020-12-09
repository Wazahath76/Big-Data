import json
import time
import socket
from threading import Thread
import sys
import random

worker_id=sys.argv[2]
threads=[]
def executing(task):				
	time.sleep(task["duration"])
	task["status"]="finished"
		
def end_message(task):
	mast_task=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	mast_task.connect(("localhost",5001))
	mast_task.send(json.dumps(task).encode())
	mast_task.close()
	print(f"Task with task id {task['task_id']} is completed execution by {task['worker_id']}")
	
		
def contact():
	worker=socket.socket(socket.AF_INET,socket.SOCK_STREAM)		#communication is established
	worker.bind(("localhost",int(sys.argv[1])))				#socket has been made
	worker.listen(1)
	while(1):
		Socket,addrress=worker.accept()
		task_data=Socket.recv(1024)
		task=json.loads(task_data.decode())	
		threads.append(task)
	Socket.close()
	
def thread_execution():
	while(1):
		while(len(threads)<1):
			time.sleep(0.001)		
		task=threads.pop(0)
		print(f"Task with task id {task['task_id']} is started execution by {task['worker_id']}")
		process=Thread(target=executing,kwargs=dict(task=task))
		process.start()
		process.join()
		end_message(task)

		

con=Thread(target=contact)
thre=Thread(target=thread_execution)
con.start()
thre.start()
con.join()
thre.join()
