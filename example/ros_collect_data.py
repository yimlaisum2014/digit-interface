from example.data_collect import collect
import rospy
import time
from cv_bridge import CvBridge
from digit_interface.digit import Digit
from sensor_msgs.msg import Image

class Collect(object):
    def __init__(self) -> None:

        # Parameter setting
        rospy.set_param("color_intensity",[5,5,5])
        color_intensity = rospy.get_param("color_intensity")
        r, g, b = color_intensity[0],color_intensity[1],color_intensity[2]

        self.bridge = CvBridge

        self.digit_right = Digit("D20356", "Right Gripper")
        self.digit_left = Digit("D20365", "Left Gripper")

        self.connect(self.digit_left)
        self.connect(self.digit_right)
        self.set_intensity(r,g,b)
        self.cv_2_rosmsg()

        # Publisher
        self.pub_left = rospy.Publisher("finger_left", Image, queue_size=10)
        self.pub_right = rospy.Publisher("finger_left", Image, queue_size=10)

    def connect(self, camera):
        connected = False
        while not connected:
            print('Try connecting....')
            try:
                camera.connect()
                print('Succeed')
                connected = True
            except:
                print('Failed')
                pass
            time.sleep(1)
    
    def set_intensity(self, r, g, b):

        for camera in {self.digit_right, self.digit_left}:
            if camera is not None:
                camera.set_intensity_rgb(r, g, b)

    def disconnect(self):
        self.digit_left.disconnect()
        self.digit_right.disconnect()

    def cv_2_rosmsg(self):
        cv_left_image = self.digit_left.get_frame()
        cv_right_image = self.digit_right.get_frame()
        
        ros_left_image = self.bridge.cv2_to_imgmsg(cv_left_image, desired_encoding='passthrough')
        ros_right_image = self.bridge.cv2_to_imgmsg(cv_right_image, desired_encoding='passthrough')

        self.pub_left.publish(ros_left_image)
        self.pub_right.publish(ros_right_image)
        


if __name__ == "__main__":
    rospy.init_node("collect",anonymous=False)
    collect = Collect()
    if rospy.spin() :
        collect.disconnect()

