# ROS package for filming video from ROS realsense wrapper

## requirements
 - RealSense camera D400 series.
 - RealSense SDK 2.0. Download and install [here][db1].
 - ROS wrapper for RealSense 2.0. You can find it [here][db2].

## Start recording
First of all, we need to start camera node:
```
roslaunch realsense2_camera rs_camera.launch
```
Don't forget to source ros package:
```
source /path/to/your/workspace/devel/setup.bash
```
Wait some time, until node will be starting.  
Then, start video recording program:
```
rosrun video_saver video_save.py
```
The program is automatically start and stop recording and save video to **/path/to/your/workspace/src/video_saver/videos**.


[db1]: <https://github.com/IntelRealSense/librealsense>
[db2]: <https://github.com/IntelRealSense/realsense-ros>
