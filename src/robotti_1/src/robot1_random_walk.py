#! /usr/bin/python3

import rospy, random
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry

def callback(data):
    vel_l_msg = Float64()
    vel_r_msg = Float64()
    position_x = data.pose.pose.position.x
    position_y = data.pose.pose.position.y
    if position_x < 0.5:
        velocity_l = -10
        velocity_r = -3

    elif position_y < 0.5:
        velocity_l = -10
        velocity_r = -3

    elif position_x > 2.5:
        velocity_l = -3
        velocity_r = -10
    
    elif position_y > 2.5:
        velocity_l = -3
        velocity_r = -10

    else:
        velocity_l = random.uniform(-0.1, -10)
        velocity_r = random.uniform(-0.1, -10)

    vel_l_msg.data = velocity_l
    vel_r_msg.data = velocity_r
    velocity_l_publisher.publish(vel_l_msg)
    velocity_r_publisher.publish(vel_r_msg)


if __name__ == '__main__':
    while not rospy.is_shutdown():
        rospy.init_node("robot1_random_walk")
        velocity_l_publisher = rospy.Publisher('robot1/wheel_l_velocity_controller/command', Float64,queue_size=1)
        velocity_r_publisher = rospy.Publisher('robot1/wheel_r_velocity_controller/command', Float64,queue_size=1)
        rospy.Subscriber("/robot1/odom", Odometry, callback)
        rospy.spin()