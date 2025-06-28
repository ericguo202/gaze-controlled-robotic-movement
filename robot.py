#!/usr/bin/env python

from __future__ import print_function
from six.moves import input

import rospy
import tf
import moveit_commander
import geometry_msgs.msg
from geometry_msgs.msg import Pose, Point, Quaternion, PoseArray, WrenchStamped
from std_msgs.msg import String, Float64MultiArray
from visualization_msgs.msg import Marker
import numpy as np
from sensor_msgs.msg import JointState
import sys
import pandas as pd
from franka_msgs.srv import SetFullCollisionBehavior, SetFullCollisionBehaviorRequest
from visualization_msgs.msg import Marker
import random
import csv
import time

seventh_joint = 0
wrench_force_z = 0

def joint_callback(msg):
    global seventh_joint
    seventh_joint = msg.position[6]

def wrench_callback(msg):
    global wrench_force_z
    wrench_force_z = msg.wrench.force.z

def move_down(move_group):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose

    end_effector_pose = geometry_msgs.msg.Pose()
    end_effector_pose.position.x = start_pose.position.x
    end_effector_pose.position.y = start_pose.position.y
    end_effector_pose.position.z = start_pose.position.z-.0075
    end_effector_pose.orientation = start_pose.orientation


            

    move_group.set_pose_target(end_effector_pose)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    print("moved down")

def move_up(move_group):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose

    end_effector_pose = geometry_msgs.msg.Pose()
    end_effector_pose.position.x = start_pose.position.x
    end_effector_pose.position.y = start_pose.position.y
    end_effector_pose.position.z = start_pose.position.z+.0075
    end_effector_pose.orientation = start_pose.orientation


            

    move_group.set_pose_target(end_effector_pose)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    print("moved up")

def move_backward(move_group):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose

    end_effector_pose = geometry_msgs.msg.Pose()
    end_effector_pose.position.x = start_pose.position.x
    end_effector_pose.position.y = start_pose.position.y+.0075
    end_effector_pose.position.z = start_pose.position.z
    end_effector_pose.orientation = start_pose.orientation


            

    move_group.set_pose_target(end_effector_pose)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    print("moved backward")

def move_left(move_group):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose

    end_effector_pose = geometry_msgs.msg.Pose()
    end_effector_pose.position.x = start_pose.position.x-.0075
    end_effector_pose.position.y = start_pose.position.y
    end_effector_pose.position.z = start_pose.position.z
    end_effector_pose.orientation = start_pose.orientation


            

    move_group.set_pose_target(end_effector_pose)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    print("moved left")

def move_right(move_group):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose

    end_effector_pose = geometry_msgs.msg.Pose()
    end_effector_pose.position.x = start_pose.position.x+.0075
    end_effector_pose.position.y = start_pose.position.y
    end_effector_pose.position.z = start_pose.position.z
    end_effector_pose.orientation = start_pose.orientation


            

    move_group.set_pose_target(end_effector_pose)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    print("moved right")

def move_forward(move_group):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose

    end_effector_pose = geometry_msgs.msg.Pose()
    end_effector_pose.position.x = start_pose.position.x
    end_effector_pose.position.y = start_pose.position.y-.0075
    end_effector_pose.position.z = start_pose.position.z
    end_effector_pose.orientation = start_pose.orientation


            

    move_group.set_pose_target(end_effector_pose)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    print("moved forward")

# def gripper_open(move_group):
#             gripper.set_joint_value_target(hand_open)
#             plan = gripper.plan()
#             plan_traj = plan[1]
#             gripper.execute(plan_traj, wait=True)
#             gripper.stop()

# def gripper_close(move_group):
#             gripper.set_joint_value_target(hand_close)
#             plan = gripper.plan()
#             plan_traj = plan[1]
#             gripper.execute(plan_traj, wait=True)
#             gripper.stop()

def main():
    rospy.init_node('set_full_collision_behavior')
    moveit_commander.roscpp_initialize(sys.argv)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "panda_arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)
    move_group.set_planning_time(10)
    move_group.set_end_effector_link("panda_hand")
    group_hand_name = "hand"
    gripper = moveit_commander.MoveGroupCommander(group_hand_name)

    rospy.Subscriber('/joint_states', JointState, joint_callback)
    rospy.Subscriber('/franka_state_controller/F_ext', WrenchStamped, wrench_callback)
    listener = tf.TransformListener()
    #all the way to the right: -0.010837358045081298

    # Get the initial pose of the end effector
    start_pose = move_group.get_current_pose().pose
    joint_home = [-0.0002249274015897828, -0.7846473935524318, 4.74312715691906e-06, -2.3559378868236878, -0.0007421279900396864, 1.571840799410771, 0.78462253368357]
    rospy.wait_for_service('/franka_control/set_full_collision_behavior')
    return move_group, listener

def main2(value, move_group, listener):

        
    if not rospy.is_shutdown():

            set_collision_behavior_service = rospy.ServiceProxy('/franka_control/set_full_collision_behavior', SetFullCollisionBehavior)
            lower_torque = [20.0,20.0,20.0,20.0,20.0,12.0,12.0]
            lower_force = [20.0,20.0,20.0,20.0,20.0,15.0]
            upper_torque =[25.0,25.0,25.0,25.0,25.0,15.0,15.0]
            upper_force = [30.0,30.0,30.0,30.0,30.0,20.0]
            lower_acceleration_torque = [5.0,5.0,5.0,5.0,5.0,3.0,3.0]
            upper_acceleration_torque = [7.0,7.0,7.0,7.0,7.0,5.0,5.0]
            lower_acceleration_force = [5.0,5.0,5.0,5.0,5.0,3.0]
            upper_acceleration_force = [7.0,7.0,7.0,7.0,7.0,5.0]
            request = SetFullCollisionBehaviorRequest(
                lower_torque_thresholds_acceleration = lower_acceleration_torque,
                upper_torque_thresholds_acceleration = upper_acceleration_torque,
                lower_torque_thresholds_nominal = lower_torque, 
                upper_torque_thresholds_nominal = upper_torque,
                lower_force_thresholds_acceleration = lower_acceleration_force,
                upper_force_thresholds_acceleration = upper_acceleration_force,
                lower_force_thresholds_nominal = lower_force,
                upper_force_thresholds_nominal = upper_force
            )
            response = set_collision_behavior_service(request)

            if response.success:
                rospy.loginfo("collision behvior set successfully")
            else:
                rospy.loginfo("collision behavior not set")

            print(seventh_joint)
            
            move_group.set_start_state_to_current_state()
            # start_pose = move_group.get_current_pose().pose

            listener.waitForTransform('panda_link0', 'panda_hand', rospy.Time(), rospy.Duration(3.0))

            (trans2, rot2) = listener.lookupTransform('panda_link0', 'panda_hand', rospy.Time(0))

            arm_pose = geometry_msgs.msg.Pose()
            arm_pose.position.x = trans2[0]
            arm_pose.position.y = trans2[1]
            arm_pose.position.z = (trans2[2])


            print("value: " +  value)

            if int(value) == 1:
                move_right(move_group)
            elif int(value) == 2:
                move_forward(move_group)
            elif int(value) == -1:
                move_left(move_group)
            elif int(value) == -2:
                move_backward(move_group)
            elif int(value) == -3:
                move_down(move_group)
            elif int(value) == 3:
                move_up(move_group)


            rospy.loginfo("############## Task completed! ##############")

if __name__ == '__main__':
    move_group, listener = main()
    main2("1",move_group, listener)
    time.sleep(1)
    main2("2",move_group, listener)