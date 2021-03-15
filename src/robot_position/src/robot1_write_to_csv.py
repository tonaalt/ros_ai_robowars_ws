#! /usr/bin/python3

import rospy, message_filters, csv
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Range

class Robotposition:
    def __init__(self):
        self.node = rospy.init_node("robot1_position_from_ultrasonic")

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
        self.subs.registerCallback(self.sensor_cb)
        self.positions_file = open('robot1_positions.csv', mode='w')
        self.position_writer = csv.writer(self.positions_file, delimiter=',')
    def sensor_cb(self, us1_sub, us2_sub, us3_sub, us4_sub, us5_sub, us6_sub, odom_sub):
        self.position_writer.writerow([odom_sub.pose.pose.orientation.x,
                                        odom_sub.pose.pose.orientation.y,
                                        odom_sub.pose.pose.orientation.z,
                                        odom_sub.pose.pose.orientation.w,
                                        us1_sub.range,
                                        us2_sub.range,
                                        us3_sub.range,
                                        us4_sub.range,
                                        us5_sub.range,
                                        us6_sub.range,
                                        odom_sub.pose.pose.position.x,
                                        odom_sub.pose.pose.position.y])

if __name__ == '__main__':
    Robotposition()
    rospy.spin()