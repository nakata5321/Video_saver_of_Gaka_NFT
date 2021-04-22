#!/usr/bin/env python
import rospkg
import ipfshttpclient
import os
import sys, time
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

rospack = rospkg.RosPack()
dirname = rospack.get_path("video_saver")
FILE_OUTPUT = dirname + "/videos/" + "output.avi"

# width of frame
WIDTH = 1280
# height of frame
HEIGHT = 720
# flag for start/stop recording
flag = ""
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 30.0, (WIDTH, HEIGHT))


def main():  # init ros node
    rospy.init_node("image_recorder", anonymous=True)
    rospy.loginfo("node is up")

    def callback_video(ros_data):
        #### direct conversion to CV2 ####
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # Saves for video
        out.write(image_np)

    def callback(ros_data):
        if ros_data.data == "start":  # start recording
            sub_video = rospy.Subscriber(
                "/camera/color/image_raw/compressed",
                CompressedImage,
                callback_video,
                queue_size=1,
            )
            rospy.loginfo(ros_data.data)
        if ros_data.data == "stop":  # stop recording and release the video
            rospy.loginfo(ros_data.data)
            out.release()
            cv2.destroyAllWindows()
            rospy.signal_shutdown("done!")

    # start-stop Subscriber
    ss_sub = rospy.Subscriber("/film", String, callback, queue_size=1)
    rospy.spin()


if __name__ == "__main__":
    main()
