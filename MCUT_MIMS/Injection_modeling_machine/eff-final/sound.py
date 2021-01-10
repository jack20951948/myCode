import os
import time
from subprocess import Popen, PIPE

class sound():
    def StartSound(self):
        #time.sleep(7)
        os.system("sudo aplay /home/pi/eff/ding2.wav") 
        #p = Popen("/home/pi/eff/ding1.wav", shell=True, stdout=PIPE, stderr=PIPE)    
        #print "This is a sound test message!!!"
        #if p.returncode != 0:  
        #   print "Sound program error !!!"  

mySound = sound()
mySound.StartSound()
