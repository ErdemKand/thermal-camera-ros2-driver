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

## Fake Thermal Publisher
The ROS2 package skeleton was reviewed and improvements were initiated. First, the package contents were listed using the `ls /ros2_ws/src/thermal-camera-ros2-driver/src/thermal_camera_driver/` command, which revealed that only the __init__.py file was present. Since a fake_thermal_publisher node was needed, a new file named `fake_thermal_publisher.py` was created. This node publishes fake thermal images over the `/thermal/image_raw` topic at 30 FPS using the `sensor_msgs/Image` message type. The image resolution was set to 256×192 pixels to match the UTi721M thermal camera. Each frame is generated in mono8 encoding with random pixel values ranging from 50 to 200, simulating warm and cold regions in the scene.
Next, the `fake_thermal_publisher entry` point was added to the entry_points section of `setup.py`, and the package was then compiled using colcon build:
```
cd ~/ros2_ws
colcon build --packages-select thermal_camera_driver
source install/setup.bash
```
To verify that frames were being published at 30 FPS, the following command was run:
`ros2 run thermal_camera_driver fake_thermal_publisher`
The output was as follows, confirming that frame publishing worked without any issues:
<img width="919" height="561" alt="Screenshot from 2026-04-17 17-05-46" src="https://github.com/user-attachments/assets/2d11c131-79f8-43f7-a6f8-4f8134a2ed41" />
To visualize the incoming data, RViz2 was launched in a separate terminal. In the RViz2 window, the Add -> By topic -> /thermal/image_raw -> Image steps were followed to open the image panel, and the frames from the fake node were successfully rendered on screen.
<img width="1220" height="901" alt="rviz" src="https://github.com/user-attachments/assets/f6165d9a-6eba-4493-86e7-36e7ad1a3ac1" />

## OpenCV – ROS2 Integration
Since OpenCV and ROS2 store image data in different formats, a converter is needed between them:
OpenCV -> numpy array — stores pixel data as a 2D/3D array
ROS2 -> sensor_msgs/Image — stores image data as a flat byte array with metadata
The data flow for the thermal camera driver is as follows:
1. Thermal Camera (USB)
2. Read frame with OpenCV    (numpy array)
3. Convert with cv_bridge   (sensor_msgs/Image)
4. Publish over ROS2 topic   (/thermal/image_raw)
To test this pipeline, a sample image was downloaded from the OpenCV GitHub repository:
`wget https://raw.githubusercontent.com/opencv/opencv/master/samples/data/butterfly.jpg -O ~/test_image.jpg`
A new node named `image_publisher.py` was then created to handle the OpenCV–cv_bridge integration. The `image_publisher` entry point was added to `setup.py` and the package was compiled using colcon build. An incorrect file path was initially provided, which caused a loading error. After correcting the path, the image was successfully published.
To visualize the output, RViz2 was launched in a separate terminal. By following Add -> By topic -> /camera/image_raw -> Image, the image was successfully rendered on screen. All changes were then pushed to GitHub.
<img width="952" height="901" alt="cv_bridge" src="https://github.com/user-attachments/assets/faecec08-a9bf-4c2f-b1a0-2372c8ea4e55" />
[referance](https://github.com/opencv/opencv)

## YAML-Based Configuration Setup
A YAML-based configuration file was created under the config/ directory. This allows the node to be configured without modifying the source code, making the system modular and parameter-driven. The following parameters were defined:

| Parameter | Description |
|---|---|
|frame_width|Horizontal resolution of the camera frame in pixels|
|frame_height|Vertical resolution of the camera frame in pixels|
|fps|Number of frames captured and published per second|
|topic_name|ROS2 topic name on which image data is published|
|frame_id|Coordinate frame identifier used in the image header|
|temp_min_threshold|Minimum temperature threshold for future fire detection logic|
|temp_max_threshold|Maximum temperature threshold for future fire detection logic|
[referance](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html)
<img width="867" height="713" alt="image" src="https://github.com/user-attachments/assets/ce6bf1fa-ae90-4719-83b2-4b6baf969861" />
The fake_thermal_publisher node was then updated to read all parameters from this YAML file at startup, replacing previously hardcoded values. The package was rebuilt using colcon build and tested with the following command:
```
ros2 run thermal_camera_driver fake_thermal_publisher --ros-args --params-file ~/ros2_ws/src/thermal-camera-ros2-driver/config/camera_params.yaml```
<img width="876" height="767" alt="Screenshot from 2026-04-18 21-00-46" src="https://github.com/user-attachments/assets/6ad1a3bb-2c3a-4ea2-bc4c-6971d5b76743" />
## Rosbag Visulization with RViz2
