# thermal-camera-ros2-driver
## Project Objective
This project aims to develop a fully functional camera driver that integrates a thermal camera with the ROS2 Humble ecosystem, broadcasting image data and capable of recording and visualizing this data. The developed driver will run on the Jetson Orin Nano and is planned to be integrated with unmanned aerial vehicle (UAV)-based forest fire detection systems in later stages.
### Things to do 
- Recognizing and reading the thermal camera via the V4L2 interface in a Linux environment(ROS2_Humble).
- Publishing image data in sensor_msgs/Image format via the /thermal/image_raw topic.
- Providing support for compressed image streams with image_transport.
- Establishing a parametric and modular structure (YAML-based configuration)
- Providing real-time visualization with RViz2.
- Creating data recording and playback infrastructure with rosbag2.
- Running the system and completing the integration on the Jetson Orin Nano.
## Hardware and software requirements
| Component | Details |
|---|---|
| OS | Ubuntu 22.04LTS |
| Target Platform | NVIDIA Jetson Orin Nano |
| Thermal Camera | UTi721M |
| ROS2 | Humble |
| Python | 3.10 |
| ROS2 Packages | cv-bridge, image-transport, sensor-msgs |
| System Tools | v4l-utils, python3-opencv |
## Essential concepts for the project
### ROS2-Humble
ROS2 (Robot Operating System 2) is an open-source middleware framework for robotics software development. It is built on the DDS (Data Distribution Service) protocol, making it suitable for real-time systems, safety-critical applications, and multi-robot scenarios. [documentation](https://docs.ros.org/en/humble/)

| Concept | Description |
|---|---|
| Node | An executable unit that performs a single function. E.g., camera reader node, image processor node|
| Topic | The communication channel between nodes. It operates using a publish/subscribe model |
| Package | In ROS2, it is the software distribution unit. It is compiled with colcon build |
| Workspace | The directory structure where packages are compiled and managed (src/, build/, install/)|
| Launch File | A configuration file that starts multiple nodes with a single command |
| Parameter | Key-value pairs that enable the configuration of nodes at runtime |
### Publisher-Subscriber structure
ROS2's fundamental communication pattern is the publish/subscribe pattern. This pattern allows nodes to operate independently; one node does not need to be aware of the existence of another.[documentation](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
 Publisher->Topic->Subscriber
- Publisher: Publishes data of a specific message type to a topic.
- Subscriber: Listens to the same topic and a callback function is triggered with each new message.
- QoS (Quality of Service): Determines the reliability and latency of message delivery.
<img width="1568" height="535" alt="image" src="https://github.com/user-attachments/assets/3bef5d3f-490b-4d39-bc0d-f690e0648445" />

### sensor_msgs/Image
sensor_msgs/Image is the standard message type used to carry raw image data in ROS2.
#### Structure of Message
(terminal code : `ros2 interface show sensor_msgs/msg/Image`) and [document](https://docs.ros.org/en/humble/p/std_msgs/)
```
std_msgs/Header header  Header timestamp should be acquisition time of image
	builtin_interfaces/Time stamp
		int32 sec
		uint32 nanosec
	string frame_id
                              Header frame_id should be optical frame of camera
                              origin of frame should be optical center of cameara
                              +x should point to the right in the image
                              +y should point down in the image
                              +z should point into to plane of the image
                              If the frame_id here and the frame_id of the CameraInfo
                              message associated with the image conflict
                              the behavior is undefined

uint32 height                 image height, that is, number of rows
uint32 width                  image width, that is, number of columns
string encoding        Encoding of pixels -- channel meaning, ordering, size
                       taken from the list of strings in include/sensor_msgs/image_encodings.hpp
uint8 is_bigendian     is this data bigendian?
uint32 step            Full row length in bytes
uint8[] data           actual matrix data, size is (step * rows)
```
### image_transport structure
Raw image data (sensor_msgs/Image) consumes significant bandwidth when transported over a network. The image_transport package provides an abstraction layer for transporting this data using various compression methods.[documentation](https://docs.ros.org/en/ros2_packages/humble/api/image_transport/)

```bash
ros2 topic list | grep thermal
```

Output:
```
/thermal/image_raw           : raw, uncompressed data
/thermal/image_raw/compressed  :JPEG/PNG compressed
/thermal/image_raw/theora      : video stream
```
### Record Data with Rosbag
rosbag2 is a tool used in ROS2 to record and replay topic data. It is critical for testing and collecting experimental data without real hardware.[documentation](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)
```bash
# Record all topics
ros2 bag record -a

# Record a specific topic
ros2 bag record /thermal/image_raw

# Play back a recording
ros2 bag play recording_folder/

# Inspect recording contents
ros2 bag info recording_folder/

# Play back at increased speed (2x)
ros2 bag play recording_folder/ --rate 2.0
```
#### Usage in the project
- Thermal image data recorded on the Jetson can be analyzed on the desktop
- The same data can be tested repeatedly during driver development
- Forest fire detection algorithms can be developed using bag files instead of live camera feeds
[referance]( https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)

### Visualization with RViz2
RViz2 is a 3D visualization tool for ROS2. It is used to visualize camera images, point clouds, robot models, and sensor data in real time.[referance](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)
#### Usage in the project
- To visually verify that the camera driver is working correctly
- Visualization of the thermal image using a colormap
- Checking the images while Rosbag is playing.

### V4L2 and USB Camera Recognition in Linux
V4L2 (Video4Linux2) is the standard API used in the Linux kernel to manage video capture devices. USB cameras are introduced to the system via this API as device files in /dev/videoX.
#### How to recognize a USB camera?
1. **USB Camera (UVC Compatible)**
2. **Linux Kernel** — `uvcvideo` driver loads automatically
3. **Device file created** — `/dev/video0`, `/dev/video1`, ...
4. **V4L2 API** — application layer reads the device file
5. **OpenCV / ROS2 Driver** — captures frames via V4L2
#### UVC(USB Video Class)Protocol
UVC is a standard protocol for USB cameras. There's no need to write special drivers for UVC-compatible cameras; the Linux kernel's uvcvideo module is automatically enabled.

#### Basic V4L2 Commands
```bash
# Install tools
sudo apt install v4l-utils
# List connected camera devices
ls /dev/video*
# Get detailed camera information
v4l2-ctl --device=/dev/video0 --info
# List supported formats
v4l2-ctl --device=/dev/video0 --list-formats-ext
# Display current settings
v4l2-ctl --device=/dev/video0 --all
# Capture a test frame
v4l2-ctl --device=/dev/video0 --stream-mmap --stream-count=1 --stream-to=test.raw
```
[referance](https://git.linuxtv.org/v4l-utils.git)
#### FPS
FPS stands for frames per second. In V4L2, it is controlled as follows:
```bash
# Display current FPS
v4l2-ctl --device=/dev/video0 --get-parm
# Set FPS
v4l2-ctl --device=/dev/video0 --set-parm=30
# List supported resolution and FPS combinations
v4l2-ctl --device=/dev/video0 --list-formats-ext
```
[general_referance]( https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/v4l2.html
)
### OpenCV-ROS2 Usage(cv_bridge)
`cv_bridge` converts between OpenCV's `cv::Mat` format and ROS2's `sensor_msgs/Image` format.

```
OpenCV (cv::Mat / numpy array)
        |
      cv_bridge
        |
ROS2 (sensor_msgs/Image)
```

```python
from cv_bridge import CvBridge
import cv2
bridge = CvBridge()
# OpenCV → ROS2 message
ros_image = bridge.cv2_to_imgmsg(cv_frame, encoding="bgr8")
# ROS2 message → OpenCV
cv_frame = bridge.imgmsg_to_cv2(ros_image, desired_encoding="bgr8")```

```bash
# Installation
sudo apt install ros-humble-cv-bridge
```
[referance](https://github.com/ros-perception/vision_opencv/tree/rolling/cv_bridge)
