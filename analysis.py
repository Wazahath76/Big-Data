#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as mat
import sys
import time
from datetime import datetime


df= pd.read_csv("log.csv")
#print(df.head())

df.head()

#end_time = df[df["status"]=="finished"]


# In[2]:


a = df.task_id.unique()
b = df.job_id.unique()


# In[3]:


t_list=[]
j_id=[]
w_id=[]

def twoseconds(ti):
    dt=datetime.strptime(ti,"%c").timetuple()
    #print(time.mktime(dt))
    return time.mktime(dt)
for i in a:
    temp = df[df["task_id"]==i].values
    t_list.append((twoseconds(temp[1][-1]))-twoseconds(temp[0][-1]))
    w_id.append(int(temp[0][-3]))
    j_id.append(int(temp[0][2]))
j_list=[]
for i in b:
    temp=df[df["job_id"]==i].values
    j_list.append(twoseconds(temp[-1][-1])-twoseconds(temp[0][-1]))


# In[4]:


t_mean=np.array(t_list).mean()
print("mean time of task:",t_mean)
t_median=np.median(np.array(t_list))
print("median time of task:",t_median)
j_mean=np.array(j_list).mean()
print("mean time of job:",j_mean)
j_median=np.median(np.array(j_list))
print("median time of job:",j_median)



# In[5]:


df1 = df[df["status"]=="initiating"]

df1.plot.bar(stacked=True)


    
#random

#df['time'] = pd.to_datetime(df['time'])
#df.plot.bar(x="task_id",y="time")


# In[ ]:




