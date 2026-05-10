import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import pytesseract
import re

class TemperatureMapNode(Node):
	def __init__(self):
		super().__init__('temperature_map_node')
		#Parameter

		self.declare_parameter('temp_min',-20.0)
		self.declare_parameter('temp_max',550.0)
		self.declare_parameter('high_temp_correction',6.0)
		self.declare_parameter('correction_threshold',70.0)
		self.declare_parameter('input_topic','/thermal/image_raw')
		self.declare_parameter('output_topic','/thermal/temperature_map')

		self.temp_min = self.get_parameter('temp_min').get_parameter_value().double_value
		self.temp_max = self.get_parameter('temp_max').get_parameter_value().double_value
		input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
		output_topic = self.get_parameter('output_topic').get_parameter_value().string_value
		#With correction and threshold can change at high temperatures
		self.high_temp_correction = self.get_parameter('high_temp_correction').get_parameter_value().double_value
		self.correction_threshold = self.get_parameter('correction_threshold').get_parameter_value().double_value

		self.ocr_temp_min = self.temp_min
		self.ocr_temp_max = self.temp_max

		self.bridge = CvBridge()
		self.subscription = self.create_subscription(Image, input_topic, self.image_callback, 10)
		self.publisher = self.create_publisher(Image, output_topic, 10)
		self.visual_publisher = self.create_publisher(Image, output_topic + '/visual', 10)

	def read_temp_range_ocr(self,frame):
		h, w = frame.shape[:2]
		left_strip = frame[0:h, 0:int(w*25)]
		gray = cv2.cvtColor(left_strip, cv2.COLOR_BGR2GRAY)
		_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
		text = pytesseract.image_to_string(thresh, config='--psm 6')
		numbers = re.findall(r'[-+]?\d+\.?\d*', text)
		numbers = [float(n) for n in numbers]
		if len(numbers) >=2:
			self.ocr_temp_max = max(numbers)
			self.ocr_temp_min = min(numbers)




	def image_callback(self, msg):
# UTi721M outputs pseudocolor BGR frames
# Grayscale intensity used as temperature proxy
# Calibrated on 3 reference points (1.7, 27, 78°C)

		frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		self.read_temp_range_ocr(frame)
		gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		temp_map = self.ocr_temp_min + (gray.astype(np.float32)/255.0)*(self.ocr_temp_max - self.ocr_temp_min)

		temp_map = np.where(
			temp_map > self.correction_threshold,
			temp_map + self.high_temp_correction,
			temp_map
		)

		temp_normalized = cv2.normalize(temp_map, None, 0, 255, cv2.NORM_MINMAX)
		temp_uint8= temp_normalized.astype(np.uint8)

		temp_colormap= cv2.applyColorMap(temp_uint8,cv2.COLORMAP_JET)
		out_msg = self.bridge.cv2_to_imgmsg(temp_map, encoding='32FC1')
		out_msg.header = msg.header
		self.publisher.publish(out_msg)

		visual_msg = self.bridge.cv2_to_imgmsg(temp_colormap, encoding='bgr8')
		visual_msg.header = msg.header
		self.visual_publisher.publish(visual_msg)
def main(args=None):
	rclpy.init(args=args)
	node= TemperatureMapNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()

