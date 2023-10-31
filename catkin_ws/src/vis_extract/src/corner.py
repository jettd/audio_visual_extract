#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CornerDetection:
    def __init__(self):
        self.node_name = "corner_detection"
        rospy.init_node(self.node_name)
        
        # Set up a subscriber to the raw image topic
        self.subscriber = rospy.Subscriber("/camera/image_raw", Image, self.callback, queue_size=1)
        
        # Set up a publisher for the corner-detected image
        self.publisher = rospy.Publisher("/visual_data/image_corners", Image, queue_size=1)
        
        # Initialize CV Bridge
        self.bridge = CvBridge()

    def callback(self, data):
        try:
            # Convert the image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
            
            # Convert to grayscale
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply the Harris corner detector
            gray_image = np.float32(gray_image)
            corners = cv2.cornerHarris(gray_image, 2, 3, 0.04)
            
            # Dilate the corner image to enhance the corners
            corners = cv2.dilate(corners, None)
            
            # Threshold to get only the corners
            cv_image[corners > 0.01 * corners.max()] = [0, 0, 255]
            
            # Convert the processed image back to ROS format and publish
            corners_msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
            self.publisher.publish(corners_msg)
            
        except Exception as e:
            rospy.logerr("Error processing image: %s", e)

if __name__ == '__main__':
    corner_detection = CornerDetection()
    rospy.spin()
