import sys
import time
import wx
from wx.lib.pubsub import pub
import threading
sys.path.insert(0, "..")

#No handlers could be found for logger "opcua.client.client"
from opcua import Client


# if __name__ == "__main__":

#     #client = Client("opc.tcp://192.168.91.201:4880/Arburg/")
#     client = Client("opc.tcp://host_computer:123@192.168.91.201:4880/Arburg/") #connect using a user
#     try:
#         client.connect()
#         OldSec = 0
#         while True:
#             current_time1 = time.localtime(time.time())
#             rangeSec = [1,16,31,46]
#             LoopNumberOld = 0
#             if current_time1.tm_sec in rangeSec :
#                if current_time1.tm_sec <> OldSec :
#                   varArburgLoop = client.get_node("ns=2;i=238982")
#                   LoopNumber = varArburgLoop.get_value()
#                   if LoopNumber <> LoopNumberOld :
#                      print("LoopNumber is : ",LoopNumber)
#                      wx.CallAfter(pub.sendMessage,'Client_Minimal',loopnumber = LoopNumber)
#                      LoopNumberOld = LoopNumber
#                   OldSec = current_time1.tm_sec
#         # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
#         #root = client.get_root_node()
#         #print("Objects node is: ", root)

#         # Node objects have methods to read and write node attributes as well as browse or populate address space
#         #print("Children of root are: ", root.get_children())

#         # get a specific node knowing its node id
#         #varLoop = client.get_node(ua.NodeId(1002, 2))
#         #varArburgLoop = client.get_node("ns=2;i=117562")
#         #print("LoopNumber is : ",varArburgLoop.get_value())
#         #print("GetDataValue  is : ",varArburgLoop.get_data_value())
#         #var.get_data_value() # get value of node as a DataValue object
#         #var.get_value() # get value of node as a python builtin
#         #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
#         #var.set_value(3.9) # set node value using implicit data type

#         # Now getting a variable node using its browse path
#         #myvar = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
#         #obj = root.get_child(["0:Objects", "2:MyObject"])
#         #print("myvar is: ", myvar)

#     finally:
#         client.disconnect()







def ClientLink():
    #client = Client("opc.tcp://192.168.91.201:4880/Arburg/")
    client = Client("opc.tcp://host_computer:123@192.168.91.201:4880/Arburg/") #connect using a user
    try:
        client.connect()
        OldSec = 0
        while True:
            current_time1 = time.localtime(time.time())
            rangeSec = [1,16,31,46]
            LoopNumberOld = 0
            if current_time1.tm_sec in rangeSec :
               if current_time1.tm_sec <> OldSec :
                  varArburgLoop = client.get_node("ns=2;i=238982")
                  LoopNumber = varArburgLoop.get_value()
                  if LoopNumber <> LoopNumberOld :
                     # print("LoopNumber is : ",LoopNumber)
                     num = LoopNumber
                     LoopNumberOld = LoopNumber
                     wx.CallAfter(pub.sendMessage,'Client_Minimal',number = num)

                  OldSec = current_time1.tm_sec
        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        #root = client.get_root_node()
        #print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        #print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id
        #varLoop = client.get_node(ua.NodeId(1002, 2))
        #varArburgLoop = client.get_node("ns=2;i=117562")
        #print("LoopNumber is : ",varArburgLoop.get_value())
        #print("GetDataValue  is : ",varArburgLoop.get_data_value())
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        #myvar = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
        #obj = root.get_child(["0:Objects", "2:MyObject"])
        #print("myvar is: ", myvar)

    finally:
        client.disconnect()

class ClientLinkThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.isOpen = False
  
  def openThreading(self):
    self.isOpen = True
    self.start()

  def run(self):
    ClientLink()

