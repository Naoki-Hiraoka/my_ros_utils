#!/usr/bin/env python
# -*- coding: utf-8 -*-

#現在のディレクトリ以下にある.bagファイルをファイル名の時系列順にappendしたものを、./append.bagとして出力
#_topics:=["/motor_states","/joint_states"]などとすることでfilterする

import rospy
rospy.init_node("rosbag_appender",anonymous=True)
topics = rospy.get_param("~topics",None)
outname = rospy.get_param("~outname","append.bag")
print topics
import os
baglist=[]
for i in os.walk("."):
    for j in i[2]:
        if(j[-4:]==".bag" and j!=outname):
            baglist.append(i[0]+"/"+j)
baglist=sorted(baglist)

import rosbag

outbag = rosbag.Bag(outname,"w")
try:
    for bagname in baglist:
        print bagname
        num=0
        bag = rosbag.Bag(bagname)
        try:
            for topic, msg, t in bag.read_messages(topics=topics):
                outbag.write(topic,msg,t)
                num+=1
        finally:
            print num, "data"
            bag.close()
finally:
    outbag.close()

