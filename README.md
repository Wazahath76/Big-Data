# Big-Data
A centralized scheduling framework is a framework that consists of a master
and this master runs on a machine and manages the cluster. The other
machines in the cluster have the worker process and in the following project 3
worker process are used. The scheduling is done in the master process and the
tasks are being executed in the worker process. The Master listens for job
requests and initiates the tasks in the jobs based on a scheduling algorithm.
The Worker processes listen for task launch messages from the master .

The various scheduling algorithms used are :
a) Round -Robin
b) Least Loaded
c) Random
