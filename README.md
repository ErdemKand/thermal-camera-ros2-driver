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
