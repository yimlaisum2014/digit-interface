import sys
import os
import time
from datetime import datetime
from digit_interface.digit import Digit
from digit_interface.digit_handler import DigitHandler

class Collect ():
    def __init__(self):
        # global variable
        self.trial = None
        self.step = None

        # connect DIGIT
        self.digit_right = Digit("D20356", "Right Gripper")
        self.digit_left = Digit("D20365", "Left Gripper")

        self.digit_left.connect()
        self.digit_right.connect()

        self.intensity(int(5)) #Under bright env. may not too high
        print("Start collecting")
        self.collect()

    def intensity(self,intensity):
        # Maximum value for each channel is 15
        rgb_list = [(intensity, 0, 0), (0, intensity, 0), (0, 0, intensity)]

        for rgb in rgb_list:
            self.digit_left.set_intensity_rgb(*rgb)
            self.digit_right.set_intensity_rgb(*rgb)
            time.sleep(1)
        self.digit_left.set_intensity(intensity)
        self.digit_right.set_intensity(intensity)
        time.sleep(1)

    def disconnect(self):
        self.digit_left.disconnect()
        self.digit_right.disconnect()

    def collect(self):
        #print(sys.argv)
        #print(type(sys.argv[1]))
        self.trial = int(sys.argv[1])
        self.step = int(sys.argv[2])
        print(type(self.trial),type(self.step))

        # whether having parmeters
        if self.trial ==None or self.time == None:
            raise Exception("There are missing parmeters -trial -time) ")
        
        # make a directionay
        savepath = "Data/_45/trial_"+ str(self.trial)+"/"
        if not os.path.exists(savepath):
            os.makedirs(savepath)

        # saving images
        for i in range(self.step):
            self.digit_left.save_frame(path = savepath + "left_{}_{}.png".format(i))
            self.digit_right.save_frame(path = savepath + "right_{}_{}.png".format(i))
            time.sleep(1)
            
        print("Finish collecting")
        self.disconnect()


if __name__ == "__main__":
    collect = Collect()
