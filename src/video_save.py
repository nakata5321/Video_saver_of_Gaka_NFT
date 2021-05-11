#!/usr/bin/env python
from std_msgs.msg import String
import pyrealsense2 as rs
import numpy as np
import rospkg
import ffmpeg
import rospy
import cv2

rospack = rospkg.RosPack()
dirname = rospack.get_path("video_saver")
FILE_OUTPUT = dirname + "/videos/" + "output.mp4"
FFMPEG_BIN = "ffmpeg"

# width of frame
WIDTH = 1280
# height of frame
HEIGHT = 720
# flag for start/stop recording
global flag
flag = ""

process2 = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(WIDTH, HEIGHT))
    .filter('fps', fps=30, round='up')
    .output(FILE_OUTPUT, pix_fmt='yuv420p', vcodec='h264')
    .overwrite_output()
    .run_async(pipe_stdin=True)
)


def callback(ros_data):
    global flag
    flag = ros_data.data
    rospy.loginfo(ros_data.data)

def main():  # init ros node
    rospy.init_node("image_recorder", anonymous=True)
    rospy.loginfo("node is up")

    # create camera object and Configure streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    #save first frame
    frame = pipeline.wait_for_frames()
    color_fram = frame.get_color_frame()
    color_imag = np.asanyarray(color_fram.get_data())
    cv2.imwrite(dirname + "/videos/pic.png", color_imag[:,:,:])

    # start-stop Subscriber
    ss_sub = rospy.Subscriber("/film", String, callback, queue_size=1)
    try:
        while True:
            global flag
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            color_image = np.asanyarray(color_frame.get_data())

            if flag == "start":
                color_image = np.asanyarray(color_frame.get_data())

                process2.stdin.write(
                color_image[:,:,::-1]
                .astype(np.uint8)
                .tobytes()
                )

            if flag == "stop":
                process2.stdin.close()
                process2.wait()
                rospy.loginfo("shutting down")

                rospy.sleep(5)
                rospy.signal_shutdown("done!")
                break



    finally:
        # Stop streaming
        pipeline.stop()
        rospy.signal_shutdown("error!")

if __name__ == "__main__":
    main()
