cmake_minimum_required(VERSION 2.8.3)

project(samk_robowar_world)

find_package(catkin REQUIRED
  gazebo_ros
  roscpp
  rospy
  controller_manager
  joint_state_controller
  robot_state_publisher
)

catkin_package()

find_package(roslaunch)

foreach(dir config launch meshes urdf models world)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
