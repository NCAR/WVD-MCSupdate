import sys
import time
import datetime
### This is just a dummy python script that prints back to the shell
print ("This is a test python script")
print (time.ctime())
print ("These are the arguments I passed in to my test script:")
for i in range(0,len(sys.argv)-1):
    print (sys.argv[i+1])
