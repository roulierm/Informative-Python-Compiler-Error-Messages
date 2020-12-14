#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys, traceback
#to allow user to input a code and print the traceback call to 
# a new file in which we will use for similarity scores.

traceBack = open("traceBackTest.txt","a")

def run_user_code(envdir):
    source = input(">>> ")
    try:
        exec(source, envdir)
    except Exception:
        formatted_lines = traceback.format_exc().splitlines()
        traceBack.write(formatted_lines[0])
        traceBack.write('\n')
        traceBack.write(formatted_lines[-1])
        
envdir = {}
run_user_code(envdir)

