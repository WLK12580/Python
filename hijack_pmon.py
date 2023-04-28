from  flask import Flask
import time

#node list which is consist of key and value,
# key is node name,value is respawn count
respawn_list={}
# Node_list=["console","network","elevator"]
Node_list=["console","rcc","elevator","network"]
def ExistsNodeName(nodename):
    if respawn_list.__contains__(nodename):
        return True
    else:
        return False
def dict():
    for p in Node_list:
        print("{} is exists {}".format(p,ExistsNodeName(p)))
        if ExistsNodeName(p):
            print("true {}".format(p))
            respawn_list[p]+=1
            print("respawn {} count={}".format(p,respawn_list[p]))
        else:
            print("false p={}".format(p))
            respawn_list[p]=0
            print("respawn {} count={}".format(p,respawn_list[p]))
        time.sleep(2)      
if __name__=="__main__":
    while True:
        dict()
    

    
       
            