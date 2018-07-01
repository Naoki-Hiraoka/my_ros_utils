#!/usr/bin/env python
# -*- coding: utf-8 -*-

#指定されたbagfileについて、グラフを書く
#例 python rosbag_draw.py _filename:=/home/hiraoka/rosbags/180613/18/rosbag_2018-06-13-18-55-30_65.bag _data:=["/motor_states/temperature(4)","/joint_states_appended/position(4)"] _titles:=["MOTOR","POS"] _title:="6/13" _xlabel:="time" _ylabel:="position,temperature"


import rospy
rospy.init_node("rosbag_draw",anonymous=True)
filename = rospy.get_param("~filename",None)
data = rospy.get_param("~data",[])
titles = rospy.get_param("~titles",data)

title = rospy.get_param("~title",None)
xlabel = rospy.get_param("~xlabel",None)
ylabel = rospy.get_param("~ylabel",None)

if len(data) != len(titles):
    titles = data
topics = []
topicdata = []
print data
for _data in data:
    print _data.find("/",1)
    if _data.find("/",1):
        topics.append(_data[:_data.find("/",1)])
        topicdata.append(_data[_data.find("/",1):].replace("/",".").replace("(","[").replace(")","]"))
    else:
        print _data, "is invalid"
        exit

import rosbag
graph_time=[]
graph_data=[]
for i in range(len(data)):
    graph_time.append([])
    graph_data.append([])
bag = rosbag.Bag(filename)
startsec=-1
num=0
try:
    for topic, msg, t in bag.read_messages(topics=topics):
        if startsec<0:
            startsec=t.secs
        index=topics.index(topic)
        graph_time[index].append(t.secs-startsec+t.nsecs*0.000000001)
        graph_data[index].append(eval("msg"+topicdata[index]))
        num+=1
        if num<20:
            print index, "msg"+topicdata[index],eval("msg"+topicdata[index])
            print graph_data
finally:
    bag.close()
    import Gnuplot
    plot_data=[]
    for i in range(len(data)):
        plot_data.append(Gnuplot.Data(graph_time[i],graph_data[i],title=titles[i]))
    gp=Gnuplot.Gnuplot(persist=1)
    gp("set style data lines")
    tmp_str="gp.plot("
    for i in range(len(plot_data)):
        tmp_str += "plot_data[" + str(i) + "],"
    tmp_str += "title=title,xlabel=xlabel,ylabel=ylabel)"
    exec(tmp_str)
