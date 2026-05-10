#YUYV veya MJPG 
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ThermalCameraDriver(Node):
    def __init__(self):
        super().__init__('thermal_camera_driver')
        self.publisher_ = self.create_publisher(Image, '/thermal/image_raw', 10)
        self.bridge = CvBridge()
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 192)
        
        self.timer = self.create_timer(0.033, self.publish_frame)
        self.get_logger().info('Thermal Camera Driver started!')

    def publish_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error('Failed to capture frame!')
            return
        
        # Convert OpenCV frame to ROS2 Image message
        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'thermal_camera'
        self.publisher_.publish(msg)
        self.get_logger().info('Frame published!')

def main(args=None):
    rclpy.init(args=args)
    node = ThermalCameraDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
