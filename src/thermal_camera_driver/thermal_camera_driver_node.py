import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ThermalCameraDriver(Node):
	def __init__(self):
		super().__init__('thermal_camera_driver')
		self.publisher_ = self.create_publisher(Image, '/thermal/image_raw', 10)
		self.raw_publisher = self.create_publisher(Image, '/thermal/image_raw16', 10)
		self.bridge = CvBridge()
		self.cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)
		self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 384)
		self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
		self.timer = self.create_timer(0.04, self.publish_frame)
		self.get_logger().info('Thermal Camera Driver started!')

	def publish_frame(self):
		ret, frame = self.cap.read()
		if not ret:
			self.get_logger().error('Failed to capture frame!')
			return
		top_y = frame[0:192, :, 0]
		top_bgr = cv2.cvtColor(top_y, cv2.COLOR_GRAY2BGR)
		raw16 = frame[192:384].view(np.uint16).reshape(192, 256)
		stamp = self.get_clock().now().to_msg()
		visual_msg = self.bridge.cv2_to_imgmsg(top_bgr, encoding='bgr8')
		visual_msg.header.stamp = stamp
		visual_msg.header.frame_id = 'thermal_camera'
		self.publisher_.publish(visual_msg)
		raw16_msg = self.bridge.cv2_to_imgmsg(raw16, encoding='mono16')
		raw16_msg.header.stamp = stamp
		raw16_msg.header.frame_id = 'thermal_camera'
		self.raw_publisher.publish(raw16_msg)

	def destroy_node(self):
		self.cap.release()
		super().destroy_node()

def main(args=None):
	rclpy.init(args=args)
	node = ThermalCameraDriver()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		node.destroy_node()
		rclpy.shutdown()

if __name__ == '__main__':
	main()
