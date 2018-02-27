import sys
import time 
### This is just a dummy python script that prints back to the shell
print ("This is a test python script")
print ("These are the arguments I passed in to my test script:")
for i in range(0,len(sys.argv)-1):
    print (sys.argv[i+1])
time.sleep(3)
