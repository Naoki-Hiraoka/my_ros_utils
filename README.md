# my_ros_utils

### rosbag
*append

python/rosbag_appender.py

*filter

rosbag filter /home/hiraoka/rosbags/180613/18/rosbag_2018-06-13-18-55-30_65.bag ./tmp.bag "topic!='/joint_state_appended' or len(m.effort)!=12"

*draw graph

python/rosbag_draw.py
