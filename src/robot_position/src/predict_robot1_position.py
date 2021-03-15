#! /usr/bin/python3

import rospy, message_filters
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Range

import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('saved_model')


class Robotposition:
    def __init__(self):
        self.node = rospy.init_node("predict_robot1_position_from_ultrasonic")

        self.us1_sub = message_filters.Subscriber('/robot1/ultrasonic1',Range)
        self.us2_sub = message_filters.Subscriber('/robot1/ultrasonic2',Range)
        self.us3_sub = message_filters.Subscriber('/robot1/ultrasonic3',Range)
        self.us4_sub = message_filters.Subscriber('/robot1/ultrasonic4',Range)
        self.us5_sub = message_filters.Subscriber('/robot1/ultrasonic5',Range)
        self.us6_sub = message_filters.Subscriber('/robot1/ultrasonic6',Range)
        self.odom_sub = message_filters.Subscriber('/robot1/odom', Odometry)

        self.subs = message_filters.ApproximateTimeSynchronizer([self.us1_sub,
                                                                self.us2_sub,
                                                                self.us3_sub,
                                                                self.us4_sub,
                                                                self.us5_sub,
                                                                self.us6_sub,
                                                                self.odom_sub],
                                                                queue_size=1,
                                                                slop=0.9,
                                                                allow_headerless=False)
        self.model = tf.keras.models.load_model('saved_model')
        self.predict_data = np.zeros((1,10))
        self.subs.registerCallback(self.sensor_cb)

    def sensor_cb(self, us1_sub, us2_sub, us3_sub, us4_sub, us5_sub, us6_sub, odom_sub):
        self.predict_data[0][0] = odom_sub.pose.pose.orientation.x
        self.predict_data[0][1] = odom_sub.pose.pose.orientation.y
        self.predict_data[0][2] = odom_sub.pose.pose.orientation.z
        self.predict_data[0][3] = odom_sub.pose.pose.orientation.w
        self.predict_data[0][4] = us1_sub.range
        self.predict_data[0][5] = us2_sub.range
        self.predict_data[0][6] = us3_sub.range
        self.predict_data[0][7] = us4_sub.range
        self.predict_data[0][8] = us5_sub.range
        self.predict_data[0][9] = us6_sub.range
        self.test_predictions = self.model.predict(self.predict_data)
        print(str(odom_sub.pose.pose.position.x) + "gt_x" + str(odom_sub.pose.pose.position.y) + "gt_y")
        print(str(self.test_predictions[0][0]) + "x" + str(self.test_predictions[0][1]) + "y")

if __name__ == '__main__':
    print("start")
    Robotposition()
    rospy.spin()
