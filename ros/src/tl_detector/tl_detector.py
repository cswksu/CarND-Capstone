#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped, Pose
from styx_msgs.msg import TrafficLightArray, TrafficLight
from styx_msgs.msg import Lane
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from scipy.spatial import KDTree
from light_classification.tl_classifier import TLClassifier
import tf
import cv2
import yaml
import numpy as np

STATE_COUNT_THRESHOLD = 3

class TLDetector(object):
    def __init__(self):
        rospy.init_node('tl_detector')
        self.count=0

        self.pose = None
        self.waypoints = None
        self.camera_image = None
        self.lights = []

        sub1 = rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        sub2 = rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)

        '''
        /vehicle/traffic_lights provides you with the location of the traffic light in 3D map space and
        helps you acquire an accurate ground truth data source for the traffic light
        classifier by sending the current color state of all traffic lights in the
        simulator. When testing on the vehicle, the color state will not be available. You'll need to
        rely on the position of the light and the camera image to predict it.
        '''
        sub3 = rospy.Subscriber('/vehicle/traffic_lights', TrafficLightArray, self.traffic_cb)
        sub6 = rospy.Subscriber('/image_color', Image, self.image_cb)

        config_string = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(config_string)

        self.upcoming_red_light_pub = rospy.Publisher('/traffic_waypoint', Int32, queue_size=1)

        self.bridge = CvBridge()
        self.light_classifier = TLClassifier()
        self.listener = tf.TransformListener()

        self.state = TrafficLight.UNKNOWN
        self.last_state = TrafficLight.UNKNOWN
        self.last_wp = -1
        self.state_count = 0
        
        self.waypoints_2d = None
        self.waypoint_tree = None
        
        self.tl_2d = None
        self.tl_tree = None

        rospy.spin()

    def pose_cb(self, msg):
        self.pose = msg

    def waypoints_cb(self, waypoints):
        self.waypoints = waypoints
        if not self.waypoints_2d:
            self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] for waypoint in waypoints.waypoints]
            self.waypoint_tree = KDTree(self.waypoints_2d)
            
    def traffic_cb(self, msg):
        self.lights = msg.lights
        if not self.tl_2d:
            self.tl_2d = [[tl.pose.pose.position.x, tl.pose.pose.position.y] for tl in msg.lights]
            self.tl_tree = KDTree(self.tl_2d)

    def image_cb(self, msg):
        """Identifies red lights in the incoming camera image and publishes the index
            of the waypoint closest to the red light's stop line to /traffic_waypoint

        Args:
            msg (Image): image from car-mounted camera

        """
        self.count=self.count+1
        self.has_image = True
        self.camera_image = msg
        if self.count==3
            light_wp, state = self.process_traffic_lights()

            '''
            Publish upcoming red lights at camera frequency.
            Each predicted state has to occur `STATE_COUNT_THRESHOLD` number
            of times till we start using it. Otherwise the previous stable state is
            used.
            '''
            if self.state != state:
                self.state_count = 0
                self.state = state
            elif self.state_count >= STATE_COUNT_THRESHOLD:
                self.last_state = self.state
                light_wp = light_wp if state == TrafficLight.RED else -1
                self.last_wp = light_wp
                self.upcoming_red_light_pub.publish(Int32(light_wp))
            else:
                self.upcoming_red_light_pub.publish(Int32(self.last_wp))
            self.state_count += 1
            self.count=0
        else:
            self.upcoming_red_light_pub.publish(Int32(self.last_wp))

        
    def get_closest_tl(self, pose):
        """Identifies closest traffic light ahead of pose
        Args:
            pose (Pose): position to match a waypoint to
        Returns:
            int: index of closest TL in self.tl_2d
        """
        if self.tl_tree:
            x = self.pose.pose.position.x
            y = self.pose.pose.position.y
            closest_idx = self.tl_tree.query([x, y], 1)[1]
            
            # Check if closest waypoint is ahead of or behind the vehicle
            closest_coord = self.tl_2d[closest_idx]
            prev_coord = self.tl_2d[closest_idx-1]

            # Equation for hyperplane through closest_coords
            cl_vect = np.array(closest_coord)
            prev_vect = np.array(prev_coord)
            pos_vect = np.array([x, y])

            # Calculate dot product between cl_vect and previous vector
            # and position vector and closest vector
            val = np.dot(cl_vect-prev_vect, pos_vect - cl_vect)

            # If val is > 0, then pos_vector is not between closest_coord
            # and prev_coord

            if val > 0:
                closest_idx = (closest_idx +1) % len(self.tl_2d)
            return closest_idx
        else:
            pass
    
    def get_closest_waypoint(self, pose, y=None):
        """Identifies the closest path waypoint to the given position
            https://en.wikipedia.org/wiki/Closest_pair_of_points_problem
        Args:
            pose (Pose): position to match a waypoint to

        Returns:
            int: index of the closest waypoint in self.waypoints

        """
        #TODO implement
        if self.waypoint_tree:
            if y is None:
                x = self.pose.pose.position.x
                y = self.pose.pose.position.y
            else:
                x=pose
            closest_idx = self.waypoint_tree.query([x, y], 1)[1]
            """
            # Check if closest waypoint is ahead of or behind the vehicle
            closest_coord = self.waypoints_2d[closest_idx]
            prev_coord = self.waypoints_2d[closest_idx-1]

            # Equation for hyperplane through closest_coords
            cl_vect = np.array(closest_coord)
            prev_vect = np.array(prev_coord)
            pos_vect = np.array([x, y])

            # Calculate dot product between cl_vect and previous vector
            # and position vector and closest vector
            val = np.dot(cl_vect-prev_vect, pos_vect - cl_vect)

            # If val is > 0, then pos_vector is not between closest_coord
            # and prev_coord

            if val > 0:
                closest_idx = (closest_idx +1) % len(self.waypoints_2d)"""
            return closest_idx
        else:
            pass
        
    

    def get_light_state(self, light):
        """Determines the current color of the traffic light

        Args:
            light (TrafficLight): light to classify

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        if(not self.has_image):
            self.prev_light_loc = None
            return False

        cv_image = self.bridge.imgmsg_to_cv2(self.camera_image, "bgr8")

        #Get classification
        return self.light_classifier.get_classification(cv_image)

    def process_traffic_lights(self):
        """Finds closest visible traffic light, if one exists, and determines its
            location and color

        Returns:
            int: index of waypoint closes to the upcoming stop line for a traffic light (-1 if none exists)
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        light = None
        light_wp = None

        # List of positions that correspond to the line to stop in front of for a given intersection
        stop_line_positions = self.config['stop_line_positions']
        if(self.pose):
            car_position = self.get_closest_waypoint(self.pose.pose)
            light = self.get_closest_tl(self.pose.pose)
            light_wp = self.get_closest_waypoint(stop_line_positions[light][0],stop_line_positions[light][1])

        #TODO find the closest visible traffic light (if one exists)
        debugFlag=True

        if light:
            if debugFlag:
                state = self.lights[light].state
            else:
                state = self.get_light_state(light)
            return light_wp, state
        self.waypoints = None
        return -1, TrafficLight.UNKNOWN

if __name__ == '__main__':
    try:
        TLDetector()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic node.')
