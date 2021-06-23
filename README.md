# ROS package for filming video with realsense camera

## requirements
 - RealSense camera D400 series.
 - RealSense SDK 2.0. Download and install [here][db1].
 - ROS. You can find it [here][db2].

## Start recording
First, we need to start `roscore`:
```
roscore
```
Don't forget to source ros package:
```
source /path/to/your/workspace/devel/setup.bash
```
Wait some time, until core will be starting.  
Then, start video recording program:
```
rosrun video_saver video_save.py
```
The program is automatically start and stop recording and save video to **/path/to/your/workspace/src/video_saver/videos** (work for robot painter).

To start recording manually, in new terminal publish _start_ :
```
rostopic pub /film std_msgs/String "start"
```
To _stop_:
```
rostopic pub /film std_msgs/String "stop"
```

[db1]: <https://github.com/IntelRealSense/librealsense>
[db2]: <https://www.ros.org/install/>
