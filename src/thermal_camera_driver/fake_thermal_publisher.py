import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np


class FakeThermalPublisher(Node):

    def __init__(self):
        super().__init__('fake_thermal_publisher')

        # Publisher: publishes sensor_msgs/Image on /thermal/image_raw topic
        # Queue size 10: holds up to 10 messages if subscriber is slow
        self.publisher_ = self.create_publisher(Image, '/thermal/image_raw', 10)

        # Timer: calls publish_frame every 0.033 seconds (~30 FPS)
        self.timer = self.create_timer(0.033, self.publish_frame)

        self.frame_count = 0
        self.get_logger().info('Fake Thermal Publisher node started!')

    def publish_frame(self):
        msg = Image()

        # Header: timestamp and coordinate frame name
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'thermal_camera'

        # Image dimensions (matches UTi721M thermal camera resolution)
        msg.height = 192
        msg.width = 256

        # Encoding: mono8 = 8-bit grayscale (1 byte per pixel)
        msg.encoding = 'mono8'
        msg.is_bigendian = False

        # Step: number of bytes per row (width x bytes_per_pixel)
        msg.step = msg.width

        # Generate fake thermal frame with random pixel values (50-200 range)
        # Simulates a thermal image where higher values = warmer areas
        frame = np.random.randint(50, 200, (msg.height, msg.width), dtype=np.uint8)

        # Flatten 2D array to 1D list as required by sensor_msgs/Image
        msg.data = frame.flatten().tolist()

        self.publisher_.publish(msg)
        self.get_logger().info(f'Published frame #{self.frame_count} ({msg.width}x{msg.height})')
        self.frame_count += 1


def main(args=None):
    rclpy.init(args=args)
    node = FakeThermalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
