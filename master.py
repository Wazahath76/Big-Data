import json
import socket
from threading import Thread
import time
import sys
import random

csv_fl=open("log.csv",'w')
csv_fl.write("task_id,job_id,worker_id,status,time\n")
csv_fl.close()

conf=open(sys.argv[1],"r")
workers=json.load(conf)['workers']
conf.close()

jobs=[]	
comp_map=[]
def worker_message(ind,task):			#we are using sockets to communicate between master and workers
		global workers
		worker=socket.socket(socket.AF_INET,socket.SOCK_STREAM)		
		worker.connect(("localhost",workers[ind]["port"]))
		task["status"]="initiating"
		task["time"]=time.asctime(time.localtime())
		task["worker_id"]=workers[ind]["worker_id"]
		worker.send(json.dumps(task).encode())		#data is stored in a log file 
		csv_fl=open("log.csv",'a+')
		csv_fl.write(f"{task['task_id']},{task['job_id']},{task['worker_id']},{task['status']},{task['time']}\n")
		csv_fl.close()
		workers[ind]["slots"]-=1
		worker.close()
		print(f"Task and task id {task['task_id']} is allocated to {task['worker_id']}")
		
def RANDOM(job):
	for j in job["map_tasks"]:
		i=random.randint(0,2)			#this is random scheduling which takes random values using randint
		while(workers[i]["slots"]<1):
			i=random.randint(0,2)
		j['job_id']=job["job_id"]
		worker_message(i,j)
	while(comp_map[int(j["job_id"])]!=0):
		time.sleep(1)
	for j in job["reduce_tasks"]:
		i=random.randint(0,2)
		while(workers[i]["slots"]<1):
			i=random.randint(0,2)
		j['job_id']=job["job_id"]
		worker_message(i,j)
		
		
RR_index=0

def RR(job):
	global RR_index
	for j in job["map_tasks"]:
		while(workers[RR_index]["slots"]<1):		#this is round robin scheduling where it goes to the next one in a circled fashion
			RR_index=(RR_index+1)%3
		j['job_id']=job["job_id"]
		worker_message(RR_index,j)
		RR_index=(RR_index+1)%3
	while(comp_map[int(j["job_id"])]!=0):
		time.sleep(1)
	for j in job["reduce_tasks"]:
		while(workers[RR_index]["slots"]<1):
			RR_index=(RR_index+1)%3
		j['job_id']=job["job_id"]
		worker_message(RR_index,j)
		RR_index=(RR_index+1)%3	
			
def free_slot_worker():
	global workers
	slots=[]
	for i in workers:
		slots.append(i["slots"])
	return slots.index(max(slots))
def LL(job):
	for j in job["map_tasks"]:
		i=free_slot_worker()				#this is the scheduling where maximum number of free slot workers are assigned the task
		while(workers[i]["slots"]<1):
			i=free_slot_worker()
		j['job_id']=job["job_id"]
		worker_message(i,j)
	while(comp_map[int(j["job_id"])]!=0):
		time.sleep(1)
	for j in job["reduce_tasks"]:
		i=free_slot_worker()
		while(workers[i]["slots"]<1):
			i=free_slot_worker()
		j['job_id']=job["job_id"]
		worker_message(i,j)
		
		
if(sys.argv[2]=='RANDOM'):
	scheduler=RANDOM		
elif(sys.argv[2]=='RR'):
	scheduler=RR	
elif(sys.argv[2]=='LL'):
	scheduler=LL
else:
	print("The Scheduling cannot be done")
	exit()


def jobs_req():
	Socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	Socket.bind(("localhost",5000))
	Socket.listen(1)
	while(1):
		connection,address=Socket.accept()
		data=connection.recv(1024)
		job=json.loads(data.decode())
		jobs.append(job)
		comp_map.append(len(job["map_tasks"]))
		scheduler(job)
	connection.close()
	
def contact():
	master=socket.socket(socket.AF_INET,socket.SOCK_STREAM)		#we retrive message from worker
	master.bind(("localhost",5001))
	master.listen(1)
	while(1):
		Socket,addr=master.accept()
		data=Socket.recv(1024)
		task=json.loads(data.decode())
		global workers
		task["time"]=time.asctime(time.localtime())
		if(task["task_id"].split('_')[1][0]=='M'):
			comp_map[int(task["job_id"])]-=1
		workers[int(task["worker_id"])-1]["slots"]+=1
		csv_fl=open("log.csv",'a+')
		csv_fl.write(f"{task['task_id']},{task['job_id']},{task['worker_id']},{task['status']},{task['time']}\n")
		csv_fl.close()
		print(f"Task and task id {task['task_id']} is completed by {task['worker_id']}")
	connectionSocket.close()

req=Thread(target=jobs_req)
con=Thread(target=contact)
req.start()
con.start()
req.join()
con.join()
