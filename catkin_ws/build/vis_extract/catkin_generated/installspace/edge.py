#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class EdgeDetection:
    def __init__(self):
        self.node_name = "edge_detection"
        rospy.init_node(self.node_name)
        
        # Set up a subscriber to the raw image topic
        self.subscriber = rospy.Subscriber("/camera/image_raw", Image, self.callback, queue_size=1)
        
        # Set up a publisher for the edge-detected image
        self.publisher = rospy.Publisher("/visual_data/image_edges", Image, queue_size=1)
        
        # Initialize CV Bridge
        self.bridge = CvBridge()

    def callback(self, data):
        try:
            # Convert the image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
            
            # Convert to grayscale
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply the Canny edge detector
            edges = cv2.Canny(gray_image, 100, 200)
            
            # Convert the processed image back to ROS format and publish
            edges_msg = self.bridge.cv2_to_imgmsg(edges, encoding='mono8')
            self.publisher.publish(edges_msg)
            
        except Exception as e:
            rospy.logerr("Error processing image: %s", e)

if __name__ == '__main__':
    edge_detection = EdgeDetection()
    rospy.spin()
