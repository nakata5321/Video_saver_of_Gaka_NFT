#!/usr/bin/env python3
from std_msgs.msg import String
import pyrealsense2 as rs
import numpy as np
import rospkg
import ffmpeg
import rospy
import signal

# width of frame
WIDTH = 1280
# height of frame
HEIGHT = 720
# flag for start/stop recording
flag = " "
sub_process = 0
rospack = rospkg.RosPack()
dirname = rospack.get_path("video_saver")
FILE_OUTPUT = dirname + "/videos/" + "output.mp4"


def callback(ros_data: String) -> None:
    global flag
    flag = ros_data.data
    rospy.loginfo(ros_data.data)


def handler_stop(signum, frame) -> None:
    global sub_process
    sub_process.wait()
    exit(0)


# init ffmpeg video save process
def subprocess_create() -> object:
    process = ffmpeg.input("pipe:", format="rawvideo", pix_fmt="rgb24", s="{}x{}".format(WIDTH, HEIGHT))
    process = ffmpeg.filter(process, "fps", fps=30, round="up")
    process = ffmpeg.output(process, FILE_OUTPUT, pix_fmt="yuv420p", vcodec="h264")
    process = ffmpeg.overwrite_output(process)
    print("create")
    return process


def main() -> None:
    global flag
    global sub_process
    filming = False
    # init ros node
    rospy.init_node("image_recorder", anonymous=True, disable_signals=True)
    signal.signal(signal.SIGTERM, handler_stop)
    signal.signal(signal.SIGINT, handler_stop)

    # create camera object and Configure streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)
    rospy.loginfo("node is up")

    # Start streaming
    pipeline.start(config)

    # start-stop Subscriber
    ss_sub = rospy.Subscriber("/film", String, callback, queue_size=1)
    try:
        while not rospy.is_shutdown():
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            if flag == "start":
                process = subprocess_create()
                rospy.loginfo("start filming")
                sub_process = ffmpeg.run_async(process, pipe_stdin=True)
                rospy.sleep(2)
                flag = " "
                filming = True

            if flag == "stop":
                filming = False
                sub_process.stdin.close()
                sub_process.wait()
                rospy.loginfo("stop filming")
                flag = " "
                rospy.sleep(5)

            if filming:
                color_image = np.asanyarray(color_frame.get_data())
                sub_process.stdin.write(color_image[:, :, ::-1].astype(np.uint8).tobytes())

    finally:
        # Stop streaming
        pipeline.stop()
        rospy.signal_shutdown("error!")


if __name__ == "__main__":
    main()
